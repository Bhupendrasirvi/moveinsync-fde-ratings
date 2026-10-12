#!/usr/bin/env python3
"""
MoveInSync Play Store Ratings & Sentiment Pulse
===============================================
A lightweight, recurring diagnostics engine designed for Forward Deployed Engineers (FDEs)
to continuously monitor Google Play Store ratings, detect version regressions, and isolate
root causes across the employee commute journey.

Ponytail Architecture:
- Single-file script with zero unnecessary dependencies.
- Uses `google-play-scraper` with stdlib `collections`, `json`, `datetime`, `re`.
- Fast, deterministic, and outputs human-readable markdown + JSON for CI/CD or Slack alerts.
"""

import sys
import json
import argparse
from datetime import datetime
from collections import Counter
try:
    from google_play_scraper import reviews, Sort, app
except ImportError:
    print("Error: google-play-scraper is required. Run: pip install google-play-scraper")
    sys.exit(1)

PACKAGE_NAME = "com.moveinsync.ets"

JOURNEY_CATEGORIES = {
    "Blocking In-App UX & Forced Rating Modals": [
        "rating", "rate", "skip", "popup", "seat belt", "click", "pop up", "annoying", "policy", "accept"
    ],
    "ETA Inaccuracy & GPS Tracking Lag": [
        "eta", "tracking", "track", "location", "live", "gps", "map", "delay", "late", "time", "inaccurate"
    ],
    "Suboptimal Routing & Detour Clustered Pickups": [
        "route", "routing", "detour", "round", "long distance", "darshan", "cab", "pilgrimage", "pickup", "drop"
    ],
    "Authentication, OTP & Session Logouts": [
        "otp", "login", "log in", "logout", "log out", "password", "register", "credential", "session", "verify"
    ],
    "App Crashes, Freezes & Update Regressions": [
        "crash", "update", "open", "uninstall", "reinstall", "stuck", "hang", "freeze", "white screen", "bug", "glitch"
    ],
    "Booking State Ambiguity & Phantom Notifications": [
        "notification", "booked", "booking", "schedule", "roster", "cancel", "waitlist", "push"
    ],
    "Driver Conduct & Operations Helpdesk Escalations": [
        "driver", "rude", "behaviour", "helpdesk", "support", "complaint", "ops", "transport desk"
    ]
}

def analyze_ratings(sample_size=300):
    print(f"[*] Fetching live metadata for {PACKAGE_NAME}...")
    app_info = app(PACKAGE_NAME)
    
    overall_score = app_info.get('score', 0.0)
    total_ratings = app_info.get('ratings', 0)
    histogram = app_info.get('histogram', [0, 0, 0, 0, 0])
    
    print(f"[*] Fetching {sample_size} most recent user reviews...")
    recent_reviews, _ = reviews(
        PACKAGE_NAME,
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=sample_size
    )

    score_dist = Counter([r['score'] for r in recent_reviews])
    low_star_reviews = [r for r in recent_reviews if r['score'] <= 2]
    critical_count = len(low_star_reviews)
    
    category_counts = Counter()
    version_counts = Counter()
    
    for r in low_star_reviews:
        text = (r['content'] or "").lower()
        v = r.get('reviewCreatedVersion') or "Unknown"
        version_counts[v] += 1
        
        matched_cats = [cat for cat, kws in JOURNEY_CATEGORIES.items() if any(k in text for k in kws)]
        if matched_cats:
            for cat in matched_cats:
                category_counts[cat] += 1
        else:
            category_counts["Uncategorized / General Negative"] += 1

    recent_avg = sum(r['score'] for r in recent_reviews) / len(recent_reviews) if recent_reviews else 0.0

    return {
        "timestamp": datetime.now().isoformat(),
        "overall": {
            "score": round(overall_score, 2),
            "total_ratings": total_ratings
        },
        "sample": {
            "size": len(recent_reviews),
            "recent_avg": round(recent_avg, 2),
            "critical_count": critical_count,
            "score_dist": dict(score_dist),
            "low_star_ratio": round(critical_count / len(recent_reviews) * 100, 1) if recent_reviews else 0.0
        },
        "category_breakdown": dict(category_counts.most_common()),
        "problem_versions": dict(version_counts.most_common(5))
    }

def print_cli_dashboard(data):
    print("\n" + "="*70)
    print(" MOVEINSYNC PLAY STORE RATINGS & JOURNEY DIAGNOSTICS")
    print("="*70)
    print(f"Snapshot Time   : {data['timestamp'][:19]}")
    print(f"Lifetime Rating : {data['overall']['score']} / 5.0  ({data['overall']['total_ratings']:,} ratings)")
    print(f"Recent Average  : {data['sample']['recent_avg']} / 5.0  (Sample: {data['sample']['size']} latest reviews)")
    print(f"Critical Rate   : {data['sample']['low_star_ratio']}% of recent reviews are 1 or 2 stars!")
    print("-" * 70)
    print(f"SCORE DISTRIBUTION (Recent {data['sample']['size']} reviews):")
    for stars in [5, 4, 3, 2, 1]:
        cnt = data['sample']['score_dist'].get(stars, 0)
        bar = "#" * int((cnt / data['sample']['size']) * 30)
        print(f"  {stars} Star : {cnt:3d} ({cnt/data['sample']['size']*100:4.1f}%) | {bar}")
    print("-" * 70)
    print("ROOT CAUSE BREAKDOWN IN LOW-STAR REVIEWS:")
    crit_total = data['sample']['critical_count']
    for cat, count in data['category_breakdown'].items():
        pct = (count / crit_total * 100) if crit_total else 0
        print(f"  - {cat:<48} : {count:2d} ({pct:4.1f}%)")
    print("-" * 70)
    print("TOP APPS/VERSIONS ATTRIBUTED TO CRITICAL FEEDBACK:")
    for ver, cnt in data['problem_versions'].items():
        print(f"  - Version {ver:<12} : {cnt} complaints")
    print("="*70 + "\n")

def main():
    parser = argparse.ArgumentParser(description="MoveInSync Play Store Sentiment Pulse")
    parser.add_argument("--count", type=int, default=300, help="Number of recent reviews to inspect")
    parser.add_argument("--json", action="store_true", help="Output pure JSON for downstream integrations")
    args = parser.parse_args()

    results = analyze_ratings(sample_size=args.count)
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_cli_dashboard(results)

if __name__ == "__main__":
    main()
