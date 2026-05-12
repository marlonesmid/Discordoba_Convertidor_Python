"""
gen_token.py
============
Genera un JWT firmado con HMAC SHA-256 para el Gateway Quirama.
La fecha/hora de vencimiento se define de forma exacta.

Uso:
    py gen_token.py                                             ← pide datos interactivamente
    py gen_token.py --expires "2026-12-31"                     ← vence el 31 dic a las 23:59:59
    py gen_token.py --expires "2026-12-31 18:00:00"            ← vence el 31 dic a las 6pm
    py gen_token.py --client AGT-002 --expires "2027-01-15"

Requisitos:
    pip install PyJWT
"""

import jwt
import datetime
import argparse
import json
import base64

# ── Configuración ─────────────────────────────────────────────────────────────
SECRET_KEY = "QU1RAM4-G4T3W4Y-X7k$mP2#vL9@nR5-PRD-2026"   # ← cambiar en producción
ALGORITHM  = "HS256"

# ── Colores para consola ──────────────────────────────────────────────────────
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# ── Helpers ───────────────────────────────────────────────────────────────────
def separar_partes(token: str):
    partes = token.split(".")
    def decode_part(part):
        padding = 4 - len(part) % 4
        part += "=" * (padding % 4)
        return json.loads(base64.urlsafe_b64decode(part).decode("utf-8"))
    return decode_part(partes[0]), decode_part(partes[1]), partes[2]

def parsear_fecha(texto: str) -> datetime.datetime:
    """Acepta 'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM:SS'."""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.datetime.strptime(texto.strip(), fmt)
            # Si solo se pasó fecha, vence al final del día
            if fmt == "%Y-%m-%d":
                dt = dt.replace(hour=23, minute=59, second=59)
            return dt.replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"Formato de fecha inválido: '{texto}'. Usa YYYY-MM-DD o YYYY-MM-DD HH:MM:SS")

def pedir_interactivo() -> tuple:
    """Solicita los datos por consola si no se pasan como argumentos."""
    print(f"\n{BOLD}{'─'*65}{RESET}")
    print(f"{BOLD}  Generador de Token JWT — Gateway Quirama{RESET}")
    print(f"{BOLD}{'─'*65}{RESET}\n")

    client_code = input(f"  Código cliente   (default: AGT-001)      : ").strip() or "AGT-001"
    created_by  = input(f"  Creado por       (default: admin@quirama.com) : ").strip() or "admin@quirama.com"
    assigned_to = input(f"  Asignado a       (default: agente-ia-whatsapp): ").strip() or "agente-ia-whatsapp"
    database    = input(f"  Base de datos    (default: SBO_QUIRAMA_PRD)   : ").strip() or "SBO_QUIRAMA_PRD"

    while True:
        expires_str = input(f"  Fecha vencimiento (YYYY-MM-DD o YYYY-MM-DD HH:MM:SS): ").strip()
        try:
            expiracion = parsear_fecha(expires_str)
            break
        except ValueError as e:
            print(f"  {RED}❌ {e}{RESET}")

    return client_code, created_by, assigned_to, database, expiracion

