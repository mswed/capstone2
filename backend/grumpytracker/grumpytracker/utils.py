from typing import Dict, List, Any, Optional


def validate_required_fields(
    data: Dict[str, Any], required_fields: List
) -> Optional[str]:
    for field in required_fields:
        if not data.get(field):
            return f"{field} is required"

    return None
