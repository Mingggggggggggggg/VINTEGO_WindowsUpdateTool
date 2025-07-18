import os
import subprocess
import logger

log = []
log.append("-------------------Mount/Install Log---------------------")

args = "/auto upgrade /quiet /noreboot /eula accept /dynamicupdate disable /compat IgnoreWarning"

def mountAndInstall(ISOPath):
    
    try:
        # Kombinierter Mount + Laufwerksbuchstabe + Start setup.exe in PowerShell
        powershell_script = f'''
        $ISOPath = "{ISOPath}"
        $MountPoint = (Mount-DiskImage -ImagePath $ISOPath -PassThru | Get-Volume).DriveLetter + ":"
        $SetupPath = "$MountPoint\\setup.exe"
        $Args = "{args}"
        Start-Process -FilePath $SetupPath -ArgumentList $Args -Wait
        '''

        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", powershell_script],
                       check=True)
        log.append("ISO gemountet und setup.exe erfolgreich gestartet.")
        return True
    except subprocess.CalledProcessError as e:
        log.append(f"Fehler beim Mounten oder Installieren: {e}")
        return False
        
def initMountAndInstall(filePath, fileName):
    if not fileName:
        iso_files = [f for f in os.listdir(filePath) if f.lower().endswith(".iso")]
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
        
    fullTargetPath = os.path.join(filePath, fileName)
    isSuccessfull = mountAndInstall(fullTargetPath)
    logger.logMessages(log)
    return isSuccessfull