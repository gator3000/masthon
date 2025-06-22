from setuptools import setup

with open("README.md") as f:
    long_description = f.read()
    
setup(
    name='Masthon',
    version='v0.3a',
    description='A simple API for linking masthodon to your python codes.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url='git@gitlab.com:Gator3000/masthon.git',
    author='org.literie.gator',
    author_email='org.literie.gator@h3110.aleeas.com',
    license='GNU/GPL v3',
    packages=['masthon'],
    zip_safe=False,
    python_requires = ">=3.10",
    install_requires=[
        "requests",
    ],
    project_urls = {
        "Homepage": "https://gitlab.com/Gator3000/masthon",
        "Bug Tracker": "https://gitlab.com/Gator3000/masthon/-/issues"
    }

)