"""
AMessage Windows - Desktop Application Entrypoint
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
windows_dir = os.path.abspath(os.path.join(current_dir, ".."))
project_root = os.path.abspath(os.path.join(windows_dir, ".."))

for path in [windows_dir, project_root]:
    if path not in sys.path:
        sys.path.insert(0, path)

from amessage_windows.bridge import CoreBridge
from amessage_windows.ui.main_window import MainWindow

def main():
    bridge = CoreBridge()
    bridge.connect()
    app = MainWindow(bridge)
    try:
        app.mainloop()
    finally:
        bridge.close()

if __name__ == "__main__":
    main()
