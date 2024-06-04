from setuptools import setup

version = "0.0.6"
repo = "https://github.com/Simatwa/livescore-api"
info = "Access and manipulate matches from Livescore.com"
author = "Smartwa"

setup(
    name="livescore-api",
    packages=["livescore_api"],
    version=version,
    license="MIT",
    author=author,
    maintainer=author,
    author_email="smartwacaleb@gmail.com",
    description=info,
    url=repo,
    project_urls={"Bug Report": f"{repo}/issues/new"},
    install_requires=[
        "argparse>=1.1",
        "requests>=2.0.2",
        "pandas>=1.3.3",
        "tabulate==0.9.0",
        "smartbetsAPI==1.3.1",
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
