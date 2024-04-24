# To develop a pipeline, utilizing NLP-based approach that processes text data extracted via OCR from laboratory test results or medical records.
# The pipeline will include the following steps:
# Data Unstructuredness and OCR Faults: The input data will be highly unstructured with potential inaccuracies due to OCR errors.
# Uniformity in Units and Parameter Names: Ensure that units and parameter names match the specifications in the attached file X1.
# Parameter Uniqueness: Each parameter name must be unique within the dataset, discarding duplicates and retaining only the first instance.
# Date Sensitivity: Focus solely on the latest test results, disregarding earlier data to ensure relevance and accuracy.
# Data Integrity: Aim for a data integrity level exceeding 90% to ensure reliability.
# adhering to the specified format: [{"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}, ...]

# Importing the required libraries
import re
import json
from collections import defaultdict
from datetime import datetime
from typing import List, Dict

# Function to read the OCR text data from the input file
def read_ocr_data(file_path: str) -> str:
    with open(file_path, 'r') as file:
        ocr_data = file.read()
    return ocr_data

# Function to extract the test results from the OCR text data
def extract_test_results(ocr_data: str) -> List[str]:
    test_results = re.findall(r'Test Result:.*?(\d{2}-\d{2}-\d{4}).*?(\d{2}-\d{2}-\d{4}).*?(\d{2}-\d{2}-\d{4})', ocr_data, re.DOTALL)
    return test_results

# Function to extract the parameters, values, and units from the test results
def extract_parameters(test_results: List[str]) -> List[Dict[str, str]]:
    parameters = []
    for result in test_results:
        parameter_values = re.findall(r'(\w+): (\d+\.\d+) (\w+)', result)
        for parameter, value, unit in parameter_values:
            parameters.append({"parameter": parameter, "value": float(value),
                                "unit": unit})
    return parameters

# Function to filter the parameters based on the latest test date
def filter_latest_test(parameters: List[Dict[str, str]]) -> List[Dict[str, str]]:
    parameter_dict = defaultdict(list)
    for parameter in parameters:
        parameter_dict[parameter["parameter"]].append(parameter)
    latest_test_parameters = []
    for parameter_values in parameter_dict.values():
        latest_test = max(parameter_values, 
                          key=lambda x: datetime.strptime(x["date"], "%d-%m-%Y"))
        latest_test_parameters.append(latest_test)
    return latest_test_parameters

# Function to ensure uniformity in units and parameter names
def standardize_units_and_names(parameters: List[Dict[str, str]], 
                                standard_units: Dict[str, str], 
                                standard_names: Dict[str, str]) -> List[Dict[str, str]]:
    standardized_parameters = []
    for parameter in parameters:
        parameter["unit"] = standard_units.get(parameter["unit"], 
                                               parameter["unit"])
        parameter["parameter"] = standard_names.get(parameter["parameter"], 
                                                    parameter["parameter"])
        standardized_parameters.append(parameter)
    return standardized_parameters

# Function to ensure parameter uniqueness
def unique_parameters(parameters: List[Dict[str, str]]) -> List[Dict[str, str]]:
    unique_parameter_dict = {}
    for parameter in parameters:
        if parameter["parameter"] not in unique_parameter_dict:
            unique_parameter_dict[parameter["parameter"]] = parameter
    unique_parameters = list(unique_parameter_dict.values())
    return unique_parameters

# Function to calculate data integrity level
def calculate_data_integrity(parameters: List[Dict[str, str]]) -> float:
    unique_parameters_count = len(unique_parameters)
    total_parameters_count = len(parameters)
    data_integrity = unique_parameters_count / total_parameters_count
    return data_integrity

# Function to create the final output in the specified format
def create_output(unique_parameters: List[Dict[str, str]]) -> str:
    output = json.dumps(unique_parameters, indent=4)
    return output

# Main function to execute the pipeline
def main(file_path: str) -> str:
    ocr_data = read_ocr_data(file_path)
    test_results = extract_test_results(ocr_data)
    parameters = extract_parameters(test_results)
    latest_test_parameters = filter_latest_test(parameters)
    standard_units = {"mmol/mL": "mmol/L", "mg/dL": "mmol/L"}
    standard_names = {"glucose": "blood glucose",
                       "cholesterol": "total cholesterol"}
    standardized_parameters = standardize_units_and_names(latest_test_parameters, 
                                                          standard_units, 
                                                          standard_names)
    unique_parameters = unique_parameters(standardized_parameters)
    data_integrity = calculate_data_integrity(unique_parameters)
    output = create_output(unique_parameters)
    return output
    # return test_results

# Example usage of the main function
file_path = "/Users/proteeksanyal/Desktop/Learning/Medical_OCR/OCR_raw_samples/0ab9800e-bc9a-4388-aaa2-d4fc05e7d111.txt"
output = main(file_path)
print(output)

