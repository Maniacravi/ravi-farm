import csv
import datetime

# Data provided by the user for Thalavaipuram
raw_data = """6 Nov	Lime	16000	22000	22000
4 Nov	Lime	16000	22000	22000
2 Nov	Lime	16000	22000	22000
1 Nov	Lime	16000	22000	22000
31 Oct	Lime	16000	22000	22000
30 Oct	Lime	16000	22000	22000
28 Oct	Lime	21000	22000	22000
27 Oct	Lime	19000	20000	20000
24 Oct	Lime	16000	20000	20000
23 Oct	Lime	16000	20000	20000
22 Oct	Lime	16000	20000	20000
19 Oct	Lime	16000	20000	20000
16 Oct	Lime	16000	20000	20000
14 Oct	Lime	15000	17000	17000
13 Oct	Lime	15000	17000	17000"""

csv_file_path = '/Users/manikandanravi/Code/ravi-farm/data/lime_prices_vdx_organized.csv'
year = 2025

def parse_date(date_str):
    # Format: "6 Nov" -> datetime object
    return datetime.datetime.strptime(f"{date_str} {year}", "%d %b %Y").strftime("%Y-%m-%d")

def get_last_sl_no(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        last_line = lines[-1].strip()
        if not last_line:
             # Try the line before if the last line is empty
            last_line = lines[-2].strip()
        
        try:
            return int(last_line.split(',')[0])
        except ValueError:
             # Handle case where header is the only line or file is empty/malformed
            return 0

def main():
    last_sl_no = get_last_sl_no(csv_file_path)
    print(f"Last Sl no: {last_sl_no}")

    new_rows = []
    current_sl_no = last_sl_no + 1

    lines = raw_data.strip().split('\n')
    # Reverse to have chronological order (Oct 13 -> Nov 6)
    lines.reverse() 

    for line in lines:
        parts = line.split('\t')
        if len(parts) < 5:
            continue
        
        date_str = parts[0]
        # commodity = parts[1] # Lime
        min_price = parts[2]
        max_price = parts[3]
        modal_price = parts[4]
        
        formatted_date = parse_date(date_str)
        
        row = [
            current_sl_no,
            "Virudhunagar",
            "Thalavaipuram(Uzhavar Sandhai )",
            "Lime",
            "Lime",
            "Local",
            min_price,
            max_price,
            modal_price,
            formatted_date
        ]
        new_rows.append(row)
        current_sl_no += 1

    with open(csv_file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)
    
    print(f"Appended {len(new_rows)} rows.")

if __name__ == "__main__":
    main()
