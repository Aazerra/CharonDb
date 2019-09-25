from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='charondb',
      version='0.2',
      description='CharonDb utils for connect to databases',
      url='http://github.com/Tahapy/CharonDB',
      author='Mohammad Taha (TahaPY)',
      author_email='taha@cerberusteam.ir',
      license='MIT',
      packages=['charondb'],
      install_requires=["pymysql"],
      long_description=long_description,
      long_description_content_type="text/markdown",
      python_requires='>=3.6')
