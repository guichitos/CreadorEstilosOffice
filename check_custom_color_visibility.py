from lxml import etree
from log_writer import log_info, log_error
import config
import os


def is_custom_color_label_visible() -> bool:
    shape_name = "CustomColorLabel"

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

        xpath = f'.//p:cNvPr[@name="{shape_name}"]'
        node = root.find(xpath, namespaces=namespaces)

        if node is None:
            log_info(f"{shape_name}: Not found")
            return False

        is_visible = node.get('hidden') != '1'
        log_info(f"{shape_name}: {'Visible' if is_visible else 'Hidden'}")
        return is_visible

    except Exception as e:
        log_error(f"Error checking {shape_name}: {e}")
        return False


if __name__ == "__main__":
    result = is_custom_color_label_visible()
    print("✅ CustomColorLabel is visible." if result else "❌ CustomColorLabel is hidden or not found.")
