# /(\w+) \((<\s*\d+|\d+\.\d+-\d+\.\d+|\d+-\d+)\) (\w+)
                                                

# remove new line from text file and save to a new file
# with open("OCR_raw_samples/0ab9800e-bc9a-4388-aaa2-d4fc05e7d111.txt", "r") as file:
#     data = file.read().replace("\n", " ")
# with open("0ab9800e-bc9a-4388-aaa2-d4fc05e7d111_new.txt", "w") as file:
#     file.write(data)


# regex
# (\w+ \(\d+.\d+.\d+.\d+\) \w+.*$)
# (\w+ \(\d+.\d+\) \w+.*$)
# (\w+ \w \d+ \w+.*$)

import spacy
from spacy.pipeline import EntityRuler
import json

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

# Function to process the document
def process_document(file_path):
    with open(file_path, "r") as file:
        text = file.read()
    doc = nlp(text)
    results = []

    # Logic to extract parameters, values, and units
    import pdb; pdb.set_trace()
    for ent in doc.ents:
        if ent.label_ == "TEST":
            # Find the next token that is a digit (value) and the following unit
            next_token = doc[ent.end].nbor()
            if next_token.like_num:
                value = next_token.text
                try:
                    unit = next_token.nbor().text
                except:
                    unit = "N/A"
                results.append({"parameter": ent.text, "value": value, "unit": unit})

    return results

# Example usage
file_path = "OCR_raw_samples/0b8706dc-c9af-4c6b-887d-2f85b5a511e7.txt"
output = process_document(file_path)
print(json.dumps(output, indent=2))

