"""
Este modulo esta basado en modulos pasados ya que revisa los archivos inseguros y esta unido al modulo de loggs
"""
#RECORDAR QUE SE NECESITA TENER A "Modulo_Extra_Permiso_Inseguros.psd1 y Modulo_Extra_Permiso_Inseguros.psm1
#YA QUE EL MODULO DE LOGGINS YA ESTA IMPLEMENTADO AQUI

import argparse
import subprocess
import logging
import platform
import os
import hashlib
import openpyxl
from datetime import datetime
from openpyxl import Workbook
from datetime import datetime
import shutil
import os
import argparse


# Establecemos el archivo de logs que sera un .txt
def establecer_loggeos(log_file='C:\\tmp\\cyberseguridad_logs.log'):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_exito(module_name):
    logging.info(f"El modulo llamado '{module_name}' se ejecuto correctamente :)")

def log_falla(module_name, error):
    logging.error(f"El modulo llamado '{module_name}' fallo. Error: {error}")

# Funcion para verificar el sistema operativo (Solo identifica Linux y windows, mete cualquier otro tipo de Sistema operativo a no reconocido
def verificar_sistema_operativo():
    sistema = platform.system()
    if sistema == "Windows":
        print("Sistema operativo: Windows")
        return "Windows"
    elif sistema == "Linux":
        print("Sistema operativo: Linux")
        return "Linux"
    else:
        print(f"Sistema operativo no reconocido: {sistema}")
        return None

import subprocess
def ejecutar_script_powershell():
    script_powershell = """
    $sourcePath = "C:\\tmp\\Modulo_Extra_Permiso_Inseguros.psd1"
    $sourceModuleFolder = "C:\\tmp"
    $destPath = "C:\\Program Files\\WindowsPowerShell\\Modules\\Modulo_Extra_Permiso_Inseguros"
    
    if (-not (Test-Path -Path $destPath)) {
        New-Item -ItemType Directory -Path $destPath -Force
    }
    
    Copy-Item -Path "$sourceModuleFolder\\*" -Destination $destPath -Recurse -Force

    if (Test-Path -Path "$destPath\\Modulo_Extra_Permiso_Inseguros.psm1") {
        Write-Host "Módulo copiado correctamente."
        Import-Module "$destPath\\Modulo_Extra_Permiso_Inseguros.psd1"
        Write-Host "Módulo importado correctamente."
    } else {
        Write-Host "Error al copiar el módulo."
        exit 1
    }
    """
    try:
        subprocess.run(["powershell", "-Command", script_powershell], check=True)
        print("Script de PowerShell ejecutado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando el script de PowerShell: {e}")
        raise

