import re


class Cnpj:
    __slots__ = ('_value',)

    def __init__(self, value: str):
        if value is None:
            raise ValueError("Cnpj value cannot be null")
        normalized = re.sub(r"\D", "", value)
        if not normalized:
            raise ValueError("Cnpj value cannot be blank")
        if len(normalized) != 14:
            raise ValueError("Cnpj must have 14 digits")
        if normalized == normalized[0] * 14:
            raise ValueError("Cnpj cannot be a repeated sequence")
        if not self._is_valid_mod11(normalized):
            raise ValueError("Invalid Cnpj value")
        self._value = normalized

    @property
    def value(self):
        return self._value

    @staticmethod
    def _is_valid_mod11(cnpj: str) -> bool:
        def calc_digit(base: str, weights):
            total = sum(int(num) * weight for num, weight in zip(base, weights))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder

        first = calc_digit(cnpj[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        second = calc_digit(cnpj[:12] + str(first), [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
        return cnpj[-2:] == f"{first}{second}"

    def __eq__(self, other):
        return isinstance(other, Cnpj) and self._value == other.value

    def __hash__(self):
        return hash(self._value)

    def __str__(self):
        return self._value

    def __len__(self):
        return len(self._value)
