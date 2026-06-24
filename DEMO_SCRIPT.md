# Demo Video Script (~90 seconds)

**Goal:** Show the complete flow end-to-end. Keep each section crisp.

---

## Opening (5s)
"Hi, I'm Brendan Lee. This is my Full-Stack submission for the PM Accelerator AI Engineer Intern assessment — an AI-powered Weather Travel Advisor."

---

## Weather Search — text input (15s)
1. Type "Tokyo, Japan" in the search bar → hit Search.
2. Show the **current weather card**: temperature, feels-like, humidity, wind speed, **AQI badge** (Air Quality Index — second API).
3. Point to the **5-day forecast grid**: icons change per condition, min/max, precipitation.

"The app resolves any free-text location — city, zip code, landmark, or GPS coordinates."

---

## Current Location (10s)
4. Click the GPS button. Browser asks for permission — allow.
5. Weather updates to user's current location automatically.

---

## AI Travel Advisor (20s)
6. Click **"Get Travel Advice"** on the advice panel.
7. Wait ~3s for NVIDIA NIM response.
8. Show the **Clothing / Packing / Activities / Travel Tips / Warnings** sections.

"The AI uses both the weather and the Air Quality Index to generate context-aware advice — not just 'bring a jacket', but specific, actionable recommendations."

---

## Save a Search + History (20s)
9. Fill the **Save Search** form: location pre-filled, pick a date range → Save.
10. Click **History** in the nav.
11. Show the table with the saved row.
12. Click the **edit pencil** → update the location → Save changes.
13. Show the row updated.
14. Click the **delete trash icon** → row removed.

---

## Export (10s)
15. Back on the History page, click the **CSV** button — file downloads.
16. Quickly show JSON and MD buttons.

"All three export formats are live backend endpoints, not frontend file generation."

---

## Code Walk (10s)
17. Briefly show repo structure in terminal or editor:
    - `backend/app/` — FastAPI + SQLAlchemy + Alembic
    - `frontend/src/features/` — feature-sliced components
    - `docs/` — API contract and architecture

---

## Closing (5s)
"Full-stack submission: both Tech Assessment #1 and #2 complete.
Backend tests pass with pytest, frontend tests pass with Vitest.
Full setup instructions are in the README. Thank you!"
