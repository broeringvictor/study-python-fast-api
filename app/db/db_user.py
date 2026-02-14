from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from pwdlib import PasswordHash

from app.db import table_registry

pwd_context = PasswordHash.recommended()


def tz_sp_now() -> datetime:
    return datetime.now(tz=ZoneInfo("America/Sao_Paulo"))


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )

    name: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True
    )

    password: Mapped[str] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=tz_sp_now,
    )

    @classmethod
    def create(
        cls,
        name: str,
        email: str,
        password: str,
    ) -> User:
        return cls(
            name=name,
            email=email.lower().strip(),
            password=pwd_context.hash(password),
        )

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    def patch_user(
        self,
        name: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ) -> None:
        if name is not None:
            self.name = name

        if email is not None:
            self.email = email.lower().strip()

        if password is not None:
            self.password = pwd_context.hash(password)

        self.touch()

    def touch(self) -> None:
        self.updated_at = tz_sp_now()

    def to_public_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }
