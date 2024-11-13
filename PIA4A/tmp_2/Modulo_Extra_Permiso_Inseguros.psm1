# Habilitar modo estricto
Set-StrictMode -Version Latest

# Función para checar los permisos inseguros
function Get-InsecureFilePermissions {
    <#
.FUNCIONALIDAD REAL
Esta funcion nos ayuda a poder supervisar y analizar de forma facil
los archivos del directorio que tomamos como path. En general es de
gran ayuda en la ciberseguridad.

.DESCRIPTION
Checa los permisos de los archivos/carpetas en una ruta específica
y detecta si existen configuraciones que no son lo suficiente seguras
como asignaciones a 'Everyone' o 'Usuarios'.

.PARAMETER 
Path: Ruta del archivo/carpeta del cual se quiere saber si tiene
permisos seguros o inseguros.

.NOTITAS
Autor: Javier Abraham Palomares Garcia

.EXAMPLE
Solo ejecuta el comando en tu terminal con el path como en 
el siguente ejemplo:.
Get-InsecureFilePermissions -Path "C:\Carpeta"
Y asi revisamos si los permisos son seguros o inseguros en la carpeta/archivo.
#>   
   param (
        [Parameter(Mandatory = $true, HelpMessage = "Escribe la ruta del archivo o carpeta")]
        [string]$Path
    )
    
    # Uso de errores y validaciones
    try {
        if (-not (Test-Path -Path $Path)) {
            Write-Host "La ruta hacia el archivo/carpeta al parecer no existe: $Path"
        }
        
        # Buscamos la lista de archivos segun el get-child
        $items = Get-ChildItem -Path $Path -Recurse -Force
        foreach ($item in $items) {
            try {
                # Obtener los permisos de cada archivo/carpeta
                $acl = Get-Acl -Path $item.FullName
                $permissions = $acl.Access
                
                # Revisar si hay permisos inseguros (ej: asignaciones a 'Everyone' o 'Usuarios')
                foreach ($permission in $permissions) {
                    if ($permission.IdentityReference -match "Everyone" -or $permission.IdentityReference -match "Usuarios") {
                        Write-Host "Permiso inseguro en $($item.FullName) para $($permission.IdentityReference)"
                    }
                }
            }
            catch {
                Write-Error "Error revisando permisos en: $($item.FullName). Error: $_"
            }
        }
    }
    catch {
        Write-Error "Error en la ruta especificada: $_"
    }
}
