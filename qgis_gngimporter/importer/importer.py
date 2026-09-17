from qgis.core import QgsFeature, QgsGeometry, QgsPointXY
from qgis.PyQt.QtWidgets import QMessageBox

LINE_TYPE_MAP = {
    "COLOR_Taxiway": "twy_centerline",
    "COLOR_TaxiwayOrange": "orange",
    "COLOR_TaxiwayBlue": "blue",
}

SURFACE_TYPE_MAP = {
    "COLOR_HardSurface4": "background",
    "COLOR_HardSurface2": "taxiway",
    "COLOR_RunwayConcrete": "runway",
    "COLOR_GrasSurface": "grass",
    "COLOR_HardSurface4": "grass_taxiway",
    "COLOR_RunwayGrass": "grass_runway",
    "COLOR_Stopbar": "cati",
    "COLOR_TaxiwayOrange": "catiii",
    "COLOR_HardSurface3": "apron",
    "COLOR_Building": "building",
}

def import_points(points, layer, fir, icao, type_):
    """
    Insert point features into FREETEXT layer.
    points = list of {lat, lon, label}
    """
    pr = layer.dataProvider()

    new_features = []

    for p in points:
        feat = QgsFeature(layer.fields())
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(p["lon"], p["lat"])))

        feat["fir"] = fir
        feat["icao"] = icao
        feat["type"] = type_
        feat["freetext"] = p["label"]
        feat["author"] = "GNGImporter"

        new_features.append(feat)

    pr.addFeatures(new_features)
    layer.triggerRepaint()


def import_lines(features, layer, fir, icao):
    pr = layer.dataProvider()
    new_features = []

    missing_line_types = set()

    for f in features:
        feat = QgsFeature(layer.fields())

        # Convert color → type
        color = f["color"]
        line_type = LINE_TYPE_MAP.get(color)

        if line_type is None:
            # Store missing type
            missing_line_types.add(color)

            # Import the line WITHOUT a type
            feat["type"] = None
        else:
            feat["type"] = line_type

        # Build polyline geometry
        qpoints = [QgsPointXY(lon, lat) for (lat, lon) in f["points"]]
        feat.setGeometry(QgsGeometry.fromPolylineXY(qpoints))

        # Attributes
        feat["fir"] = fir
        feat["icao"] = icao
        feat["type"] = line_type
        feat["author"] = "GNGImporter"

        new_features.append(feat)

    pr.addFeatures(new_features)
    layer.triggerRepaint()

    if missing_line_types:
        missing = "\n".join(sorted(missing_line_types))
        QMessageBox.warning(
            None,
            "GNG Importer — Missing Line Types",
            f"The following line types were not recognized:\n\n{missing}\n\n"
            "They were imported without a type.\n"
            "Please update LINE_TYPE_MAP to support them."
        )

def import_surfaces(surfaces, layer, fir, icao):
    missing_surface_types = set()

    layer.startEditing()

    for surf in surfaces:
        color = surf["color"]
        coords = surf["coords"]

        qpoints = [QgsPointXY(lon, lat) for lat, lon in coords]

        feat = QgsFeature(layer.fields())
        feat.setGeometry(QgsGeometry.fromPolygonXY([qpoints]))

        surface_type = SURFACE_TYPE_MAP.get(color)

        if surface_type is None:
            missing_surface_types.add(color)
            feat["type"] = None
        else:
            feat["type"] = surface_type

        feat["fir"] = fir
        feat["icao"] = icao

        layer.addFeature(feat)

    if not layer.commitChanges():
        print("Commit failed:", layer.commitErrors())

    # popup at end
    if missing_surface_types:
        missing = "\n".join(sorted(missing_surface_types))
        QMessageBox.warning(
            None,
            "GNG Importer — Missing Surface Types",
            f"The following surface types were not recognized:\n\n{missing}\n\n"
            "They were imported without a type.\n"
            "Please update SURFACE_TYPE_MAP to support them."
        )
