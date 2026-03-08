# Contributing to OpenFang Auto Clip

Thank you for your interest in contributing! We welcome contributions from everyone.

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**Bug Report Template:**

```markdown
**Description**
A clear description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Command '...'
2. Error '...'

**Expected Behavior**
What should happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. macOS 14.0]
- OpenFang version: [e.g. 0.1.9]
- Python version: [e.g. 3.11]

**Logs**
Error messages or logs.
```

### Suggesting Features

We love feature suggestions! Please provide:

- **Use case**: What problem does this solve?
- **Proposed solution**: How should it work?
- **Alternatives**: What alternatives did you consider?
- **Impact**: Who would benefit and how?

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Write/update tests
5. Update documentation
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 📋 Code Standards

### Python Code

- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to functions/classes
- Maximum line length: 100 characters

### Example

```python
def transform_video(
    input_path: Path,
    output_path: Path,
    transform_level: int = 1
) -> bool:
    """
    Transform video to copyright-safe version.

    Args:
        input_path: Source video file path
        output_path: Destination file path
        transform_level: Transformation depth (1-3)

    Returns:
        True if successful, False otherwise

    Raises:
        ValueError: If transform_level not in [1, 2, 3]
    """
    if transform_level not in [1, 2, 3]:
        raise ValueError("transform_level must be 1, 2, or 3")

    # Implementation...
```

### Shell Scripts

- Use ShellCheck for validation
- Add shebang: `#!/bin/bash`
- Quote variables: `"$var"`
- Use `set -euo pipefail`

## 🎨 Priority Areas

We especially welcome contributions in:

### 1. AI Transformation Styles
Add new visual transformation styles:

```python
# Example: New style transformation
class CyberpunkStyle(VisualTransform):
    """Cyberpunk color grading and effects"""

    def apply(self, video: Video) -> Video:
        # Neon colors, glitch effects, etc.
        pass
```

### 2. Platform Integrations
Add support for new platforms:

```python
# Example: New platform
class XHSProcessor(PlatformProcessor):
    """Xiaohongshu (Little Red Book) processor"""

    def optimize(self, video: Video) -> Video:
        # Platform-specific optimization
        pass
```

### 3. Performance Optimization
- Faster video processing
- Reduced memory usage
- Parallel processing

### 4. Documentation
- Translate to other languages
- Add more examples
- Create video tutorials
- Improve guides

### 5. Tests
- Unit tests
- Integration tests
- End-to-end tests

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_transform.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Test Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
└── fixtures/      # Test data
```

### Writing Tests

```python
import pytest
from pathlib import Path

def test_transform_level_1():
    """Test Level 1 transformation"""
    input_file = Path("fixtures/sample.mp4")
    output_file = Path("tmp/output.mp4")

    result = transform_video(input_file, output_file, level=1)

    assert result.success
    assert output_file.exists()
```

## 📖 Documentation

### Documentation Standards

- Clear, concise language
- Code examples for all features
- Update both Chinese and English versions
- Include screenshots/visuals where helpful

### Where to Document

1. **README.md**: Project overview, quick start
2. **docs/**: Detailed guides
3. **Code comments**: Complex logic
4. **Docstrings**: All public functions/classes
5. **CHANGELOG.md**: Version history

## 🎯 Development Workflow

### Setting Up Development Environment

```bash
# Clone fork
git clone https://github.com/outhsics/openfang-auto-clip.git
cd openfang-auto-clip

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Making Changes

1. Create issue (if none exists)
2. Create branch from main: `git checkout -b feature/issue-123`
3. Make changes
4. Write tests
5. Update docs
6. Run tests: `pytest`
7. Commit changes
8. Push to fork
9. Open PR

### Pull Request Checklist

- [ ] Tests pass locally
- [ ] New tests added (if applicable)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commits are clear and descriptive
- [ ] PR description explains changes
- [ ] No merge conflicts

## 🌍 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on what is best for the community

### Communication

- Use GitHub for discussions
- Be patient with responses
- Search before asking
- Share knowledge

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

- Check [Documentation](docs/)
- Search [Issues](https://github.com/outhsics/openfang-auto-clip/issues)
- Start a [Discussion](https://github.com/outhsics/openfang-auto-clip/discussions)
- Email: dev@example.com

---

**Thank you for contributing! 🎉**
