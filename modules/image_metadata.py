import requests
from PIL import Image
from PIL.ExifTags import TAGS
import io
import hashlib
from datetime import datetime
import os

def download_image(url):
    """Descarga imagen desde URL"""
    try:
        response = requests.get(url, timeout=15, stream=True)
        if response.status_code == 200:
            img_data = response.content
            return img_data
        return None
    except:
        return None

def extract_metadata_from_bytes(img_data):
    """Extrae metadatos EXIF de imagen en bytes"""
    try:
        image = Image.open(io.BytesIO(img_data))
        exifdata = image.getexif()
        
        metadata = {}
        
        # Extraer metadatos EXIF
        if exifdata:
            for tag_id, value in exifdata.items():
                tag = TAGS.get(tag_id, tag_id)
                metadata[tag] = value
        
        # Extraer información básica
        metadata['Formato'] = image.format
        metadata['Modo'] = image.mode
        metadata['Tamaño'] = f"{image.size[0]}x{image.size[1]} px"
        
        return metadata
    except Exception as e:
        return {'Error': f'No se pudo extraer metadata: {str(e)}'}

def calculate_image_hash(img_data):
    """Calcula hash de la imagen para búsqueda inversa"""
    md5_hash = hashlib.md5(img_data).hexdigest()
    sha1_hash = hashlib.sha1(img_data).hexdigest()
    return md5_hash, sha1_hash

def search_google_images(md5_hash):
    """Genera enlaces para búsqueda inversa"""
    links = {
        'Google Images': f"https://www.google.com/search?tbm=isch&q={md5_hash}",
        'TinEye': f"https://tineye.com/search?url=hash/{md5_hash}",
        'Bing Images': f"https://www.bing.com/images/search?q={md5_hash}"
    }
    return links

def analyze_image(image_input):
    """Función principal para metadata de imagen"""
    results = []
    results.append(f"\n🖼️ ANALIZANDO IMAGEN: {image_input}")
    results.append("=" * 50)
    
    # Determinar si es URL o archivo local
    img_data = None
    
    if image_input.startswith(('http://', 'https://')):
        results.append("\n📥 Descargando imagen desde URL...")
        img_data = download_image(image_input)
        if not img_data:
            results.append("❌ Error: No se pudo descargar la imagen")
            return "\n".join(results)
        results.append("✅ Imagen descargada exitosamente")
    elif os.path.exists(image_input):
        results.append("\n📁 Leyendo archivo local...")
        try:
            with open(image_input, 'rb') as f:
                img_data = f.read()
            results.append("✅ Archivo leído exitosamente")
        except:
            results.append("❌ Error: No se pudo leer el archivo")
            return "\n".join(results)
    else:
        results.append("❌ Error: La ruta no es válida (debe ser URL o ruta local)")
        return "\n".join(results)
    
    # Calcular hashes
    md5_hash, sha1_hash = calculate_image_hash(img_data)
    results.append(f"\n🔐 HASHES:")
    results.append(f"   • MD5: {md5_hash}")
    results.append(f"   • SHA1: {sha1_hash}")
    
    # Extraer metadata
    results.append(f"\n📋 METADATOS:")
    metadata = extract_metadata_from_bytes(img_data)
    
    if metadata and 'Error' not in metadata:
        # Mostrar metadatos importantes
        important_tags = ['GPSInfo', 'DateTime', 'Make', 'Model', 'Software', 
                          'Artist', 'Copyright', 'Description', 'Comment']
        
        found_important = False
        for tag in important_tags:
            if tag in metadata:
                value = metadata[tag]
                if tag == 'GPSInfo':
                    results.append(f"   • {tag}: Datos GPS presentes")
                    # Intentar convertir GPS a coordenadas
                    if isinstance(value, dict) and 'GPSLatitude' in value:
                        results.append(f"     Latitud: {value.get('GPSLatitude', 'N/A')}")
                        results.append(f"     Longitud: {value.get('GPSLongitude', 'N/A')}")
                else:
                    results.append(f"   • {tag}: {value}")
                found_important = True
        
        if not found_important:
            results.append("   • No se encontraron metadatos EXIF importantes")
        
        # Mostrar info básica de imagen
        results.append(f"\n📐 INFORMACIÓN BÁSICA:")
        results.append(f"   • Formato: {metadata.get('Formato', 'Desconocido')}")
        results.append(f"   • Modo: {metadata.get('Modo', 'Desconocido')}")
        results.append(f"   • Tamaño: {metadata.get('Tamaño', 'Desconocido')}")
    else:
        results.append("   • ❌ No se pudo extraer metadata de la imagen")
    
    # Búsqueda inversa
    results.append(f"\n🔍 BÚSQUEDA INVERSA:")
    for engine, url in search_google_images(md5_hash).items():
        results.append(f"   • {engine}: {url}")
    
    results.append(f"\n💡 RECOMENDACIONES:")
    results.append(f"   • Usa búsqueda inversa para encontrar copias de esta imagen")
    results.append(f"   • Verifica si la imagen fue modificada comparando hashes")
    results.append(f"   • Los metadatos pueden revelar dispositivo, fecha y ubicación")
    
    return "\n".join(results)
