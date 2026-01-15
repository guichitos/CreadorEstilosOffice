import os
from lxml import etree
import log_writer

TEMP_DIR = os.environ.get("TEMP", "/tmp")
SLIDE_PATH = os.path.join(TEMP_DIR, "extracted_app_pptm", "ppt", "slides", "slide1.xml")

def get_palette_alt_texts(palette_number, slide_path=SLIDE_PATH):
    if not os.path.exists(slide_path):
        log_writer.log_error(f"Slide not found at path: {slide_path}")
        return {}

    try:
        tree = etree.parse(slide_path)
        root = tree.getroot()
    except Exception as e:
        log_writer.log_error(f"Failed to parse slide XML: {e}")
        return {}

    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    }

    letters = list("ABCDEFGHIJKL")
    alt_texts = {}

    for letter in letters:
        shape_name = f"PaletteColor{letter}{palette_number}"
        xpath_query = f'.//p:sp[p:nvSpPr/p:cNvPr[@name="{shape_name}"]]'
        shape = root.xpath(xpath_query, namespaces=ns)
        
        if shape:
            cNvPr = shape[0].find(".//p:cNvPr", namespaces=ns)
            alt_text = cNvPr.get("descr", "") if cNvPr is not None else ""
            alt_texts[shape_name] = alt_text
            log_writer.log_info(f"{shape_name} → ALT: '{alt_text}'")
        else:
            alt_texts[shape_name] = None
            log_writer.log_info(f"{shape_name} not found in slide")

    return alt_texts

if __name__ == "__main__":
    log_writer.log_info("🔍 Extracting alternative text from PaletteColor shapes...")

    palette_number = 2  # Puedes cambiar este número

    try:
        alt_texts = get_palette_alt_texts(palette_number)
        for shape, text in alt_texts.items():
            print(f"{shape}: {text}")
    except Exception as e:
        log_writer.log_error(f"Unexpected error in main: {e}")
        print(f"⚠️ Error: {e}")
