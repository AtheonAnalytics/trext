from setuptools import setup

with open('README.rst', 'r') as f:
    readme = f.read()

setup(name='TRExt',
      version='0.1',
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
      install_requires=[
          'pyodbc',
          'mock',
      ]
      )
