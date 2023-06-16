from setuptools import setup
from livescore_api import __version__, __author__, __repo__, __info__

setup(
    name="livescore-api",
    packages=["livescore_api"],
    version=__version__,
    license="MIT",
    author=__author__,
    maintainer=__author__,
    author_email="smartwacaleb@gmail.com",
    description=__info__,
    url=__repo__,
    project_urls={"Bug Report": f"{__repo__}/issues/new"},
    install_requires=[
    "argparse>=1.1",
    "requests>=2.0.2",
    "pandas>=1.3.3",
    "tabulate==0.9.0",
    "smartbetsAPI==1.1.4",
    "tqdm==4.65.0",
    "colorama==0.4.6",
    ],
    python_requires=">=3.8",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: Free For Home Use",
        "Intended Audience :: Customer Service",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            ("livescore-api = livescore_api.console:main"),
        ]
    },
    keywords=["livescore", "football", "livescore-api", "api"],
)
