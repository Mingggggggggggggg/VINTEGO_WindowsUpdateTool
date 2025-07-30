import sys
import checkComp as cc
import getFile
import logger
import mountInstall
import argparse
import finalizeTool



log = []

def getArgs():
    parser = argparse.ArgumentParser(description="Kopiert ISO Datei von Quellpfad zu Zielpfad und ruft diese im Zielpfad auf und initialisiert eine Installation")
    parser.add_argument("downloadPath", help="[Pflichtfeld] Pfad zum Downloadverzeichnis. Beispiel: C:\\Users\\Praktikant WHV\\Downloads")
    parser.add_argument("--fileName", default="", help="[Optional] Name der ISO-Datei inklusive Datentypendung. Standardmäßig sucht einzige .iso Datei im Quellordner")
    parser.add_argument("--targetPath", default=r"C:\VINTEGO-Technik\Installer", help="[Optional] Zielpfad. Standardmäßig: C:\\VINTEGO-Technik\\Installer")
    parser.add_argument("--skipCheck", action="store_true", help="Optional: Kompatibilitätsprüfung überspringen")
    return parser.parse_args() 

def main():

    args = getArgs()
    downloadPath = args.downloadPath
    fileName = args.fileName
    targetPath = args.targetPath
    skipCheck = args.skipCheck

    # Wenn kein Windows 11 System und ISO im targetPath, dann wird ein Installationsfehler angenommen.
    if finalizeTool.initFinalization(targetPath, fileName):
        sys.exit(5) # Errorcode 5: Sonderfall, wenn Upgrade erfolgreich oder nicht nötig ist.
    

    result = cc.initCheck()

    if skipCheck:
        log.append("skipCheck aktiviert. Überschreibe Kompatibilitätsergebnis.")
        result = True

        
    gotFile = False
    if result:
        try:
            print("Kompatibilitätscheck erfolgreich. Starte ISO Transfer.")
            log.append("Alles kompatibel. Starte ISO Transfer.")
            gotFile = getFile.initGetFile(downloadPath=downloadPath, fileName=fileName, targetPath=targetPath)
        except Exception as e:
            print(f"Fehler beim Transfer: {e}")
            log.append(f"Fehler beim Transfer: {e}")
    else:
        print("Kompatibilitätscheck nicht erfolgreich. Beende Anwendung.")
        log.append("Anfoderungen nicht erfüllt")
        
    if not gotFile and result:
        print("ISO-Transfer fehlgeschlagen. Installation wird nicht gestartet.")
        log.append("ISO-Transfer fehlgeschlagen. Installation wurde nicht gestartet.")
    
    if gotFile:
        try:
            print("ISO Transfer erfolgreich. Starte Mount und Installation.")
            log.append("ISO Transfer erfolgreich. Starte Mount und Installation.")
            isMounted = mountInstall.initMountAndInstall(targetPath=targetPath, fileName=fileName)
            finalizeTool.createInstalledFlag(targetPath)
            log.append("Mount und Installation gestartet. Warte auf Autoneustart.")
        except Exception as e:
            print(f"Fehler beim Mount oder Installation: {e}")
            log.append(f"Fehler beim Mount oder Installation: {e}")       

# MAIN
if __name__ == "__main__":
    try:
        main()
        log.append("Hauptprogramm durchlaufen. Anwendung wird beendet.")
        logger.logMessages("Global Log", log, top=True)
    except KeyboardInterrupt:
        print("Anwendung beendet durch Nutzer.")
        log.append("Anwendung vorzeitig durch Nutzer beendet.")
        logger.logMessages("Global Log", log, top=True)
        sys.exit()
    