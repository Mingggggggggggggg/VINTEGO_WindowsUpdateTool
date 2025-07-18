import sys
import checkComp as cc

def main():
    if len(sys.argv) > 1:
        pfad = sys.argv[1]
        print(f"Übergebener Pfad: {pfad}")
        cc.initCheck(pfad)  # Pfad an checkComp übergeben
    else:
        print("Kein Pfad übergeben.")
        cc.initCheck()
    
    

# MAIN
if __name__ == "__main__":
    main()
    
    