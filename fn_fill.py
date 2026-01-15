import os
from lxml import etree
from replace_phClr import replace_schemeClr  # Importamos la función para reemplazar colores
from log_writer import log_info, log_warning, log_error

def extract_fill_styles(slide_file, shape_names, namespaces):
    log_info(f"Fill attributes extraction started {shape_names}")
    tree = etree.parse(slide_file)
    root = tree.getroot()

    fill_tags = {"noFill", "solidFill", "gradFill", "blipFill", "pattFill", "grpFill"}

    extracted_fills = [] 

    for shape_name in shape_names:
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

                                text_fill = text_fill.replace(' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"', "")
                                text_fill = text_fill.replace(' xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"', "")
                                text_fill = text_fill.replace(' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"', "")

                                extracted_fills.append(text_fill)

    if extracted_fills:
        extracted_text = "\n".join(extracted_fills)
        return replace_schemeClr(extracted_text)

    return None
