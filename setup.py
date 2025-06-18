import subprocess
import sys
from setuptools import setup, find_packages


def get_version():
    """Get version from version.py script."""
    try:
        result = subprocess.run([sys.executable, "version.py"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback version if script fails
        return "0.0.0.dev1"


setup(
    name="tofupilot",
    version=get_version(),
    description="A client library for accessing TofuPilot API v1",
    packages=find_packages(),
    package_data={
        "tofupilot": ["**/py.typed"],
    },
    include_package_data=True,
    install_requires=[
        "httpx>=0.23.0,<0.29.0",
        "attrs>=22.2.0",
        "python-dateutil>=2.8.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)