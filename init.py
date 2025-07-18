import sys
import checkComp as cc

def main():

    # Pfadübergabe simulieren -- Kein Check, ob es ein Pfad ist, nur String
    if len(sys.argv) > 1:
        pfad = sys.argv[1]
        print(f"Übergebener Pfad: {pfad}")
        cc.initCheck()  
    else:
        print("Kein Pfad übergeben.")
        cc.initCheck()

    

# MAIN
if __name__ == "__main__":
    main()
    
    