# Snipe-IT Asset Liability Term Generator

[Leia em Português (Brasil) 🇧🇷](./README.pt-br.md)

[![Quality and Test CI](https://github.com/Diogovx/Asset-term-generator/actions/workflows/ci-pipeline.yml/badge.svg)](https://github.com/Diogovx/Asset-term-generator/actions/workflows/ci-pipeline.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

A Python command-line application (CLI) that automates the creation of liability term documents for IT assets assigned to employees by querying data directly from a Snipe-IT instance.

## 📋 Table of Contents

- [Snipe-IT Asset Liability Term Generator](#snipe-it-asset-liability-term-generator)
  - [📋 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [🚀 Installation \& Setup](#-installation--setup)
  - [🛠️ Usage](#️-usage)
  - [✅ Testing](#-testing)
  - [🔧 Template Customization (Jinja2)](#-template-customization-jinja2)
    - [The 3 Golden Rules of Jinja2 Tags](#the-3-golden-rules-of-jinja2-tags)
    - [Available Data in Templates (Context)](#available-data-in-templates-context)
      - [`user` Object](#user-object)
      - [`asset` Object](#asset-object)
    - [Practical Examples](#practical-examples)
      - [1. Conditionally Showing a Paragraph](#1-conditionally-showing-a-paragraph)
      - [2. Listing All Accessories](#2-listing-all-accessories)
  - [🏛️ Architecture \& Design Decisions](#️-architecture--design-decisions)
  - [📈 Roadmap](#-roadmap)
  - [🤝 Contributing](#-contributing)
  - [✍️ Authors](#️-authors)
  - [📄 License](#-license)

---

## ✨ Features

- **Smart Search:** Finds users by their employee number and fetches all their associated assets (hardware, components, and accessories).
- **Powerful Dynamic Generation:** Uses `.docx` templates powered by the **Jinja2 templating engine**, allowing for complex logic like conditionals (`if/else`) and loops (`for`) directly within the Word document.
- **Robust Architecture:** Built with Pydantic for data validation, ensuring the integrity of information from the API.
- **Guaranteed Quality:** CI/CD pipeline with GitHub Actions to automatically run tests (`pytest`) and code analysis (`ruff`, `mypy`).
- **Reproducible Environment:** Dependency management with `pip-tools` to ensure a consistent development environment through lock files.

---

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

    ```bash
    pip install -r dev-requirements.txt
    ```

4. **Install the project in editable mode:**

    ```bash
    pip install -e .
    ```

5. **Set up environment variables:**
    -   Go to the `config/` folder.
    -   Create a copy of the `.env.example` file and rename it to `.env`.
    -   Open the `.env` file and fill it with the correct values from your Snipe-IT instance.

---

## 🛠️ Usage

With the virtual environment activated, run the application from the project root with the following command:

```bash
python -m assets_term_generator
```

The program will guide you with interactive prompts to enter the employee number and select the document type and asset category.

---

## ✅ Testing

The project uses `pytest` for automated tests. To run the test suite:

```bash
pytest
```

To generate a test coverage report:

```bash
pytest --cov=src
```

---

## 🔧 Template Customization (Jinja2)

This application uses **`docxtpl`** to allow the powerful **Jinja2** templating language directly inside your `.docx` templates. This means you can add logic like conditionals and loops to your documents without changing any Python code.

### The 3 Golden Rules of Jinja2 Tags

1. **`{{ ... }}` (Double Curly Braces):** To **SHOW** or **print** a piece of data.
    -   *Example:* `Employee Name: {{ user.name }}`

2. **`{% ... %}` (Curly Brace & Percent):** For **LOGIC** and **control flow**.
    -   *Example:* `{% if asset.notes %}` or `{% for item in asset.accessories %}`

3. **`{# ... #}` (Curly Brace & Hash):** For **COMMENTS** that are invisible in the final document.
    -   *Example:* `{# TODO: Get this clause approved by Legal #}`

### Available Data in Templates (Context)

When creating your template, you have access to these main objects:

#### `user` Object

Contains information about the employee.

- `user.name`
- `user.employee_num`
- `user.department.name`

#### `asset` Object

Contains information about the primary asset selected (e.g., the laptop or smartphone).

- `asset.asset_tag`
- `asset.model.name`
- `asset.serial`
- `asset.category.name`
- `asset.notes`
- `asset.get_custom_field('Field Name')`
- `asset.accessories`: A **list** of all accessory objects attached to this asset.
- `asset.components`: A **list** of all component objects attached to this asset.

### Practical Examples

#### 1. Conditionally Showing a Paragraph

To show a clause only for Laptops:

```jinja
{% if asset.category.name == 'Laptops' %}
BATTERY CLAUSE: It is recommended not to leave the equipment plugged in uninterruptedly to preserve battery life.
{% endif %}
```

#### 2. Listing All Accessories

To automatically create a list of all accessories:

```jinja
Additional Accessories:
{% for item in asset.accessories %}
- {{ item.name }} (Category: {{ item.category.name }})
{% else %}
- No additional accessories were provided with this equipment.
{% endfor %}
```

---

## 🏛️ Architecture & Design Decisions

This project follows modern Python development practices.

- **Logic in Templates:** By using Jinja2, presentation logic (what to show and when) is moved into the `.docx` templates, decoupling it from the Python code and empowering non-developers to modify document structures.
- **Service Layer (Facade)**: The API call orchestration logic is isolated in the `api/snipeit_client.py` module, which hides complexity and delivers clean Pydantic data objects to the application.
- **Dependency Injection**: Components like the `DocumentProcessor` receive their configurations via the constructor (`__init__`), making them decoupled and easier to test.
- **Quality Tooling**: `pre-commit` is configured to run `ruff` and `mypy` before each commit, automatically ensuring code quality and consistency.

---

## 📈 Roadmap

- [ ] Develop a web interface with FastAPI.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## ✍️ Authors

- [@Diogovx](https://github.com/Diogovx)

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
