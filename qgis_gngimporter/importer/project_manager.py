import os
import shutil
from qgis.core import QgsProject, QgsVectorLayer, QgsDefaultValue

TEMPLATE_FILES = {
    "FREETEXT": "LFXX_ICAO_FREETEXT.gpkg",
    "GEO": "LFXX_ICAO_GEO.gpkg",
    "REGIONS": "LFXX_ICAO_REGIONS.gpkg",
}

FIR_TABLE = {
    # LFBB
    "LFBA": "LFBB",
    "LFBD": "LFBB",
    "LFBE": "LFBB",
    "LFBF": "LFBB",
    "LFBH": "LFBB",
    "LFBI": "LFBB",
    "LFBM": "LFBB",
    "LFBN": "LFBB",
    "LFBO": "LFBB",
    "LFBP": "LFBB",
    "LFBR": "LFBB",
    "LFBS": "LFBB",
    "LFBT": "LFBB",
    "LFBU": "LFBB",
    "LFBY": "LFBB",
    "LFBZ": "LFBB",
    "LFCA": "LFBB",
    "LFCJ": "LFBB",
    "LFCK": "LFBB",
    "LFCL": "LFBB",
    "LFCM": "LFBB",
    "LFCN": "LFBB",
    "LFCX": "LFBB",
    "LFSL": "LFBB",
    # LFEE
    "LFGA": "LFEE",
    "LFGJ": "LFEE",
    "LFJL": "LFEE",
    "LFLH": "LFEE",
    "LFQM": "LFEE",
    "LFSB": "LFEE",
    "LFSD": "LFEE",
    "LFSG": "LFEE",
    "LFSM": "LFEE",
    "LFSN": "LFEE",
    "LFST": "LFEE",
    # LFFF
    "LFAC": "LFFF",
    "LFAQ": "LFFF",
    "LFAT": "LFFF",
    "LFAV": "LFFF",
    "LFLA": "LFFF",
    "LFOB": "LFFF",
    "LFOK": "LFFF",
    "LFOP": "LFFF",
    "LFOQ": "LFFF",
    "LFOT": "LFFF",
    "LFOZ": "LFFF",
    "LFPB": "LFFF",
    "LFPE": "LFFF",
    "LFPG": "LFFF",
    "LFPL": "LFFF",
    "LFPM": "LFFF",
    "LFPN": "LFFF",
    "LFPO": "LFFF",
    "LFPT": "LFFF",
    "LFPX": "LFFF",
    "LFPZ": "LFFF",
    "LFQA": "LFFF",
    "LFQB": "LFFF",
    "LFQQ": "LFFF",
    "LFQT": "LFFF",
    # LFFM
    "LFBC": "LFFM",
    "LFBG": "LFFM",
    "LFBM": "LFFM",
    "LFBY": "LFFM",
    "LFKS": "LFFM",
    "LFMC": "LFFM",
    "LFMI": "LFFM",
    "LFMO": "LFFM",
    "LFMY": "LFFM",
    "LFOA": "LFFM",
    "LFOE": "LFFM",
    "LFOJ": "LFFM",
    "LFPV": "LFFM",
    "LFQE": "LFFM",
    "LFQP": "LFFM",
    "LFRH": "LFFM",
    "LFRJ": "LFFM",
    "LFRL": "LFFM",
    "LFSI": "LFFM",
    "LFSO": "LFFM",
    "LFSX": "LFFM",
    # LFMM
    "LFCC": "LFMM",
    "LFCR": "LFMM",
    "LFHP": "LFMM",
    "LFHY": "LFMM",
    "LFKB": "LFMM",
    "LFKC": "LFMM",
    "LFKF": "LFMM",
    "LFKJ": "LFMM",
    "LFLB": "LFMM",
    "LFLC": "LFMM",
    "LFLG": "LFMM",
    "LFLL": "LFMM",
    "LFLN": "LFMM",
    "LFLO": "LFMM",
    "LFLP": "LFMM",
    "LFLS": "LFMM",
    "LFLU": "LFMM",
    "LFLV": "LFMM",
    "LFLW": "LFMM",
    "LFLY": "LFMM",
    "LFMA": "LFMM",
    "LFMD": "LFMM",
    "LFMH": "LFMM",
    "LFML": "LFMM",
    "LFMN": "LFMM",
    "LFMP": "LFMM",
    "LFMQ": "LFMM",
    "LFMT": "LFMM",
    "LFMU": "LFMM",
    "LFMV": "LFMM",
    "LFMZ": "LFMM",
    "LFTF": "LFMM",
    "LFTH": "LFMM",
    "LFTW": "LFMM",
    # LFRR
    "LFEA": "LFRR",
    "LFEC": "LFRR",
    "LFEQ": "LFRR",
    "LFEY": "LFRR",
    "LFJR": "LFRR",
    "LFOH": "LFRR",
    "LFOU": "LFRR",
    "LFOV": "LFRR",
    "LFRB": "LFRR",
    "LFRC": "LFRR",
    "LFRD": "LFRR",
    "LFRE": "LFRR",
    "LFRG": "LFRR",
    "LFRI": "LFRR",
    "LFRK": "LFRR",
    "LFRM": "LFRR",
    "LFRN": "LFRR",
    "LFRO": "LFRR",
    "LFRQ": "LFRR",
    "LFRS": "LFRR",
    "LFRT": "LFRR",
    "LFRU": "LFRR",
    "LFRV": "LFRR",
    "LFRZ": "LFRR",
}


def get_project_root():
    project_file = QgsProject.instance().fileName()
    if not project_file:
        raise Exception("No QGIS project loaded.")
    return os.path.dirname(project_file)

def detect_project_fir():
    root = QgsProject.instance().layerTreeRoot()
    for fir in ("LFBB", "LFFF", "LFEE", "LFMM", "LFFM", "LFRR"):
        if root.findGroup(fir) is not None:
            return fir
    return None

def get_fir(icao):
    return FIR_TABLE.get(icao, "UNKNOWN")


def get_icao_group(icao):
    root = QgsProject.instance().layerTreeRoot()
    return root.findGroup(icao)


def ensure_layer_exists(fir, icao, layer_type):
    project_root = get_project_root()

    template_dir = os.path.join(project_root, "template")
    template_file = TEMPLATE_FILES[layer_type]
    template_path = os.path.join(template_dir, template_file)

    icao_dir = os.path.join(project_root, "src", fir, icao)
    os.makedirs(icao_dir, exist_ok=True)

    expected_name = f"{fir}_{icao}_{layer_type}"
    dest_path = os.path.join(icao_dir, f"{expected_name}.gpkg")

    group = get_icao_group(icao)
    if group is None:
        raise Exception(f"ICAO group {icao} not found in project")

    # If layer already exists in QGIS tree
    for child in group.children():
        if child.name() == expected_name:
            return child.layer()

    # Clone template if missing
    if not os.path.exists(dest_path):
        shutil.copy(template_path, dest_path)

    layer = QgsVectorLayer(dest_path, expected_name, "ogr")
    if not layer.isValid():
        raise Exception(f"Failed to load cloned layer: {dest_path}")

    # Set default values for FIR and ICAO fields
    fir_idx = layer.fields().indexFromName("fir")
    icao_idx = layer.fields().indexFromName("icao")

    if fir_idx != -1:
        layer.setDefaultValueDefinition(fir_idx, QgsDefaultValue(fir))

    if icao_idx != -1:
        layer.setDefaultValueDefinition(icao_idx, QgsDefaultValue(icao))

    QgsProject.instance().addMapLayer(layer, False)
    group.addLayer(layer)

    return layer
