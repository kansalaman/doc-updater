# AI-Powered README Updater Pre-commit Hook

A pre-commit hook that automatically updates your project's README.md based on code changes using OpenAI's GPT API.

## Setup

### Recent Code Changes
<!-- Include recent code changes here if needed -->

### Installation
Ensure you have Python 3.6 or higher, OpenAI API key, and a Git repository.

1. Install the package using pip:
```bash
pip install doc-updater
```

2. Add the pre-commit configuration to your project:
Create a `.pre-commit-config.yaml` file:
```yaml
repos:
- repo: local
  hooks:
  - id: doc-updater
    name: Update documentation with code changes
    entry: doc-updater
    language: python
    types: [python]
    pass_filenames: false
    additional_dependencies: ['openai>=1.0.0']
```

3. Set up your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

4. Install the pre-commit hook:
```bash
pre-commit install
```

### Usage
The hook will automatically run on committing Python files:

1. Stage changes:
```bash
git add .
```

2. Commit changes:
```bash
git commit -m "Your commit message"
```

### Configuration
**Custom README Location:**
Specify a different path for your README:
```yaml
repos:
- repo: local
  hooks:
  - id: doc-updater
    name: Update documentation with code changes
    entry: doc-updater --readme path/to/your/README.md
    language: python
    types: [python]
    pass_filenames: false
    additional_dependencies: ['openai>=1.0.0']
```

### Troubleshooting
1. **Missing API Key:** Ensure your OpenAI API key is set as an environment variable.
2. **Hook Not Running:** Verify pre-commit is installed and configured correctly.
3. **No Updates:** The hook runs only when staging Python files.

### Contributing
Contributions are welcome! Submit a Pull Request.

### License
This project is licensed under the MIT License - see the LICENSE file for details.