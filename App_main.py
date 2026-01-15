import os
import sys
import config

# Asegurar que el script se ejecuta desde su propia carpeta
#SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_DIR = config.PATH
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from lxml_loader import load_lxml
etree = load_lxml()

from clean_dir import clean_output_files
from log_writer import log_info, log_warning, log_error, log_separator

from clean_folders import clean_FOLDER_FOR_EXTRACTED_APPs
import create_thmx
from extract_pptm import extract_pptm  # 🔹 Se importa el módulo separado
from process_styles import process_styles  # 🔹 Se importa el nuevo módulo separado
from rename_theme_elements import rename_theme_elements

# 🔹 Variables adicionales configurables

OUTPUT_THMX_PATH = os.path.splitext(config.THMX_FILE_DESTINATION)[0]+".thmx"

PPTM_PATH = os.path.join(config.TOOL_DIRECTORY, config.FILE)

log_separator()
log_info("                NEW EVENT                ")

def process_files():
    try:
        create_thmx.create_thmx_from_folder(config.DESTINATION_FOLDER_FOR_THMX, OUTPUT_THMX_PATH)
        log_info(f"Process completed: {OUTPUT_THMX_PATH}")
    except Exception as e:
        log_error(f"Error finalizing: {e}")

if __name__ == "__main__":
    log_info("🚀 Program execution started")
    if extract_pptm(config.FOLDER_FOR_EXTRACTED_APP, PPTM_PATH):
        process_styles() 
        rename_theme_elements()
        process_files()
        clean_FOLDER_FOR_EXTRACTED_APPs()
        clean_output_files()
    log_info("🏁 Program execution finished")
