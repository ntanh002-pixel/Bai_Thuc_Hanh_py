import smtplib
import imaplib
import email
from email.mime.text import MIMEText

# === BƯỚC 1: ĐỌC DỮ LIỆU TỪ FILE ===
with open('MyEmail.txt', 'r') as f:
    acc = f.readlines()
    print(acc)
    sender_email = acc[0].strip()
    app_password = acc[1].strip()

with open('NdEmail.txt', 'r', encoding='utf-8') as f:
    email_body = f.read()

with open('EmailNgNhan.txt', 'r') as f:
    recipient_email = f.read().strip()

with open('EmailNgGui.txt', 'r') as f:
    filter_sender = f.read().strip()

# === BƯỚC 2: GỬI EMAIL ===
msg = MIMEText(email_body)
msg['Subject'] = 'Email Tự Động'
msg['From'] = sender_email
msg['To'] = recipient_email

print("🔄 Đang gửi email...")
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(msg)
print("✅ Gửi email thành công.")

# === BƯỚC 3: NHẬN EMAIL ===
print("📬 Đang kiểm tra hộp thư đến...")
with imaplib.IMAP4_SSL('imap.gmail.com') as imap:
    imap.login(sender_email, app_password)
    imap.select('INBOX')

    # Tìm email từ địa chỉ trong email_filter.txt
    result, data = imap.search(None, f'FROM "{filter_sender}"')
    mail_ids = data[0].split()

    if not mail_ids:
        print("❌ Không tìm thấy email từ người gửi chỉ định.")
    else:
        latest_id = mail_ids[-1]
        result, msg_data = imap.fetch(latest_id, '(RFC822)')
        raw_email = msg_data[0][1]
        email_msg = email.message_from_bytes(raw_email)

        subject = email_msg['Subject']
        print(f"📨 Tiêu đề: {subject}")

        if email_msg.is_multipart():
            for part in email_msg.walk():
                if part.get_content_type() == 'text/plain':
                    print("📃 Nội dung:\n", part.get_payload(decode=True).decode())
                    break
        else:
            print("📃 Nội dung:\n", email_msg.get_payload(decode=True).decode())

    imap.logout()