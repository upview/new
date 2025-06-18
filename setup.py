from setuptools import setup, find_packages

setup(
    name="tofupilot",
    version="2.0.0",
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