def generar_hash_archivo(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def registrar_tarea_excel(tarea, archivo_reporte, excel_path="registro_tareas.xlsx"):
    # Verificamos si el archivo Excel existe, si no, lo creamos
    if not os.path.exists(excel_path):
        workbook = Workbook()
        sheet = workbook.active
        # Especificamos los encabezados
        sheet.append(["Tarea", "Fecha", "Hash", "Ubicación del archivo"])
    else:
        workbook = openpyxl.load_workbook(excel_path)
        sheet = workbook.active

    # Generamos el hash del archivo de reporte
    hash_reporte = generar_hash_archivo(archivo_reporte)

    # Obtenemos la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Obtenemos la ubicación absoluta del archivo
    ubicacion_archivo = os.path.abspath(archivo_reporte)

    # Agregamos la nueva fila en el Excel
    sheet.append([tarea, fecha_actual, hash_reporte, ubicacion_archivo])

    # Guardamos el archivo Excel
    workbook.save(excel_path)
    print(f"Registro de tarea guardado en {excel_path}")

# Funcion para instalar PowerShell en Linux si no esta instalado
def instalar_powershell_en_linux():
    try:
        result = subprocess.run(["pwsh", "-v"], capture_output=True, text=True)
        if result.returncode == 0:
            print("PowerShell ya esta instalado.")
        else:
            print("Instalando PowerShell...")
            subprocess.run(["sudo", "apt-get", "install", "-y", "powershell"], check=True)
            print("PowerShell instalado exitosamente.")
    except FileNotFoundError:
        print("PowerShell no encontrado. Instalando...")
        subprocess.run(["sudo", "apt-get", "install", "-y", "powershell"], check=True)
        print("PowerShell instalado exitosamente.")


def verificar_modulos_powershell():
    sistema = platform.system()
    ejecutar_script_powershell()
    # Si no se proporcionan rutas, usar las predeterminadas
    if sistema == "Windows":
        psd1_path = "C:\\Program Files\\WindowsPowerShell\\Modules\\Modulo_Extra_Permiso_Inseguros\\Modulo_Extra_Permiso_Inseguros.psd1"
        psm1_path = "C:\\Program Files\\WindowsPowerShell\\Modules\\Modulo_Extra_Permiso_Inseguros\\Modulo_Extra_Permiso_Inseguros.psm1"
        
        registrar_tarea_excel("Validacion de Integridad de Modulo powershell", psm1_path, excel_path="C:\\tmp\\registro_tareas.xlsx")
    elif sistema == "Linux":
        psd1_path = "/usr/local/share/powershell/Modules/Modulo_Extra_Permiso_Inseguros/Modulo_Extra_Permiso_Inseguros.psd1"
        psm1_path = "/usr/local/share/powershell/Modules/Modulo_Extra_Permiso_Inseguros/Modulo_Extra_Permiso_Inseguros.psm1"
    else:
        print(f"Sistema operativo no compatible: {sistema}")
        return

    # Validar si los modulos existen
    
    
    try:
        if sistema == "Windows":            
            if os.path.exists(psd1_path):
                print(f"Módulo {psd1_path} ya existe correctamente.")
            else:
                ejecutar_script_powershell()
                print(f"Módulo {psd1_path} importado correctamente.")
        elif sistema == "Linux":
            print(f"Módulo {psd1_path} importado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error importando el módulo: {e}")
        log_falla("Importación de módulo de permisos inseguros", e)
    # Intentar importar el modulo despues de verificar o instalar

# Funcion para ejecutar el script de PowerShell desde Python
def check_insecure_permissions(path):
    try:
        # Ejecutar el script de PowerShell para checar permisos inseguros
        result = subprocess.run(
            ["powershell", "-Command", f"Get-InsecureFilePermissions -Path {path}"],
            capture_output=True, text=True, check=True
        )
        log_exito("Get-InsecureFilePermissions")
        return result.stdout  # Devolvemos la salida de PowerShell
    except subprocess.CalledProcessError as e:
        log_falla("Get-InsecureFilePermissions", e)
        return None

def copiar_contenido(source_folder, destination_folder):
    # Verificar si la carpeta de destino existe
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Recorrer el contenido de la carpeta de origen
    for item in os.listdir(source_folder):
        source_path = os.path.join(source_folder, item)
        destination_path = os.path.join(destination_folder, item)
        
        # Copiar archivos o directorios
        try:
            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
            else:
                shutil.copy2(source_path, destination_path)
        except Exception as e:
            print(f"Error al copiar '{source_path}' a '{destination_path}': {e}")

# Funcion principal que manejara los argumentos
def main():
    parser = argparse.ArgumentParser(description="Script para ejecutar modulos de ciberseguridad.")
    
    # Argumentos para checar permisos
    parser.add_argument('--check-permissions', help="Ruta para checar permisos inseguros usando PowerShell", required=False)
    
    # Argumentos para proporcionar las rutas de los archivos psd1 y psm1
    parser.add_argument('--psd1-path', help="Ruta al archivo .psd1 del modulo de permisos inseguros", required=False)
    parser.add_argument('--psm1-path', help="Ruta al archivo .psm1 del modulo de permisos inseguros", required=False)
    
    
    source_folder = 'tmp_2'
    destination_folder = 'C:\\tmp'
    
    copiar_contenido(source_folder, destination_folder)

    
    verificar_modulos_powershell()
    
    
    args = parser.parse_args()
    establecer_loggeos()

    # Verificar el sistema operativo
    so = verificar_sistema_operativo()

    # Si es Linux, instalar PowerShell si no esta presente
    if so == "Linux":
        instalar_powershell_en_linux()

    # Verificar, instalar e importar el modulo de permisos inseguros
    verificar_modulos_powershell()

    if args.check_permissions:
        print(f"Checando permisos inseguros en: {args.check_permissions}")
        output = check_insecure_permissions(args.check_permissions)
        if output:
            print(output)
    else:
        print(f"Checando permisos inseguros en: C:\tmp")
        output = check_insecure_permissions("C:\tmp")
        if output:
            print(output)
        

#Ejecutar desde este archivo
#if __name__ == "__main__":
    #main()