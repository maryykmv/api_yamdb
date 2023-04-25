import datetime as dt

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_year(year):
    """Year field validation."""
    if year > dt.date.today().year or year < 1:
        raise ValidationError(
            'Значение года не может быть больше текущего или меньше 1.'
        )


def validate_slug(slug):
    return [RegexValidator(
        regex=r'^[-a-zA-Z0-9_]+$',
        message='Поле "slug" содержит недопустимый символ.'
    )]
