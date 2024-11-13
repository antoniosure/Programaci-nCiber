"""
Este modulo cuenta con requisitos de sistema operativo
por lo que realiza validaciones, tales como verificar tenga instalado powershell
para su correcta ejecución, este modulo pedirá al usuario la ruta que desea 
examinar y la ruta del archivo de salida donde se desea guardar los resultados  
"""
import os
import hashlib
import platform
import subprocess
from openpyxl import Workbook

def check_os():
    os_type = platform.system()
    if os_type not in ["Windows", "Linux"]:
        print("Este script solo es compatible con Windows o Linux.")
        exit()
    return os_type

def check_powershell():
    try:
        subprocess.run(["powershell", "-Command", "Write-Output 'Powershell está instalado'"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Powershell está instalado.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Powershell no está instalado.")
        return False

def install_powershell_linux():
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "powershell"], check=True)
        print("Powershell instalado con éxito en Linux.")
    except subprocess.CalledProcessError:
        print("Error al instalar Powershell. Por favor, instálalo manualmente.")
        exit()

def get_user_input():
    ruta_busqueda = input("Ingrese la ruta para buscar archivos ocultos: ")
    ruta_salida = input("Ingrese la ruta y nombre del archivo de salida (sin extensión): ")
    return ruta_busqueda, ruta_salida

def calculate_sha256(file_path):
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
    except FileNotFoundError:
        return None
    return hash_sha256.hexdigest()

def find_hidden_files(ruta_busqueda, ruta_salida_base):
    txt_output_path = f"{ruta_salida_base}.txt"
    
    # Comando PowerShell para encontrar archivos ocultos
    command = f"powershell -Command \"Get-ChildItem -Path '{ruta_busqueda}' -Hidden -Recurse | ForEach-Object {{ $_.FullName }}\""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        hidden_files = result.stdout.splitlines()
        
        # Guardar resultados en archivo de texto
        with open(txt_output_path, "w") as txt_file:
            for file_path in hidden_files:
                txt_file.write(f"{file_path}\n")
        
        print(f"Información de archivos ocultos guardada en: {txt_output_path}")
        
        # Crear archivo Excel para hashes
        xlsx_output_path = f"{ruta_salida_base}.xlsx"
        wb = Workbook()
        ws = wb.active
        ws.title = "Hash SHA-256"
        ws.append(["Nombre del archivo", "Ruta completa", "Hash SHA-256"])
        
        # Calcular hash y registrar en Excel
        for file_path in hidden_files:
            file_name = os.path.basename(file_path)
            file_hash = calculate_sha256(file_path)
            if file_hash:
                ws.append([file_name, file_path, file_hash])
        
        # Guardar el archivo Excel
        wb.save(xlsx_output_path)
        print(f"Registro de hashes guardado en: {xlsx_output_path}")
        
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el comando de PowerShell:", e)

def main():
    os_type = check_os()
    if os_type == "Linux" and not check_powershell():
        install_powershell_linux()
    elif os_type == "Windows" and not check_powershell():
        print("Instale PowerShell manualmente en Windows para ejecutar este script.")
        exit()

    ruta_busqueda, ruta_salida_base = get_user_input()
    find_hidden_files(ruta_busqueda, ruta_salida_base)

#Ejecutar desde este modulo
#if __name__ == "__main__":
   # main()
