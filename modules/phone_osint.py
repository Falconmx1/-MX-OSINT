import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import re

def validate_phone(phone):
    """Valida y formatea número telefónico"""
    try:
        # Limpiar número (solo dígitos y +)
        phone_clean = re.sub(r'[^\d+]', '', phone)
        
        # Intentar parsear como número internacional
        if phone_clean.startswith('+'):
            parsed = phonenumbers.parse(phone_clean, None)
        else:
            # Asumir México (+52) si no tiene código país
            parsed = phonenumbers.parse(f"+52{phone_clean}", None)
        
        if phonenumbers.is_valid_number(parsed):
            formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            return parsed, formatted, national
        return None, None, None
    except:
        return None, None, None

def get_phone_carrier(parsed_number):
    """Obtiene la compañía telefónica (soporta México)"""
    try:
        carrier_name = carrier.name_for_number(parsed_number, "es")
        return carrier_name if carrier_name else "No disponible"
    except:
        return "No disponible"

def get_phone_location(parsed_number):
    """Obtiene ubicación geográfica del número (ciudad/estado)"""
    try:
        # Usar geocoder local
        location = geocoder.description_for_number(parsed_number, "es")
        return location if location else "No disponible"
    except:
        return "No disponible"

def get_timezone(parsed_number):
    """Obtiene la zona horaria asociada"""
    try:
        tz = timezone.time_zones_for_number(parsed_number)
        return list(tz)[0] if tz else "No disponible"
    except:
        return "No disponible"

def check_breach_sites(phone):
    """Verifica en APIs públicas si el número ha sido expuesto"""
    results = []
    
    try:
        # API de haveibeenpwned para números (solo si está expuesto)
        url = f"https://haveibeenpwned.com/phone/{phone}"
        response = requests.get(url, timeout=10, headers={'User-Agent': 'MX-OSINT'})
        
        if response.status_code == 200 and "Oh no — pwned!" in response.text:
            results.append("   • ⚠️ Número encontrado en filtraciones de datos")
        else:
            results.append("   • ✅ No se encontró en filtraciones conocidas")
    except:
        results.append("   • ❌ No se pudo verificar filtraciones")
    
    return results

def search_phone_websites(phone):
    """Busca el número en directorios públicos"""
    results = []
    directories = [
        f"https://www.google.com/search?q={phone}",
        f"https://www.buscador.com.mx/resultados?q={phone}",
        f"https://www.infobel.com/es/mexico/search/{phone}"
    ]
    
    results.append("   • Para búsqueda manual revisa:")
    for url in directories[:2]:  # Mostrar solo 2 para no saturar
        results.append(f"     - {url}")
    
    return results

def analyze_phone(phone):
    """Función principal para OSINT de número telefónico"""
    results = []
    results.append(f"\n📞 ANALIZANDO NÚMERO: {phone}")
    results.append("=" * 50)
    
    # Validar y parsear
    parsed, formatted, national = validate_phone(phone)
    
    if not parsed:
        results.append("❌ Número telefónico inválido")
        results.append("   • Usa formato internacional (+521234567890)")
        results.append("   • O nacional: 1234567890 (asume México +52)")
        return "\n".join(results)
    
    results.append(f"\n📋 INFORMACIÓN DEL NÚMERO:")
    results.append(f"   • Formato internacional: {formatted}")
    results.append(f"   • Formato nacional: {national}")
    results.append(f"   • País: México (+52)")
    results.append(f"   • Compañía: {get_phone_carrier(parsed)}")
    results.append(f"   • Ubicación estimada: {get_phone_location(parsed)}")
    results.append(f"   • Zona horaria: {get_timezone(parsed)}")
    
    # Verificar filtraciones
    results.append(f"\n🔐 SEGURIDAD:")
    results.extend(check_breach_sites(national))
    
    # Enlaces para búsqueda manual
    results.append(f"\n🔍 BÚSQUEDA MANUAL:")
    results.extend(search_phone_websites(formatted))
    
    results.append(f"\n💡 RECOMENDACIONES:")
    results.append(f"   • Verifica en WhatsApp Web si tiene perfil")
    results.append(f"   • Busca en Telegram usando el número")
    results.append(f"   • Usa el comando: python mx_osint.py --phone {phone}")
    
    return "\n".join(results)
