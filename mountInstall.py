import os
import subprocess
import logger

log = []

args = "/auto upgrade /quiet /eula accept /dynamicupdate disable /compat IgnoreWarning"

def mountAndInstall(ISOPath):
    try:
        powershell_script = f'''
        $ISOPath = "{ISOPath}"
        $DiskImage = Mount-DiskImage -ImagePath $ISOPath -PassThru
        if (-not $DiskImage) {{
            Write-Error "Mounten der ISO fehlgeschlagen!"
            exit 1
        }}
        $MountPoint = (Get-Volume -DiskImage $DiskImage).DriveLetter + ":"
        if (-not (Test-Path $MountPoint)) {{
            Write-Error "Laufwerksbuchstabe nicht gefunden!"
            exit 1
        }}
        $SetupPath = "$MountPoint\\SETUP.exe"
        Start-Process -FilePath $SetupPath -ArgumentList "{args}" -Verb RunAs
        '''
        rs = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", powershell_script],
            check=True,
            text=True,
            capture_output=True
        )
        log.append(f"ISO gemountet und setup.exe gestartet. PowerShell-Ausgabe: {rs.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        log.append(f"Fehler beim Mounten/Installieren: {e.stderr}")
        return False

def initMountAndInstall(targetPath, fileName=None):
    if not fileName:
        iso_files = [f for f in os.listdir(targetPath) if f.lower().endswith(".iso")]
        if len(iso_files) == 1:
            fileName = iso_files[0]
            log.append(f"Kein Dateiname übergeben. Verwende ISO: {fileName}")
        elif len(iso_files) == 0:
            log.append("Keine .iso-Datei im Zielpfad gefunden.")
            logger.logMessages(log)
            return False
        else:
            log.append("Mehrere .iso-Dateien gefunden. Dateiname erforderlich.")
            logger.logMessages(log)
            return False   
        
    fullTargetPath = os.path.join(targetPath, fileName)
    isSuccessfull = mountAndInstall(fullTargetPath)
    logger.logMessages("Mount/Install", log)
    return isSuccessfull