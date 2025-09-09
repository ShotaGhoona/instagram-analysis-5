import json
from datetime import datetime
from typing import Dict, Any

def save_output(data: Dict[str, Any], filename: str) -> None:
    """Save API response data to outputs directory"""
    filepath = f"outputs/{filename}"
    
    # Add metadata
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "data": data
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Output saved to: {filepath}")

def format_json_output(data: Dict[str, Any]) -> str:
    """Format JSON data for console output"""
    return json.dumps(data, indent=2, ensure_ascii=False)