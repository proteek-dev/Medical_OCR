import os
import re
import sys
import json
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

ruler = nlp.add_pipe("entity_ruler", before="ner")

matcher = Matcher(nlp.vocab)

# Adding custom rules based on the synonyms in JSON
def add_custom_rules():
    with open("OCR_raw_samples/X1.json", "r") as file:
        data = json.load(file)
        patterns = []
        for entry in data:
            for synonym in entry["Synonyms"]:
                patterns.append({"label": "TEST", "pattern": synonym})
        # print(patterns)
        ruler.add_patterns(patterns)

# Load custom rules
# add_custom_rules()

def add_matcher_patterns(matcher):
    # Define the pattern for matching units
    pattern = [{"LOWER": {"IN": ["iu", "g", "mmol", "u"]}},
                {"TEXT": "/"}, {"LOWER": {"IN": ["ml", "l"]}}]
    matcher.add("unit", [pattern])

# To process units
def process_units(units):
    for unit in units:
        doc = nlp(unit)
        matches = matcher(doc)
        if matches:
            return unit  # Return the first matched unit
    return None  # Return None if no units match

# To determine if a string is a date
def is_date(string):
    return bool(re.match(r'\d{2}-\d{2}-\d{4}', string))

def process_file(file_path):

    with open(file_path, 'r') as file:
        data = file.read().replace("\n", " ")
    doc = nlp(data)

    # Dictionary to store drug parameters, values, and units
    drug_data = {}

    for ent in doc.ents:
        if ent.label_ == "TEST":
            # Start a new entry for this parameter if it doesn't exist
            if ent.text not in drug_data:
                drug_data[ent.text] = {"values": [], "units": []}
            # Focus on this parameter for subsequent values and units
            current_parameter = ent.text

        elif ent.label_ == "CARDINAL" and "current_parameter" in locals():
            # Append value to the current parameter
            drug_data[current_parameter]["values"].append(ent.text)

        elif ent.label_ == "ORG" and "current_parameter" in locals():
            # Append unit to the current parameter
            drug_data[current_parameter]["units"].append(ent.text)

    file_name = filepath.split("/")[-1].split(".")[0]
    # return drug_data, file_name
    result = convert_drug_data_to_format(drug_data)
    save_output(result, file_name)

def convert_drug_data_to_format(drug_data):

    add_matcher_patterns(matcher)

    # Convert drug_data to the required format
    output_data = []
    for drug, details in drug_data.items():
        # Filter out dates and get the last non-date value
        values = [v for v in details['values'] if not is_date(v)]
        last_value = values[-1] if values else None

        # Process units
        processed_unit = process_units(details['units'])

        output_data.append({
            "parameter": drug,
            "value": last_value,
            "unit": processed_unit.split(" ")[0] if processed_unit else None
        })

    # Output the list of dictionaries
    print(output_data)
    return output_data

def save_output(output_data, file_name):
    output_folder = "Output"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, file_name + ".json")
    with open(output_file, 'w') as json_file:
        json_file.write(json.dumps(output_data, indent=4))

    
if __name__ == "__main__":
    # get file from sys.argv
    if len(sys.argv) < 2:
        print("Please provide a file path to process")
        sys.exit(1)
    add_custom_rules()
    filepath = sys.argv[1]
    process_file(filepath)