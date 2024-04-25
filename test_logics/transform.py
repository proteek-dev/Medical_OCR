import re
import json

def extract_and_structure_data(ocr_text, specs):
    # Example specification mapping (reduced for brevity)
    params_mapping = {spec["Abbreviation"]: spec["Synonyms"][0] for spec in specs}  # simplifying to use the first synonym

    # Regular expression to extract data points: assumes format "Name Value Unit"
    pattern = re.compile(r"(\w+)\s+([\d\.]+)\s+(\w+)")
    results = {}

    for line in ocr_text.split('\n'):
        match = pattern.search(line)
        if match:
            param, value, unit = match.groups()
            # Standardize parameter name
            param = params_mapping.get(param, param)
            # Convert value to float and store if it's the most recent
            results[param] = {"parameter": param, "value": float(value), "unit": unit}

    # Convert to the required output format
    structured_data = list(results.values())
    return structured_data

# Load specifications from X1.json
file_path = "/Users/proteeksanyal/Desktop/Learning/Medical_OCR/OCR_raw_samples/X1.json"
with open(file_path, "r") as file:
    specifications = json.load(file)

# Sample OCR text (for demonstration; replace with actual OCR output)
# sample_ocr_text = """
# HGB 13.5 g/dL
# WBC 5.4 10^9/L
# PLT 230 10^9/L
# HGB 14.1 g/dL  # more recent
# """
ocr_file = "/Users/proteeksanyal/Desktop/Learning/Medical_OCR/OCR_raw_samples/0ab9800e-bc9a-4388-aaa2-d4fc05e7d111.txt"
with open(ocr_file, "r") as file:
    sample_ocr_text = file.read()

# Process the data
structured_output = extract_and_structure_data(sample_ocr_text, specifications)
print(structured_output)
