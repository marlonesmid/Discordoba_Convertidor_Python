import os
import unicodedata
import pandas as pd
import pyodbc
import logging
import time
from datetime import datetime

# ============================================================
# LOGS
# ============================================================
log_filename   = f'importacion_ITT1_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
error_filename = f'errores_ITT1_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
error_logger = logging.getLogger('errores')
_eh = logging.FileHandler(error_filename, encoding='utf-8')
_eh.setLevel(logging.ERROR)
_eh.setFormatter(logging.Formatter('%(asctime)s - ERROR - %(message)s'))
error_logger.addHandler(_eh)

# ============================================================
# CONFIGURACION
# ============================================================
CONNECTION_STRING = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=20.110.82.192\\SQLEXPRESS;"
    "Database=IA_Retos;"
    "UID=ConexionDiscordoba;"
    "PWD=Srv1Discordoba;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=60;"       # espera hasta 60s al conectar
)

TABLA = "IntegracionSAP_ITT1"

MAPEO_COLUMNAS = {
    "Orden de Produccion (Padre)" : "Father",
    "Numero de Componente"        : "ChildNum",
    "Orden Visual"                : "VisOrder",
    "Codigo Articulo"             : "Code",
    "Cantidad"                    : "Quantity",
    "Almacen"                     : "Warehouse",
    "Precio"                      : "Price",
    "Moneda"                      : "Currency",
    "Lista de Precios"            : "PriceList",
    "Precio Original"             : "OrigPrice",
    "Moneda Original"             : "OrigCurr",
    "Metodo de Emision"           : "IssueMthd",
    "Unidad de Medida"            : "Uom",
    "Comentario"                  : "Comment",
    "Instancia Log"               : "LogInstanc",
    "Tipo Objeto"                 : "Object",
    "Centro Costo 1"              : "OcrCode",
    "Centro Costo 2"              : "OcrCode2",
    "Centro Costo 3"              : "OcrCode3",
    "Centro Costo 4"              : "OcrCode4",
    "Centro Costo 5"              : "OcrCode5",
    "Insumo Principal"            : "PrncpInput",
    "Proyecto"                    : "Project",
    "Tipo"                        : "Type",
    "Codigo WIP"                  : "WipActCode",
    "Cantidad Adicional"          : "AddQuantit",
    "Texto Linea"                 : "LineText",
    "ID Etapa"                    : "StageId",
    "Nro Doc Base (UDF)"          : "U_DocNumBase",
    "Tipo Obj Base (UDF)"         : "U_ObjType",
}

LLAVE_SQL       = ["Father", "Code"]
COLUMNAS_SQL    = list(MAPEO_COLUMNAS.values())
COLUMNAS_UPDATE = [c for c in COLUMNAS_SQL if c not in LLAVE_SQL]

CAMPOS_INT     = {"ChildNum", "VisOrder", "PriceList", "LogInstanc", "StageId"}
CAMPOS_DECIMAL = {"Quantity", "Price", "OrigPrice", "AddQuantit"}

# Reintentos ante errores de conexion
MAX_REINTENTOS = 3
ESPERA_REINTENTO = 5   # segundos entre reintentos


# ============================================================
# HELPERS — conversion de tipos
# ============================================================

def limpiar_str(s):
    s = unicodedata.normalize('NFKD', str(s))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.strip().lower()


def convertir(valor_str, col_sql):
    if valor_str is None:
        return None
    if isinstance(valor_str, float) and pd.isna(valor_str):
        return None
    if isinstance(valor_str, str) and valor_str.strip() == '':
        return None

    if col_sql in CAMPOS_INT:
        try:
            return int(float(valor_str))
        except (ValueError, TypeError):
            return None

    if col_sql in CAMPOS_DECIMAL:
        try:
            return float(str(valor_str).replace(',', '.'))
        except (ValueError, TypeError):
            return None

    return str(valor_str).strip()


def val(row, col_sql):
    return convertir(row.get(col_sql), col_sql)


# ============================================================
# HELPERS — SQL
# ============================================================

def build_update_sql():
    set_clause   = ", ".join([f"[{c}] = ?" for c in COLUMNAS_UPDATE])
    where_clause = " AND ".join([f"[{k}] = ?" for k in LLAVE_SQL])
    return f"UPDATE [{TABLA}] SET {set_clause} WHERE {where_clause}"


