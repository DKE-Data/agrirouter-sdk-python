<img src="https://files.my-agrirouter.com/agrirouter_logo.svg" height="100" />

# About the project

The agrirouter is a universal data exchange platform for farmers and
agricultural contractors that makes it possible to connect machinery
and agricultural software, regardless of vendor or manufacturer.
Agrirouter does not save data; it transfers data. As a universal data
exchange platform, agrirouter fills a gap on the way to Farming 4.0.
Its underlying concept unites cross-vendor and discrimination-free
data transfer. You retain full control over your data. Even data
exchange with service providers (e.g. agricultural contractors) and
other partners is uncomplicated: Data are very rapidly transferred via
the online connection, and if you wish, is intelligently connected to
other datasets.

# The current project you’re looking at

This project contains the SDK for the communication with the agrirouter.
Everything you need for the onboard process, secure communication and
much more.

# Installation

Create your virtual environment using any kind of `conda` setup you
would like to have.

``` bash
conda create -n agrirouter-sdk-python python=3.7
conda create -n agrirouter-sdk-python python=3.8
conda create -n agrirouter-sdk-python python=3.9
conda create -n agrirouter-sdk-python python=3.10
conda create -n agrirouter-sdk-python python=3.11
```

Create one of the environments and activate it:

``` bash
conda activate agrirouter-sdk-python
```

After the activation you are ready to install the requirements for the
SDK:

``` bash
pip install -r requirements.txt
```

You are able to select the virtual environment when working with the
IDE.

# Running unit tests

`$ pytest`

# External resources

Here are some external resources for the development:

- [My Agrirouter Website](https://my-agrirouter.com)

- [Integration
  Guide](https://github.com/DKE-Data/agrirouter-interface-documentation)

- [EFDI Protobuf Definition](https://www.aef-online.org)