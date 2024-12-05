from setuptools import setup, find_packages

setup(
    name='algoritmo_genetico_ifs',
    version='0.1',
    author='Reinan Souza',
    author_email='reinangabriel1520@gmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'requests',
    ],
)
