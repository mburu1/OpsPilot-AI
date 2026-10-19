# Django Migrations and Seed Data

**Status:** proposed workflow for the intended Django backend.

Django models and committed migrations should be the source of truth for schema changes. Do not alter production schema manually and leave migration history inconsistent.

## Local workflow

Run from the directory containing manage.py with the virtual environment active and database settings configured.

    python manage.py showmigrations
    python manage.py makemigrations
    python manage.py sqlmigrate <app_label> <migration_number>
    python manage.py migrate
    python manage.py showmigrations

Replace placeholders with actual app and migration names. These commands assume Django is installed and database configuration is valid. Review generated migration operations before applying them.

## Review checklist
- Review migration operations, dependencies, defaults, and deletion behavior.
- Stage risky field additions or data transformations for safe rollout.
- Test lock behavior for indexes and constraints on representative table sizes.
- Keep data migrations deterministic and use Django's historical model registry.
- Preserve migration files already applied to shared environments.
- Test both a fresh install and an upgrade from the previous supported schema.
- Understand rollback behavior; some data transformations are not reversible.

## Seed data
Use data migrations for transformations that must travel with schema history. Use an explicit management command or idempotent fixture process for development/demo data. Never commit real customer data or credentials.

## Deployment sequence
1. Build and test the application artifact.
2. Back up the database before high-risk changes and confirm recovery procedures.
3. Run migrations as a controlled deployment step with one migration runner.
4. Verify migration state and application health.
5. Deploy compatible application code and monitor errors, locks, query latency, and background jobs.

For zero-downtime changes, consider expand-and-contract: add backward-compatible structures, deploy compatible code, backfill, switch reads/writes, then remove obsolete structures in a later release.

## Production safeguards
- Do not run makemigrations automatically during production startup.
- Do not use --fake to silence a mismatch without verifying schema and migration history.
- Do not delete migrations to repair a failed deployment.
- Do not run destructive migrations without review, a recovery plan, and a verified backup.
- Manage pgvector and other extension setup through reviewed procedures; confirm target database privileges.
