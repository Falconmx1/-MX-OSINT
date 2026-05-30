import requests
import socket
import ipaddress
from urllib.parse import urlparse

def get_ip_from_domain(domain):
    """Obtiene IP de un dominio"""
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        return None

def get_ip_geolocation(ip):
    """Obtiene geolocalización de una IP usando API gratuita"""
    try:
        # API gratuita sin llave (ip-api.com)
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                geo = {
                    'pais': data.get('country', 'Desconocido'),
                    'region': data.get('regionName', 'Desconocido'),
                    'ciudad': data.get('city', 'Desconocido'),
                    'lat': data.get('lat', 0),
                    'lon': data.get('lon', 0),
                    'isp': data.get('isp', 'Desconocido'),
                    'org': data.get('org', 'Desconocido'),
                    'zip': data.get('zip', 'Desconocido')
                }
                return geo
        return None
    except:
        return None

def get_ip_reputation(ip):
    """Verifica reputación de IP (spam, abuso)"""
    try:
        # Verificar en AbuseIPDB (sin llave, limitado)
        url = f"https://www.abuseipdb.com/check/{ip}"
        response = requests.get(url, timeout=10, headers={'User-Agent': 'MX-OSINT'})
        
        if "has been reported" in response.text:
            return "⚠️ Posible IP con reportes de abuso"
        elif "is a clean IP" in response.text:
            return "✅ IP limpia sin reportes conocidos"
        else:
            return "ℹ️ Sin información de reputación"
    except:
        return "❌ No se pudo verificar reputación"

def get_geo_from_coordinates(lat, lon):
    """Obtiene dirección aproximada de coordenadas (reverse geocoding)"""
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&addressdetails=1"
        response = requests.get(url, timeout=10, headers={'User-Agent': 'MX-OSINT'})
        
        if response.status_code == 200:
            data = response.json()
            address = data.get('display_name', 'No disponible')
            # Limitar longitud
            if len(address) > 200:
                address = address[:200] + "..."
            return address
        return "No disponible"
    except:
        return "No disponible"

def get_map_link(lat, lon):
    """Genera enlaces a mapas"""
    links = {
        'Google Maps': f"https://www.google.com/maps?q={lat},{lon}",
        'OpenStreetMap': f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}",
        'Bing Maps': f"https://www.bing.com/maps?cp={lat}~{lon}"
    }
    return links

def analyze_ip_geo(target):
    """Función principal para geolocalización"""
    results = []
    results.append(f"\n🗺️ GEOLOCALIZANDO: {target}")
    results.append("=" * 50)
    
    # Determinar si es IP o dominio
    ip = None
    is_domain = False
    
    # Validar si es dominio
    if not target.replace('.', '').isdigit():
        is_domain = True
        results.append(f"\n🌐 Resolviendo dominio: {target}")
        ip = get_ip_from_domain(target)
        if ip:
            results.append(f"   • IP encontrada: {ip}")
        else:
            results.append(f"   • ❌ No se pudo resolver el dominio")
            return "\n".join(results)
    else:
        ip = target
    
    # Geolocalizar IP
    geo = get_ip_geolocation(ip)
    
    if not geo:
        results.append(f"\n❌ No se pudo geolocalizar {ip}")
        results.append(f"   • Puede ser una IP privada o inválida")
        return "\n".join(results)
    
    results.append(f"\n📍 UBICACIÓN ESTIMADA:")
    results.append(f"   • País: {geo['pais']}")
    results.append(f"   • Región/Estado: {geo['region']}")
    results.append(f"   • Ciudad: {geo['ciudad']}")
    results.append(f"   • Código postal: {geo['zip']}")
    results.append(f"   • Coordenadas: {geo['lat']}, {geo['lon']}")
    results.append(f"   • ISP/Proveedor: {geo['isp']}")
    results.append(f"   • Organización: {geo['org']}")
    
    # Enlaces a mapas
    if geo['lat'] and geo['lon']:
        results.append(f"\n🗺️ VER EN MAPAS:")
        for name, link in get_map_link(geo['lat'], geo['lon']).items():
            results.append(f"   • {name}: {link}")
        
        # Dirección aproximada
        results.append(f"\n🏠 DIRECCIÓN APROXIMADA:")
        address = get_geo_from_coordinates(geo['lat'], geo['lon'])
        results.append(f"   {address}")
    
    # Reputación
    results.append(f"\n🛡️ REPUTACIÓN:")
    results.append(f"   • {get_ip_reputation(ip)}")
    
    # Riesgo (si es dominio)
    if is_domain:
        results.append(f"\n⚠️ NOTA:")
        results.append(f"   • La ubicación es del servidor, no del dueño del dominio")
        results.append(f"   • El sitio puede usar CDN (Cloudflare, etc) ocultando IP real")
    
    return "\n".join(results)
