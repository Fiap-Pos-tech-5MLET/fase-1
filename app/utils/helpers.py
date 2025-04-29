def clean_quantity(value):
    value = value.replace('.', '').replace('-', '0')
    return int(value) if value.isdigit() else 0