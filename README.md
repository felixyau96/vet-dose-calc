# Veterinary Drug-Dosing Calculator

Mobile-friendly, client-side dose calculator for small animal practice (dog/cat).
All maths come from `drugs.json` — the app never invents doses.

**Owner of formulary updates:** Dose bot (updates `drugs.json` only).
**Do not invent drug entries** — wait for Dose to add the hospital list.

## URLs

- Local: `http://127.0.0.1:8787/`
- LAN / Tailscale: `http://<host-or-tailscale-ip>:8787/`

## Running the server

```bash
cd /workspace/dose-calc
python3 server.py
# or: DOSE_CALC_PORT=8787 python3 server.py
```

Binds `0.0.0.0:8787` (override with `DOSE_CALC_PORT`). Serves this directory as static files.

## Formulary file

Live `drugs.json` must be:

```json
{ "drugs": [] }
```

## Schema (each drug)

```json
{
  "id": "example",
  "name": "Example Drug",
  "brandNames": ["Brand A"],
  "species": ["dog", "cat"],
  "routes": ["iv", "im", "sc", "po"],
  "doseUnit": "mg",
  "dosePerKg": { "min": 1, "max": 2 },
  "concentrationMgPerMl": 10,
  "tabletStrengthMg": [5, 10],
  "notes": "Optional clinical notes",
  "source": "Exact citation, e.g. Plumb's 10th ed. p.123",
  "sourceChecked": "2026-10-18"
}
```

| Field | Notes |
|-------|--------|
| `doseUnit` | `"mg"` or `"mcg"` only |
| `dosePerKg` | min/max per kg in `doseUnit` |
| `concentrationMgPerMl` | always **mg/ml**. For mcg doses: volume = (dose_mcg / 1000) / concentration |
| `tabletStrengthMg` | tablet strengths in mg; UI suggests nearest whole/half tablets |
| `source` | citation shown in the UI |

After editing, refresh the browser.

## Disclaimer

Always visible: *Verify against your formulary. Not a substitute for clinical judgment.*
