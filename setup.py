"""
AutoDev - AI Full-Stack Development Team
Production-ready package setup
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
README = (Path(__file__).parent / "README.md").read_text()

# Read requirements
REQUIREMENTS = (Path(__file__).parent / "requirements.txt").read_text().splitlines()

setup(
    name="autodev-ai",
    version="1.0.0",
    author="Arya Doshi",
    author_email="aryadoshii@gmail.com",
    description="AI-powered full-stack development team using Qwen3-Coder and CrewAI",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/aryadoshii/autodev",
    packages=find_packages(exclude=["tests", "docs", "output"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "autodev=autodev.cli:main",
            "autodev-generate=autodev.crews.dev_crew:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "ai",
        "code-generation",
        "full-stack",
        "crewai",
        "qwen",
        "automation",
        "development",
    ],
    project_urls={
        "Bug Reports": "https://github.com/aryadoshii/autodev/issues",
        "Source": "https://github.com/aryadoshii/autodev",
        "Documentation": "https://github.com/aryadoshii/autodev/docs",
    },
)
