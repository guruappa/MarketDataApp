import codecs
import os.path

from setuptools import setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as filepath:
        return filepath.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='market_data_api',
    version=get_version("src/market_data_api/__init__.py"),
    packages=['market_data_api'],
    package_dir={'': 'src'},
    url='https://github.com/guruappa/MarketDataApp',
    license='MIT',
    author='Guruppa Padsali',
    author_email='guruappa@gmail.com',
    description='Python SDK for working with the MarketData APIs',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: Implementation',
        'Topic :: Office/Business :: Financial :: Investment',
    ],

)
