# Contributing to LangManus

Thank you for your interest in contributing to LangManus! We welcome contributions of all kinds from the community.

## Ways to Contribute

There are many ways you can contribute to LangManus:

- **Code Contributions**: Add new features, fix bugs, or improve performance
- **Documentation**: Improve README, add code comments, or create examples
- **Bug Reports**: Submit detailed bug reports through issues
- **Feature Requests**: Suggest new features or improvements
- **Code Reviews**: Review pull requests from other contributors
- **Community Support**: Help others in discussions and issues

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/langmanus.git
   cd langmanus
   ```
3. Set up your development environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```
4. Configure pre-commit hooks:
   ```bash
   chmod +x pre-commit
   ln -s ../../pre-commit .git/hooks/pre-commit
   ```

## Development Process

1. Create a new branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. Make your changes following our coding standards:
   - Write clear, documented code
   - Follow PEP 8 style guidelines
   - Add tests for new features
   - Update documentation as needed

3. Run tests and checks:
   ```bash
   make test      # Run tests
   make lint      # Run linting
   make format    # Format code
   make coverage  # Check test coverage
   ```

4. Commit your changes:
   ```bash
   git commit -m 'Add some amazing feature'
   ```

5. Push to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```

6. Open a Pull Request

## Pull Request Guidelines

- Fill in the pull request template completely
- Include tests for new features
- Update documentation as needed
- Ensure all tests pass and there are no linting errors
- Keep pull requests focused on a single feature or fix
- Reference any related issues

## Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Write descriptive docstrings
- Keep functions and methods focused and single-purpose
- Comment complex logic

## Community Guidelines

- Be respectful and inclusive
- Follow our code of conduct
- Help others learn and grow
- Give constructive feedback
- Stay focused on improving the project

## Need Help?

If you need help with anything:
- Check existing issues and discussions
- Join our community channels
- Ask questions in discussions

We appreciate your contributions to making LangManus better!