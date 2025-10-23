# Contributing to Walmart MLOps Pipeline

Thank you for your interest in contributing to the Walmart MLOps Pipeline! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Java 8 or 11
- Git

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/walmart-mlops-pipeline.git
cd walmart-mlops-pipeline

# Set up environment
make venv
make config  # Validate configuration

# Run the pipeline
make demo
```

## 📋 How to Contribute

### 1. Fork and Clone
1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature/fix

### 2. Development Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes
# Test your changes
make config
make demo

# Commit your changes
git add .
git commit -m "Add: your feature description"
```

### 3. Testing
Before submitting a pull request, ensure:
- [ ] All tests pass: `make config`
- [ ] Pipeline runs successfully: `make demo`
- [ ] Code follows project conventions
- [ ] Documentation is updated if needed

### 4. Submit Pull Request
1. Push your branch to your fork
2. Create a pull request on GitHub
3. Provide a clear description of your changes

## 🏗️ Project Structure

```
walmart-mlops-pipeline/
├── scripts/           # ETL, training, inference scripts
├── dags/             # Airflow DAGs
├── dashboard.py      # Streamlit dashboard
├── config.py         # Configuration management
├── requirements.txt  # Python dependencies
├── Makefile         # Build commands
└── README.md        # Project documentation
```

## 🎯 Contribution Areas

### High Priority
- **Performance Optimization**: Improve Spark job performance
- **Model Improvements**: Better feature engineering, model algorithms
- **Monitoring**: Add comprehensive monitoring and alerting
- **Testing**: Unit tests, integration tests, end-to-end tests

### Medium Priority
- **Documentation**: Improve README, add tutorials
- **Configuration**: Additional configuration options
- **UI/UX**: Enhance Streamlit dashboard
- **Deployment**: Docker, Kubernetes deployment guides

### Low Priority
- **Examples**: Additional use cases and examples
- **Utilities**: Helper scripts and tools
- **Visualization**: Additional charts and graphs

## 📝 Code Standards

### Python Code
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings for functions and classes
- Keep functions focused and small

### Configuration
- Use environment variables for configuration
- Provide sensible defaults
- Document all configuration options

### Documentation
- Update README.md for significant changes
- Add inline comments for complex logic
- Keep documentation up-to-date

## 🐛 Bug Reports

When reporting bugs, please include:
- **Environment**: OS, Python version, Java version
- **Steps to reproduce**: Clear, numbered steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Error messages**: Full error traceback
- **Configuration**: Relevant config.env settings

## 💡 Feature Requests

For feature requests, please include:
- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: Other approaches considered
- **Impact**: Who would benefit from this feature?

## 🔒 Security

- Never commit sensitive data (API keys, passwords, etc.)
- Use environment variables for secrets
- Follow security best practices
- Report security issues privately

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check README.md and inline docs first

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to the Walmart MLOps Pipeline! 🚀
