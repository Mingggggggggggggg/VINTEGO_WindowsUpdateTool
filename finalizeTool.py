import os
import sys
import logger

pantherPath = r"C:\Windows\Panther\setuperr.log"
log = []


def checkSuccess():
    version = sys.getwindowsversion()
    build = version.build
    if (build > 22000):
        log.append("Windows 11 ist auf dem System gefunden worden.")
        return True
    else:
        log.append("Windows 11 ist nicht auf dem System gefunden worden.")
        return False

def checkFile(ISOPath, fileName):
    if not fileName:
        getISO = [f for f in os.listdir(ISOPath) if f.lower().endswith(".iso")]
        if len(getISO) == 1:
            fileName = getISO[0]
            log.append(f"Kein Dateiname angegeben, jedoch exisitiert eine .iso '{fileName}'")
            return True, fileName
        elif len(getISO) == 0:
            log.append("Keine .iso-Datei im Installerordner gefunden.")
            return False, None
        else:
            log.append("Mehrere .iso-Dateien im Installerordner gefunden. Bitte Dateiname angeben.")
            return False, None
    else:
        fullPath = os.path.join(ISOPath, fileName)
        if os.path.exists(fullPath):
            return True, fileName
        else:
            log.append(f"Gesuchte ISO {fileName} wurde nicht im Pfad {ISOPath} gefunden.")
            return False, None
        
        
def deleteFile(ISOPath, fileName):
    fullPath = os.path.join(ISOPath, fileName)
    try:
        if not os.path.exists(fullPath):
            log.append(f"Datei nicht gefunden in: {fullPath}")
            return False
            
        os.remove(fullPath)

        if not os.path.exists(fullPath):
            log.append("Zieldatei erfolgreich gelöscht.")
            return True
    except Exception as e:
        log.append(f"Fehler: {e}")
        return False
    
def dumpWindowsLog():
    errorLog = []
    if not os.path.exists(pantherPath):
        log.append("setuperr.log nicht gefunden.")
        return

    try:
        with open(pantherPath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.readlines()
            errorLog.extend([line.strip() for line in content if line.strip()])
        logger.logMessages("Error Dump", errorLog)
    except Exception as e:
        log.append(f"Fehler beim Lesen von setuperr.log: {e}")


def initFinalization(ISOPath, fileName):
    isSuccessful = checkSuccess()
    isFileExist, foundFileName = checkFile(ISOPath, fileName)
    result = False
    
    
    if isSuccessful and isFileExist:
        log.append("[SUCCESS] Windows Upgrade erfolgreich. ISO wird entfernt.")
        deleteFile(ISOPath, foundFileName)
        result = True
    elif isSuccessful and not isFileExist:
        log.append("[SUCCESS] Windows Upgrade erfolgreich. ISO konnte nicht gefunden werden.")
        result = True
    elif not isSuccessful and isFileExist:
        log.append("[FAILURE] Windows Upgrade nicht erfolgreich. Entferne ISO, schreibe Fehlermeldung in Log und beende Anwendung.")
        deleteFile(ISOPath, foundFileName)
        result = False
    else:
        return False
        
    logger.logMessages("Windows Status", log, top=True)
    return result