"""Save a sent email to MongoDB.

Each document has exactly these fields (plus MongoDB's automatic _id):
    company_name  the business the email is about
    date          when the email was sent (stored as a UTC datetime)
    header        the subject line
    content       the full email body as one string

Usage:
    python tools/save_email.py --company "Tata 1mg" --header "Subject line" \
        --content-file path/to/body.txt [--date 2026-09-20T09:00:00+05:30]

Environment (.env): MONGODB_URI (required), MONGODB_DB, MONGODB_COLLECTION,
REPORT_TIMEZONE (used when --date has no timezone).
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from pymongo import DESCENDING, MongoClient
from pymongo.errors import PyMongoError


def parse_date(value, tz_name):
    if not value:
        return datetime.now(timezone.utc)
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=ZoneInfo(tz_name))
    return parsed.astimezone(timezone.utc)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Save a sent email to MongoDB.")
    parser.add_argument("--company", required=True)
    parser.add_argument("--header", required=True)
    parser.add_argument("--content-file", required=True)
    parser.add_argument("--date", help="ISO date or datetime; defaults to now")
    args = parser.parse_args()

    uri = os.getenv("MONGODB_URI")
    if not uri:
        sys.exit("MONGODB_URI is not set. Add it to .env (see .env.example).")

    with open(args.content_file, encoding="utf-8") as f:
        content = f.read()
    if not content.strip():
        sys.exit(f"{args.content_file} is empty; refusing to save an empty email.")

    doc = {
        "company_name": args.company,
        "date": parse_date(args.date, os.getenv("REPORT_TIMEZONE", "Asia/Kolkata")),
        "header": args.header,
        "content": content,
    }

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=8000)
        collection = client[os.getenv("MONGODB_DB", "clarix")][os.getenv("MONGODB_COLLECTION", "emails")]
        collection.create_index([("company_name", 1), ("date", DESCENDING)])
        result = collection.insert_one(doc)
    except PyMongoError as exc:
        sys.exit(f"MongoDB error: {exc}")

    print(json.dumps({"saved": True, "id": str(result.inserted_id), "company_name": doc["company_name"],
                      "date": doc["date"].isoformat(), "header": doc["header"]}))


if __name__ == "__main__":
    main()
