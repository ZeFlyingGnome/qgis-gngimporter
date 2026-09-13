def parse_coord(text):
    direction = text[0]
    parts = text[1:].split('.')

    if len(parts) < 3:
        raise ValueError(f"Invalid coordinate format: {text}")

    d = int(parts[0])
    m = int(parts[1])
    s = float(parts[2])

    # If milliseconds exist, append them
    if len(parts) == 4:
        s = float(f"{parts[2]}.{parts[3]}")

    decimal = d + m/60 + s/3600

    if direction in ['S', 'W']:
        decimal = -decimal

    return decimal
