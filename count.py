
from datetime import datetime
import os

def main():
    # Ensure data directory exists
    data_dir = os.path.abspath("/data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    input_path = os.path.join(data_dir, "dates.txt")
    output_path = os.path.join(data_dir, "dates-wednesdays.txt")
    
    try:
        with open(input_path, 'r') as f:
            dates = f.readlines()
        
        wednesday_count = 0
        for date_str in dates:
            date_str = date_str.strip()
            try:
                # Try each possible date format
                for fmt in ["%Y-%m-%d", "%d-%b-%Y", "%b %d, %Y", "%Y/%m/%d %H:%M:%S"]:
                    try:
                        date_obj = datetime.strptime(date_str, fmt)
                        if date_obj.weekday() == 2:  # Wednesday is 2
                            wednesday_count += 1
                        break
                    except ValueError:
                        continue
            except Exception:
                continue
        
        # Write the count to the output file
        with open(output_path, 'w') as f:
            f.write(str(wednesday_count))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()