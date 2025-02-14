
import json
import os

def sort_contacts():
    # Define input and output paths
    input_path = "/data/contacts.json"
    output_path = "/data/contacts-sorted.json"
    
    try:
        # Read the contacts file
        with open(input_path, 'r') as f:
            contacts = json.load(f)
        
        # Sort contacts by last_name, then first_name
        sorted_contacts = sorted(
            contacts,
            key=lambda x: (x['last_name'].lower(), x['first_name'].lower())
        )
        
        # Write sorted contacts to new file
        with open(output_path, 'w') as f:
            json.dump(sorted_contacts, f, indent=2)
            
    except FileNotFoundError:
        print(f"Error: {input_path} not found")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {input_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    sort_contacts()