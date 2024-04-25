import re

def extract_data(file_path):
    # Regular expression to find patterns like: Name (Unit) Value
    pattern = re.compile(r"(\w+)\s+\(([^)]+)\)\s+(\d+\.?\d*)")

    results = []

    with open(file_path, 'r') as file:
        for line in file:
            matches = pattern.findall(line)
            for match in matches:
                param, unit, value = match
                # Avoid duplicates by ensuring the parameter isn't already added
                if not any(res['parameter'] == param for res in results):
                    results.append({
                        'parameter': param,
                        'value': float(value),
                        'unit': unit
                    })

    return results




# Path to the file containing the lab test results
file_path = "/Users/proteeksanyal/Desktop/Learning/Medical_OCR/OCR_raw_samples/0ab9800e-bc9a-4388-aaa2-d4fc05e7d111.txt"
data = extract_data(file_path)
print(data)

# ocr_file = "/Users/proteeksanyal/Desktop/Learning/Medical_OCR/OCR_raw_samples/0ab9800e-bc9a-4388-aaa2-d4fc05e7d111.txt"
# with open(ocr_file, "r") as file:
#     ocr_text = file.read()

