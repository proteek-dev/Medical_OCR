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

## Explaination

#### File: extract.py
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

# Load custom rules
add_custom_rules()
```
