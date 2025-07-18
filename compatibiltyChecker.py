# https://www.microsoft.com/en-us/windows/windows-11-specifications
import json
import platform
import subprocess
import sys
import psutil
import winreg



## Minimal Requirements
minCPUCores = 2
minCPUSpeed = 1000
minCPUArch = "64bit"
minRAMSize = 4
minStorageSize = 64
isTPUEnabled = True
isSecureBootEnabled = True
minOSBuildTarget = 19041
logPath = "./"
error = []


def checkCPU():
    try:
        coreCount = psutil.cpu_count(False)
        maxFreq = psutil.cpu_freq()[2]
        arch = platform.architecture()[0]
        #print(coreCount)
        #print(maxFreq)
        #print(arch)
        
        if (coreCount < minCPUCores):
            error.append(f"Ungenügende CPU Kerne -- Tatsächlich {coreCount}; Erforderlich {minCPUCores}")
        if (maxFreq < minCPUSpeed):
            error.append(f"Ungenügende CPU Geschwindigkeit -- Tatsächlich {maxFreq} MHz; Erforderlich {minCPUSpeed}")
        if (arch != minCPUArch):
            error.append(f"Falsche Architektur -- Tatsächlich: {arch} Erforderlich: {minCPUArch} ") 
            
        if (coreCount >= minCPUCores and maxFreq >= minCPUSpeed and arch == minCPUArch):
            print("CPU Mindestanforderungen sind erfüllt")
            return True
        else:
            return False
        

    except Exception as e:
        print(f"Fehler: {str(e)}")
        return False



def checkRAM():
    try:
        totalRAM = psutil.virtual_memory().total / (1024**3) # Umrechnung von bytes zu gigabytes
        #print(totalRAM)
        if (totalRAM < minRAMSize):
            error.append(f"Ungenügend Arbeitsspeicher -- Tatsächlich {totalRAM}")
            
            
        
        else:
            print("Arbeitsspeicheranforderungen erfüllt")
            return True
        
    except Exception as e:
        print(f"Fehler: {str(e)}")
        return False


def checkStorage():
    try:
        diskSpace = psutil.disk_usage("C:")[2] / (1024**3) # Umrechnung von bytes zu gigabytes
        print(diskSpace)
        
        if (diskSpace < minStorageSize):
            error.append(f"Ungenügender Speicherplatz - Tatsächlich {diskSpace}")
            
        else:
            print("Speicheranforderungen erfüllt")
            return True

    
    except Exception as e:
        print(f"Fehler: {str(e)}")
        return False


def checkSecureBoot():
    try:

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\SecureBoot\State")
        value, _ = winreg.QueryValueEx(key, "UEFISecureBootEnabled")
        return value == 1

    except FileNotFoundError:
        return False
    
    except Exception as e:
        print(f"Fehler: {str(e)}")
        return False

def checkTPM():
    getTpmInfo()
    #getTpmVersion() # Versionsfindung nicht möglich

def getTpmInfo():
    try:
        cmd = ["powershell", "-Command", "Get-Tpm | ConvertTo-Json"]
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)

        try:
            decoded = output.decode('utf-8')
        except UnicodeDecodeError:
            decoded = output.decode('cp850')  # OEM-Codepage auf vielen Windows-Systemen
            
        if "Administratorberechtigungen" in decoded:
            print("Fehlende Adminrechte")
            return

        data = json.loads(decoded)

        print(f"TPM vorhanden: {data.get('TpmPresent')}")
        print(f"TPM aktiviert: {data.get('TpmEnabled')}")
        
    except subprocess.CalledProcessError:
        print("TPM nicht verfügbar oder Zugriff verweigert.")
    except Exception as e:
        print(f"Fehler beim Auslesen des TPM-Status: {e}")


def getTpmVersion():
    try:
        cmd = [
            "powershell",
            "-Command",
            "Get-Tpm | Select-Object SpecVersion | ConvertTo-Json"
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        decoded = output.decode('utf-8').strip()
        data = json.loads(decoded)
        
        # Falls data ein dict ist, z.B. {"TpmVersion": "2.0"}
        if isinstance(data, dict) and "TpmVersion" in data:
            print(f"TPM Version: {data['TpmVersion']}")
        else:
            print("TPM Version nicht gefunden.")
            
    except subprocess.CalledProcessError:
        print("Fehler: TPM nicht verfügbar oder Zugriff verweigert.")
    except json.JSONDecodeError:
        print("Fehler: Ausgabe konnte nicht als JSON geparst werden.")
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")

'''
def checkGPU():
    
    w = wmi.WMI()
    for gpu in w.Win32_VideoController():
        print(f"Name: {gpu.Name}")
        print(f"Treiberversion: {gpu.DriverVersion}")

    pass
'''


# Windows 10 Buildversion 2004 oder höher 
def checkOSVersion():
    try:
        version = sys.getwindowsversion()
        build = version.build  # z.B. 19041 für Windows 10 Version 2004
        print(f"Buildnummer: {build}")

        if build >= minOSBuildTarget:
            print("Windows-Version ist ausreichend (Build 2004 oder höher)")
            return True
        else:
            error.append(f"Windows-Version zu alt -- Build {build}; erforderlich mindestens 19041 (Version 2004)")
            return False

    except Exception as e:
        print(f"Fehler beim Prüfen der Windows-Version: {e}")
        return False

'''
# Optional
def checkInternetCon():
    pass
'''

def totalCheck():
    #TODO Vllt Log hierein
    if (checkCPU and checkRAM and checkStorage and checkSecureBoot and checkTPM and checkOSVersion):
        return True
    else:
        print("Bedingungen sind nicht erfüllt")
        return False


# MAIN
if __name__ == "__main__":
    checkCPU()
    checkRAM()
    checkStorage()
    checkTPM()
    print(checkSecureBoot())
    checkOSVersion()
    
    #TODO Log error Daten
    if error:
        print("CPU Mindestanforderungen nicht erfüllt.")
        for err in error:
            print(err)
   