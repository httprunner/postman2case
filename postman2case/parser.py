# -*- coding: utf-8 -*-

def parse_value_from_type(value):
    if isinstance(value, int):
        return int(value)
    elif isinstance(value, float):
        return float(value)
    elif value.lower() == "false":
        return False
    elif value.lower() == "true":
        return True
    else:
        return str(value)