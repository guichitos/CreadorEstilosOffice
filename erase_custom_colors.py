from lxml import etree
import os
import config
from log_writer import log_info, log_error

def clear_custom_colors_from_thmx(thmx_folder_path: str):
    theme_file_path = os.path.join(config.TEMP_DIRECTORY, thmx_folder_path, "theme", "theme", "theme1.xml")

    if not os.path.exists(theme_file_path):
        log_error("theme1.xml not found.")
        return False

    try:
        tree = etree.parse(theme_file_path)
        root = tree.getroot()

        namespaces = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
        node = root.find(".//a:custClrLst", namespaces)

        if node is not None:
            node.clear()
            tree.write(theme_file_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
            log_info("✅ Custom colors cleared from <a:custClrLst>.")
            return True
        else:
            log_info("No <a:custClrLst> node found. Nothing to clear.")
            return False

    except Exception as e:
        log_error(f"Error clearing <a:custClrLst>: {e}")
        return False

if __name__ == "__main__":
    success = clear_custom_colors_from_thmx(config.DESTINATION_FOLDER_FOR_THMX)
    print("✅ custom colors cleared." if success else "❌ nothing was cleared or an error occurred.")
