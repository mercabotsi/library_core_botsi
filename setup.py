# setup.py
from setuptools import setup, find_packages

# Especifica la ruta completa al archivo requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    
setup(
    name='core_botsi',
    version='0.1',
    description='Core MercaBotsi para crear Bots',
    author='Leonardo MercaBotsi',
    packages=find_packages(),
    install_requires=requirements,
    license='MIT',
    url='https://github.com/mercabotsi/library_core_botsi',
)
