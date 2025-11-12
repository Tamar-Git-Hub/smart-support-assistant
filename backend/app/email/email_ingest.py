from imapclient import IMAPClient
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from dotenv import load_dotenv
import os
from app.db.database import SessionLocal
from app.models.ticket import Ticket
import logging
import time

load_dotenv()

HOST = os.getenv("EMAIL_HOST")
PORT = int(os.getenv("EMAIL_PORT", 993))
USER = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
MAILBOX = os.getenv("EMAIL_MAILBOX", "INBOX")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def decode_mime_words(s):
    if not s:
        return ""
    parts = decode_header(s)
    decoded = []
    for part, enc in parts:
        if isinstance(part, bytes):
            decoded.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            decoded.append(part)
    return "".join(decoded)

def get_email_text(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition"))
            if ctype == "text/plain" and "attachment" not in disp:
                return part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="replace")
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/html":
                html = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="replace")
                return html
    else:
        return msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="replace")
    return ""

def process_message(raw_message_bytes, session):
    msg = email.message_from_bytes(raw_message_bytes)
    subject = decode_mime_words(msg.get("Subject", "No subject"))
    from_ = decode_mime_words(msg.get("From", ""))
    message_id = msg.get("Message-ID")
    date = None
    try:
        date = parsedate_to_datetime(msg.get("Date"))
    except Exception:
        date = None

    body = get_email_text(msg)

    if message_id:
        found = session.query(Ticket).filter(Ticket.message_id == message_id).first()
        if found:
            logger.info("Skipping duplicate message_id: %s", message_id)
            return

    ticket = Ticket(
        subject=subject[:500],
        content=body,
        customer_email=from_,
        created_at=date,
        status="open",
        message_id=message_id
    )
    session.add(ticket)
    session.commit()
    logger.info("Created ticket id=%s for subject=%s", ticket.id, subject)

def fetch_unseen_and_process():
    with IMAPClient(HOST, port=PORT, use_uid=True, ssl=True) as client:
        client.login(USER, PASSWORD)
        client.select_folder(MAILBOX)
        messages = client.search(['UNSEEN'])
        logger.info("Found %d unseen messages", len(messages))
        if not messages:
            return

        response = client.fetch(messages, ['RFC822'])
        session = SessionLocal()
        try:
            for uid, data in response.items():
                raw = data[b'RFC822']
                try:
                    process_message(raw, session)
                    client.add_flags(uid, [b'\\Seen'])
                except Exception as e:
                    logger.exception("Error processing message uid=%s: %s", uid, e)
        finally:
            session.close()

if __name__ == "__main__":
    while True:
        try:
            fetch_unseen_and_process()
        except Exception as e:
            logger.exception("Inbox processing failed: %s", e)
        time.sleep(60)