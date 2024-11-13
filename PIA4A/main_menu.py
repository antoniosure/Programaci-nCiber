"""
Este es el menú principal,donde el usuario tendrá 
acesso a la paqueteria cybersecurity_modules el cual contiene
diversos modulos utilizando python,powershell y bash según corresponda
"""


# Importamos módulos necesarios de la paquetería de python
import argparse
import subprocess
import logging
import platform
import os
from datetime import datetime
import sys  
import shutil 
import requests 
import json
import hashlib
import time
import shodan

# Importamos los módulos de la paquetería cybersecurity_modules.py (nuestra paquetería)
# Importamos las funciones de powershell, python y bash
import cybersecurity_modules.Get_SystemAndMalwareInfo as Sys_Mal_Inf
import cybersecurity_modules.hidden_files_module as fun_hfm
import cybersecurity_modules.insecure_permissions_module as fun_ipm
import cybersecurity_modules.ports_lpDB_module as fun_plm
import cybersecurity_modules.shodan_api_module as fun_sam
import cybersecurity_modules.Report_Virus as fun_gIm
import cybersecurity_modules.network_monitor_module as fun_nmm


def Get_SystemAndMalwareInfo():
    Sys_Mal_Inf.main()

# Menú principal
def main():
    parser = argparse.ArgumentParser(description="Menú interactivo de herramientas de seguridad")
    parser.add_argument("opcion", type=int, choices=range(1, 9), 
                        help="Selecciona una opción:\n"
                             "1) Revisar permisos inseguros\n"
                             "2) Escaneo de puertos/Verificación de API\n"
                             "3) Analizar archivos para encontrar malware o Analizar sistema\n"
                             "4) Encontrar archivos ocultos\n"
                             "5) Utilizar Shodan API\n"
                             "6) Monitoreo de Red\n"
                             "7) Analizar documento malicioso\n"
                             "8) Salir"
                             )

    while True:
        try:
            args = parser.parse_args(input("Elige una opción (1-8 o -h para ayuda): ").split())
        except SystemExit:  # Captura el evento de ayuda
            continue

        if args.opcion == 1:
            args2 = input("escribe una ruta a validar [Ejemplo C:\\tmp]: ")
            sys.argv = ['script_name', '--check-permissions', args2]
            fun_ipm.main()
        elif args.opcion == 2:
            fun_plm.main()
        elif args.opcion == 3:
            Get_SystemAndMalwareInfo()
        elif args.opcion == 4:
            fun_hfm.main()
        elif args.opcion == 5:
            fun_sam.main_menu()
        elif args.opcion == 6:
            print("Bienvenido al sistema de monitoreo de red")
            file_path = input("Ingrese la ruta completa donde desea guardar el archivo de monitoreo de red: ")
            fun_nmm.run_network_monitoring(file_path)
        elif args.opcion == 7:
            fun_gIm.Reporte_Virus()
        elif args.opcion == 8:
            print("Saliendo del menú...")
            sys.exit()

        print("\nVuelve a elegir otra opción o selecciona '8' para salir.\n")

# Ejecuta el menú principal
if __name__ == "__main__":
    main()
