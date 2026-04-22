import re


class Cpf:
    def __init__(self, value: str):
        if value is None:
            raise ValueError("Cpf value cannot be null")
        normalized = re.sub(r"\D", "", value)
        if not normalized:
            raise ValueError("Cpf value cannot be blank")
        if len(normalized) != 11:
            raise ValueError("Cpf must have 11 digits")
        if normalized == normalized[0] * 11:
            raise ValueError("Cpf cannot be a repeated sequence")
        if not self._is_valid_mod11(normalized):
            raise ValueError("Invalid Cpf value")
        self.value = normalized

    def _is_valid_mod11(self, cpf: str) -> bool:
        def calc_digit(base: str, factor: int) -> int:
            total = sum(int(num) * (factor - idx) for idx, num in enumerate(base))
            remainder = (total * 10) % 11
            return 0 if remainder == 10 else remainder

        first = calc_digit(cpf[:9], 10)
        second = calc_digit(cpf[:10], 11)
        return cpf[-2:] == f"{first}{second}"

    def __eq__(self, other):
        return isinstance(other, Cpf) and self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return self.value

    def __len__(self):
        return len(self.value)


class Cnh:
    def __init__(self, value: str):
        if value is None:
            raise ValueError("Cnh value cannot be null")
        normalized = re.sub(r"\D", "", value)
        if not normalized:
            raise ValueError("Cnh value cannot be blank")
        if len(normalized) != 11:
            raise ValueError("Cnh must have 11 digits")
        self.value = normalized

    def __eq__(self, other):
        return isinstance(other, Cnh) and self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return self.value

    def __len__(self):
        return len(self.value)
