import sys

try:
    import lxml
    print("✅ La librería 'lxml' está instalada")
    sys.exit(0)  # La librería está instalada
except ImportError as e:
    print("❌ Error:", e)
    sys.exit(1)  # La librería no está instalada
