def clean_quantity(value):
    value = value.replace('.', '').replace('-', '0')
    return int(value) if value.isdigit() else 0

def valid_is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False