import os
import log_writer
import config


def clean_output_files():
    log_writer.log_info("Removing auxiliary files (clean_dir)")
    script_directory = config.PATH

    files_to_delete = [
        "background_extracted.txt",
        "effects_extracted.txt",
        "fill_extracted.txt",
        "ln_extracted.txt",
        "custom_colors_extracted.txt",
        "palette_extracted.txt"
    ]

    for file_name in files_to_delete:
        file_path = os.path.join(script_directory, file_name)

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                log_writer.log_info(f"Deleted: {file_name}")
            except PermissionError:
                log_writer.log_error(f"❌ Permission denied: {file_name}")
            except Exception as e:
                log_writer.log_error(f"❌ Error deleting {file_name}: {e}")
        else:
            log_writer.log_info(f"⚠️ Auxiliary file not found (skip): {file_name}")



if __name__ == "__main__":
    clean_output_files()
