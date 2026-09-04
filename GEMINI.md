# Repository Rules & Security Guardrails

## 🔒 Secret & Environment Variable Management

- **NEVER push, commit, or stage `.env` files** or any files containing private keys, access tokens, API keys, or credentials to the git repository.
- **Always verify `.env` is ignored by Git**: Ensure all `.env` files (including nested ones like `ge_api/stream_assist/.env`) remain ignored via `.gitignore`.
- **Only commit `.env.example` templates**: Only safe template files with placeholder values (e.g. `.env.example`) may be committed.
- **Pre-commit / Pre-push verification**: Always inspect `git status` and staged files before proposing or running `git add`, `git commit`, or `git push` to guarantee no sensitive files or secrets are included.
