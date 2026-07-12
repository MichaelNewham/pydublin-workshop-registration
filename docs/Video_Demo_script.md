# Video Demo — script / shotlist (max 7 minutes)

> Target length: 5–6 minutes. Each shot has a suggested on-screen caption and
> what the presenter says. Record in one take per shot, then edit together.

## 0:00-0:30 - The problem (one presenter)

**On-screen:** Title card "PyCon Ireland 2026 - Event Registration System,
Option A." Then cut to the live home page:
https://pydublin-workshop-registration.onrender.com

**Say:** A 40-seat Python conference in Dublin needs a registration tool.
Today it's run on a spreadsheet sent by email - which causes overbooking,
duplicate sign-ups, and lost edits. We built a small web app with Python
+ Flask that solves all three.

## 0:30-1:00 - The stack (same presenter)

**On-screen:** Slides: "Python + Flask", "SQLAlchemy + SQLite",
"Jinja2 templates", "Auto-deployed to Render via git push".

**Say:** The brief asks for a small web app in Python, Flask, SQLite, HTML,
CSS, and JavaScript - exactly what we've been learning this semester.
We picked Flask + SQLAlchemy + Jinja2 because they cover all six required
techs in one stack. The whole project is a git repo - every commit
triggers CI on GitHub Actions, and every merge auto-deploys to a public
URL on Render.

## 1:00-2:00 - Walkthrough: attendee journey (presenter 2)

**On-screen:** Browser at https://pydublin-workshop-registration.onrender.com
- Home page.

**Say + do:**

1. Point at the event info - date, location, price, seats remaining.
2. Click **Register now** - show the form.
3. Fill name, email, phone, company. (Do **not** submit yet.)
4. Type in the notes box — point at the live character counter.

> Caption: "JS interaction #1: notes character counter"

## 2:00–2:45 — Submit + validation (presenter 2)

**On-screen:** Same form.

**Say + do:**

5. Submit — show the confirmation ref alert.
6. Try submitting the **same email again** — show the server-side error
   "already registered".

> Caption: "Server-side validation: no duplicates, no overbooking"

## 2:45-4:00 - Organiser journey (presenter 3)

**On-screen:** Home page, then `/login`.

**Say + do:**

7. Point out that **View participants is NOT in the public nav** - a deliberate design decision (the organiser screens are gated). Visit `/login`.
8. Enter the shared organiser password, sign in. Show the nav bar now shows **Participants** + **Sign out**.
9. Click **Participants** - show the list, the count, the repeating rows.
10. Click one row - show the Detail page.
11. Click **Edit** - change the company, **Save**.
12. Back to Detail - click **Cancel registration**. Confirm. Show the status
    flips to Cancelled and a Restore button appears.

> Caption: "Organiser gate (shared password) + soft-delete audit trail"

### 4:00-4:45 - JS char counter + responsive design (presenter 3)

**On-screen:** Register page (`/register`) on a narrow browser window.

**Say + do:**

13. Open `/register` and start typing a long note into the notes box - point at the live counter ticking down, then turning red past 280 chars.
14. Resize the window narrow - show the header reflows (CSS media query).

> Captions: "JavaScript interaction: live character counter" / "Basic responsive CSS"

## 4:45-5:30 - Under the hood (presenter 4)

**On-screen:** VS Code / GitHub showing the repo.

**Say:** Here's the file layout. [`event_registration/models.py`] declares the data layer - two tables (`Event` + `Registration`) with a foreign-key relationship. [`routes.py`] wires every URL route; the organiser-only ones are protected by the `@login_required` decorator in [`auth.py`]. All the business logic - capacity checks, duplicate-email checks, cancel/restore - lives in `routes.py`. The JavaScript interaction is in [`static/js/app.js`] - a live character counter, pure vanilla JS, no libraries.

## 5:30–6:30 — Who did what (all four, one line each)

**On-screen:** Table from `docs/Individual_Contribution.csv`.

- **Michael Newham (261012020, Block A):** database schema + server functions + validation.
- **Sergiu D (261024894, Block B):** the five client Forms + form logic + navigation.
- **Paul Sealy (261018041, Block C):** theme - HTML shell + CSS + the JS interaction.
- **Alessandro Genco (262016773, Block D):** docs + test log + report + this video + git integration.

## 6:30–7:00 — Limitations & wrap

**Say:** We did not implement auth — it's on the future-work list. But the
core flow works end-to-end and is fully covered by our manual test log. Thanks
for watching.

---

## Recording checklist

- [ ] Use a 1280x720 or higher screen recording tool (OBS, Loom, QuickTime).
- [ ] Mute Slack / notifications before recording.
- [ ] Increase browser zoom to ~110% so text is readable.
- [ ] Use the **Chrome Anvil IDE** for any live editing shots - looks better
      than the local Docker view.
      (Edit after the pivot: shoot the live Render URL instead, in a normal
      browser tab - https://pydublin-workshop-registration.onrender.com)
- [ ] Speakers: **Michael Newham (261012020), Sergiu D (261024894), Paul Sealy (261018041), Alessandro Genco (262016773)**
      (watermark each shot with the speaker's name).
- [ ] Export at 1080p, MP4, H.264.
