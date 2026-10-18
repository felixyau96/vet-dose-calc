# Veterinary Drug-Dosing Calculator

Mobile-friendly, client-side dose calculator for small animal practice (dog/cat).
All maths come from `drugs.json` — the app never invents doses.

**Owner of formulary updates:** Dose bot (updates `drugs.json` only).
**Do not invent drug entries** — wait for Dose to add the hospital list.

## URLs

- Local: `http://127.0.0.1:8787/`
- LAN / Tailscale: `http://<host-or-tailscale-ip>:8787/`
- Public Pages: https://felixyau96.github.io/vet-dose-calc/

## Running the server

```bash
cd /workspace/dose-calc
python3 server.py
# or: DOSE_CALC_PORT=8787 python3 server.py
```

Binds `0.0.0.0:8787` (override with `DOSE_CALC_PORT`). Serves this directory as static files.

## UI

- **Left:** species, weight (kg), search, multi-select checklist of medications.
- **Right:** result panels for each selected drug (stack on mobile); sticky **Copy lines** box with one line per drug and a Copy button.
- Notes render as a bullet list (`notes` string or `string[]`).

## Formulary file

```json
{ "drugs": [ /* … */ ] }
```

## Schema (each drug)

```json
{
  "id": "example",
  "name": "Example Drug",
  "shortName": "Example",
  "brandNames": ["Brand A"],
  "species": ["dog", "cat"],
  "routes": ["IV", "IM", "SC", "PO"],
  "form": "tablet",
  "frequency": "SID",
  "doseUnit": "mg",
  "dosePerKg": { "min": 1, "max": 2 },
  "fixedTotal": null,
  "concentrationMgPerMl": 10,
  "tabletStrengthMg": [5, 10],
  "notes": ["Bullet one", "Bullet two"],
  "source": "Exact citation",
  "sourceChecked": "2026-10-18"
}
```

| Field | Notes |
|-------|--------|
| `doseUnit` | `"mg"`, `"mcg"`, or `"U"` (units) |
| `dosePerKg` | min/max per kg in `doseUnit`; set `null` when using `fixedTotal` |
| `fixedTotal` | `{min,max,unit,note}` for fixed (not per-kg) totals |
| `concentrationMgPerMl` | always **mg/ml**. For mcg doses: volume = (dose_mcg / 1000) / concentration |
| `tabletStrengthMg` | tablet strengths in mg; UI suggests nearest whole/half tablets |
| `form` | optional `"tablet"` \| `"capsule"` \| `"injectable"` \| `"liquid"` — drives copy-line format |
| `frequency` | optional short label for copy lines, e.g. `"SID"`, `"BID"` |
| `notes` | string (newlines / `•` / `-` lines) **or** `string[]` (preferred) — shown as bullets |
| `shortName` | optional clean name for copy lines; otherwise parentheticals are stripped from `name` |
| `source` | citation shown in the UI |

**Copy line formats**

- Tablet/capsule: `Name StrengthMg mg Ntab ROUTE FREQ` (e.g. `Maropitant 16mg 0.5tab PO SID`)
- Liquid/injectable: `Name Xmg/kg ROUTE FREQ` (e.g. `Maropitant 1mg/kg SC SID`)

Calculator prefers `doseUnit` + `dosePerKg`; falls back to legacy `doseMgPerKg` / `doseMcgPerKg`.

After editing, refresh the browser.

## Disclaimer

Always visible: *Verify against your formulary. Not a substitute for clinical judgment.*
