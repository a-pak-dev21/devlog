# Guest Data Cleaning Automation Script

## Description

This script automates the cleaning and preparation of guest arrival data stored in an Excel file (`.xlsx`). The original file contains multiple sheets, but only one ("Guests") is processed. The cleaned data is saved into a new Excel file for safe replacement of the original data.

## Functional Requirements

The script performs the following operations:

1. **Validate and clean names:**
   - Detects missing `FirstName` or cases where both names are in `LastName`.
   - Optionally logs rows needing manual name separation.

2. **Filter invalid birth dates:**
   - Removes rows where `DoB == "00.00.0000"`.

3. **Address field completion:**
   - Leaves valid addresses unchanged.
   - Fills missing addresses with country code + city (e.g. `"CN, Beijing"`) using randomized city choices.

4. **Visa validation:**
   - Uses a predefined list of nationalities requiring a visa.
   - Logs guests missing `VisaNumber` when it's required.

5. **Reason of traveling:**
   - Automatically sets `ReasonofTraveling = "10"` for all rows.

6. **Final output:**
   - A clean DataFrame is written into a new `.xlsx` file.
   - Original Excel styles and formatting are preserved using `openpyxl`.

## Usage

- Place the original `.xlsx` file in the project directory.
- Run the script locally.
- The cleaned Excel file will be saved as `cleaned_guests.xlsx`.
- Manually replace the data in the original file if needed, without affecting styles or layout.

## Logging

- A `log.txt` file is created to store all warnings and important notes (e.g. missing fields, rows skipped, etc.)

## Dependencies

- `pandas`
- `openpyxl`