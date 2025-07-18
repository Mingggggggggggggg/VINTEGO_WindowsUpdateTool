import os
import shutil
import hashlib as hl

log = []

def hashFile(fullPath):
    hashstr = hl.sha256()
    with open(fullPath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hashstr.update(chunk)
    return hashstr.hexdigest()

def getFile(downloadPath, fileName, targetPath):
    fullPath = os.path.join(downloadPath, fileName)
    fullTargetPath = os.path.join(targetPath, fileName)
    
    try:
        if not os.path.exists(fullPath):
            raise FileNotFoundError(f"Datei nicht gefunden: {fullPath}")
        
        os.makedirs(os.path.dirname(fullTargetPath), exist_ok=True)
        shutil.copy2(fullPath, fullTargetPath)

        if not os.path.exists(targetPath):
            raise IOError("Zieldatei wurde nicht erstellt.")

        size_ok = os.path.getsize(fullPath) == os.path.getsize(targetPath)
        hash_ok = hashFile(fullPath) == hashFile(targetPath)

        if size_ok and hash_ok:
            msg = "Datei erfolgreich kopiert und überprüft."
            print(msg)
            return msg
        else:
            raise IOError("Überprüfung fehlgeschlagen (Größe oder Hash stimmt nicht).")

    except Exception as e:
        msg = f"Fehler: {e}"
        print(msg)
        return msg

if __name__ == "__main__":
    downloadPath = r"C:\Users\Praktikant WHV\Downloads"
    fileName = "Windows11 Test.iso"
    targetPath = r"C:\VINTEGO-Technik\Installer"
    
    getFile(downloadPath, fileName, targetPath)