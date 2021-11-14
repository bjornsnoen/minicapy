# Minicapy, python bindings for minica, a mini CA
A small python library for using minica to create ssl certificates

## Installation
Hopefully you should be able to simply pip install this package

`pip install minicapy`

If there is no wheel built for your platform you'll have to build
the package yourself. All you need is the go language and gnu make.
Once those are installed, simply run `make` in the root of the repo.

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