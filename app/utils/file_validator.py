from fastapi import UploadFile


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

ALLOWED_CONTENT_TYPES = {
    "application/pdf"
}


def validate_resume(
    file: UploadFile
) -> None:

    # =====================================
    # CHECK CONTENT TYPE
    # =====================================

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(
            "Only PDF files are allowed."
        )

    # =====================================
    # CHECK FILE SIZE
    # =====================================

    file.file.seek(
        0,
        2
    )

    file_size = file.file.tell()

    file.file.seek(
        0
    )

    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            "Maximum file size is 5 MB."
        )

    if file_size == 0:
        raise ValueError(
            "Uploaded file is empty."
        )