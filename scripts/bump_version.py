import re

path = "qgis_gngimporter/metadata.txt"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r"version\s*=\s*([0-9]+)\.([0-9]+)", content)
if not match:
    raise SystemExit("ERROR: version not found in metadata.txt")

major, minor = match.groups()
new_minor = int(minor) + 1
new_version = f"{major}.{new_minor}"

new_content = re.sub(
    r"version\s*=\s*[0-9]+\.[0-9]+",
    f"version={new_version}",
    content
)

with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(new_version)
