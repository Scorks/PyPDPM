from setuptools import find_packages, setup

setup(
    name='PyPDPM',
    packages=find_packages(include=['PyPDPM']),
    version='0.1.0',
    description='A Python library for dealing with PDPM HIPP codes',
    author='Caro Strickland',
    author_email='carostrickland321@gmail.com',
    url = 'https://github.com/Scorks/PyPDPM',
    keywords = ['PDPM', 'HIPPS', 'ICD-10-CM Codes'],
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.3.1'],
    test_suite='tests',
)
