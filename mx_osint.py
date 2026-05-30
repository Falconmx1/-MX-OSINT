#!/usr/bin/env python3
# 🔧 MX-OSINT v3.0 - Herramienta OSINT Mexicana Completa
# Uso educativo y legal

import sys
import argparse
import os
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# Importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules import email_osint, domain_osint, social_osint, phone_osint, geo_osint, image_metadata, email_extractor

def banner():
    """Muestra el banner de la herramienta"""
    banner_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
{Fore.CYAN}║{Fore.YELLOW}      🔧 MX-OSINT v3.0 - Herramienta OSINT Mexicana Completa      {Fore.CYAN}║
{Fore.CYAN}║{Fore.GREEN}   📧 Email | 🌐 Dominio | 📱 Redes | 📞 Teléfono | 🗺️ Geo         {Fore.CYAN}║
{Fore.CYAN}║{Fore.CYAN}   🖼️ Metadata | ✉️ Email Extractor | 🔍 Búsqueda completa       {Fore.CYAN}║
{Fore.CYAN}║{Fore.MAGENTA}                    Uso educativo y legal siempre                    {Fore.CYAN}║
{Fore.CYAN}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner_text)

def menu_interactivo():
    """Menú interactivo principal"""
    while True:
        print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.YELLOW}🎯 SELECCIONA UNA OPCIÓN:")
        print(f" {Fore.GREEN}1.{Fore.WHITE} 📧 OSINT de Correo Electrónico")
        print(f" {Fore.GREEN}2.{Fore.WHITE} 🌐 OSINT de Dominio Web")
        print(f" {Fore.GREEN}3.{Fore.WHITE} 📱 OSINT de Redes Sociales (username)")
        print(f" {Fore.GREEN}4.{Fore.WHITE} 📞 OSINT de Número Telefónico")
        print(f" {Fore.GREEN}5.{Fore.WHITE} 🗺️  Geolocalización (IP o dominio)")
        print(f" {Fore.GREEN}6.{Fore.WHITE} 🖼️  Metadata de Imagen")
        print(f" {Fore.GREEN}7.{Fore.WHITE} ✉️  Extraer Emails de Sitio Web")
        print(f" {Fore.GREEN}8.{Fore.WHITE} 🚪 Salir")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        opcion = input(f"{Fore.YELLOW}👉 Opción: {Fore.WHITE}").strip()
        
        if opcion == "1":
            email = input(f"{Fore.CYAN}📧 Correo electrónico: {Fore.WHITE}")
            if email:
                print(email_osint.get_email_info(email))
            else:
                print(f"{Fore.RED}❌ No ingresaste un email válido")
        
        elif opcion == "2":
            domain = input(f"{Fore.CYAN}🌐 Dominio (ej: google.com): {Fore.WHITE}")
            if domain:
                print(domain_osint.analyze_domain(domain))
            else:
                print(f"{Fore.RED}❌ No ingresaste un dominio válido")
        
        elif opcion == "3":
            username = input(f"{Fore.CYAN}📱 Username (sin @): {Fore.WHITE}")
            if username:
                print(social_osint.search_social_media(username))
            else:
                print(f"{Fore.RED}❌ No ingresaste un username")
        
        elif opcion == "4":
            phone = input(f"{Fore.CYAN}📞 Número telefónico (ej: 1234567890 o +521234567890): {Fore.WHITE}")
            if phone:
                print(phone_osint.analyze_phone(phone))
            else:
                print(f"{Fore.RED}❌ No ingresaste un número válido")
        
        elif opcion == "5":
            target = input(f"{Fore.CYAN}🗺️  IP o dominio (ej: 8.8.8.8 o google.com): {Fore.WHITE}")
            if target:
                print(geo_osint.analyze_ip_geo(target))
            else:
                print(f"{Fore.RED}❌ No ingresaste un target válido")
        
        elif opcion == "6":
            image_input = input(f"{Fore.CYAN}🖼️  URL de imagen o ruta local: {Fore.WHITE}")
            if image_input:
                print(image_metadata.analyze_image(image_input))
            else:
                print(f"{Fore.RED}❌ No ingresaste una imagen válida")
        
        elif opcion == "7":
            website = input(f"{Fore.CYAN}🌐 Sitio web (ej: ejemplo.com): {Fore.WHITE}")
            if website:
                print(f"{Fore.YELLOW}⚠️ ¿Búsqueda profunda? (explorará todo el sitio, puede tomar tiempo)")
                deep = input(f"{Fore.CYAN}🔍 Búsqueda profunda? (s/n): {Fore.WHITE}").lower()
                deep_search = deep == 's' or deep == 'si'
                print(email_extractor.analyze_website(website, deep_search))
            else:
                print(f"{Fore.RED}❌ No ingresaste un sitio web válido")
        
        elif opcion == "8":
            print(f"{Fore.GREEN}👋 ¡Gracias por usar MX-OSINT! Hasta luego{Style.RESET_ALL}")
            sys.exit(0)
        
        else:
            print(f"{Fore.RED}❌ Opción inválida, intenta de nuevo")
        
        input(f"\n{Fore.CYAN}⏎ Presiona Enter para continuar...")

def main():
    """Función principal con argumentos CLI"""
    parser = argparse.ArgumentParser(description="MX-OSINT - Herramienta OSINT Mexicana Completa")
    parser.add_argument("--email", help="Analizar un correo electrónico")
    parser.add_argument("--domain", help="Analizar un dominio web")
    parser.add_argument("--username", help="Buscar username en redes sociales")
    parser.add_argument("--phone", help="Analizar número telefónico")
    parser.add_argument("--geo", help="Geolocalizar IP o dominio")
    parser.add_argument("--image", help="Analizar metadata de imagen (URL o ruta)")
    parser.add_argument("--extract-emails", help="Extraer emails de un sitio web")
    parser.add_argument("--deep", action="store_true", help="Búsqueda profunda con --extract-emails")
    parser.add_argument("--interactive", action="store_true", help="Abrir menú interactivo")
    
    args = parser.parse_args()
    
    banner()
    
    # Modo línea de comandos
    if args.email:
        print(email_osint.get_email_info(args.email))
    elif args.domain:
        print(domain_osint.analyze_domain(args.domain))
    elif args.username:
        print(social_osint.search_social_media(args.username))
    elif args.phone:
        print(phone_osint.analyze_phone(args.phone))
    elif args.geo:
        print(geo_osint.analyze_ip_geo(args.geo))
    elif args.image:
        print(image_metadata.analyze_image(args.image))
    elif args.extract_emails:
        print(email_extractor.analyze_website(args.extract_emails, args.deep))
    else:
        # Modo interactivo por defecto
        menu_interactivo()

if __name__ == "__main__":
    main()
