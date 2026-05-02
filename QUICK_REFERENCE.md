# Quick Command Reference

## Getting Started

```bash
# First time setup
bun install
bun x husky install

# Start development
bun run dev

# Setup backend
cd apps/api && python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r ../requirements.txt
```

## Daily Commands

| Command          | Purpose               |
| ---------------- | --------------------- |
| `bun run dev`    | Start all dev servers |
| `bun run build`  | Build all apps        |
| `bun run test`   | Run all tests         |
| `bun run lint`   | Check code style      |
| `bun run format` | Format code           |

## Testing

| Command                 | Purpose           |
| ----------------------- | ----------------- |
| `bun run test:frontend` | Jest tests only   |
| `bun run test:backend`  | Pytest tests only |
| `bun run test:watch`    | Watch mode        |
| `bun run test:coverage` | Coverage report   |

## Code Quality

| Command               | Purpose          |
| --------------------- | ---------------- |
| `bun run lint`        | Run all linters  |
| `bun run format`      | Auto-format code |
| `bun run check-types` | TypeScript check |

## Backend (Python)

```bash
cd apps/api

# Activate virtual environment
source venv/bin/activate

# Run tests
pytest tests/ -v

# Format code
black app/

# Lint code
flake8 app/
```

## Frontend (Node.js)

```bash
cd apps/web

# Run tests
bun test

# Run type check
bun x tsc --noEmit

# Lint
bun x eslint .

# Format
bun x prettier --write .
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feat/my-feature

# Make changes
# ... edit files ...

# Stage changes
git add .

# Commit (Husky pre-commit hook runs)
git commit -m "feat: add new feature"

# Push (Husky pre-push hook runs tests)
git push origin feat/my-feature

# Create Pull Request on GitHub
```

## Debugging

```bash
# Frontend: Open browser DevTools
bun run dev
# Press F12 in browser

# Backend: Add breakpoints and debug
python -m pdb script.py
```

## Useful Scripts

```bash
# Validate entire setup
node scripts/validate-setup.js

# Run all tests with coverage
./scripts/run-all-tests.sh        # macOS/Linux
scripts\run-all-tests.bat         # Windows

# Pre-push validation
./scripts/pre-push-validation.sh  # macOS/Linux
scripts\pre-push-validation.bat   # Windows
```

## Troubleshooting

| Issue                      | Solution                                    |
| -------------------------- | ------------------------------------------- |
| Port in use                | `lsof -i :3000` then `kill -9 <PID>`        |
| Python venv not activating | `pip install --upgrade pip`                 |
| Modules not found          | Delete `node_modules` and run `bun install` |
| Husky hooks not running    | `bun x husky install`                       |
| Tests failing              | `bun run test` to see details               |

## Environment Setup

Create `.env` files:

**Backend** (`apps/api/.env`):

```
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-secret
```

**Frontend** (`apps/web/.env.local`):

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Quick Links

- 📚 Full Testing Guide: [TESTING.md](TESTING.md)
- 👨‍💻 Developer Setup: [DEVELOPER_SETUP.md](DEVELOPER_SETUP.md)
- 🤝 Contributing: See CONTRIBUTING.md (if exists)
- 📖 Main README: [README.md](README.md)

## Common Scenarios

### Starting a new feature

```bash
git checkout -b feat/feature-name
bun run dev
bun run test:watch
```

### Before pushing code

```bash
bun run lint      # Check style
bun run format    # Auto-fix style
bun run test      # Run all tests
bun run check-types  # Type check
git push
```

### Running only changed tests

```bash
bun run test -- --onlyChanged
```

### Checking test coverage

```bash
bun run test:coverage
# View HTML reports:
# - Frontend: apps/web/coverage/lcov-report/index.html
# - Backend: apps/api/htmlcov/index.html
```

---

For more details, see [TESTING.md](TESTING.md) and [DEVELOPER_SETUP.md](DEVELOPER_SETUP.md)
