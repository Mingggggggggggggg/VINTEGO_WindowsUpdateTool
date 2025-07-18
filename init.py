import sys
import checkComp as cc
import getFile

def main():

    # Pfadübergabe simulieren -- Kein Check, ob es ein Pfad ist, nur String
    result = cc.initCheck()

    if result:
        print("Alles kompatibel. Starte ISO Transfer")
    else:
        print("Anfoderungen nicht erfüllt")
        
    #TODO Übergabeparamter einbinden
    if len(sys.argv) > 1:
        downloadPath = sys.argv[1]            
        targetPath = sys.argv[2]  
        fileName = sys.argv[3]          
        logPath = sys.argv[4]
        
    else:
        print("Keine Parameter übergeben")
        
    if result:
        getFile.getFile(downloadPath, fileName, targetPath=r"C:\VINTEGO-Technik\Installer")

    

# MAIN
if __name__ == "__main__":
    main()
    