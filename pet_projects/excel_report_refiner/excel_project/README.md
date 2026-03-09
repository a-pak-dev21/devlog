
# **Excel Table Automatization**

Automated Excel data cleaning and validation tool designed for internal workflow automation.  
Originally built to standardize guest data in hospitality workflows using an embedded Python runtime — works both as a standalone script and as part of a Windows batch-based deployment.

---

## 🧩 **Overview**

This script processes and refines Excel tables by:
- **Cleaning invalid or incomplete data**
- **Filling missing fields**
- **Validating and reformatting dates**
- **Reconstructing address columns using reference data**
- **Preserving original Excel formatting**

The program ensures the output file keeps the same layout and cell styling as the source document, while the data itself becomes fully standardized and ready for reporting or archiving.

---

## ⚙️ **Main Functionality**

| Task | Description |
|------|--------------|
| 🧍 Name handling | Checks if `first_name` is missing. If `last_name` contains two words, it splits and fills the name column with the second part. Otherwise, removes the row. |
| 📅 Date of birth | Removes rows with invalid birthdates (e.g., `00.00.0000`). |
| 🎯 Purpose of visit | Fills empty `purpose` cells with value `10`. |
| 🛂 Visa requirement | If citizenship belongs to a visa-obligated country **and** visa column is empty → row is removed. |
| 🏠 Address reconstruction | Modifies and completes the address column using data from `addresses_data.csv` and randomization logic to ensure natural results. |
| 🔢 Passport validation | Removes invalid passport numbers (non-matching pattern `XXXXX` or length < 5). |
| 📆 Date normalization | Converts string or Excel date objects to consistent format for `arrival` and `departure` columns. |
| 💾 Excel rewrite | Uses `openpyxl` to overwrite the original sheet row-by-row with the cleaned DataFrame, keeping styles intact. Then removes extra empty rows below the table. |

---

## 🧱 **Project Structure**

```
excel_report_refiner/
├── build/                     # build artifacts for Windows portable version
├── data/                      # reference datasets (addresses_data.csv, visa_obligated.csv)
├── dist/                      # distribution folder for embedded Python build
├── draft/                     # working directory with main editable file
├── excel_project/             # embedded project root for Windows deployment
├── excel_table_automatization.py   # main script
├── excel_table_automatization.spec # PyInstaller spec file
├── logs/                      # execution logs
├── venv_cleaner/              # helper for environment cleanup
└── README.md                  # this file
```

---

## 🧠 **Key Components**

| File / Folder | Purpose |
|----------------|----------|
| `excel_table_automatization.py` | Core script performing validation, cleanup, rewriting |
| `data/addresses_data.csv` | Contains ISO3 codes and corresponding example cities for address generation |
| `data/visa_obligated.csv` | List of countries (ISO3 codes) requiring a visa |
| `logs/` | Saves runtime logs and summary reports |
| `build/`, `dist/`, `excel_project/` | Output structure for embedded Windows deployment |
| `venv_cleaner/` | Utility for removing cached or unused dependencies |

---

## ▶️ **Usage**

### 🔹 Option 1 — Local Python environment
```bash
python excel_table_automatization.py
```
> Requires `pandas`, `openpyxl`, `datetime`, `csv`, `random`, and `logging`.

### 🔹 Option 2 — Embedded Windows package
If running on a Windows workstation without Python installed:  
Launch the program via `run_excel_cleaner.bat` (included in the `excel_project/` build).  
This version uses a portable embedded Python interpreter and runs fully offline.

---

## 🧾 **Logging**

All operations are logged to `/logs/` including:
- Start and finish time  
- Number of processed and deleted rows  
- Categories of corrections (names, dates, visas, passports, etc.)  
- Any exceptions or skipped rows  

Example log entry:
```
[INFO] 2025-10-06 15:14:22 — cleaned 214 rows, removed 17 invalid DOB, dropped 5 visa-missing citizens.
```

---

## 🧪 **Data Dependencies**

Both datasets are stored in the `/data/` folder in simple **CSV** format.

**addresses_data.csv**
```
ISO3,city
SVK,Bratislava
SVK,Kosice
SVK,Trencin
DEU,Berlin
DEU,Hamburg
DEU,Leipzig
```

**visa_obligated.csv**
```
ISO3
UKR
RUS
IND
CHN
```

---

## 🧰 **Libraries**

- `pandas`
- `openpyxl`
- `pathlib`
- `datetime`
- `csv`
- `random`
- `logging`
- `re`

---

## 📦 **Deployment Notes**

This project was adapted for **embedded Python** on Windows (no system-wide interpreter required).  
The build process uses `PyInstaller` and creates a self-contained directory with `.exe` and `.bat` launchers.  
Useful for closed corporate systems with no external package installation allowed.

---

## 📜 **License**

MIT License — free for internal or personal use.

---

## 👤 **Author**

**Artem Pak** — Python Developer (Automation & Data Processing)  
GitHub: [https://github.com/a-pak-dev21](https://github.com/a-pak-dev21)
