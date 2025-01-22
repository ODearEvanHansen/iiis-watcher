from setuptools import setup, find_packages

setup(
    name="iiis_watcher",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "python-dotenv",
        "schedule",
        "pytest"
    ],
)