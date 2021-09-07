# Bits copied from https://github.com/pypa/sampleproject/blob/main/setup.py
from setuptools import setup, find_packages
import pathlib


install_requires = ["click>=8.0.1"]

extras_require = {"test": ["pytest", "nox"], "develop": ["nox", "flake8", "black"]}


here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "readme.md").read_text(encoding="utf-8")

setup(
    name="gab_tidy_data",
    description="Python script to take gab data (from Garc) and put it into a "
    "relational SQLite database ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="QUT Digital Observatory",
    author_email="digitalobservatory@qut.edu.au",
    url="https://github.com/QUT-Digital-Observatory/gab_tidy_data",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Topic :: Sociology",
    ],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        "console_scripts": ["gab_tidy_data = gab_tidy_data.__main__:gab_tidy_data"]
    },
    include_package_data=True,
    package_data={"gab_tidy_data": ["gab_tidy_data/gab_schema.sql"]},
)
