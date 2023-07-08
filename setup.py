import setuptools
from iniparser import __version__ as version

f = open("README.md", encoding="UTF-8")
long_description = f.read()
f.close()

setuptools.setup(
    name="iniparser",
    version=version,
    author="HugeBrain16",
    author_email="hugebrain16@gmail.com",
    description="a minimalist (?) and simple ini parser.",
    license="MIT",
    keywords="cfg ini parser iniparser configparser file",
    url="https://github.com/HugeBrain16/iniparser",
    py_modules=["iniparser"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
