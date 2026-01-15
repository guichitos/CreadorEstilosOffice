from extract_alt_texts import get_palette_alt_texts
import log_writer

def build_clr_map_from_alt_texts(palette_number):
    expected_keys = [
        "bg1", "tx1", "bg2", "tx2",
        "accent1", "accent2", "accent3",
        "accent4", "accent5", "accent6",
        "hlink", "folHlink"
    ]

    alt_texts = get_palette_alt_texts(palette_number)
    descr_values = list(alt_texts.values())  # En el orden en que aparecen

    attributes = [
        f'{key}="{descr_values[i] if i < len(descr_values) else ""}"'
        for i, key in enumerate(expected_keys)
    ]

    result = f'<a:clrMap {" ".join(attributes)}/>'
    log_writer.log_event(result)
    return result

if __name__ == "__main__":
    clr_map_line = build_clr_map_from_alt_texts(1)
