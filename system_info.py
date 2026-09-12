import os
import platform
import psutil
from importlib.metadata import version, PackageNotFoundError

def get_package_version(package_name):

    try:
        return version(package_name)

    except PackageNotFoundError:
        return "Not Installed"

def get_system_info():

    processor = os.environ.get("PROCESSOR_IDENTIFIER", platform.processor())

    return {
        "Operating System": platform.system(),
        "OS Release": platform.release(),
        "OS Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": processor,
        "Python Version": platform.python_version(),
        "Logical CPU Cores": os.cpu_count(),
        "Physical CPU cores": psutil.cpu_count(logical=False),
        "Total RAM (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "Cryptography Version": get_package_version("cryptography"),
        "liboqs-python Version": get_package_version("liboqs-python")
    }