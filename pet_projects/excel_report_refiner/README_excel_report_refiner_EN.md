
# Excel Report Refiner — Automating Excel Data Cleaning

The script `excel_table_automatization.py` automatically **cleans, validates, and standardizes Excel tables** (guest lists, reports, exports) while **preserving the original structure and styles** where possible.  
It was built to eliminate repetitive manual work and reduce human errors when handling messy Excel data.

> TL;DR: Takes a *raw* Excel file → cleans and normalizes data → outputs a standardized version ready for reporting.

---

## ✨ Features

- **String normalization** — trims spaces, fixes capitalization in names, unifies addresses.  
- **Date correction** — detects various formats and converts them to ISO `YYYY-MM-DD`.  
- **Email & phone validation** — removes invalid characters and ensures consistent formatting.  
- **Column renaming** — maps different column aliases to one unified schema.  
- **Duplicate removal** — optional filtering by selected fields (e.g., name + birth date).  
- **Style preservation** — keeps original sheet formatting (via `openpyxl` + `pandas`).  
- **Change log** — generates a report summarizing all corrections and removed duplicates.  

> **Example use case:** Cleaning guest lists from multiple sources with inconsistent date and name formats into one clean report — ready to send or analyze.

---

## 🧩 Tech Stack

- **Python 3.11+**  
- Libraries: `pandas`, `openpyxl`, `python-dateutil`, `pathlib`, `re`, `logging`

---

## ⚙️ Installation

```bash
# 1) Clone or copy the project folder
git clone https://github.com/a-pak-dev21/devlog.git
cd devlog/pet_projects/excel_report_refiner

# 2) Create and activate a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt  # if present
# or:
pip install pandas openpyxl python-dateutil
```

> 💡 Always work on a copy of your original Excel file.

---

## ▶️ Quick Start

Run the script from your terminal:

```bash
python excel_table_automatization.py --input "/path/to/raw.xlsx" --sheet "Guests" --output "/path/to/clean.xlsx"
```

**Main arguments:**

| Flag | Description |
|------|--------------|
| `--input` | Path to the source Excel file |
| `--sheet` | Sheet name (defaults to the active one) |
| `--output` | Output path (defaults to `<filename>_cleaned.xlsx`) |
| `--dedupe-by` | Comma-separated fields to deduplicate by |
| `--locale` | Region/language preset (e.g. `cz`, `en`) |
| `--log` | Path for saving the process log |

**Example:**
```bash
python excel_table_automatization.py   --input "./samples/guests_raw.xlsx"   --sheet "List"   --dedupe-by "first_name,last_name,date_of_birth"   --output "./out/guests_clean.xlsx"   --log "./out/clean.log"
```

---

## 🔍 What the Script Does

1. **Columns**
   - Renames inconsistent headers to standardized names.
   - Removes empty columns and trims header spaces.  
2. **Rows**
   - Trims extra spaces, fixes capitalization (`pak artem` → `Artem Pak`).  
3. **Dates**
   - Detects formats like `DD.MM.YYYY`, `MM/DD/YY`, text-based dates.  
   - Converts to ISO `YYYY-MM-DD` using flexible parsing.  
4. **Contacts**
   - Normalizes phone numbers (removes spaces, dashes) and validates emails.  
5. **Duplicates**
   - Optional deduplication by user-defined keys.  
6. **Logs**
   - Summarizes how many values were cleaned, fixed, or removed.

---

## 📁 Project Structure

```
excel_report_refiner/
├─ excel_table_automatization.py   # main script
├─ requirements.txt                # dependencies (optional)
├─ samples/                        # example raw files
└─ out/                            # cleaned files and logs
```

---

## 🧪 Testing

You can place messy Excel files (like `guests_raw.xlsx`) in the `samples/` folder  
and verify that the script outputs consistent and well-formatted reports in `/out`.

---

## 🧾 Logging Example

Each run generates a log file summarizing actions performed:
```
[INFO] 2025-10-05 12:34:56 — normalized 217 names, fixed 143 dates, removed 12 duplicates (keys: first_name,last_name,date_of_birth)
```

---

## 🧱 Recommended Config Example (optional)

If you want to manage cleaning rules externally, use a YAML config file like:

```yaml
columns:
  aliases:
    first_name: ["First Name", "Имя", "fname"]
    last_name:  ["Last Name", "Фамилия", "lname"]
dates:
  target_format: "%Y-%m-%d"
  dayfirst: true
phones:
  country_code: "+420"
  enforce_e164: true
```

---

## 🚀 Roadmap

- [ ] Config file for column and date rules  
- [ ] Dry-run mode (report only)  
- [ ] Unit tests for normalization functions  
- [ ] Dockerfile for reproducibility  
- [ ] Locale presets (CZ/PL/EU)  
- [ ] CLI flags for strict/soft validation  

---

## ❓ FAQ

**Will it change Excel styles?**  
The script attempts to preserve styles. Minor formatting differences may occur when saving via `pandas`/`openpyxl`.

**Are password-protected files supported?**  
Not currently — please remove protection before processing.

**Can it handle `.xls` files?**  
Convert to `.xlsx` first for best results.

---

## 📜 License

MIT License — free to use and modify for personal or commercial purposes.

---

## 👤 Author

**Artem Pak** — Python Developer (Automation & Data)  
GitHub: [https://github.com/a-pak-dev21](https://github.com/a-pak-dev21)
