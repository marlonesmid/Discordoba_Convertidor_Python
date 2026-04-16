import json
import os
from datetime import datetime

# Configuración de rutas
RUTA_BASE    = r"C:\Convertidor\Wolkvox\Information\Agents"
ARCHIVO_ENTRADA = os.path.join(RUTA_BASE, 'agentes.json')
ARCHIVO_SALIDA  = os.path.join(RUTA_BASE, 'inserts_agentes.sql')
TABLA = "QUIRAMA.dbo.Integracion_Wolkvox_agentes"

COLUMNAS_SQL = [
    'agent_id', 'agent_name', 'agent_dni', 'agent_status',
    'last_use', 'agent_sso', 'enabled', 'updated_at'
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

        # Validar estructura del JSON
        if isinstance(data, dict):
            code = data.get('code', '')
            if code != "200":
                print(f"❌ El JSON retornó code={code}. No se procesará.")
                return
            registros = data.get('data', [])
        else:
            registros = data  # fallback: lista directa

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
                    else:
                        val = r.get(col, None)
                        valores_fila.append(limpiar_valor(val))

                columnas_str = ", ".join(COLUMNAS_SQL)
                valores_str  = ", ".join(valores_fila)

                # MERGE para evitar duplicados por agent_id (PK)
                f_out.write(
                    f"MERGE INTO {TABLA} AS target\n"
                    f"USING (SELECT {valores_str}) AS source ({columnas_str})\n"
                    f"ON target.agent_id = source.agent_id\n"
                    f"WHEN MATCHED THEN\n"
                    f"    UPDATE SET "
                    + ", ".join(
                        f"target.{col} = source.{col}"
                        for col in COLUMNAS_SQL if col != 'agent_id'
                    ) +
                    f"\nWHEN NOT MATCHED THEN\n"
                    f"    INSERT ({columnas_str}) VALUES ({valores_str});\n\n"
                )

            f_out.write("COMMIT TRANSACTION;\n")

        print(f"✅ ¡Éxito! {len(registros)} registro(s) generados en: {ARCHIVO_SALIDA}")

    except json.JSONDecodeError as e:
        print(f"❌ Error al parsear el JSON: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    procesar()