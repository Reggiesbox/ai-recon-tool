# Contributing to AI Reconnaissance Tool

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Remember this tool is for authorized security testing only

## Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Development Setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small

### JavaScript/React

- Use functional components with hooks
- Follow React best practices
- Use meaningful variable names
- Keep components focused and reusable

## Testing

Before submitting a PR, please:

1. Test your changes thoroughly
2. Ensure no linting errors
3. Test in a safe, isolated environment
4. Verify all integrations work correctly

## Security Considerations

- Never commit sensitive information
- Review security implications of changes
- Test in isolated environments only
- Follow responsible disclosure for vulnerabilities

## Pull Request Process

1. Update README.md if needed
2. Update documentation for new features
3. Ensure all tests pass
4. Get at least one review before merging

## Questions?

Open an issue for questions or discussions about the project.

