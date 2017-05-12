from setuptools import setup

setup(name='TRExt',
      version='0.1',
      description='TRExt - Tableau Refresh Extract (Externally)',
      url="https://github.com/AtheonAnalytics/trext",
      author='Vathsala Achar',
      author_email='vathsala@atheon.co.uk',
      license='MIT',
      packages=['trext'],
      install_requires=[
            'pyodbc',
      ]
)

