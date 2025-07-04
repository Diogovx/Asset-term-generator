# Snipe-IT Asset Liability Term Generator

[Leia em Português (Brasil) 🇧🇷](./README.pt-br.md)

[![Quality and Test CI](https://github.com/Diogovx/Asset-term-generator/actions/workflows/ci-pipeline.yml/badge.svg)](https://github.com/Diogovx/Asset-term-generator/actions/workflows/ci-pipeline.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

A Python command-line application (CLI) that automates the creation of liability term documents for IT assets (laptops, smartphones, etc.) assigned to employees by querying data directly from a Snipe-IT instance.

## 📋 Table of Contents

- [Snipe-IT Asset Liability Term Generator](#snipe-it-asset-liability-term-generator)
  - [📋 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [🚀 Installation \& Setup](#-installation--setup)
  - [🛠️ Usage](#️-usage)
  - [✅ Testing](#-testing)
  - [🏛️ Architecture \& Design Decisions](#️-architecture--design-decisions)
    - [Folder Structure](#folder-structure)
      - [Key Principles](#key-principles)
  - [📈 Roadmap](#-roadmap)
  - [🤝 Contributing](#-contributing)
  - [✍️ Autores](#️-autores)
  - [📄 License](#-license)

## ✨ Features

- **Smart Search:** Finds users by their employee number and fetches all their associated assets (hardware, components, and accessories).
- **Dynamic Generation:** Uses `.docx` templates to generate standardized and automatically populated documents.
- **Robust Architecture:** Built with Pydantic for data validation, ensuring the integrity of information from the API.
- **Guaranteed Quality:** CI/CD pipeline with GitHub Actions to automatically run tests (`pytest`) and code analysis (`ruff`, `mypy`).
- **Reproducible Environment:** Dependency management with `pip-tools` to ensure a consistent development environment through lock files.

## 🚀 Installation & Setup

Follow these steps to set up the development environment on your machine.

1. **Clone the repository:**

    ```bash
    git clone [https://github.com/Diogovx/Asset-term-generator.git](https://github.com/Diogovx/Asset-term-generator.git)
    cd Asset-term-generator
    ```

2. **Create and activate the virtual environment:**

    ```bash
    # Create the venv
    python -m venv .venv

    # Activate on Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1

    # Activate on Linux/macOS
    # source .venv/bin/activate
    ```

3. **Install dependencies:**
    This command installs all application libraries and development tools.

    ```bash
    pip install -r dev-requirements.txt
    ```

4. **Install the project in editable mode:**
    This crucial step makes your `assets_term_generator` package importable in your environment.

    ```bash
    pip install -e .
    ```

5. **Set up environment variables:**
    - Go to the `config/` folder.
    - Create a copy of the `.env.example` file and rename it to `.env`.
    - Open the `.env` file and fill it with the correct values from your Snipe-IT instance.

## 🛠️ Usage

With the virtual environment activated, run the application from the project root with the following command:

```bash
python -m assets_term_generator
```

The program will guide you with interactive prompts to enter the employee number and select the term type.

## ✅ Testing

The project uses `pytest` for automated tests. To run the test suite:

```bash
pytest
```

To generate a test coverage report:

```bash
pytest --cov=src
```

## 🏛️ Architecture & Design Decisions

This project was refactored to follow modern Python development practices.

### Folder Structure

The project uses the `src` layout for a clear separation between the source code and project configuration files.

- **`src/assets_term_generator/`**: Contains the entire Python package source code.
- **`config/`**: Application configuration files (`.yml`, `.env`).
- **`docx-template/`**: `.docx` templates used to generate terms.
- **`tests/`**: Automated tests.

#### Key Principles

- **Modeling with Pydantic**: Instead of dictionaries, we use Pydantic models (`core/models.py`) to define "data contracts". This ensures validation and makes the code safer and self-documenting.
- **Service Layer (Facade)**: The API call orchestration logic is isolated in the `api/snipeit_client.py` module, which hides complexity and delivers clean data objects to the application.
- **Dependency Injection**: Components like the UI (`Menu`) and `DocumentProcessor` receive their configurations via the constructor (`__init__`), making them decoupled and easier to test.
- **Quality Tooling**: `pre-commit` is configured to run `ruff` (linter and formatter) and `mypy` (type checker) before each commit, automatically ensuring code quality and consistency.

## 📈 Roadmap

- [ ] Implement security analysis tools (`bandit`, `pip-audit`) in the CI pipeline.
- [ ] Migrate document generation to `docxtpl` to allow conditional logic and loops (`if`/`for`) directly in the `.docx` templates.
- [ ] Develop a web interface with FastAPI for intranet use.
- [ ] Add a history of generated terms.

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## ✍️ Autores

- [@Diogovx](https://github.com/Diogovx)

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
