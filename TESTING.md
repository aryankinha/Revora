# Testing Setup Guide

This document outlines the comprehensive testing, linting, and formatting setup for the Revora project.

## Overview

The project includes:

- **Unit Tests**: Jest (Frontend), Pytest (Backend)
- **Linting**: ESLint (TypeScript), Flake8/Pylint (Python)
- **Formatting**: Prettier, Black
- **Pre-commit Hooks**: Husky with automatic checks
- **CI/CD**: GitHub Actions workflows

## Quick Start

### Install Dependencies

```bash
# Install all dependencies (from root)
bun install

# For backend development
cd apps/api
pip install -r ../requirements.txt
pip install pytest pytest-asyncio pytest-cov pytest-mock black flake8 pylint
```

### Run Tests

```bash
# Run all tests
bun run test

# Run frontend tests only
bun run test:frontend

# Run backend tests only
bun run test:backend

# Watch mode (frontend)
bun run test:watch

# Coverage report
bun run test:coverage
```

### Run Linting & Formatting

```bash
# Lint all code
bun run lint

# Format all code
bun run format

# Check formatting without changes
bun x prettier --check "**/*.{ts,tsx,js,json,md}"

# Format Python files
cd apps/api
black app/
flake8 app/
```

## 📁 Project Structure

### Test Directories

```
├── apps/
│   ├── api/
│   │   └── tests/               # Backend tests
│   │       ├── __init__.py
│   │       ├── conftest.py     # Pytest fixtures
│   │       ├── test_auth.py
│   │       └── test_leads.py
│   └── web/
│       ├── jest.config.ts      # Jest configuration
│       └── tests/              # Frontend tests
│           ├── setup.ts        # Test setup
│           ├── utils.test.ts
│           └── components.test.ts
└── .github/
    └── workflows/
        ├── test.yml            # Main CI workflow
        └── pr-validation.yml   # PR validation workflow
```

### Configuration Files

- `pytest.ini` - Pytest configuration for backend
- `jest.config.ts` - Jest configuration for frontend
- `lint-staged.config.js` - Pre-commit checks configuration
- `.husky/pre-commit` - Pre-commit hook (lint & format)
- `.husky/pre-push` - Pre-push hook (run tests)
- `.husky/commit-msg` - Commit message validation

## 🔄 Pre-commit & Pre-push Hooks

### Pre-commit Hook (Automatic)

Runs automatically before each commit:

1. Runs `lint-staged` for modified files
2. Lints TypeScript/JavaScript files
3. Checks/fixes code formatting
4. Validates Python code (black, flake8)

### Pre-push Hook (Optional)

Runs before pushing to remote:

1. Runs all tests
2. Ensures all tests pass before push

### Bypass Hooks (If Needed)

```bash
# Skip pre-commit hook
git commit --no-verify

# Skip pre-push hook
git push --no-verify
```

## 🧪 Backend Testing

### Test Files Location

- `apps/api/tests/`

### Running Backend Tests

```bash
# Run all tests
cd apps/api && pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test class
pytest tests/test_auth.py::TestAuthService -v

# Run async tests
pytest tests/ -v -m asyncio
```

### Test Structure

```python
class TestAuthService:
    def test_hash_password(self):
        """Test password hashing functionality."""
        # Test implementation

@pytest.mark.asyncio
async def test_concurrent_operations():
    """Test async operations."""
    # Test implementation
```

### Available Markers

- `@pytest.mark.asyncio` - Async test
- `@pytest.mark.slow` - Slow running test
- `@pytest.mark.integration` - Integration test
- `@pytest.mark.unit` - Unit test

## 🎨 Frontend Testing

### Test Files Location

- `apps/web/tests/`

### Running Frontend Tests

```bash
# Run all tests
bun run test:frontend

# Run in watch mode
bun run test:watch

# Generate coverage report
bun run test:coverage

# Run specific test
bun x jest tests/utils.test.ts
```

### Test Structure

```typescript
describe('Component Tests', () => {
  it('should render component without crashing', () => {
    // Test implementation
  });

  it('should handle props correctly', () => {
    // Test implementation
  });
});
```

