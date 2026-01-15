import os
import zipfile
from log_writer import log_info, log_error




def extract_pptm(FOLDER_FOR_EXTRACTED_APP, PPTM_PATH):
    """Extracts the PPTM file into a temporary folder."""
    if not os.path.exists(FOLDER_FOR_EXTRACTED_APP):
        os.makedirs(FOLDER_FOR_EXTRACTED_APP)

    try:
        with zipfile.ZipFile(PPTM_PATH, 'r') as zip_ref:
            zip_ref.extractall(FOLDER_FOR_EXTRACTED_APP)
        log_info(f"Extracted PPTM file to {FOLDER_FOR_EXTRACTED_APP}")
        return True
    except FileNotFoundError:
        log_error(f"File not found: {PPTM_PATH}")
    except zipfile.BadZipFile:
        log_error(f"Invalid ZIP file: {PPTM_PATH}")
    return False
