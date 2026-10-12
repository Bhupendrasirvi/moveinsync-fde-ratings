# Methodology & Tools Note
**Candidate Note for MoveInSync FDE Hiring Team**

---

### 1. Approach & Philosophy: The AI-First Forward Deployed Engineer

As a Forward Deployed Engineer (FDE), the objective is not to write a theoretical report or configure existing settings—it is to **understand the exact customer friction, build what is missing, and deliver a reusable capability that Product and Engineering can execute immediately**.

Following the **"Ponytail" engineering mindset** (YAGNI, minimal viable leverage, zero over-engineering, deletion before unnecessary addition):
1. **Never guess when public empirical data is accessible**: Instead of relying on generic assumptions, live review data was fetched and parsed directly from the Google Play Store for `com.moveinsync.ets`.
2. **Identify systemic causes, not just symptoms**: Separated surface complaints from root technical and UX mechanisms (e.g., discovering that the unskippable in-app rating modal was actively funneling frustrated users to the Play Store to leave 1-star reviews).
3. **Build the permanent answer, not just a one-time slide deck**: Built an automated, single-file diagnostic pipeline (`moveinsync_ratings_pulse.py`) with zero bloat that can be run anytime, answering *"How are our Play Store ratings?"* on an ongoing basis.

---

### 2. Tools & Stack Used

| Tool / Technology | Purpose | Key Details |
| :--- | :--- | :--- |
| **Python 3.11** | Core scripting & telemetry analysis | Fast, cross-platform execution with standard libraries. |
| **`google-play-scraper`** | Live Play Store data ingestion | Fetched app metadata, rating distribution histograms, and paginated user reviews sorted chronologically. |
| **`collections` & `re` (Stdlib)** | NLP semantic categorization & keyword mapping | Clustered raw review text into the 5 core employee commute journey touchpoints without heavy external ML dependencies. |
| **Windows CLI / PowerShell** | Local execution & encoding hardening | Hardened output for ASCII and UTF-8 cross-compatibility (fixing terminal cp1252 character maps). |
| **Markdown & Mermaid** | Deliverables & architecture diagrams | High-readability documentation ready for executive leadership, PMs, and engineering leads. |

---

### 3. Step-by-Step Discovery Process

1. **Reconnaissance & Metadata Ingestion:**
   - Identified MoveInSync’s primary employee application package: `com.moveinsync.ets`.
   - Extracted overall metrics: **4.32 / 5.0 lifetime score**, **114,879 ratings**, **13,570 1-star ratings (11.8%)**.

2. **Temporal Slice & Regression Isolation:**
   - Pulled the latest chronological reviews (v12.18.x to v12.20.x).
   - Uncovered that while historic rating is 4.32, **recent velocity dropped sharply to 3.73**, with **30.7% of all new reviews scoring <= 2 stars**.
   - Isolated version tag telemetry: Over **78% of recent technical complaints** traced directly to changes deployed in **v12.19.0**.

3. **Journey-Phase Qualitative Clustering:**
   - Classified low-star reviews into five distinct journey buckets:
     1. App Crashes & Update Loops (43.4%)
     2. ETA Inaccuracy & GPS Tracking Lag (26.1%)
     3. Suboptimal Routing & Detours (15.2%)
     4. Blocking In-App Rating Modals & OTP Interstitials (13.0%)
     5. Authentication & Ghost Notifications (13.0%)
     6. Operational & Driver Conduct (6.5%)

4. **Action Plan Formulation:**
   - Mapped fixes to an engineering impact-vs-effort matrix.
   - Identified P0 immediate fixes that can be merged and deployed in 48 hours to stop negative rating bleeding.
   - Formulated systemic product enhancements (closed-loop support routing, traffic-aware ETAs, smart Google In-App Review prompts).

5. **Automated Reusable Script (`moveinsync_ratings_pulse.py`):**
   - Packaged the entire scraping, scoring, version telemetry, and journey breakdown pipeline into a single, clean CLI script ready for daily CI/CD or Slack bot automation.
