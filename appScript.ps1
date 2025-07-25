$appPath = "C:\VINTEGO-Technik\Tools"
$appUrl = "https://github.com/Mingggggggggggggg/VINTEGO_WindowsUpdateTool/releases/download/v1.2.4/Windows10-UpdateTool.exe"
$exeFile = Join-Path -Path $appPath -ChildPath "Windows10-UpdateTool.exe"
$logPath = "C:\Users\VINTEGO\Logs\W10UpdateToolLog.txt"

function runExec {
    $argList = @()

    if ($env:quellverzechnis) {
        $argList += $env:quellverzechnis
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

    Write-Output "Starte Windows10-UpdateTool Anwendung mit Argumenten: $argList"
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
    if (Test-Path $exeFile) {
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