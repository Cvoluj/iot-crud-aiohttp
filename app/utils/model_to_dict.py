from datetime import datetime
from peewee import Model


def model_to_dict(model_instance: Model, exclude: list = []):
    model_dict = {}
    for field in model_instance._meta.fields.values():
        field_name = field.name
        if field_name in exclude:
            continue
        value = getattr(model_instance, field_name)
        if isinstance(value, datetime):
            model_dict[field_name] = value.isoformat()
        else:
            model_dict[field_name] = value
    return model_dict