import os
import shutil
import hashlib as hl
import logger

log = []

def hashFile(fullPath):
    hashstr = hl.sha256()
    with open(fullPath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hashstr.update(chunk)
    return hashstr.hexdigest()

def getFile(downloadPath, fileName, targetPath):
    if not fileName:
        getISO = [f for f in os.listdir(downloadPath) if f.lower().endswith(".iso")]
        if len(getISO) == 1:
            fileName = getISO[0]
            log.append(f"Kein Dateiname angegeben, verwende daher '{fileName}'")
        elif len(getISO) == 0:
            log.append("Keine .iso-Datei im Download-Pfad gefunden.")
            return False
        else:
            log.append("Mehrere .iso-Dateien im Download-Pfad gefunden. Bitte Dateiname angeben.")
            return False
        
    fullPath = os.path.join(downloadPath, fileName)
    fullTargetPath = os.path.join(targetPath, fileName)
    
    try:
        if not os.path.exists(fullPath):
            log.append(f"Datei nicht gefunden in: {fullPath}")
            return False

        if os.path.abspath(fullPath) == os.path.abspath(fullTargetPath):
            log.append("Quell- und Zielpfad sind identisch. Kein Kopieren notwendig.")
            return True

        os.makedirs(os.path.dirname(fullTargetPath), exist_ok=True)
        shutil.copy2(fullPath, fullTargetPath)

        if not os.path.exists(fullTargetPath):
            log.append("Zieldatei existiert nicht nach dem Kopieren.")
            return False

        correctSize = os.path.getsize(fullPath) == os.path.getsize(fullTargetPath)
        correctHash = hashFile(fullPath) == hashFile(fullTargetPath)

        if correctSize and correctHash:
            log.append("Datei erfolgreich kopiert und vollständig.")
            return True
        else:
            log.append("Überprüfung fehlgeschlagen (Größe oder Hash stimmt nicht).")
            return False

    except Exception as e:
        log.append(f"Fehler: {e}")
        return False


def initGetFile(downloadPath, fileName, targetPath):    
    result = getFile(downloadPath=downloadPath, fileName=fileName,targetPath=targetPath)
    logger.logMessages("Transfer",log)
    return result
    