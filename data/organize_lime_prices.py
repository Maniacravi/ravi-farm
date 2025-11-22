import pandas as pd
import re
from datetime import datetime

# Read the CSV with possible multiline fields
with open('data/lime_prices_vdx.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Join lines that are part of the same row (i.e., date fields split across lines)
rows = []
current_row = ''
for line in lines:
    if re.match(r'^\d+,', line) or line.startswith('"Sl'):
        if current_row:
            rows.append(current_row)
        current_row = line.strip('\n')
    else:
        current_row += ' ' + line.strip('\n')
if current_row:
    rows.append(current_row)

# Write to a temporary CSV for pandas to read
with open('data/lime_prices_vdx_cleaned.csv', 'w', encoding='utf-8') as f:
    for row in rows:
        f.write(row + '\n')

# Load with pandas
raw_df = pd.read_csv('data/lime_prices_vdx_cleaned.csv')

# Clean up the date column
raw_df['Price Date'] = raw_df['Price Date'].apply(lambda x: ' '.join(str(x).split()))
# Try to parse the date into a standard format
def parse_date(date_str):
    for fmt in ("%d %b %Y", "%d %B %Y"):  # e.g., 17 May 2025
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except Exception:
            continue
    return date_str
raw_df['Price Date'] = raw_df['Price Date'].apply(parse_date)

# Save the organized CSV
raw_df.to_csv('data/lime_prices_vdx_organized.csv', index=False)
print('Organized CSV saved as data/lime_prices_vdx_organized.csv')
