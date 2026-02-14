from typing import Annotated

from pydantic import AfterValidator


def _validate_password(value: str) -> str:
    has_upper = any(ch.isupper() for ch in value)
    has_symbol = any(not ch.isalnum() for ch in value)
    if not has_upper or not has_symbol:
        raise ValueError("A senha deve ter pelo menos 1 letra maiúscula e 1 símbolo.")
    return value



#typings

Password = Annotated[str, AfterValidator(_validate_password)]