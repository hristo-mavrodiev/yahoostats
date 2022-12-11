"""
Yahoo Finance stock statistics dowloader.

https://github.com/pypa/sampleproject/blob/master/setup.py

"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="yahoostats",
    version="0.0.5",
    author="Hristo Mavrodiev",
    author_email="h.mavrodiev@abv.bg",
    description="Yahoo statistics webscraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hristo-mavrodiev/yahoostats",
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas>=1.5.2',
        'requests>=2.28.1',
        'tenacity>=8.1.0',
        'bs4 >= 0.0.1',
        'beautifulsoup4 >= 4.11.1',
        # 'lxml == 4.2.6',
        ],
    project_urls={
        'Bug Reports': 'https://github.com/hristo-mavrodiev/yahoostats/issues',
        'Source': 'https://github.com/hristo-mavrodiev/yahoostats',
    },
)
