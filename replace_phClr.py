import re
from log_writer import log_info, log_warning, log_error

def replace_schemeClr(input_text):
    print("  Changing for theme colors")
    
    # Lista de colores de tema permitidos
    theme_colors = {"tx1", "tx2", "bg1", "bg2",
                    "accent1", "accent2", "accent3", "accent4", "accent5", "accent6",
                    "hlink", "folHlink", "dk1", "dk2", "lt1", "lt2"}

    # Expresión regular para <a:schemeClr>
    pattern = r'(<a:schemeClr val=")([^"]+)(")'
    
    # Bandera para detectar el primer <a:gs pos="0">
    first_gradient_found = False

    # Función de reemplazo con validación de <a:fgClr>, <a:bgClr> y <a:gs pos="0">
    def replacement(match):
        nonlocal first_gradient_found
        full_match = match.group(0)
        color_value = match.group(2)

        # Buscar la posición en input_text
        pos = input_text.find(full_match)
        if pos != -1:
            before_text = input_text[:pos]  # Texto antes de la coincidencia
            
            # Verificar si estamos dentro de <a:pattFill>
            if "<a:pattFill" in before_text[-500:]:
                
                # Si está dentro de <a:bgClr>, NO reemplazar
                if "<a:bgClr>" in before_text[-100:]:  
                    log_info(f"  Skipping replacement inside <a:bgClr>: {full_match}")
                    return full_match  # Dejarlo sin cambios
                
                # Si está dentro de <a:fgClr>, SÍ reemplazar
                if "<a:fgClr>" in before_text[-100:]:  
                    log_info(f"  Replacing inside <a:fgClr>: {full_match}")
                    return f'{match.group(1)}phClr{match.group(3)}' if color_value in theme_colors else full_match

            # Verificar si estamos dentro de <a:gradFill> y si es el primer <a:gs pos="0">
            if "<a:gradFill>" in before_text[-500:]:
                if 'pos="0"' in before_text[-100:]:  # Solo buscamos en los últimos 100 caracteres
                    if not first_gradient_found:
                        first_gradient_found = True  # Marcar que ya encontramos el primero
                        log_info(f"  Replacing first <a:gs pos='0'> inside <a:gradFill>: {full_match}")
                        return f'{match.group(1)}phClr{match.group(3)}' if color_value in theme_colors else full_match
                    else:
                        log_info(f"  Skipping subsequent <a:gs> in <a:gradFill>: {full_match}")
                        return full_match  # No reemplazar en otros <a:gs>

        # Reemplazo normal si no está dentro de <a:pattFill> o <a:gradFill>
        return f'{match.group(1)}phClr{match.group(3)}' if color_value in theme_colors else full_match

    # Aplicar reemplazo
    return re.sub(pattern, replacement, input_text)
