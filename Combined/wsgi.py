import sys
from pathlib import Path

# Add the path to the directory containing the CombinedApp package to the system path
combined_app_path = Path(__file__).resolve().parent
sys.path.append(str(combined_app_path))

# Import the app from the CombinedApp package
from Combined import app as application
