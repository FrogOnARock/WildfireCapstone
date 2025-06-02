import requests
import xml.etree.ElementTree as ET
import csv

# Step 1: GetCapabilities for WCS (raster image data)
url = "https://cwfis.cfs.nrcan.gc.ca/geoserver/public/wcs?request=GetCapabilities&service=WCS&version=1.0.0"
response = requests.get(url)
response.raise_for_status()
root = ET.fromstring(response.content)

# Define the namespaces
ns = {
    "wcs": "http://www.opengis.net/wcs",
    "ows": "http://www.opengis.net/ows",
    "gml": "http://www.opengis.net/gml"
}

coverages = []

# Step 2: Iterate over all coverages
for coverage in root.findall(".//wcs:CoverageOfferingBrief", ns):
    name = coverage.find("wcs:name", ns)
    label = coverage.find("wcs:label", ns)
    abstract = coverage.find("ows:Abstract", ns)

    # Some WCS responses embed bbox in a GML Envelope (optional)
    bbox_elem = coverage.find(".//gml:boundedBy/gml:Envelope", ns)
    if bbox_elem is not None:
        lower = bbox_elem.find("gml:lowerCorner", ns)
        upper = bbox_elem.find("gml:upperCorner", ns)
        crs = bbox_elem.attrib.get("srsName", "")
        bbox = f"{lower.text} to {upper.text}" if lower is not None and upper is not None else ""
    else:
        bbox = ""
        crs = ""

    coverages.append({
        "coverage_id": name.text if name is not None else "",
        "title": label.text if label is not None else "",
        "abstract": abstract.text.strip() if abstract is not None else "",
        "bbox": bbox,
        "crs": crs,
        "source": "CWFIS",
        "service_type": "WCS"
    })

# Step 3: Write to CSV
csv_file = "cwfis_wcs_coverages_catalog.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=coverages[0].keys())
    writer.writeheader()
    writer.writerows(coverages)

print(f"✅ Parsed and saved {len(coverages)} WCS raster layers to '{csv_file}'")
