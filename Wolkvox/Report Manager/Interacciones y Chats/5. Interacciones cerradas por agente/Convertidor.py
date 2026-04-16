import json
import os
import re
from datetime import datetime

# Configuración de rutas
RUTA_BASE       = r"C:\Convertidor\Wolkvox\Report Manager\Interacciones y Chats\5. Interacciones cerradas por agente"
ARCHIVO_ENTRADA = os.path.join(RUTA_BASE, 'Interacciones_cerradas_por_agente.json')
ARCHIVO_SALIDA  = os.path.join(RUTA_BASE, 'Interacciones_cerradas_por_agente.sql')
TABLA = "QUIRAMA.dbo.Integracion_Wolkvox_ReportManager_InteraccionesyChats_InteraccionesCerradasPorAgente"

# 'id' es IDENTITY — SQL Server lo genera automáticamente
# 'agent_id' se extrae del campo agent_name: "Nombre Apellido (12345)"
COLUMNAS_SQL = [
    'agent_name', 'agent_id', 'interactions', 'close_time', 'updated_at'
]

def limpiar_valor(valor):
    if valor is None or str(valor).strip().upper() == "NULL" or str(valor).strip() == "":
        return "NULL"
    v_safe = str(valor).replace("'", "''")
    return f"'{v_safe}'"

def extraer_agent_id(agent_name):
    """Extrae el ID numérico del paréntesis en 'Nombre Apellido (12345)'."""
    match = re.search(r'\((\d+)\)', str(agent_name))
    return match.group(1) if match else None

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
                    elif col == 'agent_id':
                        # Extraer ID del nombre: "Cristian Patiño (12978)" -> "12978"
                        agent_id = extraer_agent_id(r.get('agent_name', ''))
                        valores_fila.append(limpiar_valor(agent_id))
                    elif col == 'interactions':
                        # Guardar como entero, sin comillas
                        val = r.get('interactions', None)
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