def build_insert_sql():
    cols   = ", ".join([f"[{c}]" for c in COLUMNAS_SQL])
    params = ", ".join(["?" for _ in COLUMNAS_SQL])
    return f"INSERT INTO [{TABLA}] ({cols}) VALUES ({params})"


# ============================================================
# HELPERS — conexion con reconexion automatica
# ============================================================

def crear_conexion():
    """Abre conexion y cursor. Lanza excepcion si falla."""
    conn   = pyodbc.connect(CONNECTION_STRING, autocommit=False)
    cursor = conn.cursor()
    return conn, cursor


def es_error_conexion(exc):
    """Devuelve True si el error es de red/conexion caida."""
    codigos_red = {'08S01', '08001', 'HYT00', '08007'}
    msg = str(exc)
    return any(c in msg for c in codigos_red)


def ejecutar_con_reintento(conn, cursor, sql, params, sql_existe, sql_update, sql_insert):
    """
    Ejecuta una operacion. Si hay error de conexion, reconecta y reintenta
    hasta MAX_REINTENTOS veces.
    """
    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            cursor.execute(sql, params)
            return conn, cursor   # exito
        except Exception as e:
            if es_error_conexion(e) and intento < MAX_REINTENTOS:
                logging.warning(
                    f"  Conexion caida (intento {intento}/{MAX_REINTENTOS}). "
                    f"Reconectando en {ESPERA_REINTENTO}s..."
                )
                time.sleep(ESPERA_REINTENTO)
                try:
                    conn.close()
                except Exception:
                    pass
                conn, cursor = crear_conexion()
                logging.info("  Reconexion exitosa, reintentando operacion...")
            else:
                raise   # re-lanza si no es de red o se agotaron reintentos
    return conn, cursor


# ============================================================
# HELPERS — Excel
# ============================================================

def encontrar_archivo_excel():
    directorio = os.path.dirname(os.path.abspath(__file__))
    logging.info(f"Buscando Excel en: {directorio}")
    archivos = [f for f in os.listdir(directorio) if f.endswith(('.xlsx', '.xls'))]
    if archivos:
        logging.info(f"Archivo encontrado: {archivos[0]}")
        return os.path.join(directorio, archivos[0])
    logging.error("No se encontro ningun archivo Excel")
    return None


def normalizar_columnas(df):
    mapeo_limpio = {limpiar_str(k): v for k, v in MAPEO_COLUMNAS.items()}
    renombrar = {}
    for col in df.columns:
        clave = limpiar_str(col)
        if clave in mapeo_limpio:
            renombrar[col] = mapeo_limpio[clave]

    df.rename(columns=renombrar, inplace=True)
    logging.info(f"Columnas mapeadas: {len(renombrar)}/{len(MAPEO_COLUMNAS)}")

    faltantes = set(COLUMNAS_SQL) - set(df.columns)
    if faltantes:
        logging.warning(f"Columnas no encontradas (se usara NULL): {faltantes}")
        for col in faltantes:
            df[col] = None

    return df


# ============================================================
# PROCESO PRINCIPAL
# ============================================================

