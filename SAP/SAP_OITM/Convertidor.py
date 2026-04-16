import os
import pandas as pd
import pyodbc
import logging
from datetime import datetime

# Configurar logging
log_filename = f'importacion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
error_filename = f'errores_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

error_logger = logging.getLogger('errores')
error_handler = logging.FileHandler(error_filename, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - ERROR - %(message)s'))
error_logger.addHandler(error_handler)

def encontrar_archivo_excel():
    """Ayuda a encontrar el archivo Excel"""
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    logging.info(f"Directorio del script: {directorio_actual}")
    
    archivos_excel = [f for f in os.listdir(directorio_actual) if f.endswith('.xlsx') or f.endswith('.xls')]
    
    if archivos_excel:
        logging.info(f"Archivos Excel encontrados: {', '.join(archivos_excel)}")
        return os.path.join(directorio_actual, archivos_excel[0])
    else:
        logging.error("No se encontraron archivos Excel en el directorio actual")
        return None

def importar_upsert_fecha_actual(excel_path=None):
    """
    Importación omitiendo DateUpdate del Excel y usando fecha/hora actual
    """
    
    inicio = datetime.now()
    logging.info("="*80)
    logging.info("INICIANDO PROCESO DE IMPORTACIÓN")
    logging.info("="*80)
    
    if excel_path is None or not os.path.exists(excel_path):
        logging.info("Buscando archivo Excel...")
        excel_path = encontrar_archivo_excel()
        
        if excel_path is None:
            error_msg = f"No se encontró archivo Excel"
            logging.error(error_msg)
            error_logger.error(error_msg)
            return False
    
    if not os.path.exists(excel_path):
        error_msg = f"El archivo no existe: {excel_path}"
        logging.error(error_msg)
        error_logger.error(error_msg)
        return False
    
    try:
        # Leer Excel
        logging.info(f"Leyendo archivo: {excel_path}")
        df = pd.read_excel(excel_path)
        logging.info(f"Registros encontrados: {len(df)}")
        
        # Validar columna ItemCode
        if 'ItemCode' not in df.columns:
            error_msg = "El archivo Excel no contiene la columna 'ItemCode'"
            logging.error(error_msg)
            error_logger.error(error_msg)
            return False
        
        # Eliminar la columna DateUpdate si existe en el DataFrame
        if 'DateUpdate' in df.columns:
            df = df.drop(columns=['DateUpdate'])
            logging.info("✓ Columna DateUpdate omitida del Excel")
        
        # Conexión
        connection_string = """
            Driver={ODBC Driver 17 for SQL Server};
            Server=20.110.82.192\SQLEXPRESS;
            Database=QUIRAMA;
            UID=ConexionDiscordoba;
            PWD=Srv1Discordoba;
            TrustServerCertificate=yes;
        """
        
        logging.info("Conectando a SQL Server...")
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        logging.info("✓ Conexión establecida exitosamente")
        
        # Verificar tabla
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'IntegracionSAP_OITM'
        """)
        
        if cursor.fetchone()[0] == 0:
            error_msg = "La tabla IntegracionSAP_OITM no existe"
            logging.error(error_msg)
            error_logger.error(error_msg)
            return False
        
        # Contadores
        insertados = 0
        actualizados = 0
        errores = 0
        errores_detalle = []
        
        logging.info(f"Iniciando procesamiento de {len(df)} registros...")
        logging.info(f"Usando fecha/hora actual para DateUpdate: {datetime.now()}")
        
        for index, row in df.iterrows():
            item_code = row.get('ItemCode', 'N/A')
            
            try:
                # Obtener fecha/hora actual para este registro
                fecha_actual = datetime.now()
                
                # Verificar si existe
                cursor.execute("SELECT COUNT(*) FROM [IntegracionSAP_OITM] WHERE ItemCode = ?", 
                             row['ItemCode'])
                existe = cursor.fetchone()[0] > 0
                
                if existe:
                    # UPDATE - construir query dinámicamente sin DateUpdate del Excel
                    columnas_update = [col for col in df.columns if col != 'ItemCode']
                    set_clause = ', '.join([f'[{col}] = ?' for col in columnas_update])
                    
                    # Agregar DateUpdate al final
                    set_clause += ', [DateUpdate] = ?'
                    
                    update_query = f"""
                        UPDATE [IntegracionSAP_OITM] 
                        SET {set_clause}
                        WHERE ItemCode = ?
                    """
                    
                    # Preparar valores: datos del Excel + fecha actual + ItemCode
                    valores = tuple(row[col] if pd.notna(row[col]) else None for col in columnas_update)
                    valores = valores + (fecha_actual, row['ItemCode'])
                    
                    cursor.execute(update_query, valores)
                    actualizados += 1
                else:
                    # INSERT - construir query dinámicamente
                    columnas_insert = list(df.columns) + ['DateUpdate']
                    columnas_str = ', '.join([f'[{col}]' for col in columnas_insert])
                    placeholders = ', '.join(['?' for _ in columnas_insert])
                    
                    insert_query = f"""
                        INSERT INTO [IntegracionSAP_OITM] ({columnas_str}) 
                        VALUES ({placeholders})
                    """
                    
                    # Preparar valores: datos del Excel + fecha actual
                    valores = tuple(row[col] if pd.notna(row[col]) else None for col in df.columns)
                    valores = valores + (fecha_actual,)
                    
                    cursor.execute(insert_query, valores)
                    insertados += 1
                
                # Commit cada 100 registros
                if (insertados + actualizados) % 100 == 0:
                    conn.commit()
                    porcentaje = ((insertados + actualizados) / len(df)) * 100
                    logging.info(f"Progreso: {insertados + actualizados}/{len(df)} ({porcentaje:.1f}%) - Insertados: {insertados}, Actualizados: {actualizados}")
                    
            except Exception as e:
                errores += 1
                error_msg = f"Fila {index + 2} | ItemCode: {item_code} | Error: {str(e)}"
                errores_detalle.append(error_msg)
                logging.error(error_msg)
                error_logger.error(error_msg)
                
                # Log detallado de la fila con error
                error_logger.error(f"  Datos de la fila:")
                for col in df.columns[:10]:  # Primeras 10 columnas
                    valor = row[col]
                    error_logger.error(f"    {col}: {valor}")
        
        # Commit final
        conn.commit()
        
        # Calcular tiempo
        fin = datetime.now()
        duracion = (fin - inicio).total_seconds()
        
        # Resumen
        logging.info("\n" + "="*80)
        logging.info("RESUMEN DE IMPORTACIÓN")
        logging.info("="*80)
        logging.info(f"Archivo procesado: {os.path.basename(excel_path)}")
        logging.info(f"Total registros en Excel: {len(df)}")
        logging.info(f"Nuevos insertados: {insertados}")
        logging.info(f"Actualizados: {actualizados}")
        logging.info(f"Errores: {errores}")
        logging.info(f"Procesados exitosamente: {insertados + actualizados}")
        logging.info(f"Tasa de éxito: {((insertados + actualizados) / len(df) * 100):.2f}%")
        logging.info(f"Tiempo total: {duracion:.2f} segundos")
        logging.info(f"Velocidad: {(len(df) / duracion):.2f} registros/segundo")
        logging.info(f"\nArchivos de log generados:")
        logging.info(f"  - Log general: {log_filename}")
        logging.info(f"  - Log de errores: {error_filename}")
        logging.info("="*80)
        
        if errores > 0:
            logging.warning(f"\n⚠️ Se encontraron {errores} errores")
            logging.warning(f"Revisa {error_filename} para detalles completos")
            
            # Mostrar primeros 5 errores
            if len(errores_detalle) > 0:
                logging.warning("\nPrimeros errores:")
                for i, error in enumerate(errores_detalle[:5], 1):
                    logging.warning(f"  {i}. {error}")
        else:
            logging.info("✓ Proceso completado sin errores")
        
        cursor.close()
        conn.close()
        logging.info("✓ Conexión cerrada")
        
        return True
        
    except Exception as e:
        error_msg = f"Error crítico: {str(e)}"
        logging.error(error_msg)
        error_logger.error(error_msg)
        
        import traceback
        error_trace = traceback.format_exc()
        logging.error(error_trace)
        error_logger.error(error_trace)
        
        return False

if __name__ == "__main__":
    print("\n" + "="*80)
    print("IMPORTADOR SAP OITM - FECHA/HORA AUTOMÁTICA")
    print("="*80)
    print("La columna DateUpdate se omitirá del Excel")
    print("Se usará la fecha/hora actual del sistema")
    print("="*80 + "\n")
    
    resultado = importar_upsert_fecha_actual()
    
    print("\n" + "="*80)
    if resultado:
        print("✓ PROCESO COMPLETADO EXITOSAMENTE")
    else:
        print("❌ PROCESO FALLÓ - Revisa los logs")
    print("="*80 + "\n")