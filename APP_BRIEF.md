# App Brief: Athlete Performance Team Hub

*Working title: **Huddle***

## 1. Summary

An elite athlete works with a support team: a head coach, strength & conditioning coach, nutritionist, sports psychologist, physio, massage therapist, doctor, and sometimes an agent or manager. Right now that team coordinates through WhatsApp groups, emails, spreadsheets, and memory. Information gets lost, sessions clash, and one specialist often doesn't know what another has changed.

Huddle is a shared workspace built around the athlete. It gives every member of the performance team one calendar, one timeline of updates, and one current picture of the athlete's condition, so everyone works from the same information.

## 2. The Problem

- **Scattered communication.** Updates are spread across many chats and apps. Nobody has the full picture.
- **Scheduling conflicts.** A hard gym session gets booked the morning after a deep-tissue massage, or a nutrition consult clashes with travel.
- **Siloed decisions.** The physio flags a tight hamstring, but the coach still plans sprint work because the message never reached them.
- **Athlete overload.** The athlete ends up relaying information between specialists, which is extra mental load at the worst time.
- **No history.** When performance dips, it's hard to look back and see what changed in training, sleep, diet, or mood.

## 3. Goals

1. One source of truth for the athlete's schedule and status.
2. Fewer missed or conflicting sessions.
3. Every specialist sees the updates relevant to their work without extra effort.
4. Less coordination work for the athlete.
5. A searchable history of training, recovery, and wellbeing over time.

### Non-goals (v1)

- Replacing specialist tools such as GPS trackers, video analysis software, or medical record systems. Huddle integrates with them or links to them.
- Full team or club management for rosters of 50+ athletes. v1 focuses on an individual athlete and their personal team.
- Payments and invoicing between the athlete and practitioners.

## 4. Target Users

| Role | What they need |
|---|---|
| **Athlete** (hub owner) | See the day or week at a glance, log how they feel, avoid relaying messages, control who sees what |
| **Head Coach** | Plan the training block, see recovery and injury status before adjusting load |
| **S&C Coach** | Schedule gym sessions and see fatigue, soreness, and massage timing |
| **Nutritionist** | Know the training load and competition dates so fueling plans match, and share meal plans |
| **Sports Psychologist** | Track mood and stress trends and schedule sessions (with strict privacy on notes) |
| **Physio / Massage Therapist** | Log treatments, flag restrictions ("no high-impact for 48 hrs"), book recovery slots |
| **Doctor / Medical** | Record medical clearances and medication (restricted visibility) |
| **Manager / Agent** | See travel, competition, and media commitments that affect the schedule |

**Primary persona:** a professional or national-level individual-sport athlete (e.g. tennis, track, swimming, triathlon, golf) with 4–10 people in their support team.

## 5. Core Features (MVP)

### 5.1 Shared Performance Calendar
- One calendar covering training, recovery, treatment, nutrition, psychology, travel, competition, and media.
- Color-coded by discipline, with filters by role.
- Any team member can propose or book sessions. The athlete (or a delegate such as the head coach) can approve.
- **Conflict warnings:** flag clashes and rule breaks, e.g. "Heavy lower-body session within 12 hrs of deep-tissue massage" or "No session scheduled before race day."
- Sync with Google Calendar, Apple Calendar, and Outlook.

### 5.2 Athlete Status Board ("Today's Readiness")
- Daily check-in from the athlete in under 30 seconds: sleep, energy, soreness map, mood, stress, and optional notes.
- Active **flags and restrictions** from practitioners (e.g. "Left calf: avoid plyometrics until Thu").
- A simple readiness indicator (green / amber / red) visible to the whole team.
- Integrations (phase 2): WHOOP, Oura, Garmin, Apple Health, Polar for HRV, sleep, and load data.

### 5.3 Team Feed and Handoffs
- A timeline of session notes, updates, and flags, organized by athlete rather than by chat group.
- Structured post types: *Session Summary*, *Flag / Restriction*, *Plan Change*, *Question for Team*.
- @mention specific roles ("@Nutritionist: two sessions on Saturday, adjust fueling?").
- Read receipts on critical flags so the sender knows the coach has seen the injury note.

### 5.4 Plans and Programs
- Coaches publish training blocks (weeks or phases) that fill the calendar.
- Nutritionists attach meal plans or fueling guidance to specific days or sessions.
- Physios attach rehab protocols with exercises and progression.
- Every plan carries a version history showing who changed what and when.

