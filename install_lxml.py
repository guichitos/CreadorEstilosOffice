import sys
import subprocess

def is_lxml_installed():
    """Verifica si lxml ya está instalada."""
    try:
        import lxml
        return True
    except ImportError:
        return False

def install_lxml():
    """Instala lxml solo si no está presente."""
    if is_lxml_installed():
        print("✅ lxml is already installed!")
        return

    print("📦 Installing lxml via pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-warn-script-location", "--disable-pip-version-check", "lxml"])
        print("✅ lxml installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_lxml()  # Solo intentará instalar si no está ya instalada

    # 🚀 Verificar que lxml se instaló correctamente
    try:
        import lxml.etree
        print("✅ lxml is now available!")

        # Prueba de manipulación XML
        root = lxml.etree.Element("Root")
        child = lxml.etree.SubElement(root, "Child")
        child.text = "Test Text"
        xml_string = lxml.etree.tostring(root, pretty_print=True, encoding="utf-8").decode()
        print("✅ Generated XML:\n", xml_string)

    except ImportError:
        print("❌ lxml was not installed correctly.")
