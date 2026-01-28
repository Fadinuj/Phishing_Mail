#Fadi Nujedat ,  Ron Amsalem
#214766339 , 326029600

import os
import subprocess
import platform
import py_compile

def build_for_windows():
    print("[*] מייצר קובץ EXE בעזרת pyinstaller (Windows)...")
    result = subprocess.call(["pyinstaller", "--onefile", "--noconsole", "attachment.py"])
    if result == 0:
        print("[+] נוצר קובץ: dist/attachment.exe")
    else:
        print("[!] נכשל ביצירת הקובץ. ודא ש-pyinstaller מותקן (pip install pyinstaller)")

def build_for_linux():
    print("[*] מקמפל את attachment.py לקובץ pyc (Linux)...")
    try:
        py_compile.compile("attachment.py", cfile="attachment.pyc")
        print("[+] נוצר קובץ: attachment.pyc")
    except Exception as e:
        print(f"[!] שגיאה: {e}")

def main():
    print("=== attach_create.py ===")
    system = platform.system().lower()
    print(f"[*] זוהתה מערכת הפעלה: {system}")

    if system == "windows":
        build_for_windows()
    elif system == "linux":
        build_for_linux()
    else:
        print(f"[!] מערכת הפעלה לא נתמכת: {system}")

if __name__ == "__main__":
    main()
