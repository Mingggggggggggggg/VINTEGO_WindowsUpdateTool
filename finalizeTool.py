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
            log.append(f"Kein Dateiname angegeben, jedoch existiert eine .iso '{fileName}'")
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
    flagPath = os.path.join(ISOPath, "installed.flag")
    try:
        if not os.path.exists(fullPath):
            log.append(f"Datei nicht gefunden in: {fullPath}")
            return False

        os.remove(fullPath)
        log.append("ISO-Datei erfolgreich gelöscht.")

        if os.path.exists(flagPath):
            os.remove(flagPath)
            log.append("Flag-Datei 'installed.flag' ebenfalls gelöscht.")

        return True
    except Exception as e:
        log.append(f"Fehler beim Löschen: {e}")
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


def createInstalledFlag(ISOPath):
    flagPath = os.path.join(ISOPath, "installed.flag")
    try:
        with open(flagPath, "w") as f:
            f.write("install_done")
        log.append("Flag-Datei 'installed.flag' wurde erstellt.")
        return True
    except Exception as e:
        log.append(f"Fehler beim Erstellen der Flag-Datei: {e}")
        return False


def checkInstalledFlag(ISOPath):
    flagPath = os.path.join(ISOPath, "installed.flag")
    exists = os.path.exists(flagPath)
    log.append(f"'installed.flag' {'gefunden' if exists else 'nicht vorhanden'}.")
    return exists

def initFinalization(ISOPath, fileName):
    flagExist = checkInstalledFlag(ISOPath)
    if flagExist:
        isSuccessful = checkSuccess()
        isFileExist, foundFileName = checkFile(ISOPath, fileName)
        flagPath = os.path.join(ISOPath, "installed.flag")
        result = False

        if isSuccessful and isFileExist:
            log.append("[SUCCESS] Windows Upgrade erfolgreich. ISO und Flag werden entfernt.")
            deleteFile(ISOPath, foundFileName)  
            result = True

        elif isSuccessful and not isFileExist:
            log.append("[SUCCESS] Windows Upgrade erfolgreich. ISO nicht gefunden. Entferne Flag.")
            if os.path.exists(flagPath):
                os.remove(flagPath)
                log.append("Flag-Datei 'installed.flag' wurde entfernt.")
            result = True

        elif not isSuccessful and isFileExist:
            log.append("[FAILURE] Windows Upgrade nicht erfolgreich. Entferne Flag, logge Fehler.")
            #deleteFile(ISOPath, foundFileName)
            if os.path.exists(flagPath):
                os.remove(flagPath)
                log.append("Flag-Datei 'installed.flag' wurde entfernt.")
            dumpWindowsLog()
            result = False

        elif not isSuccessful and not isFileExist:
            log.append("[FAILURE] Windows Upgrade nicht erfolgreich. ISO nicht gefunden. Entferne Flag und logge Fehler.")
            if os.path.exists(flagPath):
                os.remove(flagPath)
                log.append("Flag-Datei 'installed.flag' wurde entfernt.")
            dumpWindowsLog()
            result = False
    else:
        log.append("Flag existiert nicht. Vermutlich Erststart. Starte restliche Anwendung.")
        result = False

    logger.logMessages("Windows Status", log, top=True)
    return result