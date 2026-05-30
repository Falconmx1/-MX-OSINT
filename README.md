# 🔧 MX-OSINT

Herramienta OSINT mexicana para correos, dominios y redes sociales desde fuentes abiertas.

## 🚀 Características
- 📧 Email OSINT (haveibeenpwned, emailrep.io, hunter.io)
- 🌐 Domain OSINT (whois, dnsdumpster, crt.sh, sublist3r)
- 📱 Redes Sociales (perfiles públicos, username search)
- 🇲🇽 Enfoque en fuentes hispanas (opcional)

## 📦 Instalación
```bash
git clone https://github.com/Falconmx1/MX-OSINT.git
cd MX-OSINT
pip install -r requirements.txt
python mx_osint.py

💻 Ejemplos de uso
# Línea de comandos
python mx_osint.py --image https://ejemplo.com/foto.jpg
python mx_osint.py --extract-emails ejemplo.com
python mx_osint.py --extract-emails ejemplo.com --deep

# Menú interactivo (tiene todas las opciones)
python mx_osint.py
