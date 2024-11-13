"""
Este modulo realiza un monitoreo de red a través del comando ifstat
en bash, por lo que solo está disponible para Linux
"""

import os
import platform
import subprocess
import hashlib
import logging
from openpyxl import Workbook

# Configuración de logging
logging.basicConfig(filename="network_monitoring.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def check_ifstat_installed():
    try:
        subprocess.run(["ifstat", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        logging.error("Error: 'ifstat' no está instalado.")
        return False

def network_monitoring(n, file_path):
    try:
        with open(file_path, "w") as file:
            for _ in range(n):
                result = subprocess.run(["ifstat", "5", "1"], capture_output=True, text=True)
                file.write(result.stdout)
                file.write("\n")
                logging.info("Monitoreo de red ejecutado correctamente.")
        return True
    except Exception as e:
        logging.error(f"Ocurrió un error en el monitoreo de red: {e}")
        return False

def live_network_monitoring():
    try:
        print("Presione Ctrl+C para salir")
        subprocess.run(["ifstat"])
        logging.info("Monitoreo de red en vivo ejecutado correctamente.")
    except Exception as e:
        logging.error(f"Ocurrió un error en el monitoreo de red en vivo: {e}")
        print("Ocurrió un error.")

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        logging.error(f"Error al calcular el hash SHA-256: {e}")
        return None

def log_to_excel(file_path, hash_value):
    excel_path = "network_reports.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Report Log"
    sheet.append(["Archivo", "Ubicación", "SHA-256"])
    
    file_name = os.path.basename(file_path)
    file_location = os.path.abspath(file_path)
    
    sheet.append([file_name, file_location, hash_value])
    workbook.save(excel_path)
    logging.info(f"Registro guardado en {excel_path}")

def run_network_monitoring(file_path):
    if platform.system() == "Windows":
        logging.warning("El módulo de monitoreo de red no está disponible en Windows.")
        print("Este módulo no está disponible en Windows.")
        return
    elif platform.system() != "Linux":
        logging.warning("El sistema operativo no es compatible.")
        print("Sistema operativo no compatible.")
        return
    
    if not check_ifstat_installed():
        print("Error: 'ifstat' no está instalado. Instálalo para volver a intentar.")
        return

    op = input("Elija una de las siguientes opciones:\n"
               "[1] Ver el monitoreo de red en vivo\n"
               "[2] Ver el monitoreo de red cierta cantidad de veces\n"
               "[3] Generar el monitoreo de red cierta cantidad de veces en un archivo\n")

    if op == '1':
        live_network_monitoring()
    elif op == '2':
        num = int(input("Ingrese la cantidad de veces que quiere ver el monitoreo: "))
        if not network_monitoring(num, file_path):
            print("Ocurrió un error en el monitoreo.")
    elif op == '3':
        num = int(input("Ingrese la cantidad de veces que quiere ver el monitoreo: "))
        if network_monitoring(num, file_path):
            print(f"El reporte ha sido generado en el archivo {file_path}")
            hash_value = calculate_sha256(file_path)
            if hash_value:
                log_to_excel(file_path, hash_value)
                print(f"El hash SHA-256 y detalles del archivo se han registrado en 'network_reports.xlsx'.")
            else:
                print("Error al calcular el hash SHA-256.")
        else:
            print("Ocurrió un error al generar el reporte.")
    else:
        print("Opción no válida")

