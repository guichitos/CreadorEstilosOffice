import os
from lxml import etree
from replace_phClr import replace_schemeClr  # Importamos la función de reemplazo
from log_writer import log_info, log_warning, log_error

def extract_background_styles(slide_file, shape_names, namespaces):
    log_info(f"Background extraction started {shape_names}")
    """
    Extrae las etiquetas de relleno de fondo dentro de <p:spPr> para una lista de formas en un archivo XML de PowerPoint.

    :param slide_file: Ruta del archivo slide1.xml ya extraído.
    :param shape_names: Lista de nombres de las formas a extraer.
    :param namespaces: Diccionario con los namespaces XML a utilizar.
    :return: Texto extraído en formato de texto plano o None si no se encuentra nada.
    """
    # Cargar el XML
    tree = etree.parse(slide_file)
    root = tree.getroot()

    # Lista de etiquetas de relleno a extraer dentro de <p:spPr>
    fill_tags = {"noFill", "solidFill", "gradFill", "blipFill", "pattFill", "grpFill"}

    extracted_content = ""

    # Recorrer las formas a buscar
    for shape_name in shape_names:
        shape_content = ""

        for cnvpr in root.findall(".//p:cNvPr", namespaces):
            if cnvpr.get("name") == shape_name:
                sp_element = cnvpr.getparent().getparent()

                if sp_element is not None:
                    spPr_element = sp_element.find(".//p:spPr", namespaces)

                    if spPr_element is not None:
                        for child in spPr_element:
                            tag_name = etree.QName(child).localname
                            if tag_name in fill_tags:
                                text_fill = etree.tostring(child, encoding="unicode", pretty_print=True)

                                # Quitar namespaces innecesarios
                                text_fill = text_fill.replace(' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"', "")
                                text_fill = text_fill.replace(' xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"', "")
                                text_fill = text_fill.replace(' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"', "")

                                shape_content += text_fill + "\n"

        if shape_content.strip():
            extracted_content += f"{shape_content}\n"
        
        # 🔍 Aplicar la función de reemplazo de colores
        extracted_content = replace_schemeClr(extracted_content)

    return extracted_content.strip() if extracted_content.strip() else None
