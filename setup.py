from setuptools import setup, find_packages

setup(
    name='progpat',
    version='0.1',
    license='MIT License',
    long_description=open('README.md').read(),
    url='https://github.com/dancps/progpat',
    author='Danilo Calhes',
    #package_dir={'': 'progpat'},
    packages=find_packages(),
    entry_points={'console_scripts': ['progpat=progpat.progpat:main',],},
)
# do the ln
# add to path