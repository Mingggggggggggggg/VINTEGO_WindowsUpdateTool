[CmdletBinding()]
param (
    [Parameter()]
    [String]$downloadPath = $env:quellverzechnis,
    [Parameter()]
    [String]$fileName = $env:dateinamen,
    [Parameter()]
    [String]$targetPath = $env:zielverzeichnis
)

# Standardwerte
$appPath = "C:\VINTEGO-Technik\Tools"
$appUrl = "https://testdownload.de/Windows10-UpdateTool.exe"
$exeFile = Join-Path -Path $appPath -ChildPath "Windows10-UpdateTool.exe"
$logPath = "C:\Users\VINTEGO\Logs\log.txt"

begin {
  # Methode zum Ausführen der Anwendung unter den vorgegebenen Parametern
  function runExec {
    $cmdArgs = @()
    $cmdArgs += $downloadPath

    if ($fileName) {
      $cmdArgs += "--fileName"
      $cmdArgs += $fileName
    } else {
      Write-Output "Kein Dateiname angegeben. Suche nach genau einer ISO im Quellverzeichnis."
    }

    if ($targetPath) {
      $cmdArgs += "--targetPath"
      $cmdArgs += $targetPath
    } else {
      Write-Output "Kein Zielpfad angegeben. Verwende Standardpfad C:\Users\VINTEGO\Installer."
    }

    Write-Output "Starte Windows10-UpdateTool Anwendung. Dies kann einen Moment dauern."
    & $exeFile @cmdArgs
  }
  
  # Methode zum Auslesen der Logs aus einer Textdatei
  function readLogs {
    if (Test-Path $logPath) {
      $log = Get-Content $logPath
      $result = $log -join "`n"
      return $result
    } else {
      return "Kein Log gefunden."
    }
  }

  # Methode zum herunterladen der exe aus einem Downloadlink
  function getApp {
    if (Test-Path -Path $exeFile) {
      Write-Output "Anwendung bereits vorhanden."
      runExec
    } else {
      if (-not (Test-Path $appPath)) {
        New-Item -Path $appPath -ItemType Directory | Out-Null
      }
      Write-Output "Lade Anwendung aus $appUrl herunter"
      Invoke-WebRequest -Uri $appUrl -OutFile $exeFile

      if (Test-Path $exeFile) {
        Write-Output "Anwendung erfolgreich heruntergeladen."
        runExec
      } else {
        Write-Output "Fehler: Anwendung konnte nicht heruntergeladen werden."
        exit 1
      }
    }
  }

  getApp
  ninja-property-set windows10updatetoollog (readLogs)
  Write-Output "Skript beendet."
}
