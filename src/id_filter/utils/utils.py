import json

def better_display_json(j)->str:
    return json.dumps(j, indent=2, separators=(",", ": "))