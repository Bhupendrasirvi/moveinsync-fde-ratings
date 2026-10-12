# MoveInSync Play Store Ratings & Sentiment Engine
**Forward Deployed Engineer (FDE) Candidate Solution**

This repository contains the complete diagnostic report, engineering action plan, and reusable automation tool for the **MoveInSync Play Store Ratings Improvement Assignment**.

---

## Deliverables

1. **[Executive Recommendation](file:///C:/Users/bhupendra_sirvi/.gemini/antigravity/scratch/moveinsync-fde-ratings/executive_recommendation.md):** 
   - Root cause analysis across the 5 employee commute journey touchpoints.
   - Empirical findings from live Google Play Store telemetry (v12.18 to v12.20).
   - Prioritized engineering & product roadmap (P0 Next-Day Quick Wins, P1 Mobile Stability, P2 Algorithmic/Operational fixes).
   - The B2B2C Closed-Loop Feedback Interceptor strategy.

2. **[Methodology & Tools Note](file:///C:/Users/bhupendra_sirvi/.gemini/antigravity/scratch/moveinsync-fde-ratings/methodology_and_tools.md):**
   - Detailed write-up on data extraction, clustering heuristics, AI tools, and the "Ponytail" high-leverage engineering mindset.

3. **[Reusable CLI Tool (`moveinsync_ratings_pulse.py`)](file:///C:/Users/bhupendra_sirvi/.gemini/antigravity/scratch/moveinsync-fde-ratings/moveinsync_ratings_pulse.py):**
   - Reusable python tool to answer *"How are our Play Store ratings?"* on an ongoing basis.
   - Computes score velocity, isolates release version regressions, and flags journey-phase complaint spikes.

---

## Quickstart: Running the Diagnostic Engine

```bash
# 1. Install lightweight dependency
pip install google-play-scraper

# 2. Run on-demand diagnostic (analyzes latest 300 reviews)
python moveinsync_ratings_pulse.py --count 300

# 3. Output raw JSON for Slack webhook or CI/CD integration
python moveinsync_ratings_pulse.py --count 100 --json
```