# ── Generación ────────────────────────────────────────────────────────────────
def generar_token(client_code: str, created_by: str, assigned_to: str,
                  database: str, expiracion: datetime.datetime) -> tuple:
    ahora = datetime.datetime.now(datetime.timezone.utc)

    if expiracion <= ahora:
        raise ValueError(f"La fecha de vencimiento {expiracion.strftime('%Y-%m-%d %H:%M:%S')} UTC ya pasó.")

    payload = {
        "clientCode": client_code,
        "createdBy":  created_by,
        "assignedTo": assigned_to,
        "database":   database,
        "iat":        ahora,
        "exp":        expiracion,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, payload

# ── Impresión ─────────────────────────────────────────────────────────────────
def imprimir_token(token: str, payload: dict, expiracion: datetime.datetime):
    header, pay_decoded, firma = separar_partes(token)
    ahora      = datetime.datetime.now(datetime.timezone.utc)
    diferencia = expiracion - ahora
    dias       = diferencia.days
    horas      = diferencia.seconds // 3600
    minutos    = (diferencia.seconds % 3600) // 60

    print(f"\n{BOLD}{'═'*65}{RESET}")
    print(f"{BOLD}  🔐  TOKEN JWT GENERADO — Gateway Quirama{RESET}")
    print(f"{BOLD}{'═'*65}{RESET}\n")

    # Token coloreado
    partes = token.split(".")
    print(f"{BOLD}Token completo:{RESET}")
    print(f"{CYAN}{partes[0]}{RESET}.{GREEN}{partes[1]}{RESET}.{YELLOW}{partes[2]}{RESET}\n")

    # Header
    print(f"{BOLD}── HEADER {CYAN}(azul){RESET}{BOLD} ─────────────────────────────{RESET}")
    for k, v in header.items():
        print(f"   {k:12} → {v}")

    # Payload
    print(f"\n{BOLD}── PAYLOAD {GREEN}(verde){RESET}{BOLD} ──────────────────────────{RESET}")
    for k, v in pay_decoded.items():
        if k in ("iat", "exp"):
            dt = datetime.datetime.fromtimestamp(v, datetime.timezone.utc)
            print(f"   {k:12} → {v}  ({dt.strftime('%Y-%m-%d %H:%M:%S UTC')})")
        else:
            print(f"   {k:12} → {v}")

    # Firma
    print(f"\n{BOLD}── FIRMA {YELLOW}(amarilla){RESET}{BOLD} ────────────────────────{RESET}")
    print(f"   {firma[:48]}...")
    print(f"   (HMAC SHA-256 con SECRET_KEY del servidor)")

    # Resumen
    print(f"\n{BOLD}{'─'*65}{RESET}")
    print(f"  ✅  Cliente    : {payload['clientCode']}")
    print(f"  ✅  Creado por : {payload['createdBy']}")
    print(f"  ✅  Asignado a : {payload['assignedTo']}")
    print(f"  ✅  Base datos : {payload['database']}")
    print(f"  ✅  Creado     : {ahora.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"  ✅  Vence      : {expiracion.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"  ✅  Vigencia   : {dias} día(s), {horas} hora(s), {minutos} minuto(s)")
    print(f"  ✅  Algoritmo  : {ALGORITHM}")
    print(f"{BOLD}{'─'*65}{RESET}")
    print(f"\n{BOLD}Uso en request:{RESET}")
    print(f"  Authorization: Bearer {token[:48]}...\n")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de JWT para Gateway Quirama")
    parser.add_argument("--client",      default="AK001", help="Código del cliente/agente (ej: AGT-001)")
    parser.add_argument("--created-by",  default="desarrollostech@discordoba.com", help="Usuario que genera el token (ej: admin@quirama.com)")
    parser.add_argument("--assigned-to", default="OneSource", help="A quién se le asigna (ej: agente-ia-whatsapp)")
    parser.add_argument("--database",    default="QUIRAMA", help="Base de datos (ej: QUIRAMA)")
    parser.add_argument("--expires",     default="2026-11-11 23:59:59", help="Fecha de vencimiento: YYYY-MM-DD o YYYY-MM-DD HH:MM:SS")
    args = parser.parse_args()

    # Si no se pasan argumentos → modo interactivo
    if not any([args.client, args.created_by, args.assigned_to, args.database, args.expires]):
        client_code, created_by, assigned_to, database, expiracion = pedir_interactivo()
    else:
        client_code = args.client      or "AGT-001"
        created_by  = args.created_by  or "admin@quirama.com"
        assigned_to = args.assigned_to or "agente-ia-whatsapp"
        database    = args.database    or "SBO_QUIRAMA_PRD"
        if not args.expires:
            print(f"{RED}❌ Debes indicar --expires 'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM:SS'{RESET}")
            exit(1)
        try:
            expiracion = parsear_fecha(args.expires)
        except ValueError as e:
            print(f"{RED}❌ {e}{RESET}")
            exit(1)

    try:
        token, payload = generar_token(client_code, created_by, assigned_to, database, expiracion)
        imprimir_token(token, payload, expiracion)
    except ValueError as e:
        print(f"\n{RED}❌ {e}{RESET}\n")
        exit(1)