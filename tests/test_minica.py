from os import chdir, getcwd
from pathlib import Path
from shutil import rmtree

import pytest
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.extensions import SubjectAlternativeName

from minicapy import minica


@pytest.fixture(autouse=True)
def fake_directory(tmpdir):
    current_dir = getcwd()

    chdir(tmpdir)
    yield

    tmp_path = Path(tmpdir)
    for file in tmp_path.iterdir():
        if file.is_dir():
            rmtree(file)
        else:
            file.unlink()

    chdir(current_dir)


def get_sans(cert: Path) -> list[str]:
    parsed_cert = x509.load_pem_x509_certificate(cert.read_bytes(), default_backend())
    san_ext = parsed_cert.extensions.get_extension_for_class(SubjectAlternativeName)
    return san_ext.value.get_values_for_type(x509.DNSName)


def get_cn(cert: Path) -> str:
    parsed_cert = x509.load_pem_x509_certificate(cert.read_bytes(), default_backend())
    cn = parsed_cert.subject
    return str(list(cn)[0].value)


def test_generate_domain_cert():
    result = minica.create_domain_cert("test.com")

    assert result == 0

    expected_directory = Path("test.com")
    expected_cert = expected_directory / "cert.pem"
    expected_key = expected_directory / "key.pem"

    for file in [expected_directory, expected_key, expected_cert]:
        assert file.exists()

    assert get_cn(expected_cert) == "test.com"

    rmtree(expected_directory)


def test_generate_ip_cert():
    result = minica.create_ip_cert("192.168.1.1")

    assert result == 0

    expected_directory = Path("192.168.1.1")
    expected_cert = expected_directory / "cert.pem"
    expected_key = expected_directory / "key.pem"

    for file in [expected_directory, expected_key, expected_cert]:
        assert file.exists()

    assert get_cn(expected_cert) == "192.168.1.1"

    rmtree(expected_directory)


def test_generate_wildcard():
    result = minica.create_wildcard_certificate("*.test.com", include_base_domain=True)

    assert result == 0

    expected_directory = Path("_.test.com")
    expected_cert = expected_directory / "cert.pem"
    expected_key = expected_directory / "key.pem"

    for file in [expected_directory, expected_key, expected_cert]:
        assert file.exists()

    sans = get_sans(expected_cert)
    assert len(sans) == 2

    assert sans[0] == "*.test.com"
    assert sans[1] == "test.com"

    rmtree(expected_directory)
