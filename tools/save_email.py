"""Save a sent email to MongoDB.

Each document has exactly these fields (plus MongoDB's automatic _id):
    company_name   the business the email is about
    date           when the email was sent (stored as a UTC datetime)
    header         the subject line
    content        the text of the attached PDF, as one string ("" if no PDF)
    email_content  the email body, as one string

Only text is stored. The PDF file itself is never copied anywhere; read it from
wherever it was generated (keep generated PDFs outside the repo, e.g. the system
temp folder).

Usage:
    python tools/save_email.py --company "Tata 1mg" --header "Subject line" \
        --email-content-file body.txt [--pdf-file report.pdf] \
        [--date 2026-09-20T09:00:00+05:30]

Environment (.env): MONGODB_URI (required), MONGODB_DB, MONGODB_COLLECTION,
REPORT_TIMEZONE (used when --date has no timezone).
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from pymongo import DESCENDING, MongoClient
from pymongo.errors import PyMongoError
from pypdf import PdfReader


def parse_date(value, tz_name):
    if not value:
        return datetime.now(timezone.utc)
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=ZoneInfo(tz_name))
    return parsed.astimezone(timezone.utc)


def pdf_text(path):
    text = "\n\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    # Bullet glyphs come out as control or private-use characters; make them plain dashes.
    return re.sub(r"[\x00-\x08\x0b-\x1f\x7f-]", "-", text).strip()


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Save a sent email to MongoDB.")
    parser.add_argument("--company", required=True)
    parser.add_argument("--header", required=True, help="the email subject line")
    parser.add_argument("--email-content-file", required=True, help="text file with the email body")
    parser.add_argument("--pdf-file", help="the attached PDF; its text is stored in `content`")
    parser.add_argument("--date", help="ISO date or datetime; defaults to now")
    args = parser.parse_args()

    uri = os.getenv("MONGODB_URI")
    if not uri:
        sys.exit("MONGODB_URI is not set. Add it to .env (see .env.example).")

    with open(args.email_content_file, encoding="utf-8") as f:
        email_content = f.read()
    if not email_content.strip():
        sys.exit(f"{args.email_content_file} is empty; refusing to save an empty email.")

    content = ""
    if args.pdf_file:
        content = pdf_text(args.pdf_file)
        if not content:
            sys.exit(f"No text could be extracted from {args.pdf_file}; refusing to save an empty `content`.")

    doc = {
        "company_name": args.company,
        "date": parse_date(args.date, os.getenv("REPORT_TIMEZONE", "Asia/Kolkata")),
        "header": args.header,
        "content": content,
        "email_content": email_content,
    }

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=8000)
        collection = client[os.getenv("MONGODB_DB", "clarix")][os.getenv("MONGODB_COLLECTION", "emails")]
        collection.create_index([("company_name", 1), ("date", DESCENDING)])
        result = collection.insert_one(doc)
    except PyMongoError as exc:
        sys.exit(f"MongoDB error: {exc}")

    print(json.dumps({"saved": True, "id": str(result.inserted_id), "company_name": doc["company_name"],
                      "date": doc["date"].isoformat(), "header": doc["header"],
                      "content_chars": len(content), "email_content_chars": len(email_content)}))


if __name__ == "__main__":
    main()
