from setuptools import find_packages, setup

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='PyPDPM',
    packages=find_packages(include=['PyPDPM']),
    version='0.0.5.22',
    description='A Python library for dealing with PDPM HIPP codes',
    author='Caro Strickland',
    author_email='carostrickland321@gmail.com',
    url = 'https://github.com/Scorks/PyPDPM',
    long_description=readme,
    keywords = ['PDPM', 'HIPPS', 'ICD-10-CM Codes'],
    license='MIT',
    install_requires=[],
    package_data={'PyPDPM': ['data/*.json']},
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.3.1'],
    test_suite='tests',
)
