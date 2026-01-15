import os
from lxml import etree
from log_writer import log_info, log_error
import config

def rename_theme_elements():
    theme_path = os.path.join(config.TEMP_DIRECTORY, "extracted_destination_thmx", "theme", "theme", "theme1.xml")
    slide_path = os.path.join(config.TEMP_DIRECTORY, "extracted_app_pptm", "ppt", "slides", "slide1.xml")

    try:
        if not os.path.exists(theme_path):
            raise FileNotFoundError("Theme file not found")
        if not os.path.exists(slide_path):
            raise FileNotFoundError("Slide file not found")

        ns = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
        }

        # Leer texto desde el shape BrandName
        slide_tree = etree.parse(slide_path)
        slide_root = slide_tree.getroot()

        brand_text = None
        shape = slide_root.find('.//p:cNvPr[@name="BrandName"]/../..', namespaces=ns)
        if shape is not None:
            text_node = shape.find('.//a:t', namespaces=ns)
            if text_node is not None:
                brand_text = text_node.text
                log_info(f'BrandName text: {brand_text}')
            else:
                log_info('BrandName shape found, but no text present')
        else:
            log_info('BrandName shape not found')

        # Modificar tema si hay texto
        theme_tree = etree.parse(theme_path)
        theme_root = theme_tree.getroot()

        clr = theme_root.find('.//a:clrScheme', namespaces=ns)
        if clr is not None:
            clr.set('name', f"{brand_text}'s color scheme" if brand_text else "Default color scheme")

        font = theme_root.find('.//a:fontScheme', namespaces=ns)
        if font is not None:
            font.set('name', f"{brand_text}'s font scheme" if brand_text else "Default font scheme")

        fmt = theme_root.find('.//a:fmtScheme', namespaces=ns)
        if fmt is not None:
            fmt.set('name', f"{brand_text}'s format scheme" if brand_text else "Default format scheme")

        theme_tree.write(theme_path, encoding="utf-8", xml_declaration=True)
        log_info("Theme style names updated with dynamic brand name")

    except Exception as e:
        log_error(f"Theme update failed: {str(e)}")

if __name__ == "__main__":
    rename_theme_elements()

