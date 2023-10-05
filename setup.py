from setuptools import setup, find_packages

setup(
    name='roj-agrirouter-sdk-python',
    version='1.0.7',
    packages=find_packages(),	
    include_package_data=True,
    python_requires=">= 3.6",
    url='https://github.com/ROJ-ITALY/agrirouter-sdk-python',
    license='Apache-2.0',
    author='Stefano Gurrieri',
    author_email='stefano.gurrieri@vandewiele.com',
    description="""Agrirouter SDK Python patched by ROJ for experimental test to run on App mobile""",
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
        'charset-normalizer~=2.0.6',
        'idna~=3.2',
        'requests~=2.26.0',
        'urllib3~=1.26.7',
        'paho-mqtt~=1.5.1',
        'protobuf~=3.18.0'
    ],
    project_urls={
        'Documentation': 'https://github.com/ROJ-ITALY/agrirouter-sdk-python',
        'Source': 'https://github.com/ROJ-ITALY/agrirouter-sdk-python',
    },
)
