# Medical_OCR

## Problem statement
To develop a pipeline utilizing NLP-based approach, which can transform unstructured, potentially faulty OCR output into a structured Python list of dictionaries, adhering to the specified format:
[{"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}, ...]

### Key Considerations
- Data Unstructuredness and OCR Faults: The input data will be highly unstructured with potential inaccuracies due to OCR errors.
- Uniformity in Units and Parameter Names: Ensure that units and parameter names match the specifications in the attached file X1.
- Parameter Uniqueness: Each parameter name must be unique within the dataset, discarding duplicates and retaining only the first instance.
- Date Sensitivity: Focus solely on the latest test results, disregarding earlier data to ensure relevance and accuracy.
- Data Integrity: Aim for a data integrity level exceeding 90% to ensure reliability.


## Challenges
- OCR data recieved is unstructured medical Data.
- Defining which entries are relavent when structuring data.
- Creating Name-entity relationship.
- Adding new rule according to the pattern to the Spacy model.
- Extracting Unit Pattern from the file.


## Description
A pipeline which utilizing NLP-based approach, that processes text data extracted via OCR from laboratory test results or medical records. It transforms the unstructured & potentially faulty OCR output into a structured json format. All the unstructured raw samples are in [OCR_raw_samples](OCR_raw_samples), and after the processing of medical records all the output are stored in [Output](Output).

## Explaination

#### File: [Main](main.py)
##### Description; 
We use Spacy library of NLP to extract information from the medical OCR document. As we are provided with X1.json file with all the parameters specification which is needed to be identified from the unstructured medical document. We create a Entity Ruler to add custom rules to the NLP Pipeline, which creates a label pattern for all the "Synonyms" mentioned in X1.json file. 
```
# Function to add custom rules based on the synonyms in JSON
def add_custom_rules():
    with open("OCR_raw_samples/X1.json", "r") as file:
        data = json.load(file)
        patterns = []
        for entry in data:
            for synonym in entry["Synonyms"]:
                patterns.append({"label": "TEST", "pattern": synonym})
        ruler.add_patterns(patterns)
```
There is a pattern matcher for matching units of the "Synonyms". This function is used when all the data has been extracted from the files and to identify unit of the medical term.
```
def add_matcher_patterns(matcher):
    # Define the pattern for matching units
    pattern = [{"LOWER": {"IN": ["iu", "g", "mmol", "u"]}},
                {"TEXT": "/"}, {"LOWER": {"IN": ["ml", "l"]}}]
    matcher.add("unit", [pattern])
```
In function process_file, a dictionary called drug_data stores each parameter defined by "TEST" label along with lists of its values and units. This structure makes it easy to add new values and units to each parameter.
**Efficiency** By checking if a parameter already exists before creating a new entry, this code avoids duplicating parameters and simplifies adding values and units.
**Scoping:** The variable current_parameter is used to keep track of the current drug parameter being processed. It helps in associating values and units correctly, assuming the data follows a logical order (parameter first, then values, then units). If the sequence is disrupted, current_parameter helps prevent incorrect associations.
**Error Handling:** This code assumes that the sequence of parameters, values, and units in the document is orderly and consistent. If this might not be the case, additional error handling could be added to check for missing data or mismatches.
```
drug_data = {}

for ent in doc.ents:
        if ent.label_ == "TEST":
            # a new entry for this parameter if it doesn't exist
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
```
