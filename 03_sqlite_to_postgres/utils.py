from dataclasses import fields


def get_fields(model):
    """
    Получение всех полей модели в виде списка
    """

    fields_lst = list(field.name for field in fields(model))
    return fields_lst


def get_fields_str(model):
    """
    Получение всех полей модели в виде строки
    """

    fields_str = ', '.join(get_fields(model))
    return fields_str
