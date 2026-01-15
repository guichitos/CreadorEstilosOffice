import os
import zipfile
from log_writer import log_info, log_warning, log_error

def create_thmx_from_folder(folder_path, output_thmx):
    print(f"Creando tema {output_thmx}.")
    
    if not os.path.exists(folder_path):
        print(f"❌ Error: No se encontró el directorio {folder_path}.")
        return False

    # Crear el archivo ZIP y renombrarlo a .thmx
    with zipfile.ZipFile(output_thmx, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Mantiene la estructura interna
                zipf.write(file_path, arcname)
    return True
