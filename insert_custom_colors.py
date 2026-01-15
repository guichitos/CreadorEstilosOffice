import zipfile
import os
from lxml import etree
import config
from log_writer import log_error, log_info

def insert_custom_colors_into_thmx(thmx_file, content):
    if not os.path.exists(os.path.join(config.TEMP_DIRECTORY, config.DESTINATION_FOLDER_FOR_THMX)):
        os.makedirs(os.path.join(config.TEMP_DIRECTORY, config.DESTINATION_FOLDER_FOR_THMX))
        with zipfile.ZipFile(thmx_file, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(config.TEMP_DIRECTORY, config.DESTINATION_FOLDER_FOR_THMX))

    theme_file = os.path.join(config.TEMP_DIRECTORY, config.DESTINATION_FOLDER_FOR_THMX, "theme", "theme", "theme1.xml")
    if not os.path.exists(theme_file):
        log_error("theme1.xml not found in extracted .thmx.")
        return False

    try:
        tree = etree.parse(theme_file)
        root = tree.getroot()
        ns = {'a': "http://schemas.openxmlformats.org/drawingml/2006/main"}

        # Eliminar custClrLst existente si lo hay
        existing = root.find("a:custClrLst", ns)
        if existing is not None:
            root.remove(existing)

        # Envolver contenido y parsear
        xml_wrapped = f'<root xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">{content}</root>'
        parsed = etree.fromstring(xml_wrapped)
        for child in parsed:
            root.insert(len(root) - 1, child)  # justo antes de <a:extLst> si existe

        tree.write(theme_file, encoding="utf-8", xml_declaration=True, pretty_print=True)
        log_info("Custom colors inserted into theme1.xml.")
        return True

    except Exception as e:
        log_error(f"Error inserting custom colors: {str(e)}")
        return False

if __name__ == "__main__":
    test_input_path = os.path.join(config.TEMP_DIRECTORY, "custom_colors_extracted.txt")

    if not os.path.exists(test_input_path):
        log_error(f"Test input not found: {test_input_path}")
    else:
        with open(test_input_path, "r", encoding="utf-8") as f:
            test_content = f.read()

        result = insert_custom_colors_into_thmx(config.THMX_FILE_SOURCE, test_content)

        if result:
            log_info("Test insertion completed successfully.")
        else:
            log_error("Test insertion failed.")
