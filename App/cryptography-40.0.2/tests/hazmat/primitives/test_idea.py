# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.


import binascii
import os

import pytest

from cryptography.hazmat.primitives.ciphers import algorithms, modes

from ...utils import load_nist_vectors
from .utils import generate_encrypt_test


@pytest.mark.supported(
    only_if=lambda backend: backend.cipher_supported(
        algorithms._IDEAInternal(b"\x00" * 16), modes.ECB()
    ),
    skip_message="Does not support IDEA ECB",
)
class TestIDEAModeECB:
    test_ecb = generate_encrypt_test(
        load_nist_vectors,
        os.path.join("ciphers", "IDEA"),
        ["idea-ecb.txt"],
        lambda key, **kwargs: algorithms._IDEAInternal(
            binascii.unhexlify(key)
        ),
        lambda **kwargs: modes.ECB(),
    )


@pytest.mark.supported(
    only_if=lambda backend: backend.cipher_supported(
        algorithms._IDEAInternal(b"\x00" * 16), modes.CBC(b"\x00" * 8)
    ),
    skip_message="Does not support IDEA CBC",
)
class TestIDEAModeCBC:
    test_cbc = generate_encrypt_test(
        load_nist_vectors,
        os.path.join("ciphers", "IDEA"),
        ["idea-cbc.txt"],
        lambda key, **kwargs: algorithms._IDEAInternal(
            binascii.unhexlify(key)
        ),
        lambda iv, **kwargs: modes.CBC(binascii.unhexlify(iv)),
    )


@pytest.mark.supported(
    only_if=lambda backend: backend.cipher_supported(
        algorithms._IDEAInternal(b"\x00" * 16), modes.OFB(b"\x00" * 8)
    ),
    skip_message="Does not support IDEA OFB",
)
class TestIDEAModeOFB:
    test_ofb = generate_encrypt_test(
        load_nist_vectors,
        os.path.join("ciphers", "IDEA"),
        ["idea-ofb.txt"],
        lambda key, **kwargs: algorithms._IDEAInternal(
            binascii.unhexlify(key)
        ),
        lambda iv, **kwargs: modes.OFB(binascii.unhexlify(iv)),
    )


@pytest.mark.supported(
    only_if=lambda backend: backend.cipher_supported(
        algorithms._IDEAInternal(b"\x00" * 16), modes.CFB(b"\x00" * 8)
    ),
    skip_message="Does not support IDEA CFB",
)
class TestIDEAModeCFB:
    test_cfb = generate_encrypt_test(
        load_nist_vectors,
        os.path.join("ciphers", "IDEA"),
        ["idea-cfb.txt"],
        lambda key, **kwargs: algorithms._IDEAInternal(
            binascii.unhexlify(key)
        ),
        lambda iv, **kwargs: modes.CFB(binascii.unhexlify(iv)),
    )
