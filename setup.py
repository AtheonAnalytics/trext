import os
import io
import re
from setuptools import setup

with open('README.rst', 'r') as f:
    readme = f.read()


def read(*names, **kwargs):
    with io.open(
            os.path.join(os.path.dirname(__file__), *names),
            encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='TRExt',
      version=find_version("trext", "__init__.py"),
      description='TRExt - Tableau Refresh Extract (Externally)',
      url="https://github.com/AtheonAnalytics/trext",
      author='Vathsala Achar',
      author_email='vathsala@atheon.co.uk',
      license='MIT',
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Programming Language :: Python :: 2.7",
      ],
      packages=[
          'trext',
          'trext.db',
          'trext.extract'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=[
          'pyodbc',
          'mock',
      ]
      )
