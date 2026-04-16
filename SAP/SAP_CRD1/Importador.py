import os
import pandas as pd
import pyodbc
import logging
from datetime import datetime

# Configurar logging
log_filename = f'importacion_CRD1_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
error_filename = f'errores_CRD1_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

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

def importar_CRD1_upsert(excel_path=None):
    """
    Importa direcciones de clientes desde Excel a SQL Server (tabla IntegracionSAP_CRD1).
    Si el registro existe (CardCode + Address + AdresType) -> UPDATE
    Si NO existe -> INSERT
    
    Columnas esperadas en el Excel:
        Address, CardCode, AdresType, U_BO_Name, U_BO_LastName,
        U_BO_Cellolar, Street, Block, State, City, County,
        Status_Integration, Status_Comments, CreationDate
    """
    
    inicio = datetime.now()
    logging.info("="*80)
    logging.info("INICIANDO PROCESO DE IMPORTACIÓN CRD1 (DIRECCIONES DE CLIENTES)")
    logging.info("="*80)
    
    if excel_path is None or not os.path.exists(excel_path):
        logging.info("Buscando archivo Excel...")
        excel_path = encontrar_archivo_excel()
        
        if excel_path is None:
            error_msg = "No se encontró archivo Excel"
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
        logging.info(f"Columnas: {', '.join(df.columns.tolist())}")

        # Forzar parseo de CreationDate como datetime desde la lectura
        # errors='coerce' convierte cualquier valor invalido a NaT (NULL) en lugar de romper
        if 'CreationDate' in df.columns:
            df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', dayfirst=True)
            nulos_fecha = df['CreationDate'].isna().sum()
            if nulos_fecha > 0:
                logging.warning(f"  {nulos_fecha} valores en 'CreationDate' no pudieron parsearse y se insertaran como NULL")
        
        # Validar columnas requeridas (mínimo obligatorio)
        columnas_requeridas = ['Address', 'CardCode', 'AdresType']
        columnas_faltantes = set(columnas_requeridas) - set(df.columns)
        
        if columnas_faltantes:
            error_msg = f"Columnas obligatorias faltantes: {columnas_faltantes}"
            logging.error(error_msg)
            error_logger.error(error_msg)
            return False
        
        # Columnas opcionales — se insertan como NULL si no existen en el Excel
        columnas_opcionales = [
            'U_BO_Name', 'U_BO_LastName', 'U_BO_Cellolar',
            'Street', 'Block', 'State', 'City', 'County',
            'Status_Integration', 'Status_Comments', 'CreationDate'
        ]
        for col in columnas_opcionales:
            if col not in df.columns:
                logging.warning(f"Columna opcional '{col}' no encontrada en el Excel — se usará NULL")
                df[col] = None

        # Conexión
        connection_string = """
            Driver={ODBC Driver 17 for SQL Server};
            Server=20.110.82.192\SQLEXPRESS;
            Database=QUIR-273;
            UID=ConexionDiscordoba;
            PWD=Srv1Discordoba;
            TrustServerCertificate=yes;
        """
        
        logging.info("Conectando a SQL Server...")
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        logging.info("✓ Conexión establecida exitosamente")
        
        # Verificar que la tabla existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'IntegracionSAP_CRD1'
        """)
        
        if cursor.fetchone()[0] == 0:
            error_msg = "La tabla IntegracionSAP_CRD1 no existe en la base de datos"
            logging.error(error_msg)
            error_logger.error(error_msg)
            return False
        
        # Contadores
        insertados = 0
        actualizados = 0
        errores = 0
        errores_detalle = []
        
        logging.info(f"Procesando {len(df)} registros...")
        
        def val(row, col):
            """Retorna el valor o None si es NaN"""
            v = row.get(col)
            return None if pd.isna(v) else v

        def val_fecha(row, col):
            """
            Convierte el valor de una columna de fecha a datetime de Python.
            Soporta: objetos datetime, Timestamps de pandas, strings en varios formatos.
            Retorna None si el valor es nulo o no se puede parsear.
            """
            v = row.get(col)
            if v is None or (isinstance(v, float) and pd.isna(v)):
                return None
            # Ya es datetime nativo o Timestamp de pandas
            if isinstance(v, (datetime, pd.Timestamp)):
                return pd.Timestamp(v).to_pydatetime()
            # Es string — intentar parsear
            if isinstance(v, str):
                v = v.strip()
                if not v:
                    return None
                formatos = [
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d",
                    "%d/%m/%Y %H:%M:%S",
                    "%d/%m/%Y",
                    "%m/%d/%Y",
                    "%d-%m-%Y",
                ]
                for fmt in formatos:
                    try:
                        return datetime.strptime(v, fmt)
                    except ValueError:
                        continue
                # Último intento con pandas (más flexible)
                try:
                    return pd.to_datetime(v, dayfirst=True).to_pydatetime()
                except Exception:
                    logging.warning(f"No se pudo parsear la fecha '{v}' en columna '{col}' — se usará NULL")
                    return None
            return None

        for index, row in df.iterrows():
            address   = row.get('Address', 'N/A')
            card_code = row.get('CardCode', 'N/A')
            adres_type = row.get('AdresType', 'N/A')
            
            try:
                # Verificar existencia (CardCode + Address + AdresType)
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM [IntegracionSAP_CRD1] 
                    WHERE CardCode = ? AND Address = ? AND AdresType = ?
                """, card_code, address, adres_type)
                
                existe = cursor.fetchone()[0] > 0
                
                if existe:
                    # UPDATE
                    update_query = """
                        UPDATE [IntegracionSAP_CRD1]
                        SET U_BO_Name          = ?,
                            U_BO_LastName      = ?,
                            U_BO_Cellolar      = ?,
                            Street             = ?,
                            Block              = ?,
                            State              = ?,
                            City               = ?,
                            County             = ?,
                            Status_Integration = ?,
                            Status_Comments    = ?,
                            CreationDate       = ?,
                            SyncDate           = ?
                        WHERE CardCode = ? AND Address = ? AND AdresType = ?
                    """
                    valores = (
                        val(row, 'U_BO_Name'),
                        val(row, 'U_BO_LastName'),
                        val(row, 'U_BO_Cellolar'),
                        val(row, 'Street'),
                        val(row, 'Block'),
                        val(row, 'State'),
                        val(row, 'City'),
                        val(row, 'County'),
                        val(row, 'Status_Integration'),
                        val(row, 'Status_Comments'),
                        val_fecha(row, 'CreationDate'),
                        datetime.now(),
                        card_code, address, adres_type
                    )
                    cursor.execute(update_query, valores)
                    actualizados += 1
                else:
                    # INSERT (Id es identidad/autoincremental, no se incluye)
                    insert_query = """
                        INSERT INTO [IntegracionSAP_CRD1]
                            (Address, CardCode, AdresType, U_BO_Name, U_BO_LastName,
                             U_BO_Cellolar, Street, Block, State, City, County,
                             Status_Integration, Status_Comments, CreationDate, SyncDate)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    valores = (
                        address,
                        card_code,
                        adres_type,
                        val(row, 'U_BO_Name'),
                        val(row, 'U_BO_LastName'),
                        val(row, 'U_BO_Cellolar'),
                        val(row, 'Street'),
                        val(row, 'Block'),
                        val(row, 'State'),
                        val(row, 'City'),
                        val(row, 'County'),
                        val(row, 'Status_Integration'),
                        val(row, 'Status_Comments'),
                        val_fecha(row, 'CreationDate'),
                        datetime.now(),
                    )
                    cursor.execute(insert_query, valores)
                    insertados += 1
                
                # Commit cada 100 registros
                if (insertados + actualizados) % 100 == 0:
                    conn.commit()
                    porcentaje = ((insertados + actualizados) / len(df)) * 100
                    logging.info(
                        f"Progreso: {insertados + actualizados}/{len(df)} ({porcentaje:.1f}%) "
                        f"- Insertados: {insertados}, Actualizados: {actualizados}"
                    )
                    
            except Exception as e:
                errores += 1
                error_msg = (
                    f"Fila {index + 2} | CardCode: {card_code}, Address: {address}, "
                    f"AdresType: {adres_type} | Error: {str(e)}"
                )
                errores_detalle.append(error_msg)
                logging.error(error_msg)
                error_logger.error(error_msg)
                error_logger.error(
                    f"  Valores: CardCode={card_code}, Address={address}, AdresType={adres_type}, "
                    f"Street={row.get('Street')}, City={row.get('City')}"
                )
        
        # Commit final
        conn.commit()
        
        # Calcular tiempo
        fin = datetime.now()
        duracion = (fin - inicio).total_seconds()
        
        # Resumen
        logging.info("\n" + "="*80)
        logging.info("RESUMEN DE IMPORTACIÓN CRD1")
        logging.info("="*80)
        logging.info(f"Archivo procesado:          {os.path.basename(excel_path)}")
        logging.info(f"Total registros en Excel:   {len(df)}")
        logging.info(f"Nuevos insertados:          {insertados}")
        logging.info(f"Actualizados:               {actualizados}")
        logging.info(f"Errores:                    {errores}")
        logging.info(f"Procesados exitosamente:    {insertados + actualizados}")
        logging.info(f"Tasa de éxito:              {((insertados + actualizados) / len(df) * 100):.2f}%")
        logging.info(f"Tiempo total:               {duracion:.2f} segundos")
        logging.info(f"Velocidad:                  {(len(df) / duracion):.2f} registros/segundo")
        logging.info(f"\nArchivos de log generados:")
        logging.info(f"  - Log general:    {log_filename}")
        logging.info(f"  - Log de errores: {error_filename}")
        logging.info("="*80)
        
        if errores > 0:
            logging.warning(f"\n⚠️  Se encontraron {errores} errores")
            logging.warning(f"Revisa {error_filename} para detalles completos")
            if errores_detalle:
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
    print("IMPORTADOR SAP CRD1 - DIRECCIONES DE CLIENTES")
    print("="*80)
    print("Columnas obligatorias : Address, CardCode, AdresType")
    print("Columnas opcionales   : U_BO_Name, U_BO_LastName, U_BO_Cellolar,")
    print("                        Street, Block, State, City, County,")
    print("                        Status_Integration, Status_Comments, CreationDate")
    print("Nota: 'Id' es autoincremental — NO debe incluirse en el Excel")
    print("="*80 + "\n")
    
    # Opción 1: Buscar automáticamente el archivo Excel en el directorio actual
    resultado = importar_CRD1_upsert()
    
    # Opción 2: Especificar ruta manualmente (descomenta si prefieres esta opción)
    # resultado = importar_CRD1_upsert(r"C:\ruta\exacta\CRD1.xlsx")
    
    print("\n" + "="*80)
    if resultado:
        print("✓ PROCESO COMPLETADO EXITOSAMENTE")
    else:
        print("❌ PROCESO FALLÓ - Revisa los logs")
    print("="*80 + "\n")