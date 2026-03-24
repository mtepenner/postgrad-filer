# ==========================================
# LLM PROCESSING
# ==========================================
def analyze_file(file_path, file_name, ext):
    """Uses an LLM with specific category definitions to determine placement and new name."""
    snippet = ""
    
    # Safely extract a small snippet if it's a simple text file
    if ext.lower() in ['.txt', '.md', '.csv', '.py', '.js', '.rs', '.json']:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                snippet = f.read(400) 
        except Exception:
            pass

    prompt = f"""
    Analyze the following downloaded file to determine its category and suggest a clean, descriptive name.
    Original Name: {file_name}
    Extension: {ext}
    Content Snippet (if any): {snippet}
    
    Category Definitions:
    - Career-Documents: Resumes, cover letters, and software engineering portfolios.
    - Source-Code: Programming files and scripts (e.g., Python, Rust, React, Node.js).
    - Event-Tickets: Concert passes, convention badges, or event QR codes.
    - Travel-Itineraries: Flight bookings, hotel reservations, or trip plans.
    - Games: Game installers, mods, or related assets.
    - Tax-Documents: W-2s, 1099s, or official tax returns.
    - Financial-Statements: Bank summaries or investment reports.
    - Receipts-and-Invoices: Food delivery receipts, digital purchase invoices.
    - Legal-Documents: Contracts, NDAs, or official agreements.
    - Work-Related: General company documents, meeting notes.
    - eBooks: PDFs or EPUBs for reading.
    - Installation-Software: General executable setups (.exe, .dmg).
    - Pictures: Image files.
    - Music: Audio files.
    - Videos: Video files.
    - Archives-and-Zips: Compressed folders (.zip, .tar.gz).
    
    Rules:
    1. Select the most appropriate category from the definitions above. If none fit well, use "Uncategorized".
    2. Suggest a short, descriptive name based on the content or original name. Use hyphens or underscores instead of spaces.
    3. Do NOT include the file extension in your suggested name.
    
    Respond strictly with a JSON object in this exact format, with no markdown formatting:
    {{"category": "Category-Name", "suggested_name": "Clean_Name"}}
    """

    try:
        response = model.generate_content(prompt)
        # Clean up the response to ensure it's valid JSON
        json_text = response.text.strip().replace('```json', '').replace('```', '')
        result = json.loads(json_text)
        
        category = result.get("category", "Uncategorized")
        if category not in CATEGORIES:
            category = "Uncategorized"
            
        return category, result.get("suggested_name", "Unknown_File")
        
    except Exception as e:
        print(f"LLM Error parsing {file_name}: {e}")
        return "Uncategorized", file_name.replace(ext, "")
