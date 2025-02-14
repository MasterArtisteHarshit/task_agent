
import os
from datetime import datetime

def get_recent_logs():
    logs_dir = "/data/logs"
    output_file = "/data/logs-recent.txt"
    
    try:
        # Get all .log files with their modification times
        log_files = []
        for filename in os.listdir(logs_dir):
            if filename.endswith('.log'):
                file_path = os.path.join(logs_dir, filename)
                mod_time = os.path.getmtime(file_path)
                log_files.append((file_path, mod_time))
        
        # Sort by modification time (most recent first) and get top 10
        recent_logs = sorted(log_files, key=lambda x: x[1], reverse=True)[:10]
        
        # Extract first line from each file and write to output
        with open(output_file, 'w') as out_f:
            for log_path, _ in recent_logs:
                try:
                    with open(log_path, 'r') as log_f:
                        first_line = log_f.readline().strip()
                        out_f.write(f"{first_line}\n")
                except Exception as e:
                    print(f"Error reading {log_path}: {str(e)}")
                    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    get_recent_logs()