def main():
 
    import sys  # Gestiona la salida del programa y terminarlo de manera controlada.
    import subprocess  # Conecta los subprocesos de linux con python.
    import shutil  # Verificar si el ejecutable de nmap está disponible en la ruta especificada. Esta funcion es usada para el copiado y borrado de archivos entre mas varias cosas.
    import requests  # Uso en el API.
    import json  # Darle formato a la salida del API.
    from datetime import datetime  # Para obtener la fecha actual
    import platform  # Para verificar el sistema operativo
    import os
    import hashlib #Para crear valores hash para los docuemntos.
    import openpyxl #Uso de paginas excel en el codigo.
    from openpyxl import Workbook
    from pathlib import Path  #Para crear lsas rutas de archuivos para gaurdar la descarga de nmap.
   
    #IMPORTANTE, para usar la opción acerca las ips maliciosas usted se tiene que registrar para obtener una API KEY en el sitio de; https://www.abuseipdb.com/api aqui podra obtener
    #su llave para asi depués guardarla en el folder done tendra este script con el nombre -> ApiKey.txt, de no ser asi el apikey no podrá ser leida y no funcionará esta parte del codigo.
    # #La fecha de cada uno de los archivos cuando se guardan se imprime en la creación del archivo como encabezado.
 
    # Verifica la versión de Python
    if sys.version_info[0] < 3:
        print("Este script requiere Python 3 o superior.")
        sys.exit(1)  # Salie del programa si no se cumple la condición.
 
    # Verifica el sistema operativo.
    SO = platform.system()
    if SO == "Windows":
        print("Ejecutando en Windows. Algunas funciones pueden requerir Nmap y PowerShell debido a la instalación del mismo nmap.")
    elif SO == "Linux":
        print("Ejecutando en Linux. Algunas funciones pueden requerir Bash y Nmap.")
    else:
        print(f"SO no soportado: {SO}. Algunas funciones pueden no funcionar correctamente.")
        sys.exit(1)
       
    def guardar_en_archivo(nombre_archivo, contenido):
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(f"Fecha de impresión: {fecha_actual}\n")
            archivo.write(contenido)
 
        print(f"Los resultados se han guardado en: {nombre_archivo}")
 
        # Calcula el hash del contenido.
        hash_obj = hashlib.sha256(contenido.encode())
        hash_hex = hash_obj.hexdigest()
 
        # Guarda el nombre del archivo y su hash en un archivo Excel.
        archivo_excel = "registro_archivos.xlsx"
        if not os.path.exists(archivo_excel):
            # Creamos el archivo si no existe.
            wb = Workbook()
            ws = wb.active
            ws.title = "Registro" #Es el nombre del worksheet donde andamos trabajando.
            ws.append(["Nombre del archivo", "Hash"])
        else:
            # Abrir el archivo si ya existe.
            wb = openpyxl.load_workbook(archivo_excel)
            ws = wb["Registro"]
 
        # Agregaos el nombre del archivo y el hash.
        ws.append([nombre_archivo, hash_hex])
 
        # Guardamos los cambios en el archivo Excel.
        wb.save(archivo_excel)
        print(f"El nombre del archivo y su hash se han registrado en: {archivo_excel}")
 
    def download_nmap():
        # Descarga Nmap si no está disponible con PowerShell.
        nmap_url = "https://nmap.org/dist/nmap-7.93-setup.exe"
        ruta = Path(r"C:\Temp\nmap-setup.exe")
        ruta.parent.mkdir(parents=True, exist_ok=True)
        response = requests.get(nmap_url)
 
        if response.status_code == 200:
            with open(ruta, 'wb') as file:
                file.write(response.content)
 
            # Ejecutamos el instalador.
            subprocess.run([str(ruta)], check=True)
            print("Instalación completada.")
 
            # Elimina el instalador después de la instalación para que posteriormente en nuevas descargas el archivo no se convierta en duplicado y haya interrupciones con el codigo.
            ruta.unlink()
 
        else:
            print("Error al descargar Nmap.")
            sys.exit(1)
   
   
    OPCIÓN = int(input("""Ingresa la opción que desees:
                        [1] Para entrar al escaneo de puertos.
                        [2] Para verificar Ip's con AbuseIp.\n"""))
 
    def Ports_Scanning():
        def verificar_nmap():
            # Verificamos si Nmap está disponible en la ruta especificada
            nmap_path = r"C:\Program Files (x86)\Nmap\nmap.exe" if SO == "Windows" else "nmap"  # Cambia según SO
            if not shutil.which(nmap_path):
                print("Nmap no está instalado en la ruta especificada.")
                download_nmap()  # Llama a la función para descargar e instalar Nmap
                nmap_path = r"C:\Program Files (x86)\Nmap\nmap.exe" if SO == "Windows" else "nmap"  # Vuelve a establecer la ruta
                if not shutil.which(nmap_path):
                    print("Nmap no se pudo instalar correctamente.")
                    sys.exit()  # Salida del programa si no se pudo instalar Nmap
            else:
                print("Nmap está instalado y listo para usarse.")
 
        def obtener_adaptadores():
            print("Entraste a la opción para saber cuáles son tus adaptadores en la red")
            result = subprocess.run("ipconfig" if SO == "Windows" else "ifconfig", capture_output=True, text=True)
            # Captura la salida del comando donde aqui mismo se agrega el nombre al archivo y se imprimen los resultados.
            guardar_en_archivo('adaptadores_red.txt', result.stdout)
 
             
 
        def get_ports():
            nmap_path = r"C:\Program Files (x86)\Nmap\nmap.exe" if SO == "Windows" else "nmap"  # Cambia según SO
            opc1 = input("Ingrese la opción [1] para proporcionar la IP de algún dispositivo, [2] para usar la IP del adaptador testeado o [3] para salir: ")
           
            if opc1 == "1":
                print("Elegiste la opción número 1")
                ipsele = input("Ingrese la IP de la que vamos a mostrar la información: ")
                try:
                    result = subprocess.run([nmap_path, ipsele], capture_output=True, text=True)
                    guardar_en_archivo('resultado_nmap.txt', result.stdout)
                except FileNotFoundError:
                    error_mensaje = "Nmap no esta en este script o no está instalado."
                    guardar_en_archivo('error_nmap.txt', error_mensaje)
           
            elif opc1 == "2":
                print("Elegiste la opción número 2") #Escribimos qaue adaptador que nos guardo en el archivo de texo -> adap....txt queremos
                #que lea la herramienta de nmap para asi ya no proporcionar lo que viene siendo una ip.
                adaptador = input("Ingrese el adaptador que quieres que sea testeado(De no ser un adaptador con nombre eth0 etc en tu red este indice del programa no podrá mapear los puertos abiertos por adaptador.): ")
                #Aqui lo que viene siendo nos da le ip buscando por adaptador acerca el sistema linux y nos lo manda a un archivo que el mismo lo lee, desde el shell y obtiene el output que
                #los mismos comandos nos arrojaron.
                ip = subprocess.run(f"ipconfig | findstr /R /C:\"{adaptador}\"" if SO == "Windows" else f"ifconfig | grep {adaptador}", shell=True, capture_output=True, text=True).stdout.strip()
                if not ip:
                    #si no se encutra una ip por medio del adaptador nos manda al mensaje de que no se encontro ip para el adpatador seleccionado.
                    mensaje = f"No se encontró la dirección IP para el adaptador {adaptador}"
                    guardar_en_archivo('error_ip.txt', mensaje)
                    return
                print(f"La dirección IP es {ip}")
               
                try:
                    #De ser exitoso nos mandara a correr el comando nmap con la ip proporcionada y este mismo rsultado se alojara en el arch txt.
                    result = subprocess.run([nmap_path, ip], capture_output=True, text=True)
                    guardar_en_archivo('resultado_nmap_adaptador.txt', result.stdout)
                except FileNotFoundError:
                    error_mensaje = "Nmap no es compatible con Windows en este script o no está instalado."
                    guardar_en_archivo('error_nmap.txt', error_mensaje)
           
            elif opc1 == "3":
                print("Saliendo...")
                sys.exit()
 
        # Verificación de nmap antes de ejecutar el script
        verificar_nmap()
        # Ejecución
        obtener_adaptadores()
        get_ports()
 
    def ipdb(): #toda esta informacion acerca del script fue sacada ade la documentación oficial de código de la página de abuseipdb, lo que hizimos nada mas fue darle el formato
        #para darle ingreso a las varaiables que el usuario debera de introducir.
        opc = int(input("""Ingresa la opción que desees:
                        [1] Para checar si una IP ha sido colocada en la lista negra de IPs maliciosas
                        [2] Para checar el CIDR ("Familia de IPs maliciosas")
                        [3] Para reportar una IP maliciosa.\n"""))
 
        if opc == 1:
            print("Usted entró a la opción de checar si la IP está en la lista negra de IPs maliciosas")
            url1 = 'https://api.abuseipdb.com/api/v2/check' #url a donde nos conectamos para conectarnos a la informacion de la abse de datos de las ips.
            ipb = str(input("Ingresa la IP que quieres verificar si se encuentra en la lista negra: "))
            #Este diccionario nos deja introducir lo que viene siendo la infroamcion que tendra que consultar en el api.
            querystring = {
                'ipAddress': ipb,
                'maxAgeInDays': '90'
            }
            #Volvemos a abrir el archivo txt con el nombre ApiKey.txt para que se pueda leer de ahi por cuestiones de seguridad. En la priemr parte del código mencionamos esto.
            with open('ApiKey.txt', 'r') as archivo:
                llave = archivo.read().strip()
            headers = {
                'Accept': 'application/json',
                'Key': llave
            }
            response = requests.get(url=url1, headers=headers, params=querystring)
            decodedResponse = response.json()
            guardar_en_archivo('resultado_ip_verificacion.txt', json.dumps(decodedResponse, sort_keys=True, indent=4))
 
            #Repetimos mas de la informacion que antes explicamos.
        elif opc == 2:
            print("Usted ingresó a la opción de checar la familia de la IP ingresada")
            url = 'https://api.abuseipdb.com/api/v2/check-block'
            network1 = input("Ingresa la IP con la notación CIDR (8.8.8.8/24): ")
            querystring = {
                'network': network1,
                'maxAgeInDays': '15'
            }
            with open('apikey.txt', 'r') as archivo:
                llave = archivo.read().strip()
            headers = {
                'Accept': 'application/json',
                'Key': llave
            }
            response = requests.get(url=url, headers=headers, params=querystring)
            decodedResponse = response.json()
            guardar_en_archivo('resultado_cidr.txt', json.dumps(decodedResponse, sort_keys=True, indent=4))
 
        elif opc == 3:
            print("Usted ingresó a la opción para reportar una IP")
            url = 'https://api.abuseipdb.com/api/v2/report'
            ip = input("Ingrese la IP que quiere reportar: ")
            categories = input("""Ingrese el número de la categoria en la que se encuentra la IP maliciosa
                            1. Compromiso de DNS: Alteración de registros DNS que resulta en una redirección incorrecta.
                            2. Envenenamiento de DNS: Falsificación de la caché del servidor de dominio (envenenamiento de caché).
                            3. Pedidos fraudulentos: Órdenes fraudulentas.
                            4. Ataque DDoS: Participación en un ataque de denegación de servicio distribuido (usualmente parte de una botnet).
                            5. Fuerza bruta en FTP.
                            6. Ping de la muerte: Paquete IP de gran tamaño.
                            7. Phishing: Sitios web o correos electrónicos de phishing.
                            8. Fraude en VoIP.
                            9. Proxy abierto: Proxy abierto, relé abierto o nodo de salida de Tor.
                            10. Spam web: Spam en comentarios/foros, spam en HTTP referer, u otro spam en CMS.
                            11. Spam de correo electrónico: Contenido de correo electrónico spam, archivos adjuntos infectados y correos electrónicos de phishing. Nota: Limita los comentarios a solo la información relevante (en lugar de volcados de registros) y asegúrate de eliminar PII si deseas permanecer anónimo.
                            12. Spam en blogs: Spam en comentarios de blogs en CMS.
                            13. IP de VPN: Categoría conjunta.
                            14. Escaneo de puertos: Escaneo en busca de puertos abiertos y servicios vulnerables.
                            15. Hackeo.
                            16. Inyección SQL: Intentos de inyección SQL.
                            17. Suplantación: Suplantación del remitente de correo electrónico.
                            18. Fuerza bruta: Ataques de fuerza bruta de credenciales en inicios de sesión de páginas web y servicios como SSH, FTP, SIP, SMTP, RDP, etc. Esta categoría es diferente de los ataques DDoS.
                            19. Bot web malicioso: Raspado de páginas web (para direcciones de correo electrónico, contenido, etc.) y rastreadores que no respetan robots.txt. Las solicitudes excesivas y la suplantación del agente de usuario también pueden ser reportadas aquí.
                            20. Host explotado: El host probablemente esté infectado con malware y siendo utilizado para otros ataques o para alojar contenido malicioso. El propietario del host puede no estar al tanto del compromiso. Esta categoría a menudo se usa en combinación con otras categorías de ataque.
                            21. Ataque a aplicaciones web: Intentos de explorar o explotar aplicaciones web instaladas, como un CMS (sistema de gestión de contenido) como WordPress/Drupal, soluciones de comercio electrónico, software de foros, phpMyAdmin y varios otros plugins/soluciones de software.
                            22. Abuso de SSH: Abuso de Secure Shell (SSH). Usa esta categoría en combinación con otras categorías más específicas.
                            23. Objetivo IoT: El abuso fue dirigido a un dispositivo del "Internet de las cosas" (IoT). Incluye información sobre qué tipo de dispositivo fue objetivo en los comentarios. """)
            comentarios = input("Ingrese algún comentario acerca del comportamiento de esta IP maliciosa: ")
            params = {
                'ip': ip,
                'categories': categories,
                'comment': comentarios
            }
            with open('apikey.txt', 'r') as archivo:
                llave = archivo.read().strip()
            headers = {
                'Accept': 'application/json',
                'Key': llave
            }
            response = requests.post(url=url, headers=headers, params=params)
            decodedResponse = response.json()
            guardar_en_archivo('resultado_reporte.txt', json.dumps(decodedResponse, sort_keys=True, indent=4))
 
        else:
            print("Opción no válida. Por favor ingrese una opción válida (1, 2 o 3).")
 
    # Llamada a las funciones basadas en la opción seleccionada
    if OPCIÓN == 1:
        Ports_Scanning()
    elif OPCIÓN == 2:
        ipdb()
    else:
        print("Opción no válida.")

#Ejecutar desde este modulo
#if __name__ == "__main__":
    #main()
