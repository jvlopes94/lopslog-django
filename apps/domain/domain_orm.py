from django.db import models
from django.core.exceptions import ValidationError


class DomainField(models.CharField):
    """Base class for domain-enriched strings."""

    def __init__(self, *args, **kwargs):
        # We ensure it's stored as a string in the DB
        kwargs.setdefault('max_length', 20)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None or isinstance(value, self.domain_class):
            return value
        try:
            return self.domain_class(value)
        except ValueError as e:
            raise ValidationError(str(e))

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return self.domain_class(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        # Ensure it's the domain class, then extract the string
        if not isinstance(value, self.domain_class):
            value = self.domain_class(value)
        return str(value)
