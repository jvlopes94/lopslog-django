import re


class LicensePlate:
    LEGACY = re.compile(r"^[A-Z]{3}-?\d{4}$")
    MERCOSUL = re.compile(r"^[A-Z]{3}-?\d[A-Z]\d{2}$")

    def __init__(self, value: str):
        if value is None:
            raise ValueError("LicensePlate value cannot be null")
        normalized = value.strip().upper()
        if not normalized:
            raise ValueError("LicensePlate value cannot be blank")
        if not (self.LEGACY.match(normalized) or self.MERCOSUL.match(normalized)):
            raise ValueError("Invalid LicensePlate value")
        self.value = normalized.replace("-", "")

    def __eq__(self, other):
        return isinstance(other, LicensePlate) and self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return self.value

    def __len__(self):
        return len(self.value)
