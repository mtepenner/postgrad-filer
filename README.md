# Filer: LLM File Analyzer (`analyze_file.py`)

## Overview
The `analyze_file.py` script acts as the brain behind your automated file organization system. Rather than relying on rigid, hard-coded rules based solely on file extensions, this script leverages Generative AI to understand the *context* of your files. By evaluating a combination of the file's original name, its extension, and a safe snippet of its contents (for text-based files), it accurately sorts your downloads into specific directories and suggests clean, web-safe filenames.

## Key Features

* **Intelligent Categorization:** Sorts files into specific, predefined categories rather than just grouping by file type.
* **Smart Renaming:** Automatically generates short, descriptive names using hyphens or underscores instead of spaces, making your files easier to search and manage.
* **Safe Snippet Extraction:** For safe, text-based files (`.txt`, `.md`, `.csv`, `.py`, `.js`, `.rs`, `.json`), the script reads a small 400-character snippet of the content to provide the LLM with deeper context without exposing massive amounts of data.
* **Strict JSON Output:** The LLM prompt enforces a strict JSON response format (`{"category": "Category-Name", "suggested_name": "Clean_Name"}`), stripping out markdown wrappers to ensure the Python script can reliably parse the results.
* **Built-in Error Handling:** If the LLM fails to parse the file or returns an invalid category, the script defaults to an "Uncategorized" folder and strips the extension from the original file name to prevent data loss or crashes.

## Supported Categories
The prompt is strictly instructed to classify files into one of the following definitions:
* **Career-Documents:** Resumes, cover letters, and software engineering portfolios.
* **Source-Code:** Programming files and scripts (e.g., Python, Rust, React, Node.js).
* **Event-Tickets:** Concert passes, convention badges, or event QR codes.
* **Travel-Itineraries:** Flight bookings, hotel reservations, or trip plans.
* **Games:** Game installers, mods, or related assets.
* **Tax-Documents:** W-2s, 1099s, or official tax returns.
* **Financial-Statements:** Bank summaries or investment reports.
* **Receipts-and-Invoices:** Food delivery receipts, digital purchase invoices.
* **Legal-Documents:** Contracts, NDAs, or official agreements.
* **Work-Related:** General company documents, meeting notes.
* **eBooks:** PDFs or EPUBs for reading.
* **Installation-Software:** General executable setups (.exe, .dmg).
* **Pictures:** Image files.
* **Music:** Audio files.
* **Videos:** Video files.
* **Archives-and-Zips:** Compressed folders (.zip, .tar.gz).

## How It Works Under the Hood

1.  **Input Reception:** The `analyze_file(file_path, file_name, ext)` function is called whenever a new file is detected.
2.  **Snippet Generation:** It checks if the extension is in the safe-list. If so, it reads the first 400 characters. 
3.  **Prompt Construction:** An f-string combines the file details, the content snippet, the rigid category definitions, and a strict rule set (e.g., "Do NOT include the file extension in your suggested name").
4.  **LLM Execution:** The prompt is sent to the configured generative model (`model.generate_content(prompt)`).
5.  **Parsing:** The script strips any markdown (like ````json`) from the response, loads it as a JSON object, and validates the category.
6.  **Return:** It returns a tuple containing the final `category` and the `suggested_name`.
