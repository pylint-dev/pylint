"""XML generation — no duplicate code here."""
import xml.etree.ElementTree as ET


def generate_xml(data):
    """Generate an XML document from data."""
    root = ET.Element("root")
    for key, value in data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    return ET.tostring(root, encoding="unicode")
