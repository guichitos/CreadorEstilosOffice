import os
import sys
import config

# Asegurar que el script se ejecuta desde su propia carpeta
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
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

def configure_runtime_paths(cli_param):
    """Set working folders. If a file parameter is provided, use its folder."""
    if not cli_param:
        return

    execution_directory = os.path.dirname(os.path.abspath(cli_param))
    if not execution_directory:
        return

    config.PATH = execution_directory
    config.TEMP_DIRECTORY = execution_directory

    os.chdir(execution_directory)
    if execution_directory not in sys.path:
        sys.path.insert(0, execution_directory)

    log_info(f"📁 Carpeta de ejecución ajustada al directorio del parámetro: {execution_directory}")


def get_output_thmx_path():
    """Build output path in the active execution directory."""
    output_name = os.path.splitext(os.path.basename(config.THMX_FILE_DESTINATION))[0] + ".thmx"
    return os.path.join(config.PATH, output_name)


def resolve_source_thmx_path():
    """Resolves the source .thmx path using CLI arg[1] when provided."""
    default_source = config.THMX_FILE_SOURCE

    if len(sys.argv) > 1 and sys.argv[1].strip():
        param_source = os.path.abspath(sys.argv[1])
        configure_runtime_paths(param_source)
        config.THMX_FILE_SOURCE = param_source
        log_info(f"🧭 Ejecución con parámetro: {param_source}")

        if os.path.exists(param_source):
            log_info(f"✅ Archivo fuente por parámetro encontrado: {param_source}")
        else:
            log_error(f"❌ Archivo fuente por parámetro no encontrado: {param_source}")
        return param_source

    default_source_path = os.path.abspath(os.path.join(config.PATH, default_source))
    log_info("🧭 Ejecución sin parámetros")
    log_info(f"📄 Usando archivo fuente por defecto: {default_source_path}")

    if os.path.exists(default_source_path):
        log_info(f"✅ Archivo fuente por defecto encontrado: {default_source_path}")
    else:
        log_error(f"❌ Archivo fuente por defecto no encontrado: {default_source_path}")

    return default_source_path


SOURCE_THMX_PATH = resolve_source_thmx_path()
PPTM_PATH = os.path.join(config.TOOL_DIRECTORY, config.FILE)

log_separator()
log_info("                NEW EVENT                ")

def process_files():
    try:
        output_thmx_path = get_output_thmx_path()
        created = create_thmx.create_thmx_from_folder(config.DESTINATION_FOLDER_FOR_THMX, output_thmx_path)
        if created and os.path.exists(output_thmx_path):
            log_info(f"Process completed: {output_thmx_path}")
            return output_thmx_path

        log_error(f"❌ Failed to generate output file: {output_thmx_path}")
        return None
    except Exception as e:
        log_error(f"Error finalizing: {e}")
        return None


def should_delete_source_file(output_thmx_path):
    """Delete source only when CLI param was used and output exists."""
    if len(sys.argv) <= 1:
        return False

    if not output_thmx_path or not os.path.exists(output_thmx_path):
        return False

    if not os.path.exists(SOURCE_THMX_PATH):
        return False

    if os.path.abspath(SOURCE_THMX_PATH) == os.path.abspath(output_thmx_path):
        log_warning("⚠️ Source and output are the same file. Source will not be deleted.")
        return False

    return True


def delete_source_file_if_needed(output_thmx_path):
    if not should_delete_source_file(output_thmx_path):
        return

    try:
        os.remove(SOURCE_THMX_PATH)
        log_info(f"Deleted source theme file: {SOURCE_THMX_PATH}")
    except Exception as e:
        log_error(f"❌ Could not delete source theme file ({SOURCE_THMX_PATH}): {e}")

if __name__ == "__main__":
    log_info("🚀 Program execution started")
    log_info(f"📄 Fuente .thmx seleccionada para esta ejecución: {SOURCE_THMX_PATH}")
    if extract_pptm(config.FOLDER_FOR_EXTRACTED_APP, PPTM_PATH):
        process_styles() 
        rename_theme_elements()
        output_thmx_path = process_files()
        delete_source_file_if_needed(output_thmx_path)
        clean_FOLDER_FOR_EXTRACTED_APPs()
        clean_output_files()
    log_info("🏁 Program execution finished")
