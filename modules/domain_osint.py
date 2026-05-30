import whois
import dns.resolver
import requests
from datetime import datetime

def get_whois_info(domain):
    """Obtiene información WHOIS del dominio"""
    try:
        w = whois.whois(domain)
        info = []
        info.append(f"   • Registrado por: {w.registrar if w.registrar else 'No disponible'}")
        info.append(f"   • Fecha creación: {w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date}")
        info.append(f"   • Fecha expiración: {w.expiration_date[0] if isinstance(w.expiration_date, list) else w.expiration_date}")
        return "\n".join(info)
    except Exception as e:
        return f"   • Error WHOIS: {str(e)}"

def get_dns_records(domain, record_type):
    """Obtiene registros DNS específicos"""
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        answers = resolver.resolve(domain, record_type)
        records = [str(rdata) for rdata in answers]
        return records if records else ["No encontrados"]
    except:
        return ["No disponibles"]

def get_subdomains(domain):
    """Busca subdominios usando crt.sh"""
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            subdomains = set()
            for entry in data[:50]:
                name = entry.get('name_value', '')
                if name:
                    for sub in name.split('\n'):
                        if domain in sub:
                            subdomains.add(sub.strip())
            return list(subdomains)[:20]
        return []
    except:
        return []

def analyze_domain(domain):
    """Función principal para OSINT de dominio"""
    results = []
    results.append(f"\n🌐 ANALIZANDO DOMINIO: {domain}")
    results.append("=" * 50)
    
    # WHOIS
    results.append("\n📋 WHOIS:")
    results.append(get_whois_info(domain))
    
    # DNS Records
    results.append("\n🔧 REGISTROS DNS:")
    for record in ['A', 'MX', 'NS', 'TXT']:
        records = get_dns_records(domain, record)
        results.append(f"   • {record}: {', '.join(records)}")
    
    # Subdominios
    results.append("\n🔍 SUBDOMINIOS ENCONTRADOS:")
    subdomains = get_subdomains(domain)
    if subdomains:
        for sub in subdomains[:10]:
            results.append(f"   • {sub}")
    else:
        results.append("   • No se encontraron subdominios públicos")
    
    return "\n".join(results)
