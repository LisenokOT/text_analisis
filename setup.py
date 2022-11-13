import re
from os import path

import setuptools


def read(fname):
    return open(path.join(path.dirname(__file__), fname),
                encoding="utf-8").read()


metadata = dict(
    re.findall(
        r"""__([a-z]+)__ = '([^']+)""", read("TextAnalysis/__init__.py")
    )
)


setuptools.setup(
    name='TextAnalysis',
    version=metadata["version"],
    author="IKBO-02-20",
    description='Определение темы текста по его содержанию',
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=['TextAnalysis'],
    package_data={
        'FTA': ['hunspell/*', 'demo_data/*']
    },
    entry_points={
        'console_scripts': [
            'TextAnalysis = TextAnalysis.__main__:main'
        ]
    },
    install_requires=[
        'hunspell',
        'docopt',
    ],
    extras_require={
        'dev': [
            'setuptools',
            'pytest',
            'autopep8',
            'pydocstyle',
            'pylint',
            'sphinx',
            'sphinx_rtd_theme'
        ]
    },
    python_requires='>=3.7, <4'
)
