"""
Setup configuration for daily-tracker package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="daily-tracker",
    version="1.0.0",
    author="Your Team",
    author_email="team@yourcompany.com",
    description="Automated daily work tracker with AI-generated summaries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourcompany/daily-tracker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pygetwindow>=0.0.9",
        "pillow>=10.0.0",
        "pytesseract>=0.3.10",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "daily-tracker=daily_tracker.cli:main",
        ],
    },
    include_package_data=True,
)
