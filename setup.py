from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name = "Masthon",
    version = "v0.1a",
    author = "org.literie.gator",
    author_email = "aelian.brd@proton.me",
    description = "A simple API for linking masthodon to your python codes.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "package URL",
    project_urls = {
        "Homepage": "https://gitlab.com/Gator3000/masthon",
        "Bug Tracker": "https://gitlab.com/Gator3000/masthon/-/issues"
    },
    package_dir = {"": "masthon"},
    packages = setuptools.find_packages(where="masthon"),
    python_requires = ">=3.10"
)
