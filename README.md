# 🎣 Phishing & DNS Tunneling Toolkit

A comprehensive **Cyber Security** educational project demonstrating a full attack chain: from automated **Phishing** email generation to data exfiltration using a **DNS Tunneling** covert channel.

> ⚠️ **DISCLAIMER:** This software is for **EDUCATIONAL PURPOSES ONLY**. It is intended to demonstrate vulnerabilities and testing methods. Usage of this tool for attacking targets without prior mutual consent is illegal.

## 🚀 Features

### 📧 Stage 1: Phishing Automation
The tool automates the creation of tailored phishing emails to increase success rates.
* [cite_start]**Dynamic Content:** Generates emails based on target profile (Username, Job Title, Personal Status, etc.)[cite: 3].
* [cite_start]**Benign Merging:** Capable of injecting malicious payloads into innocent-looking email contexts (e.g., forwarding a message from a "Boss")[cite: 3].
* [cite_start]**Attachment Generation:** Automatically creates a malicious executable (or script) designed to be downloaded by the victim[cite: 8].

### 🚇 Stage 2: DNS Tunneling (Covert Channel)
Once the victim opens the attachment, a post-exploitation script (`attachment.py`) executes:
1.  **Information Gathering:** Harvests sensitive data such as:
    * Password files
    * Current username & OS version
    * [cite_start]IP address & Available languages[cite: 7].
2.  [cite_start]**Data Exfiltration:** Encodes the stolen data and smuggles it out via **DNS Queries** to a controlled server (simulating a C&C server)[cite: 7].
3.  **Server-Side Analysis:** Includes a script (`analyze_dns_queries.py`) to capture and decode the incoming DNS traffic.

## 🛠️ Architecture

1.  **Attacker Machine:** Runs `full_phishing_tool.py` to generate the email and `attach_create.py` to compile the payload.
2.  **Victim Machine:** Receives the email, executes the attachment.
3.  [cite_start]**DNS Channel:** The attachment sends data to the Attacker's IP (acting as a DNS server)[cite: 7].

## 📂 Project Structure
```text
├── PyCharmMiscProject/
   ├── full_phishing_tool.py   # Main script for generating the campaign
   ├── attach_create.py        # Generates the malicious attachment
   ├── attachment.py           # The payload running on the victim's machine
   ├── analyze_dns_queries.py  # Server-side script to decode exfiltrated data
   └── *.html                  # Generated phishing email templates
