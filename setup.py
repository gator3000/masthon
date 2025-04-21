from setuptools import find_packages, setup

setup(
    name="masthon",
    description="A simple package to handle masthodon bots.",
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3',
    url="https://gitlab.com/Gator3000/masthon.git",
    author="org.literie.gator",
    license="GNU/GPL v3",
    install_requires=[],
    zip_safe=False
)