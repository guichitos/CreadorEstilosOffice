import os
import zipfile
import shutil
import tempfile

def compress_and_rename_to_thmx():
    temp_dir = os.environ.get("TEMP", tempfile.gettempdir())
    folder_to_zip = os.path.join(temp_dir, "extracted_destination_thmx")
    zip_path = os.path.join(temp_dir, "new_theme.zip")
    thmx_path = os.path.join(temp_dir, "new_theme.thmx")

    if not os.path.exists(folder_to_zip):
        print(f"❌ La carpeta no existe: {folder_to_zip}")
        return

    # Crear archivo ZIP
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_to_zip):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, folder_to_zip)
                zipf.write(abs_path, rel_path)

    # Renombrar a .thmx
    if os.path.exists(thmx_path):
        os.remove(thmx_path)

    shutil.move(zip_path, thmx_path)
    print(f"✅ Tema comprimido y guardado como: {thmx_path}")

if __name__ == "__main__":
    compress_and_rename_to_thmx()
