import shutil
import os
import stat
from log_writer import log_info, log_warning, log_error
import config
import tempfile

def handle_rmtree_exception(exc):
    path = exc.filename
    if path:
        os.chmod(path, stat.S_IWRITE)
        try:
            os.remove(path)
            log_warning(f"🔄 Retried and removed: {path}")
        except Exception as e:
            log_error(f"❌ Failed to remove {path}: {e}")

def remove_directory(folder_path):
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path, onexc=handle_rmtree_exception) 
            log_info(f"Folder erased: {folder_path}")
        except Exception as e:
            log_error(f"Can't erase {folder_path}: {e}")

def clean_FOLDER_FOR_EXTRACTED_APPs():
    folders_to_remove = [config.FOLDER_FOR_EXTRACTED_APP, config.DESTINATION_FOLDER_FOR_THMX]

    for folder in folders_to_remove:
        remove_directory(os.path.join(config.TEMP_DIRECTORY, folder))


if __name__ == "__main__":
    clean_FOLDER_FOR_EXTRACTED_APPs()

