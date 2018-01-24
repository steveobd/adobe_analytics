import os
import io
import re
import setuptools


# Read version from __init__.py file of project
# Taken from https://packaging.python.org/guides/single-sourcing-package-version/
def read(*names, **kwargs):
    file_path = os.path.dirname(__file__)
    with io.open(
            os.path.join(file_path, *names),
            encoding=kwargs.get("encoding", "utf8")) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


PACKAGES = [
    "adobe_analytics"
]

DEPENDENCIES = [
    'requests',
    'python-dateutil',
]

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Programming Language :: Python :: 3.6'
]

KEYWORDS = [
    'data',
    'analytics',
    'api',
    'wrapper',
    'adobe',
    'omniture',
    'sitecatalyst',
    'python',
    'report',
    'bi'
]

setuptools.setup(
    name='adobe_analytics',
    description='A wrapper for the Adobe Analytics API.',
    keywords=" ".join(KEYWORDS),
    author='Martin Winkel',
    author_email='martin.winkel.ppsn@gmail.com',
    url='http://stdbrouw.github.com/adobe_analytics/',
    download_url='http://www.github.com/stdbrouw/adobe_analytics/tarball/master',
    version=find_version("adobe_analytics", "__init__.py"),
    license='MIT',
    packages=PACKAGES,
    install_requires=DEPENDENCIES,
    classifiers=CLASSIFIERS
)
