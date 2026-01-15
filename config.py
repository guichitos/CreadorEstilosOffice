import os
import sys
import tempfile

# 🔹 Configuración centralizada de archivos y rutas

# Modo de ejecución: "original" usa PATH, "temp" usa la carpeta temporal
RUN_MODE = "temp"  
FILE="App.pptm"
THMX_FILE_SOURCE = "OriginalTheme.thmx"
THMX_FILE_DESTINATION = "CustomTheme.thmx"
DESTINATION_FOLDER_FOR_THMX = "extracted_destination_thmx"
FOLDER_FOR_EXTRACTED_APP = "extracted_app_pptm"
CURRENT_FILE_PATH = os.path.abspath(__file__)
PARENT_DIR = os.path.dirname(CURRENT_FILE_PATH)

if getattr(sys, "frozen", False):
    EXECUTABLE_DIR = os.path.dirname(sys.executable)
    TOOL_DIRECTORY = os.path.dirname(EXECUTABLE_DIR)
else:
    TOOL_DIRECTORY = PARENT_DIR
TEMP_DIRECTORY=tempfile.gettempdir()


# Ruta final según el modo seleccionado
if RUN_MODE == "temp":
    PATH = os.environ.get("TEMP", "/tmp")  # Carpeta temporal en Windows o Linux/macOS
    
else:
    PATH = PARENT_DIR
    
FINAL_PATH = os.path.join(PATH, THMX_FILE_DESTINATION)    
