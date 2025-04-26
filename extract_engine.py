import re

# Function to accept the user's radiology report and extract data
def extract_organ_and_anatomy(text):
    organ_patterns = [
        r"MRI of the (\w+)", r"CT of the (\w+)", r"(\w+) region", r"in the (\w+ \w+ lobe)",
        r"in the (\w+ \w+ region)", r"in the (\w+ lobe)"
    ]
    for pattern in organ_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()
    return "Unknown"

# Function to extract dimensions (length, width, height) from the report
def extract_dimensions(text):
    dim_patterns = [
        r'(\d+(?:\.\d+)?)\s*[x×*]\s*(\d+(?:\.\d+)?)\s*[x×*]\s*(\d+(?:\.\d+)?)\s*cm',
        r'measures approximately (\d+(?:\.\d+)?)\s*cm'
    ]
    for pattern in dim_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            dims = list(map(float, match.groups()))
            while len(dims) < 3:
                dims.append(None)
            return dims
    return [None, None, None]

# Function to detect specific findings (tumors, cysts, etc.)
def extract_findings_with_size(text):
    findings = []
    keywords = {
        "tumor": r"(tumor|mass|neoplasm).*?(\d+(?:\.\d+)?\s*cm)?",
        "cyst": r"(cyst).*?(\d+(?:\.\d+)?\s*cm)?",
        "stone": r"(stone|calculus).*?(\d+(?:\.\d+)?\s*cm)?",
        "cancer": r"(cancer|carcinoma|malignancy).*?(\d+(?:\.\d+)?\s*cm)?",
        "lesion": r"(lesion).*?(\d+(?:\.\d+)?\s*cm)?",
        "granuloma": r"(granuloma).*?(\d+(?:\.\d+)?\s*cm)?"
    }
    for label, pattern in keywords.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            size = match.group(2) if match.group(2) else "unknown size"
            findings.append(f"{label.capitalize()} detected (Size: {size.strip()})")
    return findings or ["None detected"]

# Convert biological units to Blender units (example: 1 cm = 0.01 m)
def convert_to_blender_units(length, width, height):
    return [length * 0.01 if length else None,
            width * 0.01 if width else None,
            height * 0.01 if height else None]

# Function to get the user's input report and extract information
def process_report(user_input):
    text_report = user_input

    # Extracting results
    organ = extract_organ_and_anatomy(text_report)
    length, width, height = extract_dimensions(text_report)
    findings = extract_findings_with_size(text_report)

    # Convert to Blender units
    blender_units = convert_to_blender_units(length, width, height)

    # Final output
    print(f"🧠 Organ/Region: {organ}")
    print(f"📅 Report Date: {text_report.strip().split('.')[0]}")
    print(f"📐 Dimensions (Biological Units in cm):")
    print(f"  - Length = {length if length else 'Not provided'} cm")
    print(f"  - Width = {width if width else 'Not provided'} cm")
    print(f"  - Height = {height if height else 'Not provided'} cm")
    print(f"📏 Dimensions (Blender Units in meters):")
    print(f"  - Length = {blender_units[0] if blender_units[0] else 'Not provided'} m")
    print(f"  - Width = {blender_units[1] if blender_units[1] else 'Not provided'} m")
    print(f"  - Height = {blender_units[2] if blender_units[2] else 'Not provided'} m")

    print("🩺 Findings:")
    for finding in findings:
        print(f"  - {finding}")

    condition_summary = "The report indicates the presence of the following conditions:\n"
    condition_summary += "  - " + "\n  - ".join([finding for finding in findings if "detected" in finding])
    print(f"\n🔑 *Condition Summary:*\n{condition_summary}")

# Example usage
if __name__ == "__main__":
    user_input = input("Please paste your medical radiology report here: ")
    process_report(user_input)