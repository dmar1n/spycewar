from setuptools import setup

setup(
    name="Spacewar!",
    version="0.1.0",
    install_requires=[
        "pygame",
        "pre-commit",
        "loguru",
    ],
    packages=["spacewar"],
)
