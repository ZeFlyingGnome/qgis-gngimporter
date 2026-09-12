import os
from .coord_parser import parse_coord

def normalize_type(type_):
    t = type_.lower()

    if "gate" in t:
        return "Gate"

    if "taxi" in t:
        return "Taxiway"

    # fallback for other types
    return type_


def detect_icao_and_type(path):
    """
    Extract ICAO and file type from filename.
    Example: LFBD Gates.txt → ICAO=LFBD, type=Gates
    """
    filename = os.path.basename(path)
    name, _ = os.path.splitext(filename)

    parts = name.split()
    icao = parts[0]
    type_ = " ".join(parts[1:])

    type_ = normalize_type(type_)

    return icao, type_


def parse_point_file(path):
    points = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()

            # Must have at least 3 fields
            if len(parts) < 3:
                continue

            lat_txt = parts[0]
            lon_txt = parts[1]
            label = " ".join(parts[2:])  # Support multi-word labels

            lat = parse_coord(lat_txt)
            lon = parse_coord(lon_txt)

            points.append({
                "lat": lat,
                "lon": lon,
                "label": label
            })

    return points
