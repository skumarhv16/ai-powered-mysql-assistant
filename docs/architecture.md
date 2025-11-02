# Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  User Interface                      │
│         (Streamlit Web App / CLI)                    │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│            Query Assistant (Orchestrator)            │
└───┬──────────┬─────────────┬─────────────┬──────────┘
    │          │             │             │
┌───▼───┐  ┌──▼────┐   ┌────▼────┐   ┌───▼────┐
│ Query │  │Query  │   │Database │   │Schema  │
│ Gen   │  │Optim  │   │Manager  │   │Analyzer│
└───┬───┘  └──┬────┘   └────┬────┘   └───┬────┘
    │         │             │             │
    └─────────┴──────┬──────┴─────────────┘
                     │
           ┌─────────▼──────────┐
           │    AI Service      │
           │  (OpenAI/Gemini)   │
           └────────────────────┘
```

## Component Details

### 1. Query Assistant
- Main orchestrator
- Coordinates all components
- Handles user requests

### 2. Query Generator
- Converts natural language to SQL
- Uses AI for generation
- Validates syntax

### 3. Query Optimizer
- Analyzes query performance
- Suggests optimizations
- Recommends indexes

### 4. Database Manager
- Manages MySQL connections
- Executes queries
- Handles connection pooling

### 5. AI Service
- Integrates with AI models
- Generates SQL
- Provides explanations

### 6. Schema Analyzer
- Analyzes database schema
- Finds relationships
- Provides context to AI

## Data Flow

1. User submits natural language question
2. Query Assistant receives request
3. Schema Analyzer provides database context
4. AI Service generates SQL query
5. Query Generator validates syntax
6. Database Manager executes query
7. Query Optimizer analyzes performance
8. AI Service explains results
9. Results returned to user

## Technology Stack

- **Backend**: Python 3.9+
- **Database**: MySQL 8.0+
- **AI**: OpenAI GPT-4 / Google Gemini
- **Web**: Streamlit
- **ORM**: SQLAlchemy
- **Testing**: Pytest

## Security Considerations

- SQL injection prevention
- Parameterized queries
- Read-only mode option
- API key security
- Audit logging

---

**Author**: Sandeep Kumar H V
**Last Updated**: November 2024
