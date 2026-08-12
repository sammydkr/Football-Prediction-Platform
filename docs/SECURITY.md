# Security Notes

This repository is demo-ready but still needs production hardening before handling real money or sensitive customer data.

## Implemented

- Passwords are hashed with Passlib bcrypt.
- Access tokens are short-lived JWTs.
- Refresh tokens are random, stored only as SHA-256 hashes, and rotated on every refresh.
- Protected routes use bearer authentication.
- Payment integration is abstracted behind a demo provider and does not collect card data.
- Secrets are configured through environment variables.

## Before Production

- Replace `SECRET_KEY` with a strong secret in each environment.
- Use TLS everywhere and set secure cookie policies if moving tokens into cookies.
- Add rate limiting on login, registration, and prediction creation.
- Integrate a real payment provider webhook verifier.
- Add row-level authorization rules for multi-tenant organizations.
- Configure structured audit logs and alerting for auth and billing events.
- Store refresh tokens with a keyed hash if token database exposure is in scope.

