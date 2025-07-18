import sys
import checkComp as cc

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
        logPath = sys.argv[3]
        
    else:
        print("Keine Parameter übergeben")

    

# MAIN
if __name__ == "__main__":
    main()
    