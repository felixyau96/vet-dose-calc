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
- **Right:** result panels for each selected drug (stack on mobile); sticky **Copy lines** box with one line per drug and a Copy button. Tablet drugs with multiple `tabletStrengthMg` values show a strength picker: the closest mg match is auto-selected and marked **Best**, preferring whole tablets over halves/quarters (then fewer tabs); other strengths stay selectable and drive Give amount + copy lines. Drugs with `frequencyOptions` (length ≥ 2) show a **BID / SID** frequency picker; choosing frequency selects that option’s mg/kg (and prefills the desired-dose box) and re-runs Best tablet match. A desired-dose number box appears when the **top-level** formulary `dosePerKg` has min ≠ max **or** the effective band (after frequency) has min ≠ max — so liquid/paste/injectable range drugs (e.g. doxycycline 5–10) keep the box even when BID/SID is a point dose. Typed values clamp to the top-level band when it is a range; clearing the box falls back to the selected frequency option’s dose (else midpoint). Point-only top-level doses (e.g. maropitant 1 mg/kg) hide the box.
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
  "frequencyOptions": [
    { "freq": "BID", "dosePerKg": { "min": 5, "max": 5 } },
    { "freq": "SID", "dosePerKg": { "min": 10, "max": 10 } }
  ],
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
| `dosePerKg` | min/max per kg in `doseUnit`; set `null` when using `fixedTotal`. Top-level min ≠ max (labelled formulary band) shows a desired mg/kg (or mcg/kg) input even if a selected `frequencyOptions` entry is a point dose; clamp uses this band |
| `fixedTotal` | `{min,max,unit,note}` for fixed (not per-kg) totals |
| `concentrationMgPerMl` | always **mg/ml**. For mcg doses: volume = (dose_mcg / 1000) / concentration |
| `tabletStrengthMg` | tablet strengths in mg; UI auto-selects Best match by lowest mg error, then whole > half > quarter tabs, then fewer tablets (badge **Best**); other strengths stay selectable |
| `form` | optional `"tablet"` \| `"capsule"` \| `"injectable"` \| `"liquid"` — drives copy-line format |
| `frequency` | optional short label for copy lines, e.g. `"SID"`, `"BID"` (default selected when `frequencyOptions` present) |
| `frequencyOptions` | optional `[{freq, dosePerKg}]` for drugs with SID **or** BID and different mg/kg (e.g. doxycycline). UI shows BID/SID pills; default dose / volume / Best / copy use the selected option’s `dosePerKg` (user can override within the top-level labelled band). Keep top-level `dosePerKg` as the labelled band. Drugs without this field are unchanged. |
| `notes` | string (newlines / `•` / `-` lines) **or** `string[]` (preferred) — shown as bullets |
| `shortName` | optional clean name for copy lines; otherwise parentheticals are stripped from `name` |
| `source` | citation shown in the UI |

**Copy line formats**

- Tablet/capsule: `Name StrengthMg mg Ntab ROUTE FREQ` (e.g. `Maropitant 16mg 0.5tab PO SID`)
- Liquid/injectable: `Name Xmg/kg (volume mL) ROUTE FREQ` (e.g. `Maropitant 1mg/kg (0.4 mL) SC SID` for 4 kg at 10 mg/mL)

Calculator prefers `doseUnit` + `dosePerKg`; falls back to legacy `doseMgPerKg` / `doseMcgPerKg`.

After editing, refresh the browser.

## Disclaimer

Always visible: *Verify against your formulary. Not a substitute for clinical judgment.*
