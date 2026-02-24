from lxml import etree
import config
import os
from log_writer import log_error


def has_any_visible_palette():
    slide_path = os.path.join(
        config.PATH,
        config.FOLDER_FOR_EXTRACTED_APP,
        "ppt",
        "slides",
        "slide1.xml"
    )

    namespaces = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }

    try:
        tree = etree.parse(slide_path)
        root = tree.getroot()

        for i in range(1, 5):
            xpath = f'.//p:cNvPr[@name="CopyCurrentColorPalette{i}"]'
            node = root.find(xpath, namespaces=namespaces)
            if node is not None and node.get("hidden") != "1":
                return True

        return False

    except Exception as e:
        log_error(f"Error checking for visible palettes: {e}")
        return False


if __name__ == "__main__":
    result = has_any_visible_palette()
    if result:
        print("✅ Al menos una paleta está visible.")
    else:
        print("❌ Todas las paletas están ocultas (o ocurrió un error).")
