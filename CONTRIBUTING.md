# Contributing to sorry.monster

Thank you for your interest in contributing to Apology-as-a-Service!

## Development Process

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch from `main`
4. **Make** your changes
5. **Test** thoroughly
6. **Commit** with clear messages
7. **Push** to your fork
8. **Submit** a pull request

## Code Standards

### Python (Backend)
- Use Python 3.12+
- Follow PEP 8 style guide
- Type hints required
- Run `ruff check` and `mypy` before committing
- Write tests for new features

### TypeScript (Frontend)
- Use TypeScript strict mode
- Follow project ESLint rules
- Use functional components with hooks
- Write accessible UI components

### Commit Messages
Follow conventional commits format:
```
feat: add brand profile management
fix: resolve rate limiting bug
docs: update API documentation
test: add tests for LLM engine
```

## Testing

### Backend Tests
```bash
cd apps/api
pytest -v
```

### Frontend Tests
```bash
cd apps/frontend
npm test
```

## Pull Request Guidelines

- Keep PRs focused on a single feature/fix
- Include tests for new functionality
- Update documentation as needed
- Ensure CI passes
- Add screenshots for UI changes
- Reference related issues

## Questions?

Open an issue for discussion before major changes.
