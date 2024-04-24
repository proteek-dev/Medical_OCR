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

