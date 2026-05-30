import requests
import hashlib

def check_breaches(email):
    """Verifica si el email ha sido filtrado usando HaveIBeenPwned"""
    try:
        sha1_hash = hashlib.sha1(email.encode()).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]
        
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            hashes = [line.split(':')[0] for line in response.text.splitlines()]
            if suffix in hashes:
                return f"⚠️  El email {email} ha sido encontrado en filtraciones de datos"
            else:
                return f"✅ No se encontraron filtraciones para {email}"
        return "❌ No se pudo verificar filtraciones"
    except Exception as e:
        return f"❌ Error verificando filtraciones: {str(e)}"

def get_email_info(email):
    """Función principal para OSINT de email"""
    results = []
    results.append(f"\n📧 ANALIZANDO EMAIL: {email}")
    results.append("=" * 50)
    
    # Verificar filtraciones
    results.append(check_breaches(email))
    
    # Información básica
    results.append(f"\n🔍 Datos básicos:")
    results.append(f"   • Dominio: {email.split('@')[-1]}")
    results.append(f"   • Usuario: {email.split('@')[0]}")
    
    return "\n".join(results)
