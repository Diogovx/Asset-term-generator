# User Manual - Liability Waiver Generator

Welcome! This program helps you quickly and automatically create liability waivers for IT equipment.

## Requirements

- Computer with Windows operating system.

## ⚙️ Initial Configuration (One-Time Only)

Before using the program for the first time, you need to configure your API access information.

1. **Open the `config`** folder that comes with this manual.
2. Inside, you will find a file called `.env`. **Open this file with Notepad**. 3. You'll see text similar to this:

```env
API_KEY="YOUR_API_KEY_GENERATED_IN_SNIPE_IT"
API_USERS_URL="http://your-snipe-it/api/v1/users"
API_HARDWARE_URL="http://your-snipe-it/api/v1/hardware"
API_ACCESSORIES_URL="http://your-snipe-it/api/v1/accessories"
API_COMPONENTS_URL="http://your-snipe-it/api/v1/components"
```

4. **Replace the example text** with the correct values ​​for your company. For example, replace `"YOUR_API_KEY_GENERATED_IN_SNIPE_IT"` with your actual key.
5. **Save and close** the file.

Done! The configuration is complete.

## ▶️ How to Use the Program

1. **Double-click** the `Assets_term_generator.exe` file.
2. A black terminal screen will open.
3. Follow the on-screen instructions:
   - Enter the employee's **registration number** and press Enter.
   - Use the arrow keys to **select the term type** (Laptop, Cell Phone, etc.) and press Enter.
   - If necessary, select the specific device.
4. At the end of the process, a Word document will be created and opened automatically for you.
5. The generated `.docx` file is saved in the `output` folder.

## ❓ Common Troubleshooting

- **"The program flashes on the screen and closes"**:
- Check that you have correctly filled in the `.env` file in the `config` folder. Any typos in the URLs or API key can cause this.
- Make sure your computer has internet access and can communicate with the Snipe-IT system.

- **"User not found" or "Asset not found"**:
- Verify that the entered registration number is correct and that the user actually has that type of equipment associated with them in the Snipe-IT system.

For any other issues, please contact IT support.

## 📋 Generation History

For auditing and control purposes, every time a term is successfully generated, the program records an event in a log file.

This log file is called `generation_history.csv` and is located in the `logs` folder. You can open this file directly with Microsoft Excel to view, filter, and create reports on the generated terms.

Each line in the log contains the following information:

- **timestamp**: The exact date and time the term was generated.

- **user_generator**: The computer username of the person who generated the term.
- **employee_number**: The employee's registration number for whom the term was created.
- **employee_name**: The employee's full name.
- **asset_tag**: The asset tag of the main device described in the term.
- **modelo_ativo**: The model of the main device.
- **user_template**: The type of term generated (e.g., `laptops`, `smartphones`).
- **generated_term_path**: The exact location on the computer where the final `.docx` file was saved.

## 🔧 Customizing Templates (Advanced)

With the new system, you have full control over creating and modifying templates directly in Microsoft Word. The "intelligence" of how data is displayed now lives within the document itself, using a system of **smart tags**.

### The 3 Golden Rules of Tags

There are 3 types of special tags you can use in your .docx document:

1. **`{{ ... }}` (Double Braces):** To **SHOW** information.

   - Example: `The collaborator's name is {{ user.name }}`.

2. **`{% ... %}` (Bracket and Percentage):** For **LOGIC**, such as creating lists or showing a paragraph only if a condition is true.

   - Example: `{% for item in asset.accessories %}`.

3. **`{# ... #}` (Bracket and Tic-Tac-Toe):** For **COMMENTS** that will not appear in the final document.

   - Example: `{# TODO: Ask Legal to review this clause #}`.

---

### Data Dictionary (Your "Cheat Sheet")

Here is the main information you can use in your templates.

#### `user` Object (Employee Information)

| To Insert... | Use the Tag |
| :--- | :--- |
| Full Name | `{{ user.name }}` |
| Registration Number | `{{ user.employee_num }}` |
| Department | `{{ user.department.name }}` |

#### `asset` Object (The Main Equipment)

| To Insert... | Use the Tag |
| :--- | :--- |
| Asset Tag | `{{ asset.asset_tag }}` |
| Model Name | `{{ asset.model.name }}` |
| Serial Number | `{{ asset.serial }}` |
| Category Name | `{{ asset.category.name }}` |
| Notes | `{{ asset.notes }}` |
| Custom Field | `{{ asset.get_custom_field('FIELD_NAME') }}` |

