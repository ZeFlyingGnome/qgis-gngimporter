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

def parse_line_file(path):
    """
    Parse Groundlayout AVISO line file.
    Returns list of segments:
    [
        {
            "p1": (lat, lon),
            "p2": (lat, lon),
            "color": "COLOR_Taxiway"
        },
        ...
    ]
    """
    segments = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            lat1_txt, lon1_txt, lat2_txt, lon2_txt, color = line.split()

            p1 = (parse_coord(lat1_txt), parse_coord(lon1_txt))
            p2 = (parse_coord(lat2_txt), parse_coord(lon2_txt))

            segments.append({
                "p1": p1,
                "p2": p2,
                "color": color
            })

    return segments

def group_segments(segments):
    """
    Group segments into polyline features.
    Returns list of grouped features:
    [
        {
            "color": "COLOR_Taxiway",
            "points": [(lat, lon), (lat, lon), ...]
        },
        ...
    ]
    """

    features = []
    current = None

    for seg in segments:
        p1 = seg["p1"]
        p2 = seg["p2"]
        color = seg["color"]

        if current is None:
            # start new feature
            current = {
                "color": color,
                "points": [p1, p2]
            }
            continue

        last_point = current["points"][-1]

        # continuation condition
        if color == current["color"] and p1 == last_point:
            current["points"].append(p2)
        else:
            # finish previous feature
            features.append(current)
            # start new one
            current = {
                "color": color,
                "points": [p1, p2]
            }

    # add last feature
    if current is not None:
        features.append(current)

    return features
