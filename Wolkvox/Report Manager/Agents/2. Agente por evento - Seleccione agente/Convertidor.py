import json
import os
from datetime import datetime

# Configuración de rutas
RUTA_BASE       = r"C:\Convertidor\Wolkvox\Report Manager\Agents\2. Agente por evento - Seleccione agente"
ARCHIVO_ENTRADA = os.path.join(RUTA_BASE, 'agentes_por_evento.json')
ARCHIVO_SALIDA  = os.path.join(RUTA_BASE, 'inserts_agentes_por_evento.sql')
TABLA = "QUIRAMA.dbo.Integracion_Wolkvox_ReportManager_Agents_AgentePorEvento"

# Sin 'id' ya que es IDENTITY(1,1) — SQL Server lo genera automáticamente
COLUMNAS_SQL = [
    'agent_id', 'agent_status', 'time', 'date_ini', 'date_end',
    'conn_id', 'type_interaction', 'destiny', 'telephone',
    'campaign_id', 'updated_at'
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

                # INSERT directo: cada fila es un evento/estado histórico único
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
