# TODO for Implementing Separate Reports & OEE Enhancements

## 1. API Endpoints (app/api/routes/reports.py)
- [x] Add separate CSV/PDF endpoints for availability, MTBF, performance, quality metrics.
- [x] Endpoints: /availability.csv, /availability.pdf, /mtbf.csv, /mtbf.pdf, /performance.csv, /performance.pdf, /quality.csv, /quality.pdf.

## 2. Service Layer (app/services/oee_service.py)
- No changes needed; reuse existing compute functions.

## 3. Scheduled Reports (app/services/scheduler.py)
- Optional: Add support for scheduling individual metrics (skipped for now to avoid complexity).

## 4. Testing (tests/test_reports.py)
- [x] Add tests for new CSV/PDF endpoints.
- Note: Tests require PostgreSQL database running (via docker-compose up db). If Docker is not available, tests will fail with connection errors.

## Follow-up Steps
- Run critical-path tests to verify functionality.
- Provide usage documentation for new endpoints.
