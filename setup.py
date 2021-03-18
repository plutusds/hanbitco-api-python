from setuptools import setup, find_packages

version = "1.0.2"

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name             = "hanbitco-api",
    version          = version,
    description      = "Offical API Python Wrapper for Hanbitco Exchange",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author           = "Kevin Kim",
    author_email     = "kevink1103@plutusds.com",
    license          = "MIT",
    url              = "https://github.com/plutusds/hanbitco-api",
    download_url     = "https://github.com/plutusds/hanbitco-api/dist/hanbitco_api-{}-py3-none-any.whl".format(version),
    install_requires = [],
    packages         = find_packages(exclude = []),
    keywords         = ["cryptocurrency", "exchange", "api"],
    python_requires  = ">=3.6",
    zip_safe         = False,
    classifiers      = [
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)
