import os
from datetime import datetime

def logMessages(data, folderPath=r"C:\VINTEGO-Technik\Logs", fileName="log.txt"):
    # Ordner erstellen, falls nicht vorhanden
    os.makedirs(folderPath, exist_ok=True)
    
    fullPath = os.path.join(folderPath, fileName)
    
    with open(fullPath, "a", encoding="utf-8") as file:
        file.write(f"\n\n\n --------------------------------------------------------------------------------------------------------\n")
        for i in data:
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
            file.write(f"{timestamp}" + " - " + f"{str(i)} "+" \n \n")
        file.write("\n --------------------------------------------------------------------------------------------------------\n")
