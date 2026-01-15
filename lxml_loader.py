import sys
import lxml.etree
def load_lxml():
    """Importa lxml.etree directamente sin intentar instalarla."""
    try:
        
        print("✅ lxml loaded successfully!")
        return lxml.etree
    except ImportError:
        print("❌ Error: lxml is not installed. Please install it using 'pip install lxml'.")
        sys.exit(1)  # Salir si lxml no está instalado

if __name__ == "__main__":
    print("🔹 Running lxml_loader.py as standalone script")
    try:
        etree = load_lxml()

        # 🚀 Prueba de manipulación XML
        root = etree.Element("Root")
        child = etree.SubElement(root, "Child")
        child.text = "Test Text"
        xml_string = etree.tostring(root, pretty_print=True, encoding="utf-8").decode()
        print("✅ Generated XML:\n", xml_string)

    except Exception as e:
        print(f"❌ Error: {e}")
