import sys
import checkComp as cc
import getFile
import logger




log = []
log.append("---------------- Global Log ----------------")


def main():

    # Standardwerte
    downloadPath = r"C:\Users\Praktikant WHV\Downloads"
    targetPath = r"C:\VINTEGO-Technik\Installer"
    fileName = "" 
    
    

    

    result = cc.initCheck()
    result = True
    if result:
        log.append("Alles kompatibel. Starte ISO Transfer")
    else:
        log.append("Anfoderungen nicht erfüllt")
        

    if len(sys.argv) >= 3:
        downloadPath = sys.argv[1]
        targetPath = sys.argv[2]
        if len(sys.argv) > 3:
            fileName = sys.argv[3]       
        
    else:
        log.append("Fehlende Parameter")
        log.append(f"Downloadpfad: {downloadPath}")
        log.append(f"Zielpfad: {targetPath}")
        log.append(f"Dateinamen: {fileName}")


    if result:
        try:
            getFile.initGetFile(downloadPath=downloadPath, fileName=fileName, targetPath=targetPath)
        except Exception as e:
            log.append(f"Fehler beim Transfer: {e}")
            
    logger.logMessages(log)

    

# MAIN
if __name__ == "__main__":
    main()
    