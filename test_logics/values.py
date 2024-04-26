import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
import json

# Load Spacy's English model
nlp = spacy.load("en_core_web_sm")

# Initialize the PhraseMatcher
matcher = PhraseMatcher(nlp.vocab, attr='LOWER')

# Load document text
document_text = """
Patient Name: John Doe
HbA1c (Glycosylated Hemoglobin): 7.5 %
Glucose: 120 mg/dL
Another HbA1c (Glycosylated Hemoglobin): 6.8 %
Final Glucose result: 115 mg/dL
"""

# # Convert the document text to a Spacy document object
# file_path = "OCR_raw_samples/0ab9800e-bc9a-4388-aaa2-d4fc05e7d111.txt"
# with open(file_path, "r") as file:
#     text = file.read()
# doc = nlp(text)
doc = nlp(document_text)

# Load the synonyms data (example shown earlier)
# This part should actually load the JSON file, but for this example, we simulate the loaded data
synonyms_data = [
    {"Abbreviation": "HBA1C", "Synonyms": ["HbA1c", "Glycated Hemoglobin", "Glycohemoglobin", "A1c", "Hemoglobin A1c",
                                           "Hemoglobin A1c Test", "Hemoglobin A1c Level", "Glycosylated Hemoglobin",
                                           "A1c Test", "A1c Level"]},
    {"Abbreviation": "GLUC", "Synonyms": ["Glucose", "Blood Sugar", "Blood Glucose", "Dextrose", "Blood Sugar Level",
                                          "Serum Glucose", "Glycemia", "Glycose", "Blood Glucose Level", "Plasma Glucose"]}
]
# with open("OCR_raw_samples/X1.json", "r") as file:
#     synonyms_data = json.load(file)
    
# Add synonyms to the matcher
for item in synonyms_data:
    for synonym in item['Synonyms']:
        matcher.add(item['Abbreviation'], None, nlp(synonym))

# Find matches in the document
matches = matcher(doc)

# Create a dictionary to store the latest values for each parameter
latest_results = {}

# Extract values for matches
for match_id, start, end in matches:
    span = doc[start:end]  # The matched span
    param = nlp.vocab.strings[match_id]  # Get the parameter abbreviation from the match ID
    
    # Search in a window around the matched span for the numeric value and unit
    window = doc[max(start-5, 0):min(end+5, len(doc))]
    
    # Use regular expressions to find numeric values and units
    import re
    search_pattern = r'(\d+\.?\d*)\s*(\%|mg/dL)'
    for value, unit in re.findall(search_pattern, window.text):
        latest_results[param] = {"parameter": param, "value": float(value), "unit": unit}

# Convert results to JSON
results_json = json.dumps(list(latest_results.values()), indent=2)
print(results_json)