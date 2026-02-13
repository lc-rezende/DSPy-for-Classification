from __future__ import annotations

import csv
import json
import os
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ChurnRecord:
    customer_id: str
    site_id: str
    year_month: str
    risk_category: str
    probability: str


def load_records(path: Path) -> list[ChurnRecord]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        records: list[ChurnRecord] = []
        for row in reader:
            records.append(
                ChurnRecord(
                    customer_id=(row.get("customer_id") or "").strip(),
                    site_id=(row.get("site_id") or "").strip(),
                    year_month=(row.get("year_month") or "").strip(),
                    risk_category=(row.get("risk_category") or "").strip(),
                    probability=(row.get("probability") or "").strip(),
                )
            )
        return records


def is_high_risk(record: ChurnRecord) -> bool:
    return record.risk_category.strip().lower() == "high"


def build_message(record: ChurnRecord) -> str:
    return (
        "High churn risk detected: "
        f"customer_id={record.customer_id}, "
        f"site_id={record.site_id}, "
        f"year_month={record.year_month}, "
        f"risk_category={record.risk_category}, "
        f"probability={record.probability}"
    )


def post_to_slack(webhook_url: str, channel: str | None, message: str) -> None:
    payload: dict[str, str] = {"text": message}
    if channel:
        payload["channel"] = channel

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        status = response.getcode()
        if status < 200 or status >= 300:
            raise RuntimeError(f"Slack webhook returned status {status}")


def main() -> int:
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("Missing SLACK_WEBHOOK_URL env var.", file=sys.stderr)
        return 1

    channel = os.getenv("SLACK_CHANNEL")
    path = Path("data/trusted/fact_churn_risk.csv")
    if not path.exists():
        print(f"Missing CSV file: {path}", file=sys.stderr)
        return 1

    records = load_records(path)
    high_risk = [record for record in records if is_high_risk(record)]

    if not high_risk:
        print("No high-risk records found.")
        return 0

    for record in high_risk:
        message = build_message(record)
        post_to_slack(webhook_url, channel, message)

    print(f"Sent {len(high_risk)} Slack notification(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
