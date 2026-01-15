import zipfile
import os
from lxml import etree
import config

def insert_into_thmx(thmx_file, tag_name, content):

    # Extraer el .thmx si no está extraído
    if not os.path.exists( config.DESTINATION_FOLDER_FOR_THMX):
        os.makedirs(config.DESTINATION_FOLDER_FOR_THMX)
        with zipfile.ZipFile(thmx_file, 'r') as zip_ref:
            zip_ref.extractall(config.DESTINATION_FOLDER_FOR_THMX)

    # Ruta del archivo theme1.xml dentro del .thmx extraído
    theme_file = os.path.join(config.DESTINATION_FOLDER_FOR_THMX, "theme", "theme", "theme1.xml")

    if not os.path.exists(theme_file):
        return False

    # Cargar XML
    tree = etree.parse(theme_file)
    root = tree.getroot()

    # Namespaces utilizados en el archivo
    ns = {'a': "http://schemas.openxmlformats.org/drawingml/2006/main"}

    # Buscar la etiqueta dentro de <fmtScheme>
    target_element = root.find(f".//a:fmtScheme/a:{tag_name}", ns)

    if target_element is not None:
        target_element.clear()

        # Agregar declaración del namespace para que `a:` sea reconocido
        xml_wrapped = f'<root xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">{content}</root>'

        try:
            parsed_content = etree.fromstring(xml_wrapped)

            # Agregar cada hijo individualmente sin la etiqueta <root>
            for child in parsed_content:
                target_element.append(child)

            # Guardar los cambios en theme1.xml
            tree.write(theme_file, encoding="utf-8", xml_declaration=True, pretty_print=True)
            return True

        except etree.XMLSyntaxError:
            return False

    return False
