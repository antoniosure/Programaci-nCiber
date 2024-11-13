"""
Este modulo hace la solicitud a virustotal para escanear archivos
"""

import os
import hashlib
import requests
import json

def get_virustotal_report(file_path):
    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        raise FileNotFoundError("El archivo no existe en la ruta especificada.")
    
    # Obtener el hash SHA256 del archivo
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Leer el archivo en bloques de 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    file_hash = sha256_hash.hexdigest()
    
    # Consultar la API de VirusTotal
    headers = {
        'x-apikey': "74aa481607cbd2321823ed749b244f5ca3a2b39011d74e34aad20b72898476cb"
    }
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza un error si la respuesta es un error HTTP
        return response.json().get('data').get('attributes').get('last_analysis_stats')
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el reporte hash de VirusTotal: {e}")
        return None

def print_terminal(file_path):
    # Calcular el hash del archivo
    with open(file_path, 'rb') as f:
        file_bytes = f.read()
    
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_bytes)
    file_hash = sha256_hash.hexdigest()
    
    # Obtener la ubicación del archivo
    dir_actual = os.path.dirname(os.path.abspath(file_path))
    print(f'Se guardó el documento con el nombre: {os.path.basename(file_path)}')
    print(f'Se guardó en la ubicación: {dir_actual}')
    print(f'Hash del archivo: {file_hash}')

def Reporte_Virus():
    file_path = input("Ingrese la ruta del archivo a analizar: ")
    report = get_virustotal_report(file_path)  
    if report is not None:
        print_terminal(file_path)
        report_file_path = 'Reporte_Virus.txt'
        with open(report_file_path, mode='w') as file_object:
            json.dump(report, file_object, indent=4)
        print(f'Reporte guardado en: {os.path.abspath(report_file_path)}')