# 🔒 Security Standards

## Authentication
- JWT in HTTP-only cookies
- Never use localStorage for tokens

## XSS Prevention
- Use DOMPurify
- Never custom regex sanitization

## Input Validation
- Use serializers/validators
- Never trust user input

## Tenant Isolation
- Check ownership on EVERY endpoint