def importar_itt1_upsert(excel_path=None):
    inicio = datetime.now()
    logging.info("=" * 80)
    logging.info("INICIANDO IMPORTACION  -->  IntegracionSAP_ITT1")
    logging.info("=" * 80)

    # Localizar Excel
    if not excel_path or not os.path.exists(excel_path):
        excel_path = encontrar_archivo_excel()
    if not excel_path or not os.path.exists(excel_path):
        error_logger.error("Archivo Excel no encontrado")
        return False

    # Leer Excel
    try:
        logging.info(f"Leyendo: {excel_path}")
        df = pd.read_excel(excel_path, dtype=str)
        df = df.where(pd.notna(df), None)
        logging.info(f"Registros leidos  : {len(df)}")
        logging.info(f"Columnas en Excel : {', '.join(df.columns.tolist())}")
    except Exception as e:
        error_logger.error(f"Error leyendo Excel: {e}")
        return False

    df = normalizar_columnas(df)

    for col in LLAVE_SQL:
        if col not in df.columns:
            error_logger.error(f"Columna llave no mapeada: '{col}'")
            return False

    # Conectar
    try:
        logging.info("Conectando a SQL Server...")
        conn, cursor = crear_conexion()
        logging.info("Conexion establecida")
    except Exception as e:
        error_logger.error(f"Error de conexion: {e}")
        return False

    # Verificar tabla
    cursor.execute(
        "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?", TABLA
    )
    if cursor.fetchone()[0] == 0:
        error_logger.error(f"La tabla {TABLA} no existe en la BD")
        conn.close()
        return False

    sql_existe = (
        f"SELECT COUNT(*) FROM [{TABLA}] "
        f"WHERE [{LLAVE_SQL[0]}] = ? AND [{LLAVE_SQL[1]}] = ?"
    )
    sql_update = build_update_sql()
    sql_insert = build_insert_sql()

    logging.info(f"SQL UPDATE: {sql_update}")
    logging.info(f"SQL INSERT: {sql_insert}")

    insertados, actualizados, errores = 0, 0, 0
    errores_detalle = []
    BATCH = 50   # commit mas frecuente para reducir perdida ante caidas

    logging.info(f"Procesando {len(df)} filas (commit cada {BATCH})...")

    for index, row in df.iterrows():
        father = val(row, "Father")
        code   = val(row, "Code")

        try:
            # CHECK existe — con reintento
            conn, cursor = ejecutar_con_reintento(
                conn, cursor, sql_existe, (father, code),
                sql_existe, sql_update, sql_insert
            )
            existe = cursor.fetchone()[0] > 0

            if existe:
                vals = tuple(val(row, c) for c in COLUMNAS_UPDATE) + (father, code)
                conn, cursor = ejecutar_con_reintento(
                    conn, cursor, sql_update, vals,
                    sql_existe, sql_update, sql_insert
                )
                actualizados += 1
            else:
                vals = tuple(val(row, c) for c in COLUMNAS_SQL)
                conn, cursor = ejecutar_con_reintento(
                    conn, cursor, sql_insert, vals,
                    sql_existe, sql_update, sql_insert
                )
                insertados += 1

            procesados = insertados + actualizados
            if procesados % BATCH == 0:
                conn.commit()
                pct = (procesados / len(df)) * 100
                logging.info(
                    f"Progreso: {procesados}/{len(df)} ({pct:.1f}%) "
                    f"| INS: {insertados} | UPD: {actualizados}"
                )

        except Exception as e:
            errores += 1
            msg = f"Fila {index + 2} | Father={father}, Code={code} | {e}"
            errores_detalle.append(msg)
            logging.error(msg)
            error_logger.error(msg)

            # Si es error de conexion irreversible, intentar reconectar para las siguientes filas
            if es_error_conexion(e):
                logging.warning("Error de red persistente, intentando reconexion para continuar...")
                try:
                    conn.close()
                except Exception:
                    pass
                try:
                    conn, cursor = crear_conexion()
                    logging.info("Reconexion exitosa, continuando con siguiente fila")
                except Exception as re:
                    logging.error(f"No se pudo reconectar: {re}. Abortando.")
                    error_logger.error(f"Reconexion fallida: {re}")
                    break

    # Commit final
    try:
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        pass

    duracion = (datetime.now() - inicio).total_seconds()
    total_ok  = insertados + actualizados

    logging.info("\n" + "=" * 80)
    logging.info("RESUMEN")
    logging.info("=" * 80)
    logging.info(f"Total en Excel : {len(df)}")
    logging.info(f"Insertados     : {insertados}")
    logging.info(f"Actualizados   : {actualizados}")
    logging.info(f"Errores        : {errores}")
    if len(df) > 0:
        logging.info(f"Exito          : {total_ok / len(df) * 100:.2f}%")
        logging.info(f"Duracion       : {duracion:.2f} s  ({len(df)/duracion:.1f} reg/s)")
    logging.info(f"Log errores    : {error_filename}")
    logging.info("=" * 80)

    if errores:
        logging.warning(f"  {errores} errores -- revisa {error_filename}")
        for i, e in enumerate(errores_detalle[:5], 1):
            logging.warning(f"  {i}. {e}")
    else:
        logging.info("Sin errores")

    return errores == 0


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("IMPORTADOR SAP ITT1  --  IntegracionSAP_ITT1")
    print("=" * 80)
    print(f"Campos mapeados : {len(MAPEO_COLUMNAS)}")
    print(f"Reintentos red  : {MAX_REINTENTOS} (cada {ESPERA_REINTENTO}s)")
    print("=" * 80 + "\n")

    resultado = importar_itt1_upsert()
    # resultado = importar_itt1_upsert(r"C:\ruta\exacta\ITT1.xlsx")

    print("\n" + "=" * 80)
    print("PROCESO COMPLETADO" if resultado else "PROCESO FALLO -- revisa los logs")
    print("=" * 80 + "\n")