import os
import string
from lxml import etree
from log_writer import log_info, log_error
from check_palette_buttons_visibility import is_copy_from_theme_button_visible
from bool_add_palette import has_any_visible_palette
from build_clr_map_from_alt_texts import build_clr_map_from_alt_texts


TEMP_DIR = os.environ.get("TEMP", "/tmp")
SLIDE_PATH = os.path.join(TEMP_DIR, "extracted_app_pptm", "ppt", "slides", "slide1.xml")
OUTPUT_FILE = os.path.join(TEMP_DIR, "palette_extracted.txt")

def extract_palette_colors_from_slide(slide_path):
    # Verifica si el archivo existe
    if not os.path.exists(slide_path):
        log_error(f"Slide file not found: {slide_path}")
        return {}, {}

    # Carga el archivo XML y obtiene el nodo raíz
    tree = etree.parse(slide_path)
    root = tree.getroot()

    # Define los namespaces utilizados en archivos de PowerPoint
    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main"
    }

    # Diccionarios para almacenar colores de figuras y nombres de paletas
    palette_colors = {}
    palette_names = {}

    # Busca todas las formas <p:sp> dentro del archivo XML
    shapes = root.xpath(".//p:sp", namespaces=ns)

    # Recorre todas las formas encontradas
    for shape in shapes:
        # Extrae el nombre asignado a la forma
        name_element = shape.xpath(".//p:cNvPr", namespaces=ns)
        if not name_element:
            continue
        shape_name = name_element[0].get("name", "")

        # Si la forma representa el nombre de una paleta (PaletteNameX)
        if shape_name.startswith("PaletteName"):
            number = shape_name.replace("PaletteName", "")
            text_elements = shape.xpath(".//a:t", namespaces=ns)
            if text_elements and number.isdigit():
                palette_name = text_elements[0].text.strip()
                print(f"PaletteName{number}: {palette_name}")
                palette_names[int(number)] = palette_name

        # Si no es una forma tipo PaletteColorXX, continuar
        if not shape_name.startswith("PaletteColor"):
            continue

        # Filtra solo PaletteColor1X, PaletteColor2X, PaletteColor3X, PaletteColor4X
        try:
            # El nombre tiene el formato: PaletteColor[A–L][1–4], ej: PaletteColorC3
            base = shape_name.replace("PaletteColor", "")  # e.g. "A1"
            number_part = ''.join(filter(str.isdigit, base))  # e.g. "1"
            if int(number_part) not in range(1, 5):
                continue
        except:
            continue  # En caso de error al interpretar el número

        # Busca el color dentro del bloque <a:solidFill><a:srgbClr>
        srgb_element = shape.xpath(".//a:solidFill/a:srgbClr", namespaces=ns)
        if not srgb_element:
            continue

        # Extrae el valor hexadecimal del color (ej. "FF0000") y lo guarda
        color_val = srgb_element[0].get("val", "").upper()
        if color_val:
            palette_colors[shape_name] = color_val

    # Devuelve los diccionarios de colores y nombres de paletas
    return palette_colors, palette_names



def generate_extra_scheme_block(palette_number, color_dict, palette_names):
    # Elementos XML del esquema de color
    keys = [
        "dk1", 
        "lt1", 
        "dk2", 
        "lt2",
        "accent1", 
        "accent2", 
        "accent3",
        "accent4", 
        "accent5", 
        "accent6",
        "hlink", 
        "folHlink"
    ]

    # Nombres de forma del slide que corresponden a los colores
    shape_names = [
        f"PaletteColorB{palette_number}",
        f"PaletteColorA{palette_number}",
        f"PaletteColorD{palette_number}",
        f"PaletteColorC{palette_number}",
        f"PaletteColorE{palette_number}",
        f"PaletteColorF{palette_number}",
        f"PaletteColorG{palette_number}",
        f"PaletteColorH{palette_number}",
        f"PaletteColorI{palette_number}",
        f"PaletteColorJ{palette_number}",
        f"PaletteColorK{palette_number}",
        f"PaletteColorL{palette_number}"
    ]


    # Nombre personalizado para la paleta
    palette_name = palette_names.get(palette_number, f"Palette {palette_number}")
    xml = f'\t<a:extraClrScheme>\n'
    xml += f'\t\t<a:clrScheme name="{palette_name}">\n'

    # Generación del bloque de colores
    for key, shape_name in zip(keys, shape_names):
        color = color_dict.get(shape_name, "000000")
        xml += f'\t\t\t<a:{key}>\n'
        xml += f'\t\t\t\t<a:srgbClr val="{color}"/>\n'
        xml += f'\t\t\t</a:{key}>\n'

    xml += f'\t\t</a:clrScheme>\n'

    # Mapeo de colores
    #xml += (
    #    f'\t\t<a:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" '
    #    f'accent1="accent1" accent2="accent2" accent3="accent3" '
    #    f'accent4="accent4" accent5="accent5" accent6="accent6" '
    #    f'hlink="hlink" folHlink="folHlink"/>\n'
    #)

    clr_map_line = build_clr_map_from_alt_texts(palette_number)
    xml += clr_map_line + '\n'

    xml += f'\t</a:extraClrScheme>'
    return xml


def extract_color_palettes(slide_file):
    all_colors, palette_names = extract_palette_colors_from_slide(slide_file)
    if not all_colors:
        log_info("No colors found in the slide.")
        return None

    if not has_any_visible_palette():
        final_output = "<a:extraClrSchemeLst/>"
        log_info("No palettes visible. Custom color schemes will be cleared.")
        return final_output

    all_blocks = []
    for i in range(1, 5):
        if is_copy_from_theme_button_visible(i):
            block = generate_extra_scheme_block(i, all_colors, palette_names)
            all_blocks.append(block)
        else:
            log_info(f"Palette {i} skipped because CopyFromThemeBtn{i} is hidden")

    final_output = "\n".join(all_blocks)
    return final_output



    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(final_output)
        log_info(f"Palettes saved to {OUTPUT_FILE}")
    except Exception as e:
        log_error(f"Error saving palette file: {e}")

    return final_output

def extract_color_palettes_wrapper(slide_file, shape_names, namespaces):
    return extract_color_palettes(slide_file)

if __name__ == "__main__":
    print("🎯 Extrayendo paletas visibles y generando XML...\n")
    result = extract_color_palettes(SLIDE_PATH)

    if result:
        print("\n✅ Resultado generado:\n")
        print(result)
    else:
        print("\n⚠️  No se pudo generar el XML.")
