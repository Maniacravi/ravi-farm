
import pdfplumber
import pandas as pd

pdf_path = "data/lime_prices_vdx.pdf"
csv_path = "data/lime_prices_vdx.csv"

all_rows = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                all_rows.append(row)

# Remove empty rows and deduplicate header if present
clean_rows = [row for row in all_rows if any(cell is not None and str(cell).strip() != '' for cell in row)]
if len(clean_rows) > 1 and clean_rows[0] == clean_rows[1]:
    clean_rows = [clean_rows[0]] + clean_rows[2:]

df = pd.DataFrame(clean_rows[1:], columns=clean_rows[0])
df.to_csv(csv_path, index=False)
print(f"CSV file created successfully: {csv_path}")
