from qgis.core import QgsFeature, QgsGeometry, QgsPointXY

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
