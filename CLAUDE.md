# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Clove is a sophisticated Claude.ai reverse proxy that provides both OAuth API access and web interface reverse proxy capabilities. It's built with FastAPI (Python) backend and React (TypeScript) frontend, enabling various AI applications to connect to Claude with high compatibility.

## Common Development Commands

### Building and Running

```bash
# Full build (frontend + Python wheel)
make build

# Build only frontend
make build-frontend
# or manually:
cd front && pnpm install && pnpm run build

# Build only Python wheel
make build-wheel

# Install and run
make install
clove

# Development mode
make install-dev
make run
# or
python -m app.main
```

### Frontend Development

```bash
cd front
pnpm install      # Install dependencies
pnpm run dev      # Development server (port 5173, proxies to backend on 5201)
pnpm run build    # Production build
pnpm run lint     # Run ESLint
```

### Python Development

```bash
# Install with optional dependencies
pip install -e ".[rnet,curl,dev]"

# Run in development
python -m app.main

# Linting (when ruff is installed)
ruff check app/
ruff format app/
```

## Architecture Overview

### Dual-Mode Operation
1. **OAuth Mode**: Direct Claude API access with full functionality (system messages, prefilling, etc.)
2. **Web Reverse Proxy Mode**: Claude.ai simulation when OAuth unavailable

### Request Processing Pipeline
The core architecture uses a processor pipeline pattern (Chain of Responsibility):

```
Request → ClaudeAIProcessorPipeline → [
    ClaudeAPIProcessor (OAuth) or ClaudeWebProcessor (Web)
    → EventParsingProcessor
    → ToolCallEventProcessor
    → StreamingResponseProcessor
    → ... specialized processors
] → Response
```

Key processors:
- `app/processors/claude_ai/pipeline.py`: Main pipeline orchestrator
- `app/processors/claude_ai/claude_api_processor.py`: OAuth API handling
- `app/processors/claude_ai/claude_web_processor.py`: Web interface handling
- `app/processors/claude_ai/tool_call_event_processor.py`: Function calling support

### Service Layer Architecture
- **Account Service** (`app/services/account.py`): Multi-account management with failover
- **Session Service** (`app/services/session.py`): Claude.ai session lifecycle
- **OAuth Service** (`app/services/oauth.py`): OAuth authentication flow
- **Cache Service** (`app/services/cache.py`): Response caching

### API Endpoints
- `/v1/messages`: Claude messages API (OpenAI-compatible)
- `/chat/completions`: OpenAI chat completions compatibility
- `/models`: Available models listing
- `/accounts`: Account management
- `/settings`: Configuration management
- `/statistics`: Usage statistics

### Configuration Management
Configuration hierarchy (from highest to lowest priority):
1. Environment variables
2. .env file
3. config.json file
4. Default values in `app/core/config.py`

Key configuration class: `app/core/config.py:Settings`

### Frontend Architecture
- **React 19** with TypeScript
- **Vite** build tool with Tailwind CSS
- **Shadcn/UI** component library
- **API Client**: `front/src/api/` using Axios
- **Pages**: Dashboard, Accounts, Settings (`front/src/pages/`)

## Key Implementation Details

### Adding New Features
1. **New API Endpoint**: Add route in `app/api/routes/`, register in `app/api/main.py`
2. **New Processor**: Extend `BaseProcessor` in `app/processors/base.py`, add to pipeline
3. **New Frontend Page**: Create in `front/src/pages/`, add route in `App.tsx`

### Model Handling
- Model definitions: `app/models/claude.py` (Claude), `app/models/openai.py` (OpenAI compatibility)
- Model mapping: `app/api/routes/models.py:MODELS` dictionary
- Token counting: Uses tiktoken with model-specific encodings

### Session Management
- Automatic session cleanup via background tasks
- Session persistence in `data/` directory
- Cookie-based authentication for web mode

### Error Handling
- Global error handler: `app/core/error_handler.py`
- Custom exceptions in respective modules
- Structured logging with loguru to `logs/` directory

## Development Notes

### Testing
Currently no formal test framework implemented. When adding tests:
- Consider pytest for Python testing
- Add test files as `test_*.py` or `*_test.py`
- Frontend tests would use Vitest (already configured with Vite)

### Type Safety
- Python: Full type hints throughout, validate with mypy if needed
- TypeScript: Strict mode enabled, run `tsc` for type checking

### Async Patterns
- All I/O operations use async/await
- Background tasks for long-running operations
- Proper connection pooling with httpx

### Security Considerations
- Never commit secrets or API keys
- Use environment variables for sensitive configuration
- Validate all user inputs with Pydantic models
- CORS configuration in `app/api/main.py`

## Debugging Tips

1. **Logging**: Check `logs/` directory for detailed logs
2. **API Testing**: Use the built-in FastAPI docs at `http://localhost:5201/docs`
3. **Frontend Dev**: React DevTools and Network tab for API debugging
4. **Session Issues**: Check `data/` directory for session persistence files
5. **OAuth Flow**: Monitor browser DevTools for redirect chains

## Common Tasks

### Adding a New Claude Model
1. Update `MODELS` in `app/api/routes/models.py`
2. Add token encoding if needed in `app/models/claude.py`
3. Update model selection logic in processors

### Modifying Request/Response Format
1. Update Pydantic models in `app/models/`
2. Adjust processors in `app/processors/claude_ai/`
3. Update API routes if needed

### Frontend Styling
- Use Tailwind CSS classes
- Follow Shadcn/UI component patterns
- Maintain dark mode support