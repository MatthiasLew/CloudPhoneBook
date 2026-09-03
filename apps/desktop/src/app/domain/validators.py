"""Validation functions for desktop user forms."""

import re


def validate_email(email: str) -> tuple[bool, str]:
    if not email:
        return True, ""  # Optional
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email.strip()):
        return False, "Nieprawidlowy format adresu e-mail."
    return True, ""


def validate_phone(phone: str) -> tuple[bool, str]:
    if not phone or not phone.strip():
        return False, "Numer telefonu jest wymagany."
    cleaned = re.sub(r"[\s\-\(\)\+]", "", phone.strip())
    if len(cleaned) < 3 or len(cleaned) > 20 or not cleaned.isdigit():
        return False, "Numer telefonu powinien skladac sie z cyfr (min. 3 znaki)."
    return True, ""


def validate_contact_form(first_name: str, phone: str, email: str | None) -> tuple[bool, str]:
    if not first_name or not first_name.strip():
        return False, "Imie jest wymagane."
    valid_p, p_err = validate_phone(phone)
    if not valid_p:
        return False, p_err
    if email:
        valid_e, e_err = validate_email(email)
        if not valid_e:
            return False, e_err
    return True, ""
