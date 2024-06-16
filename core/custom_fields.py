from django.db import models

class CoordinateField(models.CharField):
    description = "A field to store latitude and longitude coordinates as a pair of floats."

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 50  # Adjust max length as needed
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return [float(coord) for coord in value.split(',')]

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return value
        return [float(coord) for coord in value.split(',')]

    def get_prep_value(self, value):
        if value is None:
            return value
        return ','.join(str(coord) for coord in value)