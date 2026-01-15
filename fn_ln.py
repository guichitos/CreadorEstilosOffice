from lxml import etree
from replace_phClr import replace_schemeClr
from log_writer import log_info, log_warning, log_error

def extract_line_styles(slide_file, shape_names, namespaces):
    log_info(f"Line attributes extraction started {shape_names}")
    tree = etree.parse(slide_file)
    root = tree.getroot()

    extracted_content = ""

    for shape_name in shape_names:
        shape_content = ""

        for cnvpr in root.findall(".//p:cNvPr", namespaces):
            if cnvpr.get("name") == shape_name:
                sp_element = cnvpr.getparent().getparent()

                if sp_element is not None:
                    ln_element = sp_element.find(".//a:ln", namespaces)

                    if ln_element is None:
                        sppr_element = sp_element.find(".//p:spPr", namespaces)
                        if sppr_element is not None:
                            ln_element = sppr_element.find(".//a:ln", namespaces)

                    if ln_element is not None:
                        text_ln = etree.tostring(ln_element, encoding="unicode", pretty_print=True)
                        text_ln = text_ln.replace(' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"', "")
                        text_ln = text_ln.replace(' xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"', "")
                        text_ln = text_ln.replace(' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"', "")

                        shape_content += text_ln + "\n"

        if shape_content.strip():
            extracted_content += shape_content + "\n"

    if not extracted_content.strip():
        return None

    extracted_content = replace_schemeClr(extracted_content)
    return extracted_content.strip()
