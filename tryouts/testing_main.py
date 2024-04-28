import spacy
from spacy.matcher import Matcher
import json

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize the matcher with the vocab
matcher = Matcher(nlp.vocab)

# Initialize the entity ruler
ruler = nlp.add_pipe("entity_ruler", before="ner")

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

def add_matcher_patterns():
    # Define the pattern for matching units
    pattern = [{"LOWER": {"IN": ["iu", "g", "mmol", "u"]}}, {"TEXT": "/"}, {"LOWER": {"IN": ["ml", "l"]}}]
    matcher.add("unit", [pattern])

# Add the matcher patterns
add_matcher_patterns()

def extract_information(doc_nlp):
    # Loop through sentences to check entities and units
    for sent in doc_nlp.sents:
        # Initialize unit found flag
        unit_found = False
        
        # Find matches for the unit pattern in the current sentence
        matches = matcher(sent)
        units = [sent[start:end].text for match_id, start, end in matches]

        # Check for "TEST" label and next number token
        for ent in sent.ents:
            if ent.label_ == "TEST":
                end_position = ent.end
                # Check the next token if it's a number and not out of bounds
                if end_position < len(sent) and sent[end_position].like_num:
                    next_token = sent[end_position]
                    # Check if units were found in the sentence
                    if units:
                        for unit in units:
                            print(f"{ent.text} {next_token} {unit}")
                            unit_found = True
                    # If no units were found, print "no unit"
                    if not unit_found:
                        print(f"{ent.text} {next_token} no unit")
                        break  # Avoids multiple prints if no units are found

def process_document(file_path):
    with open(file_path, "r") as file:
        text = file.read()
    doc = nlp(text)
    extract_information(doc)

# Path to the text file
# file_path = "OCR_raw_samples/0b8706dc-c9af-4c6b-887d-2f85b5a511e7.txt"
file_path = "OCR_raw_samples/0ab9800e-bc9a-4388-aaa2-d4fc05e7d111.txt"
process_document(file_path)
