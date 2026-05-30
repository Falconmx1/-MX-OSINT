#!/usr/bin/env python3
# 🔧 MX-OSINT - Herramienta OSINT Mexicana
# Uso educativo y legal

import sys
import argparse
import os
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# Importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules import email_osint, domain_osint, social_osint

def banner():
    """Muestra el banner de la herramienta"""
    banner_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════╗
{Fore.CYAN}║{Fore.YELLOW}      🔧 MX-OSINT v1.0 - Herramienta OSINT      {Fore.CYAN}║
{Fore.CYAN}║{Fore.GREEN}   Correos | Dominios | Redes Sociales         {Fore.CYAN}║
{Fore.CYAN}║{Fore.MAGENTA}        Uso educativo y legal siempre         {Fore.CYAN}║
{Fore.CYAN}╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner_text)

def menu_interactivo():
    """Menú interactivo principal"""
    while True:
        print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.YELLOW}🎯 SELECCIONA UNA OPCIÓN:")
        print(f" {Fore.GREEN}1.{Fore.WHITE} OSINT de Correo Electrónico")
        print(f" {Fore.GREEN}2.{Fore.WHITE} OSINT de Dominio Web")
        print(f" {Fore.GREEN}3.{Fore.WHITE} OSINT de Redes Sociales (username)")
        print(f" {Fore.GREEN}4.{Fore.WHITE} Salir")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
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
            print(f"{Fore.GREEN}👋 ¡Gracias por usar MX-OSINT! Hasta luego{Style.RESET_ALL}")
            sys.exit(0)
        
        else:
            print(f"{Fore.RED}❌ Opción inválida, intenta de nuevo")
        
        input(f"\n{Fore.CYAN}⏎ Presiona Enter para continuar...")

def main():
    """Función principal con argumentos CLI"""
    parser = argparse.ArgumentParser(description="MX-OSINT - Herramienta OSINT Mexicana")
    parser.add_argument("--email", help="Analizar un correo electrónico")
    parser.add_argument("--domain", help="Analizar un dominio web")
    parser.add_argument("--username", help="Buscar username en redes sociales")
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
    else:
        # Modo interactivo por defecto
        menu_interactivo()

if __name__ == "__main__":
    main()
