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
- **Right:** result panels for each selected drug (stack on mobile); sticky **Copy lines** box with one line per drug and a Copy button. Tablet drugs with multiple `tabletStrengthMg` values show a strength picker: the closest mg match is auto-selected and marked **Best**, preferring whole tablets over halves/quarters (then fewer tabs); other strengths stay selectable and drive Give amount + copy lines. Drugs with `frequencyOptions` (length ≥ 2) show a **BID / SID** frequency picker; choosing frequency selects that option’s mg/kg (and prefills the desired-dose box on liquid/paste/injectable forms) and re-runs Best tablet match. A desired-dose number box appears for **liquid / injectable / paste only** (not tablet/capsule) when the **top-level** formulary `dosePerKg` has min ≠ max **or** the effective band (after frequency) has min ≠ max — e.g. doxycycline paste 5–10 keeps the box even when BID/SID is a point dose; doxycycline tablets keep Best strength only (no dose box). The box is a text field (`inputMode=decimal`) that keeps a raw draft while typing so intermediate values like `7.` / `7.2` are not snapped away; it accepts/displays up to **2 decimal places**. Complete numbers update volume live; blur/Enter clamps to the top-level band when it is a range; clearing the box falls back to the selected frequency option’s dose (else midpoint). Point-only top-level doses (e.g. maropitant 1 mg/kg) hide the box. Volume (Give card + copy-line mL): **&lt; 1 mL** up to 2 d.p.; **≥ 1 mL** up to 1 d.p. (trailing zeros trimmed).
- **Days to supply / Quantity required:** each result card has a **Days to supply** number box (integer ≥ 1; blank = no quantity) and a read-only **Quantity required** readout. Formula: Give amount × doses/day × days. Doses/day maps clear frequency only — SID→1, BID→2, TID→3, QID→4, EOD→0.5; otherwise quantity shows “—” with hint “set frequency”. Tablets/capsules: `tabs_per_dose × doses/day × days`, then **Math.ceil** to a whole tab count (e.g. 1 tab BID × 7d → **14 tab**); liquids/injectables: total mL then `fmtVolMl` (e.g. 0.5 mL BID × 7d → **7 mL**; 0.4 mL SID × 5d → **2 mL**). Missing weight or Give → “—”. Course quantity stays on the card only — copy lines do **not** append `→ tabs/mL`.
- **Taper schedule** (`supportsTaper: true` only): when results are shown, the card replaces Days to supply with a **Taper schedule** block (Add phase / Remove phase). Default: one phase prefilled from current Give mg/kg + selected frequency. Each phase: mg/kg · frequency (SID/BID/EOD) · days · per-dose tabs/mL. **Quantity required** = sum of phase quantities (ceil tabs once on the sum). UX: one phase with days ≡ simple Days to supply; add phases for a multi-step taper. Drugs without the flag are unchanged (Days to supply only).
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
  "supportsTaper": false,
  "notes": ["Bullet one", "Bullet two"],
  "source": "Exact citation",
  "sourceChecked": "2026-10-18"
}
```

| Field | Notes |
|-------|--------|
| `doseUnit` | `"mg"`, `"mcg"`, or `"U"` (units) |
| `dosePerKg` | min/max per kg in `doseUnit`; set `null` when using `fixedTotal`. Top-level min ≠ max (labelled formulary band) shows a desired mg/kg (or mcg/kg) input on **liquid/injectable/paste** forms only (never tablets/capsules), even if a selected `frequencyOptions` entry is a point dose; clamp uses this band; input up to 2 d.p. |
| `fixedTotal` | `{min,max,unit,note}` for fixed (not per-kg) totals |
| `concentrationMgPerMl` | always **mg/ml**. For mcg doses: volume = (dose_mcg / 1000) / concentration |
| `tabletStrengthMg` | tablet strengths in mg; UI auto-selects Best match by lowest mg error, then whole > half > quarter tabs, then fewer tablets (badge **Best**); other strengths stay selectable |
| `form` | optional `"tablet"` \| `"capsule"` \| `"injectable"` \| `"liquid"` — drives copy-line format |
| `frequency` | optional short label for copy lines, e.g. `"SID"`, `"BID"` (default selected when `frequencyOptions` present) |
| `frequencyOptions` | optional `[{freq, dosePerKg}]` for drugs with SID **or** BID and different mg/kg (e.g. doxycycline). UI shows BID/SID pills; default dose / volume / Best / copy use the selected option’s `dosePerKg` (user can override within the top-level labelled band). Keep top-level `dosePerKg` as the labelled band. Drugs without this field are unchanged. |
| `supportsTaper` | optional boolean. When `true`, result cards show a **Taper schedule** (phase rows) instead of Days to supply; Quantity sums phases; copy becomes multi-line when ≥2 phases or any phase has days. Omit or `false` for no behaviour change. Enable when publishing a tapering drug (e.g. prednisolone). |
| `indicationOptions` | optional `[{id, label, dosePerKg, frequencyChoices?}]`. UI shows indication pills (default = `defaultIndication` or first). Selected option supplies the labelled mg/kg band. Use for anti-inflammatory vs immunosuppressive (prednisolone). |
| `defaultIndication` | optional id matching an `indicationOptions[].id` (e.g. `"anti-inflammatory"`). |
| `dosePerKgIsDailyTotal` | optional boolean. When `true`, `dosePerKg` is **total daily** mg/kg; BID divides that same total across 2 doses (does **not** double like doxycycline’s separate BID/SID bands). SID/EOD use the full daily per dose on dosing days. |
| `notes` | string (newlines / `•` / `-` lines) **or** `string[]` (preferred) — shown as bullets |
| `shortName` | optional clean name for copy lines; otherwise parentheticals are stripped from `name` |
| `source` | citation shown in the UI |

**Copy line formats**

- Tablet/capsule: `Name StrengthMg mg Ntab ROUTE FREQ` (e.g. `Maropitant 16mg 0.5tab PO SID`) — no course-quantity suffix
- Liquid/injectable: `Name Xmg/kg (volume mL) ROUTE FREQ` (e.g. `Maropitant 1mg/kg (0.4 mL) SC SID` for 4 kg at 10 mg/mL). Volume decimals: &lt;1 mL up to 2 d.p.; ≥1 mL up to 1 d.p.
- Taper (`supportsTaper`, when ≥2 phases or any phase has days): one line per phase — `Name X mg/kg (N tab) ROUTE FREQ × Nd` (final tab count in parens; phase days only, no `→ qty` suffix). Example:
  - `Prednisolone 1 mg/kg (1 tab) PO SID × 5d`
  - `Prednisolone 0.5 mg/kg (0.5 tab) PO SID × 5d`

Calculator prefers `doseUnit` + `dosePerKg`; falls back to legacy `doseMgPerKg` / `doseMcgPerKg`.

After editing, refresh the browser.

## Disclaimer

Always visible: *Verify against your formulary. Not a substitute for clinical judgment.*
