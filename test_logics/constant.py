FILEPATH = "OCR_raw_samples/0ab9800e-bc9a-4388-aaa2-d4fc05e7d111.txt"

import spacy
from spacy.tokens import Span
import re
import json
from datetime import datetime

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Create a new EntityRuler and add it to the pipeline with a custom name
ruler = nlp.add_pipe("entity_ruler", before="ner")

# Function to add custom rules based on the synonyms in JSON
def add_custom_rules():
    with open("OCR_raw_samples/X1.json", "r") as file:
        data = json.load(file)
        patterns = []
        for entry in data:
            for synonym in entry["Synonyms"]:
                patterns.append({"label": "TEST", "pattern": synonym})
        ruler.add_patterns(patterns)

# Load custom rules
add_custom_rules()

# Function to preprocess the text to add custom spans for dates
def preprocess_dates(doc):
    date_pattern = re.compile(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b')
    for match in date_pattern.finditer(doc.text):
        start, end = match.span()
        span = Span(doc, start=start, end=end, label="DATE")
        doc.ents = list(doc.ents) + [span]
    return doc

# Add the preprocessing function to the pipeline
nlp.add_pipe(preprocess_dates, before="ner")

# Function to parse and sort dates
def parse_date(text):
    try:
        return datetime.strptime(text, "%d/%m/%Y")
    except ValueError:
        return None

# Function to process the document and extract latest results
def extract_latest_results(file_path):
    with open(file_path, "r") as file:
        text = file.read()
    doc = nlp(text)

    # Finding the latest date mentioned in the text
    dates = [parse_date(ent.text) for ent in doc.ents if ent.label_ == "DATE" and parse_date(ent.text)]
    if not dates:
        return "No dates found in the document."

    latest_date = max(dates)

    # Extracting results associated with the latest date
    results = []
    for ent in doc.ents:
        if ent.label_ in ["CHEMICAL", "QUANTITY"]:
            # Check for nearest previous date entity
            prev_date = max([d for d in dates if d <= latest_date], default=None)
            if prev_date and (latest_date == prev_date):
                value = next(doc[ent.end:].sent, None)
                if value:
                    results.append({"parameter": ent.text, "value": value.text, "date": latest_date.strftime("%Y-%m-%d")})
    return results

# Example usage
file_path = FILEPATH
output = extract_latest_results(file_path)
print(output)
