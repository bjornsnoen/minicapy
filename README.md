# Minicapy, python bindings for minica, a mini CA A small python library for
using minica to create ssl certificates

## Installation
This package is pip installable, simply

`pip install minicapy`

If you want to build it yourself there is a makefile included.  If there is no
binary wheel for your platform you'll need to have `gnu make` and `go` installed
in order to install this package.

## Usage
```python
from minicapy import minica

success = minica.create_domain_cert("somedomain.com")
if success > 0:
    print("Something went wrong")

# Or
success = minica.create_ip_cert("10.0.0.25")
if success > 0:
    print("Something went wrong")
```

## Return codes
The functions return ints, which have the following meanings

| Return code | Meaning                                                   |
|-------------|-----------------------------------------------------------|
| 0           | Success                                                   |
| 1           | Couldn't create root cert files minica.pem/minica-key.pem |
| 2           | Couldn't create domain/ip cert, probably already exist    |
