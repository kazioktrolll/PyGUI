from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="PyGUI",
    version="0.1.1",
    author="kazioktrolll",
    author_email="",
    description="A short description of your project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kazioktrolll/PyGUI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[]
)
