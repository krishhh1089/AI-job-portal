import uuid

from sqlalchemy import (
    Column,
    Text,
    String,
    Boolean,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class Resume(Base, TimestampMixin):
    __tablename__ = "resumes"

    resume_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.user_id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    file_path = Column(
        Text,
        nullable=False
    )

    file_name = Column(
        String(255),
        nullable=True
    )

    parsed_text = Column(
        Text,
        nullable=True
    )

    is_default = Column(
        Boolean,
        nullable=False,
        default=False
    )

    user = relationship(
        "User",
        back_populates="resumes"
    )

    # applications relationship will be added later

    def __repr__(self):
        return (
            f"<Resume("
            f"resume_id={self.resume_id}, "
            f"user_id={self.user_id}, "
            f"file_name='{self.file_name}'"
            f")>"
        )