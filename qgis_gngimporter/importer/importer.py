from qgis.core import QgsFeature, QgsGeometry, QgsPointXY

LINE_TYPE_MAP = {
    "COLOR_Taxiway": "twy_centerline",
    "COLOR_TaxiwayOrange": "orange",
    "COLOR_TaxiwayBlue": "blue",
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

    for f in features:
        color = f["color"]

        # Convert color → type
        line_type = LINE_TYPE_MAP.get(color)
        if line_type is None:
            raise ValueError(f"Unknown line color: {color}")

        feat = QgsFeature(layer.fields())

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
