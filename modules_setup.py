import subprocess
import sys

# import os
# import platform

# pip install modules to avoid "ModuleNotFoundError: No module found named '...'"
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("pandas")
install("elasticsearch")
install("bs4")
install("requests")
install("gitpython")

# maybe pipinstall these modules
# install("platform")
