# WAT Framework Project

This workspace is set up around the WAT architecture:

- Workflows live in `workflows/` and describe the standard operating procedure for each task.
- Agents coordinate execution and decision-making.
- Tools live in `tools/` and perform the deterministic work.

## Structure

- `.tmp/` - disposable intermediate files
- `tools/` - Python scripts and utility executables
- `workflows/` - SOP markdown files
- `profiles/` - one business profile per business being monitored (copy `_template.md`)
- `.env.example` - template for local environment variables
- `.gitignore` - protects secrets and generated files
- `requirements.txt` - base Python dependencies

## Quick start

1. Copy `.env.example` to `.env` and fill in any required values.
2. Add or update workflow documents in `workflows/` for each job.
3. Build deterministic tools under `tools/` and keep them testable.
4. Treat anything in `.tmp/` as disposable output.

## Current workflow

- [workflows/01_competitor_intelligence_market_monitoring.md](workflows/01_competitor_intelligence_market_monitoring.md) lays out the business-wide competitor intelligence and market monitoring process for any company, including automation and data collection steps.

## Notes

- Do not commit real secrets.
- Prefer small, deterministic scripts over ad hoc logic.
- Keep workflow docs current as the system improves.