---

### Practical Examples

#### **1. Display a paragraph only if a condition is true**

Do you want a clause about "battery care" to appear only for laptops? Use an `if` block.

**Example in Word:**

```jinja
{% if asset.category.name == 'Laptops' %}
BATTERY CLAUSE: It is recommended not to leave the device plugged in continuously to preserve battery life.
{% endif %}
```

*The entire paragraph will only appear if the main asset category is "Laptops".*

#### **2. Create an automatic list of items**

This is the most powerful feature. You can create a list of all associated accessories or components.

**Example in Word:**

```jinja
Additional Accessories List:
{% for item in asset.accessories %}
- {{ item.name }} (Category: {{ item.category.name }})
{% else %}
- No additional accessories were delivered with this equipment.
{% endfor %}
```

- **What this does:** The `{% for ... %}` creates a new line for each accessory. The `{% else %}` displays a default message if the accessory list is empty.

---

### ❓ Troubleshooting Common Template Errors

If the program gives an error when generating the document, it's usually a typo in the template.

- **Error `Encountered unknown tag 'user'`:**
- **Cause:** You probably wrote `{% user.name %}` instead of `{{ user.name }}`.
- **Solution:** Remember, to **display** data, always use double curly braces `{{ }}`.

- **Error `unexpected '%'`:**
- **Cause:** You probably used a `%` character in normal text (e.g., "Battery at 100% charge") inside a `{% if ... %}` block.
- **Solution:** Wrap the problematic text with the `{% raw %}` and `{% endraw %}` tags so the system ignores it.

```jinja
{% raw %}Text with % that causes a problem.{% endraw %}
```

- **The placeholder appears blank in the final document:**
- **Cause:** The variable name is incorrect. You may have typed `{{ user.nome }}` instead of `{{ user.name }}.`
- **Solution:** Consult the "Data Dictionary" above to use the exact field name.

## 🔧 Configuring the Application (`config.yml`)

The `config.yml` file, located in the `config` folder, is the program's main control panel. This is where you define which "term types" the application can generate.

### General Structure

The file is divided into simple sections:

#### `ui` Section

Controls the appearance of the program interface in the terminal.

- **`theme`**: Defines the color theme. Can be `dark` or `light`.
- **`logo_path`**: The path to the logo image that appears in the interface (currently not implemented).

#### `document` Section

Controls everything about document generation.

- **`template_path`**: The folder where your `.docx` template files are stored. The default is `docx-template/`.
- **`templates`**: A dictionary with all the "document types" the program can create.

---

### Tutorial: How to Add a New Term Type

Imagine you need to create a new "Non-Disclosure Agreement." The process is done in two steps, without any programming.

#### Step 1: Create the Template in Word

1. Create a new `.docx` file named, for example, `CONFIDENTIALITY_TERM.docx`.
2. Write all the text and add any necessary **smart tags (Jinja2)** (e.g., `{{ user.name }}`, `{{ asset.asset_tag }}`, etc.).
3. Save this file in the `docx-template/` folder.

#### Step 2: Register the New Template in `config.yml`

1. Open the `config.yml` file with a text editor.
2. Within the `document` -> `templates` section, add a new entry for your term.

**Example of addition:**

```yaml
document:
template_path: docx-template/
templates:
term_of_responsibility:
file_name: TERMO_MASTRE_RESPONSIBILIDADE.docx
description: "Generates the standard asset receipt term."

# ...

term_confidentiality:
file_name: TERMO_CONFIDENTIALIDADE.docx
description: "Generates the confidentiality agreement for special projects."
target_categories: # Optional: Restricts which asset categories this agreement applies to.
- Laptops
```

**Done!** The next time you run the program, the "Generate the confidentiality agreement for special projects" option will automatically appear in the document selection menu.

#### Understanding Template Keys

- **`termo_confidencialidade:`**: This is the "ID" of your new agreement. You choose the name.
- **`file_name`**: **Required.** The exact name of the `.docx` file you created.
- **`description`**: **Required.** The friendly text that will appear in the menu for the user to select. - **`target_categories`**: **Optional.** A list of asset categories to which this term can be applied. If you omit this key, the term can be applied to any asset type.
