"""
Development Diary - Setup Configuration
Configuración para la instalación y empaquetado
"""

from setuptools import setup, find_packages
import os

# Leer README
def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()

# Leer requirements
def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='development-diary',
    version='1.0.0',
    description='Diario de desarrollo con IA para documentar tu código',
    long_description=read_file('README.md') if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    author='Tu Nombre',
    author_email='tu.email@example.com',
    url='https://github.com/tuusuario/development-diary',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'development-diary=app:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)