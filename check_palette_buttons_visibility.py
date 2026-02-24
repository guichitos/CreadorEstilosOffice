from lxml import etree
from log_writer import log_info, log_error
import config
import os


def is_copy_from_theme_button_visible(button_number: int) -> bool:
    if button_number not in range(1, 5):
        log_error(f"Invalid button number: {button_number}")
        print(f"Button {button_number}: ❌ INVALID NUMBER")
        return False

    shape_name = f"CopyCurrentColorPalette{button_number}"

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
        if not os.path.exists(slide_path):
            log_error(f"Slide file not found: {slide_path}")
            print(f"Button {button_number}: ❌ SLIDE NOT FOUND")
            return False

        tree = etree.parse(slide_path)
        root = tree.getroot()

        xpath = f'.//p:cNvPr[@name="{shape_name}"]'
        node = root.find(xpath, namespaces=namespaces)

        if node is None:
            log_info(f"{shape_name}: Not found")
            print(f"Button {button_number}: ❌ NOT FOUND ({shape_name})")
            return False

        if node.get('hidden') == '1':
            log_info(f"{shape_name}: Hidden")
            print(f"Button {button_number}:❌ HIDDEN")
            return False

        log_info(f"{shape_name}: Visible")
        print(f"Button {button_number}: ✅ VISIBLE")
        return True

    except Exception as e:
        log_error(f"Error checking {shape_name}: {e}")
        print(f"Button {button_number}:ERROR")
        return False


if __name__ == "__main__":
    print("🔍 Checking visibility of CopyCurrentColorPalette1 to CopyCurrentColorPalette4...")
    for i in range(1, 5):
        is_copy_from_theme_button_visible(i)
