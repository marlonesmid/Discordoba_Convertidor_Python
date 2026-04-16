import json
import os
from datetime import datetime

# Configuración de rutas
RUTA_BASE       = r"C:\Convertidor\Wolkvox\Report Manager\Skills\2. Detalle de llamadas abandonadas"
ARCHIVO_ENTRADA = os.path.join(RUTA_BASE, 'llamadas_abandonadas.json')
ARCHIVO_SALIDA  = os.path.join(RUTA_BASE, 'inserts_llamadas_abandonadas.sql')
TABLA = "QUIRAMA.dbo.Integracion_Wolkvox_ReportManager_Skills_DetalleLlamadasAbandonadas"

# Campos enteros — se insertan sin comillas
CAMPOS_INT = {'abandon_time'}

# 'id' es IDENTITY — SQL Server lo genera automáticamente
COLUMNAS_SQL = [
    'skill_name', 'skill_id', 'conn_id', 'date', 'result',
    'ani', 'abandon_time', 'type_interaction', 'customer_id', 'updated_at'
]

def limpiar_valor(valor):
    if valor is None or str(valor).strip().upper() == "NULL" or str(valor).strip() == "":
        return "NULL"
    v_safe = str(valor).replace("'", "''")
    return f"'{v_safe}'"

def procesar():
    try:
        if not os.path.exists(ARCHIVO_ENTRADA):
            print(f"❌ Error: No se encontró {ARCHIVO_ENTRADA}")
            return

        with open(ARCHIVO_ENTRADA, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict):
            code = data.get('code', '')
            if code != "200":
                print(f"❌ El JSON retornó code={code}. No se procesará.")
                return
            registros = data.get('data', [])
        else:
            registros = data

        if not registros:
            print("⚠️ No hay registros en 'data' para procesar.")
            return

        timestamp_ejecucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f_out:
            f_out.write("SET NOCOUNT ON;\nBEGIN TRANSACTION;\n\n")

            for r in registros:
                valores_fila = []
                for col in COLUMNAS_SQL:
                    if col == 'updated_at':
                        valores_fila.append(f"'{timestamp_ejecucion}'")
                    elif col in CAMPOS_INT:
                        val = r.get(col, None)
                        if val is None or str(val).strip() == "":
                            valores_fila.append("NULL")
                        else:
                            valores_fila.append(str(int(val)))
                    else:
                        val = r.get(col, None)
                        valores_fila.append(limpiar_valor(val))

                columnas_str = ", ".join(COLUMNAS_SQL)
                valores_str  = ", ".join(valores_fila)

                f_out.write(
                    f"INSERT INTO {TABLA} ({columnas_str}) VALUES ({valores_str});\n"
                )

            f_out.write("\nCOMMIT TRANSACTION;\n")

        print(f"✅ ¡Éxito! {len(registros)} registro(s) generados en: {ARCHIVO_SALIDA}")

    except json.JSONDecodeError as e:
        print(f"❌ Error al parsear el JSON: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    procesar()
