import uuid
from pathlib import Path

from fastapi import UploadFile


UPLOAD_DIR = Path("uploads/resumes")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def save_resume(
    file: UploadFile
) -> tuple[str, str]:

    extension = Path(
        file.filename
    ).suffix

    unique_name = (
        f"{uuid.uuid4()}{extension}"
    )

    file_path = (
        UPLOAD_DIR / unique_name
    )

    with open(
        file_path,
        "wb"
    ) as buffer:
        buffer.write(
            file.file.read()
        )

    return (
        str(file_path),
        file.filename
    )