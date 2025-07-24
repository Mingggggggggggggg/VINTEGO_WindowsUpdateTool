import os
from datetime import datetime

def logMessages(name, data, folderPath=r"C:\VINTEGO-Technik\Logs", fileName="W10UpdateToolLog.txt"):
    os.makedirs(folderPath, exist_ok=True)
    fullPath = os.path.join(folderPath, fileName)

    puffer = len(name)
    dashes = (50 - puffer) // 2

    with open(fullPath, "a", encoding="utf-8") as file:
        file.write("\n\n")
        file.write("-" * dashes + f" {name} " + "-" * dashes + "\n")

        for entry in data:
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
            file.write(f"{timestamp} - {entry}\n")

        file.write("-" * (dashes - 3) + f" End{name} " + "-" * (dashes - 3) + "\n")
