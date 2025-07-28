$appPath = "C:\VINTEGO-Technik\Tools"
$appUrl = "https://github.com/Mingggggggggggggg/VINTEGO_WindowsUpdateTool/releases/download/v1.2.4/Windows10-UpdateTool.exe"
$exeFile = Join-Path -Path $appPath -ChildPath "Windows10-UpdateTool.exe"
$logPath = "C:\Users\VINTEGO\Logs\W10UpdateToolLog.txt"
$isoFile = Join-Path -Path $env:quellverzeichnis -ChildPath "Win11.iso"

function runExec {
    $argList = @()

    if ($env:quellverzeichnis) {
        $argList += $env:quellverzeichnis
    } else {
        Write-Output "Fehler: Kein Quellverzeichnis angegeben."
        exit 1
    }

    if ($env:dateinamen) {
        $argList += $env:dateinamen
    }

    if ($env:zielverzeichnis) {
        $argList += $env:zielverzeichnis
    }

    Write-Output "Starte Windows10-UpdateTool mit Argumenten: $argList"
    Start-Process -FilePath $exeFile -ArgumentList $argList -NoNewWindow -Wait -Verb runAs
}

function readLogs {
    if (Test-Path $logPath) {
        return Get-Content $logPath -Raw
    } else {
        return "Kein Log gefunden."
    }
}

function getApp {
    if (-not (Test-Path $exeFile)) {
        if (-not (Test-Path $appPath)) {
            New-Item -Path $appPath -ItemType Directory | Out-Null
        }

        Write-Output "Lade Anwendung von $appUrl herunter..."
        Invoke-WebRequest -Uri $appUrl -OutFile $exeFile

        if (-not (Test-Path $exeFile)) {
            Write-Output "Fehler: Anwendung konnte nicht heruntergeladen werden."
            exit 1
        }

        Write-Output "Anwendung erfolgreich heruntergeladen."
    } else {
        Write-Output "Anwendung bereits vorhanden."
    }

    if ($env:onlinedownload -eq "true") {
        Write-Output "Online-Modus aktiviert – lade ISO-Datei von $env:quellverzeichnis herunter..."
        Invoke-WebRequest -Uri $env:quellverzeichnis -OutFile $isoFile
    } else {
        Write-Output "Offline-Modus: Verwende Quelle unter $env:quellverzeichnis"
    }

    runExec
}

getApp
#Warte 5 Sekunden, weil keine Ahnung, ob die Logs gelesen werden, wenn die Anwendung noch läuft. aaaaaaaaaaaaaaaaaaaaaa
Start-Sleep 5

$logs = readLogs
ninja-property-set windows10updatetoollog "$logs"
Write-Output "Skript beendet."