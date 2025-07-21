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
    parser.add_argument("--fileName", default="", help="[Optional] Name der ISO-Datei inklusive Datentypendung. Wenn leer sucht einzige .iso Datei im Quellordner")
    parser.add_argument("--targetPath", default=r"C:\VINTEGO-Technik\Installer", help="[Optional] Zielpfad. Wenn leer: C:\\VINTEGO-Technik\\Installer")
    return parser.parse_args() 

def main():

    args = getArgs()
    downloadPath = args.downloadPath
    fileName = args.fileName
    targetPath = args.targetPath

    
    

    result = cc.initCheck()
    # result überschreiben zu Testzwecken
    result = True
    if result:
        log.append("Alles kompatibel. Starte ISO Transfer")
    else:
        log.append("Anfoderungen nicht erfüllt")
        


    gotFile = False
    if result:
        try:
            gotFile = getFile.initGetFile(downloadPath=downloadPath, fileName=fileName, targetPath=targetPath)
        except Exception as e:
            log.append(f"Fehler beim Transfer: {e}")
    
    
    if gotFile:
        mountInstall.initMountAndInstall(targetPath=targetPath, fileName=fileName)
    logger.logMessages(log)

    

# MAIN
if __name__ == "__main__":
    main()
    