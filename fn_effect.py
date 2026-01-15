import os
from lxml import etree
from log_writer import log_info, log_warning, log_error

def extract_effect_styles(slide_file, shape_names, namespaces):
 
    log_info(f"Effect attributes extraction started {shape_names}")
 
    # Cargar el XML
    tree = etree.parse(slide_file)
    root = tree.getroot()

    # Lista de etiquetas de efectos a extraer dentro de <p:spPr>
    effect_tags = {"effectLst", "effectDag", "scene3d", "sp3d"}

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
                            if tag_name in effect_tags:
                                text_effect = etree.tostring(child, encoding="unicode", pretty_print=True)

                                # Quitar namespaces innecesarios
                                text_effect = text_effect.replace(' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"', "")
                                text_effect = text_effect.replace(' xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"', "")
                                text_effect = text_effect.replace(' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"', "")

                                shape_content += text_effect + "\n"

        if shape_content.strip():
            extracted_content += f"<a:effectStyle>\n{shape_content}</a:effectStyle>\n\n"

    return extracted_content.strip() if extracted_content.strip() else None
