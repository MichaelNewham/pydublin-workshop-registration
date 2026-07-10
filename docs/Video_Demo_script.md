# Video Demo — script / shotlist (max 7 minutes)

> Target length: 5–6 minutes. Each shot has a suggested on-screen caption and
> what the presenter says. Record in one take per shot, then edit together.

## 0:00–0:30 — The problem (one presenter)

**On-screen:** Title card "PyDublin Workshop 2026 — Event Registration System,
Option B."

**Say:** A 40-seat Python workshop in Dublin needs a registration tool. Today
it's run on a spreadsheet sent by email — which causes overbooking, duplicate
sign-ups, and lost edits. We built a small low-code app with **Anvil** that
solves all three.

## 0:30–1:00 — The stack (same presenter)

**On-screen:** Slides: Anvil logo, "Pure Python FE + BE", "SQLite via Data
Tables", "Open-source standalone server".

**Say:** The brief asked for a low-code app from Week 10. We picked **Anvil**
because it's the only platform that uses Python on both front-end and back-end,
which fits what we've been learning all semester. The whole project is a
git repo — Python Forms, YAML config, HTML/CSS theme.

## 1:00–2:00 — Walkthrough: attendee journey (presenter 2)

**On-screen:** Browser at http://localhost:3030 — Home page.

**Say + do:**

1. Point at the event info — date, location, price, seats remaining.
2. Click **Register now** — show the form.
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

## 2:45–4:00 — Organiser journey (presenter 3)

**On-screen:** Home → Participants → click a row.

**Say + do:**

7. Click **View participants** — show the list, the count, the repeating rows.
8. Click one row — show the Detail page.
9. Click **Edit** — change the company, **Save**.
10. Back to Detail — click **Cancel registration**. Confirm. Show the status
    flips to Cancelled and a Restore button appears.

> Caption: "Soft-delete preserves the audit trail"

## 4:00–4:45 — JS clipboard + responsive design (presenter 3)

**On-screen:** Home page on a narrow browser window.

**Say + do:**

11. Click **Copy event ref to clipboard** — paste into a text editor to prove it.
12. Resize the window narrow — show the header reflows (CSS media query).

> Captions: "JS interaction #2: clipboard" / "Basic responsive CSS"

## 4:45–5:30 — Under the hood (presenter 4)

**On-screen:** VS Code / GitHub showing the repo.

**Say:** Here's the file layout. [`event_registration/anvil.yaml`] declares the
database — two tables, one Related, with a liveObject link. This is where the
required JS interaction is wired in too. All the business logic — capacity
checks, duplicate-email checks, cancel/restore — lives in
[`server_code/ServerModule1.py`].

## 5:30–6:30 — Who did what (all four, one line each)

**On-screen:** Table from `docs/Individual_Contribution.csv`.

- **Michael Newham (Block A):** database schema + server functions + validation.
- **Sergiu D (Block B):** the five client Forms + form logic + navigation.
- **Paul Sealy (Block C):** theme - HTML shell + CSS + the JS interaction.
- **Alessandro Genco (Block D):** docs + test log + report + this video + git integration.

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
- [ ] Speakers: **Michael Newham, Sergiu D, Paul Sealy, Alessandro Genco**
      (watermark each shot with the speaker's name).
- [ ] Export at 1080p, MP4, H.264.
