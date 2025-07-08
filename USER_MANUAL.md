# User Manual - Liability Term Generator

Welcome! This program helps you create liability terms for IT equipment quickly and automatically.

## Requirements

- A computer with a Windows operating system.

## ⚙️ Initial Setup (One-Time Only)

Before using the program for the first time, you need to configure your API access information.

1. **Open the `config` folder**, which is located alongside this manual.
2. Inside it, you will find a file named `.env`. **Open this file with Notepad**.
3. You will see text similar to this:

    ```env
    API_KEY="YOUR_SNIPE_IT_API_KEY"
    API_USERS_URL="http://your-snipe-it/api/v1/users"
    API_HARDWARE_URL="http://your-snipe-it/api/v1/hardware"
    API_ACCESSORIES_URL="http://your-snipe-it/api/v1/accessories"
    API_COMPONENTS_URL="http://your-snipe-it/api/v1/components"
    ```

4. **Replace the example texts** with the correct values for your company. For instance, replace `"YOUR_SNIPE_IT_API_KEY"` with your actual key.
5. **Save and close** the file.

That's it! The setup is complete.

## ▶️ How to Use the Program

1. **Double-click** on the `Assets_term_generator.exe` file.
2. A black terminal window will open.
3. Follow the instructions on the screen:
   - Type the employee's **ID number** and press Enter.
   - Use the arrow keys to **select the term type** (Notebook, Smartphone, etc.) and press Enter.
   - If necessary, select the specific piece of equipment.
4. At the end of the process, a Word document will be created and opened for you automatically.
5. The generated `.docx` file is saved in the `output` folder.

## ❓ Common Troubleshooting

- **"The program flashes on the screen and closes"**:
  - Check that you have correctly filled out the `.env` file in the `config` folder. Any typo in the URLs or the API key can cause this.
  - Ensure your computer has internet access and can communicate with the Snipe-IT system.

- **"User not found" or "Asset not found"**:
  - Verify that the entered ID number is correct and that the user actually has that type of equipment assigned to them in the Snipe-IT system.

For any other issues, please contact IT support.

## 🔧 Customizing Terms (`config.yml`)

The `config.yml` file, located in the `config` folder, is the brain of the document generation. It allows you to add new term types or customize existing placeholders.

### General Structure

The file is divided into two main sections: `ui` and `document`.

#### `ui` Section

Controls the appearance of the program's interface.

- **`theme`**: Defines the color theme. Can be `dark` or `light`.
- **`logo_path`**: The path to the logo image that appears in the interface.

---

#### `document` Section

Controls everything related to the Word document generation.

- **`template_path`**: The folder where your `.docx` template files are stored.
- **`templates`**: A list of all term types that can be generated (e.g., `laptops`, `smartphones`).
  - **`file_name`**: The exact name of the `.docx` file corresponding to this term.
  - **`placeholders`**: The list of all "tags" that will be replaced within that document.
- **`default_placeholders`**: A list of placeholders that are common to **all** terms, such as the employee's name and ID number.

---

### Understanding a `placeholder`

Each item in the `placeholders` list is a "tag" that the program will replace. It has several keys that define its behavior:

- **`name`**: The exact text of the placeholder in the Word document. Ex: `[LAPTOPMODEL]`.
- **`type`**: The data type. Usually `text`.
- **`category`**: The Snipe-IT asset category to which this placeholder refers. Ex: `"Laptops"`, `"Mouses"`, `"SIM Card"`. **It is crucial that this name is identical to the category name in Snipe-IT.**
- **`description`**: A brief description of what this placeholder represents.
- **`required`**: If `true`, the program will raise an error if it cannot find a value for this placeholder. If `false`, it will simply leave the space blank.
- **`identifier`**: If `true`, indicates that this field is the main user identifier (in this case, the employee ID).
- **`generates_presence_marker`**: If `true`, the program will also look for a presence placeholder (e.g., `[HASLAPTOP]`) and fill it with the `presence_marker_value`.
- **`presence_marker_value`**: The text to be used in the presence marker (usually `"X"`).
- **`source`**: **The most important part.** Tells the program where to fetch the information from.
  - **`type`**: Defines the origin of the data. Can be:
        -   `text`: Fetches an attribute from the **user** object.
        -   `asset`: Fetches an attribute from the **main asset**.
        -   `accessories`: Searches in the asset's **accessories** list.
        -   `components`: Searches in the asset's **components** list.
  - **`path`**: Used with `type: text`, `accessories`, or `components`. It is the exact name of the field to be extracted from the corresponding object (e.g., `name`, `serial`, `employee_num`).
  - **`format`**: Used with `type: asset` or for composite values. It allows you to create a text by combining multiple data points.
        -   Ex: `format: "{model} - {asset_tag}"` will join the model name with the asset tag.
        -   Ex: `format: "{item.name} - {asset.get_custom_field('NUMERO')}"` gets the name of a component (`item.name`) and combines it with a custom field from the parent asset.
