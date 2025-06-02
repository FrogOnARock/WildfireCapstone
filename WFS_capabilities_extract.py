import requests
import xml.etree.ElementTree as ET
import csv

# Step 1: Fetch the WFS GetCapabilities XML
url = "https://cwfis.cfs.nrcan.gc.ca/geoserver/public/wfs?request=GetCapabilities"
response = requests.get(url)
response.raise_for_status()

print("Status Code:", response.status_code)
print("Content Type:", response.headers.get("Content-Type"))
print("First 500 characters:\n", response.text[:500])


xml_data = response.content

# Step 2: Parse the XML
root = ET.fromstring(xml_data)
ns = {
    "wfs": "http://www.opengis.net/wfs/2.0",
    "ows": "http://www.opengis.net/ows/1.1"
}

layers = []

# Loop through FeatureTypes (these are your data layers)
for feature in root.findall(".//wfs:FeatureType", ns):

    print(feature)


    name = feature.find("wfs:Name", ns)
    title = feature.find("wfs:Title", ns)
    abstract = feature.find("ows:Abstract", ns)
    keywords = feature.findall(".//ows:Keyword", ns)

    layers.append({
        "layer_name": name.text if name is not None else "",
        "title": title.text if title is not None else "",
        "abstract": abstract.text.strip() if abstract is not None else "",
        "keywords": "; ".join(k.text for k in keywords) if keywords else "",
        "source": "CWFIS",
        "service_type": "WFS"
    })
# Step 4: Output to CSV
csv_file = "cwfis_wfs_layers_catalog.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=layers[0].keys())
    writer.writeheader()
    writer.writerows(layers)

print(f"Parsed {len(layers)} WFS layers to '{csv_file}'")