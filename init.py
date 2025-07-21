import os
import sys
import time
import checkComp as cc
import getFile
import logger
import mountInstall
import argparse



log = []
log.append("---------------- Global Log ----------------")

def getArgs():
    parser = argparse.ArgumentParser(description="Kopiert ISO Datei von Quellpfad zu Zielpfad und ruft diese im Zielpfad auf und initialisiert eine Installation")
    parser.add_argument("downloadPath", help="[Pflichtfeld] Pfad zum Downloadverzeichnis")
    parser.add_argument("--fileName", default="", help="[Optional] Name der ISO-Datei inklusive Datentypendung. Standardmäßig sucht einzige .iso Datei im Quellordner")
    parser.add_argument("--targetPath", default=r"C:\VINTEGO-Technik\Installer", help="[Optional] Zielpfad. Standardmäßig: C:\\VINTEGO-Technik\\Installer")
    return parser.parse_args() 

def main():

    args = getArgs()
    downloadPath = args.downloadPath
    fileName = args.fileName
    targetPath = args.targetPath

    
    

    result = cc.initCheck()
    # result überschreiben zu Testzwecken
    #result = True

        
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
    
    
    if gotFile:
        try:
            print("ISO Transfer erfolgreich. Starte mount und Installation.")
            log.append("ISO Transfer erfolgreich. Starte mount und Installation.")
            isMounted = mountInstall.initMountAndInstall(targetPath=targetPath, fileName=fileName)
        except Exception as e:
            print(f"Fehler beim mount oder Installation: {e}")
            log.append(f"Fehler beim mount oder Installation: {e}") 
    else:
        print("Probleme beim Transfer. Beende Anwendung.")
        log.append("Probleme beim Transfer.")
        
    if isMounted:
        logger.logMessages(log)
        try:
            print("Gerät wird in 10 Sekunden neugestartet. STRG + C zum Abbrechen.")
            time.sleep(10)
            os.system("shutdown /r /t 0")
        except KeyboardInterrupt:
            print("Neustart wurde vom Nutzer abgebrochen.")



    

# MAIN
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Anwendung beendet durch Nutzer")
        sys.exit()
    