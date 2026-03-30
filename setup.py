from setuptools import setup, find_packages

setup(
    name="pdf-solutions",
    version="1.0.0",
    description="All-in-one PDF Solutions Desktop Application",
    author="Tuhin",
    packages=find_packages(),
    install_requires=[
        "PySide6>=6.5.0",
        "PyMuPDF>=1.23.0",
        "pypdf>=3.0.0",
        "reportlab>=4.0.0",
        "Pillow>=10.0.0",
        "openpyxl>=3.1.0",
        "python-docx>=1.0.0",
        "pikepdf>=8.0.0",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "pdf-solutions=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
