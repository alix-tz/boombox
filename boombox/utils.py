# utils for boombox
# Author: Alix Chagué
# Date: 2023-03-13

import lxml.etree as ET
import os

# = = = = = = = = = = I/O for XML and TXT

def load_alto_xml(path: str) -> ET.ElementTree:
    """Load an ALTO XML file and return the XML tree."""
    try:
        return ET.parse(path, ET.XMLParser(encoding="utf-8"))
    except Exception:
        return False


def save_noisy_alto_xml(path: str, xml: ET.ElementTree):
    """Save an ALTO XML file with a new name"""
    with open(path, "w", encoding="utf8") as f:
        f.write(ET.tostring(xml, encoding=str))


def is_alto(xml: ET.ElementTree) -> bool:
    """Check if an XML file is an ALTO file."""
    xml = load_alto_xml(xml)
    if not xml:
        "Not a valid XML file."
        return False
    root = xml.getroot()
    ns = dict(namespaces={"a": "http://www.loc.gov/standards/alto/ns-v4#"})
    if root.tag == "alto":
        return True
    elif root.tag == "{http://www.loc.gov/standards/alto/ns-v4#}alto":
        return True
    elif root.xpath("//a:TextBlock", **ns):
        return True
    else:
        return False


def load_text(path: str) -> str:
    """Load a text file and return the text as a string."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_noisy_text(path: str, text: str):
    """Save a text file with a new name"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


# = = = = = = = = = = XML Parsing
def get_strings_in_alto(xml: ET.ElementTree) -> list:
    """Return a list of all the <String> elements in an ALTO XML file."""
    strings = []
    ns = dict(namespaces={"a": "http://www.loc.gov/standards/alto/ns-v4#"})
    for line in xml.xpath("//a:TextLine", **ns):
        for string in line.xpath("./a:String", **ns):
            strings.append(string)
    return strings


# = = = = = = = = = = Config control

def check_and_fix_weights(weights_conf: dict) -> dict:
    """Fix the weights in the config file so that they sum to 1."""
    if sum(weights_conf.values()) == 1:
        return weights_conf
    else:
        corrected_weights = {}
        for key, value in weights_conf.items():
            corrected_weights[key] = value / sum(weights_conf.values())
        return corrected_weights


def pop_invalid_modes(mode_opts):
    """Remove invalid modes from the config file."""
    valid_modes = ["swap", "delete", "insert", "nearby", "similar", "agglomerate", "repeat", "unichar", "split"] 
    for mode in mode_opts.keys():
        if mode not in valid_modes:
            mode_opts.pop(mode)
    return mode_opts
