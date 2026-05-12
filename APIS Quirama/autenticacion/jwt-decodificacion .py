"""
decode_token.py
===============
Decodifica un JWT del Gateway Quirama e imprime todos sus valores
con validación de firma, expiración y audiencia.

Uso:
    python decode_token.py --token "eyJhbGci..."
    python decode_token.py                         ← pide el token interactivamente
    python decode_token.py --no-verify             ← solo lee el contenido sin validar firma

Requisitos:
    pip install PyJWT
"""

import jwt
import datetime
import argparse
import json
import base64
import sys

# ── Configuración ─────────────────────────────────────────────────────────────
SECRET_KEY = "QU1RAM4-G4T3W4Y-X7k$mP2#vL9@nR5-PRD-2026"   # ← misma que en gen_token.py
ALGORITHM  = "HS256"

# ── Colores para consola ──────────────────────────────────────────────────────
CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

def decode_base64_part(part: str) -> dict:
    """Decodifica una parte Base64Url del JWT sin verificar firma."""
    padding = 4 - len(part) % 4
    part   += "=" * (padding % 4)
    return json.loads(base64.urlsafe_b64decode(part).decode("utf-8"))

def calcular_estado(exp_timestamp: int) -> tuple:
    """Calcula si el token está vigente o expirado."""
    ahora      = datetime.datetime.now(datetime.timezone.utc)
    expiracion = datetime.datetime.fromtimestamp(exp_timestamp, datetime.timezone.utc)
    diferencia = expiracion - ahora

    if diferencia.total_seconds() > 0:
        minutos = int(diferencia.total_seconds() // 60)
        segundos = int(diferencia.total_seconds() % 60)
        return True, f"VIGENTE — expira en {minutos}m {segundos}s"
    else:
        transcurrido = ahora - expiracion
        minutos = int(transcurrido.total_seconds() // 60)
        return False, f"EXPIRADO hace {minutos} minuto(s)"

def imprimir_raw(token: str):
    """Imprime el contenido del token SIN verificar la firma."""
    partes = token.strip().split(".")
    if len(partes) != 3:
        print(f"{RED}❌ Token malformado: debe tener 3 partes separadas por '.'{RESET}")
        sys.exit(1)

    header  = decode_base64_part(partes[0])
    payload = decode_base64_part(partes[1])

    print(f"\n{YELLOW}⚠️  MODO SIN VERIFICACIÓN — La firma NO fue validada{RESET}")
    imprimir_resultado(header, payload, partes[2], verificado=False)

def imprimir_resultado(header: dict, payload: dict, firma: str, verificado: bool):
    """Imprime el resultado de la decodificación de forma visual."""
    vigente, estado_msg = calcular_estado(payload.get("exp", 0))
    estado_color = GREEN if vigente else RED
    estado_icon  = "✅" if vigente else "❌"

    print(f"\n{BOLD}{'═'*65}{RESET}")
    print(f"{BOLD}  🔍  TOKEN JWT DECODIFICADO — Gateway Quirama{RESET}")
    print(f"{BOLD}{'═'*65}{RESET}\n")

    # ── HEADER ────────────────────────────────────────────────────────────────
    print(f"{BOLD}── HEADER ────────────────────────────────────────────{RESET}")
    print(f"   {'Campo':<15} {'Valor':<20} {'Significado'}")
    print(f"   {'─'*55}")
    significados_header = {
        "alg": "Algoritmo de firma",
        "typ": "Tipo de token",
    }
    for k, v in header.items():
        sig = significados_header.get(k, "")
        print(f"   {k:<15} {str(v):<20} {sig}")

    # ── PAYLOAD ───────────────────────────────────────────────────────────────
    print(f"\n{BOLD}── PAYLOAD ───────────────────────────────────────────{RESET}")
    print(f"   {'Campo':<15} {'Valor':<28} {'Significado'}")
    print(f"   {'─'*65}")

    significados = {
        "clientCode": "Código del cliente en Quirama",
        "createdBy":  "Usuario que generó el token",
        "assignedTo": "A quién está asignado el token",
        "database":   "Base de datos SAP B1 a la que se conecta",
        "iat":        "Issued At — cuándo fue creado",
        "exp":        "Expires At — cuándo vence",
    }

    for k, v in payload.items():
        sig = significados.get(k, "")
        if k in ("iat", "exp"):
            dt  = datetime.datetime.fromtimestamp(v, datetime.timezone.utc)
            val = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
            print(f"   {k:<15} {val:<28} {sig}")
        elif k == "aud" and isinstance(v, list):
            print(f"   {k:<15} {', '.join(v):<28} {sig}")
        else:
            print(f"   {k:<15} {str(v):<28} {sig}")

    # ── FIRMA ─────────────────────────────────────────────────────────────────
    print(f"\n{BOLD}── FIRMA ─────────────────────────────────────────────{RESET}")
    print(f"   {firma[:48]}...")
    if verificado:
        print(f"   {GREEN}✅ Firma válida — el token no fue modificado{RESET}")
    else:
        print(f"   {YELLOW}⚠️  Firma NO verificada{RESET}")

    # ── ESTADO ────────────────────────────────────────────────────────────────
    print(f"\n{BOLD}── ESTADO ────────────────────────────────────────────{RESET}")
    print(f"   {estado_icon} {estado_color}{estado_msg}{RESET}")


    print(f"{BOLD}{'═'*65}{RESET}\n")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decodificador de JWT para Gateway Quirama")
    parser.add_argument("--token",     default=None,  help="Token JWT a decodificar")
    parser.add_argument("--no-verify", action="store_true", help="Decodificar sin validar firma")
    args = parser.parse_args()

    # Obtener el token
    token = args.token
    if not token:
        print(f"\n{BOLD}Pega el token JWT y presiona Enter:{RESET}")
        token = input("Token: ").strip()

    if not token:
        print(f"{RED}❌ No se proporcionó ningún token.{RESET}")
        sys.exit(1)

    # ── Sin verificación ──────────────────────────────────────────────────────
    if args.no_verify:
        imprimir_raw(token)
        sys.exit(0)

    # ── Con verificación completa ─────────────────────────────────────────────
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_aud": False},
        )
        partes = token.strip().split(".")
        header = decode_base64_part(partes[0])
        imprimir_resultado(header, payload, partes[2], verificado=True)

    except jwt.ExpiredSignatureError:
        print(f"\n{RED}{'═'*65}{RESET}")
        print(f"{RED}  ❌  TOKEN EXPIRADO{RESET}")
        print(f"{RED}{'═'*65}{RESET}")
        print(f"\n  El token venció. Solicita uno nuevo con POST /api/Auth/GetToken\n")
        print(f"  {YELLOW}Tip: usa --no-verify para ver el contenido del token expirado{RESET}\n")

    except jwt.InvalidSignatureError:
        print(f"\n{RED}{'═'*65}{RESET}")
        print(f"{RED}  ❌  FIRMA INVÁLIDA{RESET}")
        print(f"{RED}{'═'*65}{RESET}")
        print(f"\n  El token fue modificado o fue firmado con otra SECRET_KEY.\n")

    except jwt.InvalidAudienceError:
        print(f"\n{RED}{'═'*65}{RESET}")
        print(f"{RED}  ❌  AUDIENCIA INVÁLIDA{RESET}")
        print(f"{RED}{'═'*65}{RESET}")
        print(f"\n  El token no fue emitido para '{AUDIENCE}'.\n")

    except jwt.DecodeError as e:
        print(f"\n{RED}❌ Token malformado: {e}{RESET}\n")

    except Exception as e:
        print(f"\n{RED}❌ Error inesperado: {e}{RESET}\n")