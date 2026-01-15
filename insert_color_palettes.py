import zipfile
import os
from lxml import etree
import config
from log_writer import log_info, log_warning, log_error
from check_palette_buttons_visibility import is_copy_from_theme_button_visible

def insert_into_thmx(thmx_file, tag_name, content):

    
    # Extraer el .thmx si no está extraído
    if not os.path.exists(config.DESTINATION_FOLDER_FOR_THMX):
        os.makedirs(config.DESTINATION_FOLDER_FOR_THMX)
        with zipfile.ZipFile(thmx_file, 'r') as zip_ref:
            zip_ref.extractall(config.DESTINATION_FOLDER_FOR_THMX)

    # Ruta del archivo theme1.xml dentro del .thmx extraído
    theme_file = os.path.join(config.DESTINATION_FOLDER_FOR_THMX, "theme", "theme", "theme1.xml")

    if not os.path.exists(theme_file):
        log_error("❌ theme1.xml not found.")
        return False

    # Cargar XML
    tree = etree.parse(theme_file)
    root = tree.getroot()

    # Namespaces utilizados en el archivo
    ns = {'a': "http://schemas.openxmlformats.org/drawingml/2006/main"}

    # Buscar la etiqueta extraClrSchemeLst
    target_element = root.find(".//a:extraClrSchemeLst", ns)

    if target_element is not None:
        log_info("Se encontró el nodo <a:extraClrSchemeLst>.")

        # Mostrar el contenido del nodo como XML
        content_str = etree.tostring(target_element, encoding="unicode", pretty_print=True)
        #print("Contenido del nodo extraClrSchemeLst:\n", content_str)

        target_element.clear()

        # Agregar declaración del namespace para que `a:` sea reconocido
        xml_wrapped = f'<root xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">{content}</root>'

        try:
            parsed_content = etree.fromstring(xml_wrapped)

            # Agregar cada hijo individualmente sin la etiqueta <root>
            for child in parsed_content:
                target_element.append(child)

            # Guardar los cambios
            tree.write(theme_file, encoding="utf-8", xml_declaration=True, pretty_print=True)
            return True

        except etree.XMLSyntaxError as e:
            log_error(f"❌ XML Syntax Error: {e}")
            return False

    else:
        log_error("❌ No se encontró el nodo <a:extraClrSchemeLst> en theme1.xml.")
        return False
