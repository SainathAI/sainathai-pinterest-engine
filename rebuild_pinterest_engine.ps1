Write-Host "Rebuilding SainathAI Pinterest Engine (Stable Snapshot)..."

# Base path
$BASE = "engine_runner"

# Clean old structure if exists
if (Test-Path $BASE) {
    Remove-Item -Recurse -Force $BASE
}

# Create directories
New-Item -ItemType Directory -Path `
    $BASE,
    "$BASE\jobs\high",
    "$BASE\jobs\medium",
    "$BASE\jobs\low",
    "$BASE\exports\high",
    "$BASE\exports\medium",
    "$BASE\exports\low" | Out-Null

# -------------------------
# pin_executor.py
# -------------------------
@'
import argparse
import os
import json
import csv
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--tier", choices=["high", "medium", "low"])
parser.add_argument("--limit", type=int)
args = parser.parse_args()

BASE = os.path.dirname(__file__)
JOBS_DIR = os.path.join(BASE, "jobs")
EXPORTS_DIR = os.path.join(BASE, "exports")
TIERS = ["high", "medium", "low"]

def ok(job_id):
    print(f"EXPORTED | {job_id}")

def fail(job_id, reason):
    print(f"FAILED | {job_id} | {reason}")

def validate(job):
    for k in ["seo", "pin", "monetization"]:
        if k not in job:
            raise Exception(f"missing_{k}")

    m = job["monetization"]
    if not m.get("destination_url"):
        raise Exception("missing_destination_url")
    if not m.get("cta"):
        raise Exception("missing_cta")
    if not m.get("tier"):
        raise Exception("missing_tier")

def export_job(job, tier):
    job_id = job["job_id"]
    seo = job["seo"]
    pin = job["pin"]
    m = job["monetization"]

    out_dir = os.path.join(EXPORTS_DIR, tier)
    os.makedirs(out_dir, exist_ok=True)

    payload = {
        "title": seo["title"][:100],
        "description": (seo["description"] + " " + " ".join(seo.get("hashtags", [])))[:500],
        "board": pin["board_name"],
        "image_path": pin["image_path"],
        "destination_url": m["destination_url"] +
            "?utm_source=pinterest&utm_campaign=" + tier +
            "&utm_content=" + job_id,
        "cta": m["cta"],
        "tier": tier,
        "exported_at": datetime.utcnow().isoformat()
    }

    with open(os.path.join(out_dir, f"{job_id}.json"), "w", encoding="utf-8") as jf:
        json.dump(payload, jf, indent=2)

    with open(os.path.join(out_dir, f"{job_id}.csv"), "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=payload.keys())
        writer.writeheader()
        writer.writerow(payload)

tiers = [args.tier] if args.tier else TIERS

for tier in tiers:
    tier_dir = os.path.join(JOBS_DIR, tier)
    if not os.path.isdir(tier_dir):
        continue

    count = 0
    for fn in sorted(os.listdir(tier_dir)):
        if not fn.endswith(".json"):
            continue

        try:
            with open(os.path.join(tier_dir, fn), "r", encoding="utf-8") as f:
                job = json.load(f)

            validate(job)
            export_job(job, tier)
            ok(job["job_id"])

            count += 1
            if args.limit and count >= args.limit:
                break

        except Exception as e:
            fail(job.get("job_id", "unknown"), str(e))
'@ | Set-Content "$BASE\pin_executor.py"

# -------------------------
# README.md
# -------------------------
@'
SainathAI Pinterest Engine (Stable)

Purpose:
- Generate monetized, SEO-optimized Pinterest pins
- Export scheduler-ready assets (CSV + JSON)
- NO UI automation
- NO Playwright
- SAFE for production

Run:
python pin_executor.py
python pin_executor.py --tier high --limit 5

Output:
engine_runner/exports/
'@ | Set-Content "$BASE\README.md"

Write-Host "Rebuild complete. Engine is stable and production-ready."
