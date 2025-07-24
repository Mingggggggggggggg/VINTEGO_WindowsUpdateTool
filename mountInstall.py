import os
import subprocess
import logger

log = []

args = "/auto upgrade /quiet /eula accept /dynamicupdate disable /compat IgnoreWarning" # entferne /noreboot aus args

def mountAndInstall(ISOPath):
    
    try:
        # Kombinierter Mount + Laufwerksbuchstabe + Start setup.exe in PowerShell
        powershell_script = f'''
        $ISOPath = "{ISOPath}"
        $MountPoint = (Mount-DiskImage -ImagePath $ISOPath -PassThru | Get-Volume).DriveLetter + ":"
        $SetupPath = "$MountPoint\\SETUP.exe"
        $Args = "{args}"
        Start-Process -FilePath $SetupPath -ArgumentList $Args -Wait
        '''

        rs = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", powershell_script])
        log.append(f"ISO gemountet und setup.exe gestartet. Rückgabecode: {rs.returncode}")
        return True
    except subprocess.CalledProcessError as e:
        log.append(f"Fehler beim Mounten oder Installieren: {e}")
        return False
        
def initMountAndInstall(targetPath, fileName):
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
    logger.logMessages("Mount/Install",log)
    return isSuccessfull