import json
from pathlib import Path

def clean_profiles():
    path = Path(r"c:\git\gh-copilot-demo\tools\data\toy_profiles.json")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        if 'owner_oid' in item:
            del item['owner_oid']
            
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Cleaned toy_profiles.json")

if __name__ == "__main__":
    clean_profiles()
