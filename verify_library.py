import sys
import os

print("Executable:", sys.executable)
print("Version:", sys.version)
print("PATH:", os.environ.get("PATH"))

try:
    import lxml
    print("lxml OK")
    #input("Press Enter to exit...")
    sys.exit(0)
except ImportError as e:
    print("ImportError:", e)
    #input("Press Enter to exit...")
    sys.exit(1)
