# import pdfplumber
# import re

# def extract_text_skip_sanskrit(pdf_path, output_txt_path):
#     print(f"Processing {pdf_path}...")
    
#     with pdfplumber.open(pdf_path) as pdf:
#         clean_text_list = []
        
#         for i, page in enumerate(pdf.pages):
#             text = page.extract_text()
            
#             if text:
#                 # --- FILTERING LOGIC ---
                
#                 # Option 1: Strictly remove Devanagari (Sanskrit/Hindi) characters
#                 # The range \u0900-\u097F covers the Devanagari block
#                 text_no_sanskrit = re.sub(r'[\u0900-\u097F]+', '', text)
                
#                 # Option 2: Cleanup extra spaces left behind by removed words
#                 # This turns "Sun  is hot" into "Sun is hot"
#                 text_clean = re.sub(r'\s+', ' ', text_no_sanskrit).strip()
                
#                 # Add page marker (optional)
#                 clean_text_list.append(f"--- Page {i+1} ---")
#                 clean_text_list.append(text_clean)

#     # Save the cleaned text
#     with open(output_txt_path, "w", encoding="utf-8") as f:
#         f.write("\n".join(clean_text_list))
        
#     print(f"Done! Cleaned text saved to {output_txt_path}")

# # Usage
# extract_text_skip_sanskrit("lalkitab.pdf", "english_only_data.txt")


import fitz  # PyMuPDF

def extract_raw_fitz(pdf_path, output_path):
    print(f"Opening {pdf_path}...")
    doc = fitz.open(pdf_path)
    full_text = []

    for page_num, page in enumerate(doc):
        # get_text("text") grabs text blocks in their natural reading order
        text = page.get_text("text")
        
        if text:
            full_text.append(f"--- Page {page_num + 1} ---")
            full_text.append(text)

    # Save raw data
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(full_text))
        
    print(f"Complete! All raw text saved to {output_path}")

# Usage
extract_raw_fitz("lalkitab.pdf", "raw_data_fitz.txt")