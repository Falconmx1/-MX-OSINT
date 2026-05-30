import requests
from concurrent.futures import ThreadPoolExecutor

# Lista de plataformas principales para verificar
PLATFORMS = {
    "GitHub": f"https://github.com/{{username}}",
    "Twitter": f"https://twitter.com/{{username}}",
    "Instagram": f"https://www.instagram.com/{{username}}",
    "Reddit": f"https://www.reddit.com/user/{{username}}",
    "TikTok": f"https://www.tiktok.com/@{{username}}",
    "LinkedIn": f"https://www.linkedin.com/in/{{username}}",
    "YouTube": f"https://www.youtube.com/@{{username}}",
    "Pinterest": f"https://www.pinterest.com/{{username}}",
    "Twitch": f"https://www.twitch.tv/{{username}}",
    "Spotify": f"https://open.spotify.com/user/{{username}}"
}

def check_platform(platform_name, url_template, username):
    """Verifica si existe el perfil en una plataforma"""
    url = url_template.format(username=username)
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            # Evitar falsos positivos de páginas de error personalizadas
            content = response.text.lower()
            if "not found" not in content and "doesn't exist" not in content:
                return f"   • ✅ {platform_name}: {url}"
    except:
        pass
    return None

def search_social_media(username):
    """Función principal para OSINT de redes sociales"""
    results = []
    results.append(f"\n📱 BUSCANDO USUARIO: {username}")
    results.append("=" * 50)
    results.append("\n🔍 PERFILES ENCONTRADOS:")
    
    found = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for platform, url_template in PLATFORMS.items():
            future = executor.submit(check_platform, platform, url_template, username)
            futures.append(future)
        
        for future in futures:
            result = future.result()
            if result:
                results.append(result)
                found += 1
    
    if found == 0:
        results.append("   • ❌ No se encontraron perfiles públicos")
    else:
        results.append(f"\n📊 Total de perfiles encontrados: {found}")
    
    results.append("\n💡 Sugerencia: Revisa también plataformas hispanas como Taringa, Dailymotion, etc.")
    return "\n".join(results)
