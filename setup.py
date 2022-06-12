from setuptools import setup

from mypyc.build import mypycify

setup(
    name="yomigaeri",
    packages=["yomigaeri"],
    ext_modules=mypycify([
        "yomigaeri/__init__.py",
        "yomigaeri/bot.py",
        "yomigaeri/command.py"
    ]),
    install_requires=[
        "hikari~=2.0.0.dev108",
        "mypy~=0.961"
    ]
)
