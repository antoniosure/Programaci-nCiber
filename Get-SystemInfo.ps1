# Script de recolección de información del sistema en PowerShell

<#
.SYNOPSIS
    Script para generar reportes sobre uso de memoria RAM, CPU, adaptadores de red, estadísticas de red y discos del sistema.

.DESCRIPTION
    Este script utiliza varias funciones para recopilar información detallada del sistema y genera reportes en archivos de texto.
    Incluye el hash SHA-256 del reporte y muestra un mensaje en la terminal con la ubicación exacta del archivo generado.

.EXAMPLE
    .\Get-SystemInfo.ps1
    Ejecuta el script completo generando reportes de cada recurso monitoreado.

.NOTES
    Cada función genera un reporte en un archivo .txt y calcula el hash SHA-256 para validación.
#>

# Función para calcular el hash del archivo
function Get-FileHashString {
    <#
    .SYNOPSIS
        Calcula el hash SHA-256 de un archivo dado.

    .PARAMETER FilePath
        Ruta del archivo del cual calcular el hash.

    .OUTPUTS
        Devuelve el hash SHA-256 en formato de texto.

    .EXAMPLE
        Get-FileHashString -FilePath "C:\Report.txt"
    #>
    param (
        [string]$FilePath
    )
    $hash = Get-FileHash -Path $FilePath -Algorithm SHA256
    return $hash.Hash
}

# Función para obtener la fecha y hora actual en un formato amigable
function Get-FormattedTimestamp {
    <#
    .SYNOPSIS
        Genera una marca de tiempo formateada para los nombres de los reportes.

    .OUTPUTS
        Devuelve la fecha y hora actual en el formato "yyyyMMdd_HHmmss".

    .EXAMPLE
        Get-FormattedTimestamp
    #>
    return (Get-Date -Format "yyyyMMdd_HHmmss")
}

# Función para guardar y reportar el resultado en un archivo CSV
function Save-Report {
    <#
    .SYNOPSIS
        Guarda el contenido del reporte en un archivo CSV y muestra el hash y la ubicación en la terminal.

    .PARAMETER ReportContent
        Contenido del reporte a guardar.

    .PARAMETER ReportType
        Tipo de reporte (por ejemplo, "MemoriaRAM", "CPU").

    .EXAMPLE
        Save-Report -ReportContent $content -ReportType "MemoriaRAM"
    #>
    param (
        [string]$ReportContent,
        [string]$ReportType
    )
    $timestamp = Get-FormattedTimestamp
    $filePath = "$PSScriptRoot/${ReportType}_Report_$timestamp.txt"
    $ReportContent | Out-File -FilePath $filePath -Encoding UTF8
    $fileHash = Get-FileHashString -FilePath $filePath

    # Guardar detalles del reporte en un archivo CSV
    $csvPath = "$PSScriptRoot/reportes_sistema.csv"
    $reportData = [PSCustomObject]@{
        ReportName = "${ReportType}_Report_$timestamp.txt"
        FileHash   = $fileHash
        Date       = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    }
    # Exportar en modo Append para agregar nuevas filas sin sobrescribir
    $reportData | Export-Csv -Path $csvPath -Append -NoTypeInformation -Encoding UTF8

    Write-Host "Se ejecutó la tarea de '$ReportType' y el reporte fue guardado en $filePath con el hash $fileHash"
}

# Función para generar el reporte de Memoria RAM
function Get-AvailableRAM {
    <#
    .SYNOPSIS
        Genera un reporte de la memoria RAM visible y disponible en GB.

    .DESCRIPTION
        Usa Win32_OperatingSystem para obtener datos de memoria RAM total y disponible en el sistema.

    .EXAMPLE
        Get-AvailableRAM
    #>
    $reportContent = Get-WmiObject Win32_OperatingSystem | Select-Object @{
        Name="Memoria total visible (GB)";
        Expression={[math]::round($_.TotalVisibleMemorySize / 1MB, 2)}
    }, @{
        Name="Memoria física disponible (GB)";
        Expression={[math]::round($_.FreePhysicalMemory / 1MB, 2)}
    } | Out-String
    Save-Report -ReportContent $reportContent -ReportType "MemoriaRAM"
}

# Función para generar el reporte de CPU
function Get-TopCPUProcesses {
    <#
    .SYNOPSIS
        Genera un reporte de los procesos que más consumen CPU.

    .PARAMETER TopN
        Número de procesos a listar, por defecto 15.

    .EXAMPLE
        Get-TopCPUProcesses -TopN 10
    #>
    param(
        [int]$TopN = 15
    )
    $reportContent = Get-Process | Sort-Object CPU -Descending | Select-Object -First $TopN Id, ProcessName, CPU | Out-String
    Save-Report -ReportContent $reportContent -ReportType "ProcesosCPU"
}

# Función para generar el reporte de adaptadores de red
function Get-NetworkAdapters {
    <#
    .SYNOPSIS
        Genera un reporte de los adaptadores de red del sistema.

    .EXAMPLE
        Get-NetworkAdapters
    #>
    $reportContent = Get-NetAdapter | Select-Object Name, Status, LinkSpeed | Out-String
    Save-Report -ReportContent $reportContent -ReportType "AdaptadoresRed"
}

# Función para generar el reporte de estadísticas de red
function Get-NetworkStatistics {
    <#
    .SYNOPSIS
        Genera un reporte de estadísticas de red.

    .EXAMPLE
        Get-NetworkStatistics
    #>
    $reportContent = Get-NetAdapterStatistics | Select-Object Name, ReceivedBytes, SentBytes | Out-String
    Save-Report -ReportContent $reportContent -ReportType "EstadísticasRed"
}

# Función para generar el reporte de discos físicos
function Get-PhysicalDisks {
    <#
    .SYNOPSIS
        Genera un reporte de los discos físicos del sistema.

    .EXAMPLE
        Get-PhysicalDisks
    #>
    $reportContent = Get-PhysicalDisk | Select-Object FriendlyName, MediaType, HealthStatus, @{
        Name="Size (GB)";
        Expression={[math]::round($_.Size / 1GB, 2)}
    } | Out-String
    Save-Report -ReportContent $reportContent -ReportType "DiscosFísicos"
}

# Función para generar el reporte de discos lógicos
function Get-LogicalDisks {
    <#
    .SYNOPSIS
        Genera un reporte de los discos lógicos del sistema.

    .EXAMPLE
        Get-LogicalDisks
    #>
    $reportContent = Get-WmiObject Win32_LogicalDisk -Filter "DriveType=3" | Select-Object DeviceID, VolumeName, @{
        Name="Size (GB)";
        Expression={[math]::round($_.Size / 1GB, 2)}
    }, @{
        Name="FreeSpace (GB)";
        Expression={[math]::round($_.FreeSpace / 1GB, 2)}
    } | Out-String
    Save-Report -ReportContent $reportContent -ReportType "DiscosLógicos"
}

# Ejemplo de uso de cada función para generar reportes
Get-AvailableRAM
Get-TopCPUProcesses -TopN 10
Get-NetworkAdapters
Get-NetworkStatistics
Get-PhysicalDisks
Get-LogicalDisks