### 5.5 Permissions and Privacy
- The athlete owns their data and controls access.
- Role-based visibility, e.g. psychology notes visible only to the psychologist and athlete, medical notes only to medical staff.
- Invite and remove team members easily, with access revoked immediately.
- Clear audit log of who viewed or edited sensitive records.

### 5.6 Notifications and Digest
- Smart notifications: only what's relevant to each role.
- A daily morning digest per team member: today's sessions, readiness status, new flags.
- A weekly summary for the athlete and head coach.

## 6. Future Features (post-MVP)

- **AI weekly insights:** summaries such as "Soreness has trended up over 3 weeks alongside increased volume" (advisory only, not medical advice).
- **Wearable and platform integrations:** TrainingPeaks, Catapult, Hudl, MyFitnessPal.
- **Competition mode:** travel itinerary, time-zone adjustment, and taper plans in one view.
- **Multi-athlete view** for coaches and practitioners who work with several athletes.
- **Document vault:** scans, blood work, contracts, and anti-doping (e.g. whereabouts) reminders.
- **Voice notes and quick video** for session feedback.
- **Offline mode** for training camps with poor connectivity.

## 7. Key User Flows

1. **Onboarding:** The athlete creates a hub, then invites team members by email or link and assigns each a role. Each member gets role-appropriate default permissions.
2. **Morning check-in:** The athlete completes the check-in, the readiness score updates, and the coach and S&C coach see it before the session.
3. **Flag an injury:** The physio logs a restriction. The coach and S&C coach get a priority alert, and affected calendar sessions are highlighted for review.
4. **Plan a training block:** The coach publishes a 4-week block. The nutritionist is notified and attaches fueling plans to the high-load days.
5. **Resolve a conflict:** The massage therapist books a session. The system warns about a clash with a heavy gym day, and the therapist picks a suggested alternative slot.

## 8. Platforms

- **Mobile first** (iOS and Android). The athlete and most practitioners use it on the go.
- **Web app** for coaches planning blocks and reviewing history on a larger screen.
- Real-time sync across devices.

## 9. Design Principles

- **Athlete-centered:** everything revolves around one person's performance.
- **Fast to use:** check-ins and session notes take seconds, not minutes.
- **Calm, not noisy:** fewer, better notifications. Critical items stand out.
- **Trust by default:** privacy controls are visible and easy to understand.
- **Glanceable:** today's status is readable in 3 seconds.

## 10. Data, Privacy and Compliance

- Health and wellbeing data is sensitive. Plan for **GDPR** and **HIPAA**-aligned handling, plus local equivalents depending on market.
- Encryption in transit and at rest.
- Athletes can export or delete all their data.
- Clear separation between medical or clinical data and general training data.
- No sharing of data with third parties (sponsors, federations) without explicit athlete consent.

## 11. Success Metrics

| Metric | Target (6 months post-launch) |
|---|---|
| Weekly active team members per athlete hub | ≥ 4 |
| Daily athlete check-in completion | ≥ 70% of days |
| Scheduling conflicts caught before they happen | Tracked and trending up |
| Self-reported "I know what the rest of the team is doing" (team survey) | ≥ 8/10 |
| Reduction in messages sent via external chat apps | Qualitative, via interviews |

## 12. Open Questions

1. Who pays: the athlete, the coach, an agency, or a federation? This shapes pricing and onboarding.
2. Should the athlete or the head coach be the default hub administrator?
3. How much should the app suggest or automate, versus simply showing information?
4. Which sports should the beta target? Individual sports are simpler than team sports.
5. Do we build conflict rules ourselves, or let each team define its own rules?
6. How do we handle practitioners who refuse to adopt a new app? (e.g. email-in updates, lightweight guest access)

## 13. Suggested MVP Scope and Phasing

**Phase 1 (MVP, ~3 months):** Shared calendar, athlete check-in, team feed with flags, role-based permissions, invites, notifications.

**Phase 2:** Plans and programs, conflict rules engine, calendar sync, daily digests, web app.

**Phase 3:** Wearable integrations, AI insights, competition mode, multi-athlete view.

## 14. Suggested Tech Considerations (for the build team)

- Cross-platform mobile: React Native or Flutter.
- Backend with real-time sync, e.g. Supabase or Firebase, or a custom Node or Postgres stack.
- Role-based access control designed in from the start, not bolted on later.
- Health-data-compliant hosting region options.
- Push notifications with priority tiers.
