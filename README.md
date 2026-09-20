# Bank Saathi

A smart banking assistance platform that helps customers understand forms, know what
documents to carry, catch mistakes before submitting, track requests, and get a
prototype branch queue token - while giving bank staff a dashboard that reduces
repeat visits and back-and-forth document requests.

This upgrade preserves the original guided, Hindi text-to-speech field-by-field
walkthrough (now at `/classic-walkthrough` in the frontend, and still served from
`/form-template`, `/explain`, `/validate` on the backend) and adds seven new features
on top of it.

## Project structure

```
bank-saathi/
  backend/            FastAPI application
    main.py           App entrypoint, routers, CORS, error handling
    config/           Environment-driven settings
    database/         MongoDB connection (Motor) with safe in-memory fallback
    schemas/          Pydantic request/response models
    services/         Business logic (framework-independent)
    routes/           Thin HTTP routers per feature
    data/             Configurable reference data (templates, checklists, branches)
    utils/            Shared helpers (ids, error formatting)
    requirements.txt
    .env.example
  frontend/           React (Vite) application
    src/
      api/client.js   Single place all backend calls go through
      context/        Lightweight customer identity (localStorage-backed)
      components/     Shared UI (layout, badges, loading/empty/error states)
      pages/          One page per feature
    package.json
    .env.example
```

## Features

1. **Form Scanner + Template Matching** - upload a form (PDF/text; images are
   honestly reported as "OCR not configured" rather than faking a result) or type
   values manually, and compare against a bank form template field-by-field.
2. **Simple Language Assistant** - paste formal banking text and get a plain-language
   explanation. Uses a rule-based fallback simplifier out of the box; wire in an AI
   provider via `AI_PROVIDER_API_KEY` later without changing the API contract.
3. **Document Checklist** - per-service checklist of documents to carry, with
   available/missing/not-applicable status per customer.
4. **Error Checker** - server-side validation (required fields, account number
   format, phone, email, PAN format, dates, repeated-field mismatches, consent,
   signature) with human-readable messages and suggestions.
5. **Status + Digital Receipt Vault** - create/track requests through
   submitted → pending → completed (or action_required/rejected), with a receipt
   number. Only minimal, non-sensitive data is stored.
6. **Branch Token / Appointment (prototype)** - generates a digital queue token
   per branch/service. Clearly marked as a prototype, not a real bank system.
7. **Employee Dashboard** - aggregated view of customer requests, missing
   documents, and validation alerts, to reduce repeat visits and document requests.
8. **English / Hindi / Hinglish language support** - a language switcher (sidebar,
   also in the mobile drawer) lets the customer pick English, हिंदी, or Hinglish.
   This isn't just a UI skin: form template names & field labels, checklist service
   & document names, error-checker messages/suggestions, the token disclaimer, and
   the Simple Language Assistant's fallback note are all translated **server-side**
   (see `backend/data/i18n.py`, `templates.py`, `checklists.py`, `branches.py`) via
   a `lang` query param/body field (`en` / `hi` / `hinglish`) that the frontend
   forwards on every relevant API call. The original `/classic-walkthrough` page
   keeps its own independent Hindi + text-to-speech experience, unchanged.

## Running locally

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # or your preferred env tool
pip install -r requirements.txt
cp .env.example .env   # fill in MONGODB_URI etc. if you have a MongoDB Atlas cluster
uvicorn main:app --reload --port 8000
```

If `MONGODB_URI` is left empty, the API automatically falls back to an in-memory
store so every feature still works end-to-end for local development/demo - just
without persistence across restarts. Set `MONGODB_URI` and `MONGODB_DB_NAME` to
use real MongoDB / MongoDB Atlas.

> Note: because the backend package uses `from backend.xxx import ...` imports,
> run uvicorn from the **project root** as `uvicorn backend.main:app --reload
> --port 8000`, or adjust to run directly inside `backend/` with
> `uvicorn main:app` after changing the imports to relative - the former is
> recommended and is what was tested.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # point VITE_API_URL at your backend if not localhost:8000
npm run dev
```

Then open the printed local URL (typically http://localhost:5173).

## Environment variables

**Backend** (`backend/.env`):
- `MONGODB_URI` - MongoDB / MongoDB Atlas connection string (optional; falls back to in-memory store if empty)
- `MONGODB_DB_NAME` - database name (default `bank_saathi`)
- `ALLOWED_ORIGINS` - comma-separated list of frontend origins allowed by CORS
- `AI_PROVIDER_API_KEY` / `AI_PROVIDER_MODEL` - optional, to enable AI-generated Simple Language explanations
- `MAX_UPLOAD_SIZE_MB` - form-scanner upload size limit (default 10)

**Frontend** (`frontend/.env`):
- `VITE_API_URL` - base URL of the backend API (default `http://localhost:8000`)

## Security notes

- No credentials are hard-coded anywhere; everything sensitive comes from
  environment variables (see `.env.example` files, never commit real `.env` files).
- The Status & Receipt Vault stores only the minimum necessary fields - no account
  numbers, documents, or balances.
- All form validation happens server-side (Error Checker), not just in the browser.
- Raw exceptions are never returned to the client; errors are logged server-side
  and a clean, generic message is returned instead.
