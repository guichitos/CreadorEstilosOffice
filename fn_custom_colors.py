import os
from lxml import etree
from log_writer import log_info, log_error

def extract_custom_colors(slide_file, shape_names, namespaces):
    log_info(f"Custom color extraction started: {shape_names}")
    
    if not os.path.exists(slide_file):
        log_error(f"Slide not found: {slide_file}")
        return None

    custom_colors = []
    used_colors = set()

    try:
        tree = etree.parse(slide_file)
        root = tree.getroot()

        shapes = root.xpath(".//p:sp", namespaces=namespaces)
        i= 1  # Contador para CustomColor
        for shape in shapes:
            name_element = shape.xpath(".//p:cNvPr", namespaces=namespaces)
            if not name_element:
                continue

            shape_name = name_element[0].get("name", "")
            if not shape_name.startswith("CustomColor") or shape_name == "CustomColorLabel":
                continue

            alt_text = None
            if "descr" in name_element[0].attrib:
                alt_text = name_element[0].get("descr").strip()
                log_info(f"Nombre Alternativo para CustomColor: {alt_text}")

            srgb_element = shape.xpath(".//a:solidFill/a:srgbClr", namespaces=namespaces)
            if not srgb_element:
                continue

            color_val = srgb_element[0].get("val", "").upper()
            print(f"{i} - CustomColor found: {color_val} (no alt text)")
            i=i+1
            if not color_val or color_val in used_colors:
                continue

            # Construcción del bloque XML según si hay texto alternativo
            if alt_text:
                xml_block = (
                    f'\t<a:custClr name="{alt_text}">\n'
                    f'\t\t<a:srgbClr val="{color_val}">\n'
                    #f'\t\t\t<a:shade val="100000"/>\n'
                    f'\t\t</a:srgbClr>\n'
                    f'\t</a:custClr>'
                )
            else:
                xml_block = (
                    f'\t<a:custClr>\n'
                    f'\t\t<a:srgbClr val="{color_val}">\n'
                    #f'\t\t\t<a:shade val="100000"/>\n'
                    f'\t\t</a:srgbClr>\n'
                    f'\t</a:custClr>'
                )

            custom_colors.append(xml_block)
            used_colors.add(color_val)

    except Exception as e:
        log_error(f"Error processing custom colors: {str(e)}")
        return None

    if not custom_colors:
        log_info("No custom colors found.")
        return None

    result_xml = (
        "<a:custClrLst>\n" +
        "\n".join(custom_colors) +
        "\n</a:custClrLst>\n"
    )

    log_info(f"{len(custom_colors)} custom colors extracted.")
    return result_xml.strip()


if __name__ == "__main__":
    slide_file = r'C:\Users\PC\AppData\Local\Temp\extracted_app_pptm\ppt\slides\slide1.xml'
    namespaces = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main"
    }
    shape_names = []  # no se usa realmente, pero se requiere por firma de función

    result = extract_custom_colors(slide_file, shape_names, namespaces)

    if result:
        print("✅ Custom colors XML generated:\n")
        print(result)
    else:
        print("⚠️  No custom colors found or an error occurred.")

