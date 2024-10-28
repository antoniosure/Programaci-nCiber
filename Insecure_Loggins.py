#RECORDAR QUE SE NECESITA TENER A "Modulo_Extra_Permiso_Inseguros.psd1 y Modulo_Extra_Permiso_Inseguros.psm1
#YA QUE EL MODULO DE LOGGINS YA ESTA IMPLEMENTADO AQUI
import argparse
import subprocess
import logging
import platform
import os
from datetime import datetime

# Establecemos el archivo de logs
def establecer_loggeos(log_file='cyberseguridad_logs.log'):
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

# Funcion para verificar el sistema operativo
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
    # Código de PowerShell que queremos ejecutar
    script_powershell = """
    # Ruta origen del módulo
    $sourcePath = "C:\\tmp\\Modulo_Extra_Permiso_Inseguros.psd1"
    $sourceModuleFolder = "C:\\tmp"

    # Ruta destino en los módulos de PowerShell
    $destPath = "C:\\Program Files\\WindowsPowerShell\\Modules\\Modulo_Extra_Permiso_Inseguros"

    # Verificar si la carpeta de destino existe, si no, crearla
    if (-not (Test-Path -Path $destPath)) {
        New-Item -ItemType Directory -Path $destPath -Force
    }

    # Copiar todos los archivos del módulo (.psd1 y .psm1) al destino
    Copy-Item -Path "$sourceModuleFolder\\*" -Destination $destPath -Recurse -Force

    # Verificar si el módulo fue copiado correctamente
    if (Test-Path -Path "$destPath\\Modulo_Extra_Permiso_Inseguros.psd1") {
        Write-Host "Módulo copiado correctamente en $destPath."
        
        # Importar el módulo en PowerShell
        Import-Module "$destPath\\Modulo_Extra_Permiso_Inseguros.psd1"
        Write-Host "Módulo importado correctamente."
    } else {
        Write-Host "Error al copiar el módulo."
    }
    """

    try:
        # Ejecutar el script de PowerShell usando subprocess
        subprocess.run(["powershell", "-Command", script_powershell], check=True)
        print("Script de PowerShell ejecutado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando el script de PowerShell: {e}")




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

# Funcion para verificar si los modulos de PowerShell estan instalados
# def verificar_modulos_powershell():
    # psd1_path = "C:\\Program Files\\WindowsPowerShell\\Modules\\Modulo_Extra_Permiso_Inseguros.psd1"
    # psm1_path = "C:\\Program Files\\WindowsPowerShell\\Modules\\Modulo_Extra_Permiso_Inseguros.psm1"
    
    # if not os.path.exists(psd1_path) or not os.path.exists(psm1_path):
        # print("El modulo de permisos inseguros no esta instalado. Instalandolo...")
        # try:
            # # Comando para instalar el modulo en Windows
            # subprocess.run(["powershell", "-Command", "Install-Module -Name Modulo_Extra_Permiso_Inseguros -Force"], check=True)
            # print("Modulo instalado correctamente.")
        # except subprocess.CalledProcessError as e:
            # print(f"Error instalando el modulo: {e}")
            # log_falla("Instalacion de modulo de permisos inseguros", e)
    # else:
        # print("El modulo de permisos inseguros ya esta instalado.")

def verificar_modulos_powershell():
    sistema = platform.system()

    # Si no se proporcionan rutas, usar las predeterminadas
    if sistema == "Windows":
        psd1_path = "C:\\Program Files\\WindowsPowerShell\\Modules\\Modulo_Extra_Permiso_Inseguros\\Modulo_Extra_Permiso_Inseguros.psd1"
        psm1_path = "C:\\Program Files\\WindowsPowerShell\\Modules\\Modulo_Extra_Permiso_Inseguros\\Modulo_Extra_Permiso_Inseguros.psm1"
    elif sistema == "Linux":
        psd1_path = "/usr/local/share/powershell/Modules/Modulo_Extra_Permiso_Inseguros/Modulo_Extra_Permiso_Inseguros.psd1"
        psm1_path = "/usr/local/share/powershell/Modules/Modulo_Extra_Permiso_Inseguros/Modulo_Extra_Permiso_Inseguros.psm1"
    else:
        print(f"Sistema operativo no compatible: {sistema}")
        return

    # Validar si los modulos existen
    ejecutar_script_powershell()
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

# Funcion principal que manejara los argumentos
def main():
    parser = argparse.ArgumentParser(description="Script para ejecutar modulos de ciberseguridad.")
    
    # Argumentos para checar permisos
    parser.add_argument('--check-permissions', help="Ruta para checar permisos inseguros usando PowerShell", required=True)
    
    # Argumentos para proporcionar las rutas de los archivos psd1 y psm1
    parser.add_argument('--psd1-path', help="Ruta al archivo .psd1 del modulo de permisos inseguros", required=False)
    parser.add_argument('--psm1-path', help="Ruta al archivo .psm1 del modulo de permisos inseguros", required=False)

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

if __name__ == "__main__":
    main()