### Coverage Thresholds

- Branches: 50%
- Functions: 50%
- Lines: 50%
- Statements: 50%

## ✅ Linting & Formatting

### Frontend Linting

```bash
# Check lint errors
bun run lint

# Fix ESLint issues
bun x eslint --fix apps/web/

# Check formatting
bun x prettier --check apps/web/

# Format code
bun x prettier --write apps/web/
```

### Backend Linting

```bash
# Flake8
flake8 apps/api/app/ --max-line-length=100

# Black formatting
black apps/api/app/

# Pylint
pylint apps/api/app/
```

### Lint Configuration

- **ESLint**: `apps/web/eslint.config.js`
- **Prettier**: Root `.prettierrc` or `prettier.config.js`
- **Flake8**: `setup.cfg` or `.flake8`
- **Black**: `pyproject.toml`

## 🔗 GitHub Workflows

### Test Workflow (`test.yml`)

Runs on:

- Push to `main` or `develop`
- Pull requests to `main` or `develop`

Steps:

1. **Lint & Format Check**
   - Node 18.x, 20.x
   - Runs ESLint, Prettier, type checking

2. **Backend Tests**
   - Python 3.9, 3.10, 3.11
   - Runs pytest with coverage

3. **Frontend Tests**
   - Node 18.x, 20.x
   - Runs Jest with coverage

4. **Test Summary**
   - Aggregates results from all checks

### PR Validation Workflow (`pr-validation.yml`)

Runs on:

- Pull requests to `main` or `develop`
- Changes to monitored paths

Features:

- Detects which parts changed (backend/frontend)
- Runs only relevant checks
- Posts results as PR comment

## 📊 Coverage Reports

### Viewing Coverage

```bash
# Frontend coverage
open coverage/lcov-report/index.html

# Backend coverage
cd apps/api && open htmlcov/index.html
```

### Coverage Files

- Frontend: `coverage/`
- Backend: `apps/api/htmlcov/`

## 🐛 Troubleshooting

### Pre-commit Hook Not Running

```bash
# Reinstall Husky
bun x husky install
```

### Tests Not Found

```bash
# Ensure pytest is installed
pip install pytest pytest-asyncio pytest-cov

# Ensure Jest is installed
bun install jest ts-jest @testing-library/react
```

### Module Not Found Errors (Backend)

```bash
# Add app directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/apps/api"
```

### Formatting Conflicts

```bash
# Format entire project
bun run format

# Format specific app
bun x prettier --write apps/web/
```

## 📝 Adding New Tests

### Add Backend Test

1. Create test file in `apps/api/tests/test_*.py`
2. Import fixtures from `conftest.py`
3. Write test functions with `test_` prefix
4. Use `@pytest.mark` for categorization

### Add Frontend Test

1. Create test file in `apps/web/tests/*.test.ts(x)`
2. Import testing utilities
3. Write test cases using `describe` and `it`
4. Mock external dependencies as needed

## 🔐 Commit Guidelines

### Conventional Commits

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `test`: Adding tests
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `chore`: Maintenance

Example:

```
feat(auth): add JWT token refresh

- Implement refresh token endpoint
- Add token expiration handling
- Update auth service tests

Closes #123
```

## 🚦 Status Checks

Before pushing, ensure:

- All tests pass locally: `bun run test`
- Linting passes: `bun run lint`
- Formatting correct: `bun run format`
- Types check out: `bun run check-types`

## 📚 Resources

- [Jest Documentation](https://jestjs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [ESLint Documentation](https://eslint.org/)
- [Prettier Documentation](https://prettier.io/)
- [Husky Documentation](https://typicode.github.io/husky/)
- [Turbo Repository](https://turbo.build/)

## 🤝 Contributing

1. Create a feature branch
2. Make changes and write tests
3. Ensure all tests pass
4. Format and lint code
5. Create a pull request
6. Wait for CI checks to pass
7. Request review from maintainers

---

For questions or issues, open a GitHub issue or contact the team.
