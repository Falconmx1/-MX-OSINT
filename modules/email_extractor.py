import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class EmailExtractor:
    def __init__(self, domain):
        self.domain = domain
        self.emails = set()
        self.visited = set()
        self.max_pages = 30
        
    def extract_emails_from_text(self, text):
        """Extrae emails usando regex mejorado"""
        # Patrón regex para emails
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        found_emails = re.findall(email_pattern, text)
        
        # Filtrar por dominio si se especificó
        emails_filtered = []
        for email in found_emails:
            if email not in self.emails:
                emails_filtered.append(email)
                
        return emails_filtered
    
    def get_page_emails(self, url):
        """Extrae emails de una sola página"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, timeout=10, headers=headers)
            
            if response.status_code == 200:
                # Extraer del HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                emails = self.extract_emails_from_text(text)
                
                # También buscar en atributos href
                for link in soup.find_all('a', href=True):
                    if 'mailto:' in link['href']:
                        mailto_email = link['href'].replace('mailto:', '')
                        if '@' in mailto_email:
                            emails.append(mailto_email)
                
                return set(emails)
        except:
            return set()
        return set()
    
    def find_links(self, url):
        """Encuentra links internos en una página"""
        links = set()
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, timeout=10, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                base_domain = urlparse(self.domain).netloc
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    parsed = urlparse(full_url)
                    
                    # Solo mantener links del mismo dominio
                    if parsed.netloc == base_domain and full_url not in self.visited:
                        # Limpiar URL
                        clean_url = parsed.scheme + '://' + parsed.netloc + parsed.path
                        if clean_url not in self.visited:
                            links.add(clean_url)
        except:
            pass
        
        return links
    
    def crawl_and_extract(self):
        """Crawl principal con multithreading"""
        start_url = f"http://{self.domain}" if not self.domain.startswith('http') else self.domain
        to_visit = {start_url}
        
        print(f"\n🔍 Iniciando crawler en: {self.domain}")
        print(f"📊 Máximo de páginas a analizar: {self.max_pages}")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            while to_visit and len(self.visited) < self.max_pages:
                batch = list(to_visit)[:5]  # Procesar en lotes de 5
                to_visit -= set(batch)
                
                # Enviar tareas para obtener emails y links
                futures = []
                for url in batch:
                    if url not in self.visited:
                        self.visited.add(url)
                        futures.append(executor.submit(self.get_page_emails, url))
                        futures.append(executor.submit(self.find_links, url))
                
                # Procesar resultados
                for future in as_completed(futures):
                    result = future.result()
                    if isinstance(result, set):  # Es un conjunto de emails
                        self.emails.update(result)
                    elif isinstance(result, set):  # Es un conjunto de links
                        to_visit.update(result)
                
                # Mostrar progreso
                print(f"   • Páginas analizadas: {len(self.visited)} | Emails encontrados: {len(self.emails)}")
                
                # Pequeña pausa para no sobrecargar el servidor
                time.sleep(0.5)
        
        return list(self.emails)

def extract_emails_from_text_manual(text):
    """Extrae emails directamente de texto (útil para modo manual)"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return list(set(emails))

def extract_from_url_direct(url):
    """Extrae emails de una URL específica (sin crawling)"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=15, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            emails = extract_emails_from_text_manual(text)
            
            # Buscar mailto
            for link in soup.find_all('a', href=True):
                if 'mailto:' in link['href']:
                    mailto_email = link['href'].replace('mailto:', '')
                    if '@' in mailto_email:
                        emails.append(mailto_email)
            
            return list(set(emails))
        else:
            return []
    except:
        return []

def analyze_website(domain, deep_search=False):
    """Función principal para extraer emails de sitios web"""
    results = []
    results.append(f"\n🌐 EXTRAYENDO EMAILS DE: {domain}")
    results.append("=" * 50)
    
    if deep_search:
        results.append("\n🔎 Modo búsqueda profunda (crawling)")
        results.append("⚠️ Puede tomar varios minutos dependiendo del tamaño del sitio\n")
        
        extractor = EmailExtractor(domain)
        emails = extractor.crawl_and_extract()
        
        if emails:
            results.append(f"\n✅ EMAILS ENCONTRADOS ({len(emails)}):")
            for email in sorted(emails):
                # Clasificar emails
                if 'info' in email.lower() or 'contact' in email.lower() or 'admin' in email.lower():
                    results.append(f"   • 📧 {email} [Contacto principal]")
                elif 'support' in email.lower() or 'help' in email.lower():
                    results.append(f"   • 🛟 {email} [Soporte]")
                elif 'ventas' in email.lower() or 'sales' in email.lower():
                    results.append(f"   • 💰 {email} [Ventas]")
                else:
                    results.append(f"   • 📧 {email}")
        else:
            results.append("\n❌ No se encontraron emails en el sitio")
    
    else:
        results.append("\n🔎 Modo rápido (solo página principal)")
        emails = extract_from_url_direct(domain)
        
        if emails:
            results.append(f"\n✅ EMAILS ENCONTRADOS ({len(emails)}):")
            for email in sorted(emails):
                results.append(f"   • 📧 {email}")
        else:
            results.append("\n❌ No se encontraron emails en la página principal")
        
        results.append("\n💡 SUGERENCIA:")
        results.append("   • Usa --deep para búsqueda profunda (explora todo el sitio)")
        results.append("   • python mx_osint.py --extract-emails ejemplo.com --deep")
    
    # Mostrar resumen
    if emails:
        results.append(f"\n📊 RESUMEN:")
        results.append(f"   • Total de emails únicos: {len(emails)}")
        domains_found = set(email.split('@')[1] for email in emails if '@' in email)
        results.append(f"   • Dominios encontrados: {', '.join(domains_found)}")
    
    return "\n".join(results)
