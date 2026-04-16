import json
import os

# Configuración de rutas
RUTA_BASE = r"C:\Convertidor\INVAS" 
ARCHIVO_ENTRADA = os.path.join(RUTA_BASE, 'datos.json')
ARCHIVO_SALIDA = os.path.join(RUTA_BASE, 'inserts_inventario.sql')
TABLA = "IntegracionINVAS_consultaWmsCajaAlmacenadasWS"

# EL ORDEN DEBE SER FIJO PARA EVITAR EL ERROR 10709
COLUMNAS_SQL = [
    'idLpn', 'sku', 'lote', 'fechaAlmacenado', 'numSerieInvariable', 
    'estado', 'unidadesDisponibles', 'nombre', 'tipounidad', 
    'tipoUbicacion', 'zonaUbicacion', 'transaccion', 'ubicacion', 
    'qa', 'condicionLpn', 'sitio', 'deshabilitado'
]

def limpiar_valor(valor):
    if valor is None or str(valor).strip().upper() == "NULL" or str(valor).strip() == "":
        return "NULL"
    # Escapar comillas simples para evitar errores de sintaxis SQL
    v_safe = str(valor).replace("'", "''")
    return f"'{v_safe}'"

def procesar():
    try:
        if not os.path.exists(ARCHIVO_ENTRADA):
            print(f"❌ Error: No se encontró {ARCHIVO_ENTRADA}")
            return

        with open(ARCHIVO_ENTRADA, 'r', encoding='utf-8') as f:
            data = json.load(f)

        registros = data.get('listaWmsCaja', []) if isinstance(data, dict) else data

        with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f_out:
            f_out.write("SET NOCOUNT ON;\nBEGIN TRANSACTION;\n\n")
            
            for r in registros:
                valores_fila = []
                for col in COLUMNAS_SQL:
                    # Si la columna no está en este registro del JSON, usamos None
                    val = r.get(col, None)
                    valores_fila.append(limpiar_valor(val))
                
                columnas_str = ", ".join(COLUMNAS_SQL)
                valores_str = ", ".join(valores_fila)
                
                # Insertamos fila por fila para evitar errores de estructura irregular
                f_out.write(f"INSERT INTO {TABLA} ({columnas_str}) VALUES ({valores_str});\n")

            f_out.write("\nCOMMIT TRANSACTION;")
            
        print(f"✅ ¡Éxito! SQL generado en: {ARCHIVO_SALIDA}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    procesar()