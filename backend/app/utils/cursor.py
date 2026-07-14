import base64
import json
from datetime import datetime
from uuid import UUID

from app.exceptions.custom_exceptions import BadRequestException


def encode_cursor(
    sort_value,
    record_id: UUID,
    sort_by: str,
    sort_order: str
) -> str:

    if isinstance(sort_value, datetime):
        sort_value = sort_value.isoformat()

    cursor_data = {
        "sort_value": sort_value,
        "record_id": str(record_id),
        "sort_by": sort_by,
        "sort_order": sort_order
    }

    json_data = json.dumps(cursor_data)
    bytes_data = json_data.encode("utf-8")

    return base64.urlsafe_b64encode(
        bytes_data
    ).decode("utf-8")


def decode_cursor(cursor: str) -> dict:
    try:
        bytes_data = base64.urlsafe_b64decode(
            cursor.encode("utf-8")
        )

        json_data = bytes_data.decode("utf-8")
        cursor_data = json.loads(json_data)

        cursor_data["record_id"] = UUID(
            cursor_data["record_id"]
        )

        return cursor_data

    except Exception as exc:
        raise BadRequestException(
            "Invalid cursor"
        ) from exc