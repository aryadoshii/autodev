```markdown
# Contributing to [Project Name]

Thank you for your interest in contributing to [Project Name]! We welcome contributions from everyone, whether you're reporting bugs, suggesting features, or submitting code changes. This guide will help you get started and ensure your contributions align with our project standards.

## How to Contribute

### Report Bugs
If you find a bug, please create an issue on our GitHub repository:
1. Search existing issues to avoid duplicates
2. Provide a clear description of the problem
3. Include steps to reproduce the issue
4. Add any relevant logs, screenshots, or error messages
5. Specify your environment (OS, browser, version)

### Suggest Features
We're always looking for ways to improve our project:
1. Check if the feature has already been requested
2. Clearly describe the feature and its benefits
3. Explain how it would be used
4. Consider providing examples or mockups

### Submit Pull Requests
To submit code changes:
1. Fork the repository
2. Create a feature branch
3. Make your changes following our coding standards
4. Write tests for your changes
5. Ensure all tests pass
6. Submit a pull request with a clear description

## Development Setup

### Fork and Clone
1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/[project-name].git
   cd [project-name]
   ```

### Create Branch
Create a new branch for your work:
```bash
git checkout -b feature/your-feature-name
```
Use descriptive names that clearly indicate what you're working on.

### Install Dependencies
Install project dependencies using the package manager of your choice:
```bash
# For npm
npm install

# For pip (Python projects)
pip install -r requirements.txt

# For other package managers
# [Add appropriate installation commands]
```

## Coding Standards

### Code Style
We enforce consistent code style using automated tools:
- **Python**: Black formatter
- **JavaScript/TypeScript**: ESLint with Airbnb style guide
- **Other languages**: [Specify appropriate linters/formatters]

Run formatting tools before committing:
```bash
# Python
black .

# JavaScript/TypeScript
npm run lint:fix

# Other languages
# [Add appropriate formatting commands]
```

### Naming Conventions
- Use descriptive variable and function names
- Follow camelCase for variables and functions
- Use PascalCase for classes and constructors
- Prefix private members with underscore (`_private_method`)
- Use uppercase for constants (`MAX_SIZE`)

### Documentation Requirements
All public APIs must include documentation:
- Function docstrings with parameters and return values
- Class docstrings explaining purpose and usage
- Inline comments for complex logic
- README updates for new features
- Examples where appropriate

## Testing Requirements

### Write Tests for New Features
Every new feature or bug fix must include tests:
- Unit tests for individual functions/components
- Integration tests for complex interactions
- Test edge cases and error conditions
- Follow existing test patterns in the codebase

### Run Test Suite
Before submitting changes, run the full test suite:
```bash
# Run all tests
npm test

# Run specific test files
npm test -- test/unit/example.test.js

# Run tests with coverage
npm run test:coverage
```

### Coverage Requirements
Maintain at least 80% code coverage:
- Aim for 90%+ coverage when possible
- Coverage reports are generated automatically during CI
- Fix uncovered lines before merging

## Commit Guidelines

### Conventional Commits Format
We use the Conventional Commits specification for commit messages:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(parser): add support for new file format

Added parsing logic for .xyz files with comprehensive error handling.

Fixes #123
```

### Clear Commit Messages
- Keep subject line under 50 characters
- Use imperative mood ("Add feature" not "Added feature")
- Explain what and why, not how
- Reference related issues with `Fixes #issue-number`

## Pull Request Process

### Create Pull Request
1. Push your branch to your fork
2. Open a pull request against the main branch
3. Fill out the PR template completely
4. Link any related issues

### Description Requirements
Your PR description should include:
- Summary of changes made
- Motivation for the change
- How to test the changes
- Any breaking changes
- Related issues or discussions

### Code Review Process
1. All PRs require at least one approval
2. Address all feedback before merging
3. Update your branch if conflicts arise
4. Re-request review after making changes

### Merging
- PRs must pass all CI checks
- Code must meet quality standards
- Final approval required before merging
- Squash and merge for cleaner history

## Code of Conduct

### Be Respectful
We maintain a welcoming and inclusive environment for all contributors:
- Treat everyone with respect and professionalism
- Avoid personal attacks or derogatory comments
- Focus on constructive criticism and feedback

### Inclusive Language
- Use gender-neutral language
- Avoid jargon or technical terms without explanation
- Be mindful of cultural differences
- Welcome newcomers and provide helpful guidance

## Getting Help

### Where to Ask Questions
- GitHub Discussions: [Link to discussions page]
- Stack Overflow: Tag with `[project-name]`
- Email: [contact-email@example.com]

### Community Channels
- Discord Server: [Invite link]
- Twitter: [@project_handle]
- Newsletter: [Subscribe link]

We're excited to have you as part of our community! Your contributions make this project better for everyone.
```