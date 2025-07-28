import os
from datetime import datetime

def logMessages(name, data, folderPath=r"C:\VINTEGO-Technik\Logs", fileName="W10UpdateToolLog.txt", top=False):
    os.makedirs(folderPath, exist_ok=True)
    fullPath = os.path.join(folderPath, fileName)

    puffer = len(name)
    dashes = (55 - puffer) // 2

    header = "-" * dashes + f" {name} " + "-" * dashes + "\n"
    footer = "-" * (dashes - 3) + f" End{name} " + "-" * (dashes - 3) + "\n"


    logBlock = "\n\n" + header
    for entry in data:
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
        logBlock += f"{timestamp} - {entry}\n"
    logBlock += footer

    if top:
        if os.path.exists(fullPath):
            with open(fullPath, "r", encoding="utf-8") as file:
                prevContent = file.read()
        else:
            prevContent = ""

        with open(fullPath, "w", encoding="utf-8") as file:
            file.write(logBlock + prevContent)
    else:
        with open(fullPath, "a", encoding="utf-8") as file:
            file.write(logBlock)
