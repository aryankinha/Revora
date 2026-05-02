# Revora - Enterprise Lead Generation and Outreach Platform

Revora is a comprehensive platform designed for automated lead generation, Ideal Customer Profile (ICP) analysis, and secure email outreach. The project is architected as a high-performance monorepo, demonstrating enterprise-grade system design, object-oriented programming principles, and scalable architecture.

## Platform Features

- **Automated Lead Generation**: Integration with external providers such as Apollo and LinkedIn via strategy-driven interfaces to generate robust leads based on specific ICP parameters.

* **Gmail Outreach Integration**: Secure connection to the Google Gmail API via OAuth2, enabling personalized cold-email campaigns directly from the platform.
* **Dynamic Dashboard**: Interactive data visualization and campaign management interface.
* **JWT Authentication**: Secure, user-scoped access control ensuring data segmentation and privacy.
* **System Design Excellence**: Implementation of core design patterns and SOLID principles for maintainability and scalability.

## Technology Stack

### Frontend

- **Framework**: Next.js 15 with React 19
- **Styling**: Tailwind CSS
- **Animations**: GSAP (GreenSock Animation Platform)
- **Smooth Scrolling**: Lenis
- **Visualization**: Recharts and Three.js
- **Package Manager**: Bun

### Backend

- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Migrations**: Alembic
- **Validation**: Pydantic

### Infrastructure & Tooling

- **Monorepo Management**: Turborepo
- **Testing**: Jest (Frontend), Pytest (Backend)
- **Code Quality**: Husky, Lint-staged, ESLint, Prettier, Flake8, Black

## System Architecture and Design Patterns

The platform implements standard enterprise design patterns to ensure a modular and extensible codebase.

### 1. Singleton Pattern

- **Implementation**: `app/db/database.py`
- **Rationale**: Manages database connection engines strictly, ensuring a single connection engine is utilized across the application lifecycle to optimize resource consumption.

### 2. Strategy Pattern

- **Implementation**: `app/services/lead_generation_strategy.py`
- **Rationale**: Enables seamless switching between different lead sources (Apollo, LinkedIn, etc.). The application interacts with an abstract interface, decoupling the execution logic from specific provider implementations.

### 3. Factory Pattern

- **Implementation**: `app/services/lead_factory.py`
- **Rationale**: Dynamically instantiates the appropriate lead generation strategy based on runtime requirements, reducing tight coupling between API endpoints and strategy classes.

### 4. Adapter Pattern

- **Implementation**: `app/services/apollo_adapter.py`
- **Rationale**: Standardizes external API responses into internal Data Transfer Objects (DTOs), shielding the application core from third-party schema changes.

## SOLID Principles

- **Single Responsibility Principle**: Responsibilities are strictly segregated (e.g., separating HTTP fetching from JSON normalization).
- **Open/Closed Principle**: New data sources can be integrated by extending existing strategies without modifying core execution logic.
- **Liskov Substitution Principle**: Lead generation strategies are interchangeable via their shared abstract interface.
- **Interface Segregation Principle**: Abstract Base Classes enforce specific logic constraints rather than utilizing monolithic handlers.
- **Dependency Inversion Principle**: Higher-level route logic depends on abstractions rather than low-level implementation details.

## Getting Started

### Prerequisites

- Bun 1.0 or higher
- Python 3.11 or higher
- PostgreSQL

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SatyamKumarCS/Revora
   cd Revora
   ```

2. Install dependencies:

   ```bash
   bun install
   bun x husky install
   ```

3. Setup backend environment:
   ```bash
   cd apps/api
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   pip install -r ../requirements.txt
   ```

### Running the Platform

To start all applications (Frontend, Backend, Docs) in development mode:

```bash
bun run dev
```

## Project Structure

```text
Revora/
├── apps/
│   ├── api/                # FastAPI Backend
│   ├── docs/               # Documentation Application (Next.js)
│   └── web/                # Main Web Application (Next.js)
├── packages/               # Shared Monorepo Packages
│   ├── ui/                 # Shared React Components
│   ├── eslint-config/      # Shared ESLint Configuration
│   └── typescript-config/  # Shared TypeScript Configuration
├── scripts/                # Validation and Utility Scripts
├── turbo.json              # Turborepo Configuration
└── package.json            # Project Configuration
```

## Testing

The platform maintains high quality standards with comprehensive testing suites.

```bash
bun run test             # Run all tests
bun run test:frontend    # Run Jest tests
bun run test:backend     # Run Pytest tests
```

For detailed testing instructions, refer to [TESTING.md](TESTING.md).
