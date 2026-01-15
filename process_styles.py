import os
import log_writer
import insert_fillstyle
import fn_ln
import fn_fill
import fn_effect
import fn_bg
import fn_custom_colors
import fn_color_palette
import insert_custom_colors
import insert_color_palettes
from check_custom_color_visibility import is_custom_color_label_visible
from erase_custom_colors import clear_custom_colors_from_thmx


import config

FOLDER_FOR_EXTRACTED_APP = config.FOLDER_FOR_EXTRACTED_APP
THMX_PATH = os.path.join(config.PATH, config.THMX_FILE_SOURCE)
def process_styles():
    """Extracts and processes styles from the presentation."""
    slide_file = os.path.join(config.TEMP_DIRECTORY, FOLDER_FOR_EXTRACTED_APP, "ppt", "slides", "slide1.xml")
    if not os.path.exists(slide_file):
        log_writer.log_error("slide1.xml not found")
        return

    namespaces = {
        'p': "http://schemas.openxmlformats.org/presentationml/2006/main",
        'a': "http://schemas.openxmlformats.org/drawingml/2006/main"
    }

    separate_by_style = True

    tasks = [
        {"function": fn_ln.extract_line_styles, "names": ["Line1Style", "Line2Style", "Line3Style"], "output": "ln_extracted.txt", "xml_tag": "lnStyleLst"},
        {"function": fn_fill.extract_fill_styles, "names": ["Fill1Style", "Fill2Style", "Fill3Style"], "output": "fill_extracted.txt", "xml_tag": "fillStyleLst"},
        {"function": fn_effect.extract_effect_styles, "names": ["Effect1Style", "Effect2Style", "Effect3Style"], "output": "effects_extracted.txt", "xml_tag": "effectStyleLst"},
        {"function": fn_bg.extract_background_styles, "names": ["Background1Style", "Background2Style", "Background3Style"], "output": "background_extracted.txt", "xml_tag": "bgFillStyleLst"},
        {"function": fn_custom_colors.extract_custom_colors, "names": ["CustomColor"], "output": "custom_colors_extracted.txt", "xml_tag": "custClrLst"},
        {"function": fn_color_palette.extract_color_palettes_wrapper, "names": ["CustomPalettes"], "output": "palette_extracted.txt", "xml_tag": "extraClrSchemeLst"}

    ]


    for task in tasks:
        # Validación para custClrLst
        if task["xml_tag"] == "custClrLst":
            if not is_custom_color_label_visible():
                log_writer.log_info("CustomColorLabel is hidden. Clearing <a:custClrLst>.")
                clear_custom_colors_from_thmx(config.DESTINATION_FOLDER_FOR_THMX)
                continue

        extracted_texts = []

        for style_name in task["names"]:
            extracted_text = task["function"](slide_file, [style_name], namespaces)
            if extracted_text:
                if separate_by_style:
                    extracted_text = f"<!-- 🔹 Extracted Style: {style_name} -->\n" + extracted_text
                extracted_texts.append(extracted_text)

        if extracted_texts:
            final_text = "\n\n".join(extracted_texts)
            try:
                with open(task["output"], "w", encoding="utf-8") as f:
                    f.write(final_text)

                if task["xml_tag"] == "custClrLst":
                    insert_custom_colors.insert_custom_colors_into_thmx(THMX_PATH, final_text)
                elif task["xml_tag"] == "extraClrSchemeLst":
                    insert_color_palettes.insert_into_thmx(THMX_PATH, task["xml_tag"], final_text)
                else:
                    insert_fillstyle.insert_into_thmx(THMX_PATH, task["xml_tag"], final_text)

                log_writer.log_info(f"Processed styles saved to {task['output']}")
            except IOError as e:
                log_writer.log_error(f"Error writing {task['output']}: {e}")

if __name__ == "__main__":
    process_styles()
