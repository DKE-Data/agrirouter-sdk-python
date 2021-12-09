from setuptools import setup

setup(
    name='agrirouter',
    version='1.0.0',
    packages=['agrirouter'],
    python_requires=">= 3.6",
    url='https://github.com/DKE-Data/agrirouter-sdk-python',
    license='Apache-2.0',
    author='agrirouter',
    author_email='info@dke-data.com',
    description="""This project contains the API for the communication with the agrirouter. Everything you need for the
                    onboarding process, secure communication and much more.""",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        'certifi~=2021.5.30',
        'cffi~=1.14.6',
        'charset-normalizer~=2.0.6',
        'cryptography~=3.4.8',
        'idna~=3.2',
        'pycparser~=2.20',
        'requests~=2.26.0',
        'urllib3~=1.26.7',
        'paho-mqtt~=1.5.1',
        'protobuf~=3.18.0'
    ],
    project_urls={
        'Documentation': 'https://github.com/DKE-Data/agrirouter-sdk-python',
        'Source': 'https://github.com/DKE-Data/agrirouter-sdk-python',
    },
)
