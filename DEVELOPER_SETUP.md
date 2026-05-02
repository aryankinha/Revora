# Developer Setup Guide

## Prerequisites

- **Node.js**: 18.x or higher (use nvm for version management)
- **Bun**: 1.0 or higher (preferred package manager)
- **Python**: 3.9+ (for backend development)
- **Git**: For version control

## Initial Setup

### 1. Clone and Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd Revora

# Install all dependencies
bun install

# Setup Husky hooks
bun x husky install
```

### 2. Backend Setup

```bash
# Navigate to API directory
cd apps/api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt

# Install testing dependencies
pip install pytest pytest-asyncio pytest-cov pytest-mock black flake8 pylint
```

### 3. Frontend Setup

```bash
# From root directory
bun install

# Install Jest and testing libraries (should be in package.json)
bun add --dev jest ts-jest @testing-library/react @testing-library/jest-dom
```

## Running Development Servers

### Frontend

```bash
bun run dev
# Runs Next.js on http://localhost:3000
```

### Backend

```bash
cd apps/api
uvicorn app.main:app --reload
# Runs FastAPI on http://localhost:8000
```

## Common Commands

### Development

```bash
# Start development servers (all apps)
bun run dev

# Build all apps
bun run build

# Run type checking
bun run check-types
```

### Testing

```bash
# Run all tests
bun run test

# Run frontend tests
bun run test:frontend

# Run backend tests
bun run test:backend

# Run tests in watch mode
bun run test:watch

# Generate coverage reports
bun run test:coverage
```

### Code Quality

```bash
# Run linters
bun run lint

# Format code
bun run format

# Check if formatting is needed
bun x prettier --check "**/*.{ts,tsx,js,json,md}"
```

## Git Workflow

### Before Committing

```bash
# Stage changes
git add .

# Husky pre-commit hook will automatically:
# - Run lint-staged
# - Check formatting
# - Lint code

# Commit changes
git commit -m "feat: describe your changes"
```

### Before Pushing

```bash
# Husky pre-push hook will automatically:
# - Run all tests
# - Check linting
# - Verify types

git push origin <branch-name>
```

## IDE Setup

### VS Code Extensions

- ESLint
- Prettier - Code formatter
- TypeScript Vue Plugin (Vue)
- Python
- Pylance
- Thunder Client (or REST Client)

### VS Code Settings

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  }
}
```

## Database Setup

```bash
# Navigate to API directory
cd apps/api

# Create PostgreSQL database
createdb revora_db

# Run migrations
alembic upgrade head

# Seed with test data
python scripts/seed.py
```

## Environment Variables

### Backend (.env)

```
DATABASE_URL=postgresql://user:password@localhost/revora_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Debugging

### Frontend Debugging

```bash
# Run with debugging
bun run dev

# Use Chrome DevTools (F12)
# Check console, network, and React component tree
```

### Backend Debugging

```bash
# Add breakpoints in code
# Run with debugger
python -m pdb app/main.py

# Or use VSCode debugger with launch.json config
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Kill process
kill -9 <PID>
```

### Module Not Found (Python)

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r ../requirements.txt
```

### Node Modules Issues

```bash
# Clear cache and reinstall
rm -rf node_modules bun.lock
bun install
```

### Husky Hooks Not Running

```bash
# Reinstall Husky
bun x husky install

# Make hooks executable
chmod +x .husky/pre-commit
chmod +x .husky/pre-push
```

## Useful Tools

- **Postman/Thunder Client**: API testing
- **DBeaver**: Database management
- **GitKraken**: Git GUI (optional)
- **Insomnia**: API debugging

## Performance Tips

1. **Use bun workspaces** for faster installs
2. **Enable Turbo caching** for faster builds
3. **Use Code splitting** in React components
4. **Optimize database queries** with indexes
5. **Use lazy loading** for images and components

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Jest Documentation](https://jestjs.io/)
- [Pytest Documentation](https://docs.pytest.org/)

## Getting Help

1. Check existing GitHub issues
2. Ask in team Slack channel
3. Review documentation in TESTING.md
4. Create a new issue with details

## Code Review Checklist

Before submitting a PR:

- [ ] Tests pass: `bun run test`
- [ ] Linting passes: `bun run lint`
- [ ] Code formatted: `bun run format`
- [ ] Types check: `bun run check-types`
- [ ] No console errors/warnings
- [ ] Updated relevant documentation
- [ ] Changes tested locally
- [ ] No hardcoded secrets or credentials

---

Professional setup complete.
