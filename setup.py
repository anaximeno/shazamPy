from setuptools import setup, find_packages

with open("VERSION", "rt") as v:
    __version__ = v.read()

with open("README.md", "rt") as ld:
    long_desc = ld.read()

setup(
    name='shazam',
    version=__version__,
    packages=find_packages(),
    package_dir={'': 'usr/share/'},
    py_modules=["shazam"],
    url='https://github.com/anaximeno/checksum',
    license='GPL-3.0 License',
    author='Anaximeno Brito',
    author_email='anaximenobrito@gmail.com',
    description='A CLI-based program that compares the sum',
    long_description=long_desc,
    zip_safe=False,
    install_requires=[
        'argparse',
        'termcolor',
        'alive-progress',
    ],
    entry_points='''
        [console_scripts]
        shazam=shazam:cli
    ''',
    classfiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
        'Operating System :: Linux',
        'Topic :: Software Development :: File Integrity',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
    ]
)
