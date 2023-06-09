.. hazmat::

Two-factor authentication
=========================

.. currentmodule:: cryptography.hazmat.primitives.twofactor

This module contains algorithms related to two-factor authentication.

Currently, it contains an algorithm for generating and verifying
one time password values based on Hash-based message authentication
codes (HMAC).

.. class:: InvalidToken

    This is raised when the verify method of a one time password function's
    computed token does not match the expected token.

.. currentmodule:: cryptography.hazmat.primitives.twofactor.hotp

.. data:: HOTPHashTypes

    .. versionadded:: 40.0.0

    Type alias: A union of supported hash algorithm types:
    :class:`~cryptography.hazmat.primitives.hashes.SHA1`,
    :class:`~cryptography.hazmat.primitives.hashes.SHA256` or
    :class:`~cryptography.hazmat.primitives.hashes.SHA512`.

.. class:: HOTP(key, length, algorithm, *, enforce_key_length=True)

    .. versionadded:: 0.3

    HOTP objects take a ``key``, ``length`` and ``algorithm`` parameter. The
    ``key`` should be :doc:`randomly generated bytes </random-numbers>` and is
    recommended to be 160 :term:`bits` in length. The ``length`` parameter
    controls the length of the generated one time password and must be >= 6
    and <= 8.

    This is an implementation of :rfc:`4226`.

    .. doctest::

        >>> import os
        >>> from cryptography.hazmat.primitives.twofactor.hotp import HOTP
        >>> from cryptography.hazmat.primitives.hashes import SHA1
        >>> key = os.urandom(20)
        >>> hotp = HOTP(key, 6, SHA1())
        >>> hotp_value = hotp.generate(0)
        >>> hotp.verify(hotp_value, 0)

    :param key: Per-user secret key. This value must be kept secret
                and be at least 128 :term:`bits`. It is recommended that
                the key be 160 bits.
    :type key: :term:`bytes-like`
    :param int length: Length of generated one time password as ``int``.
    :param cryptography.hazmat.primitives.hashes.HashAlgorithm algorithm: A
        :class:`~cryptography.hazmat.primitives.hashes`
        instance (must match :data:`HOTPHashTypes`).
    :param enforce_key_length: A boolean flag defaulting to True that toggles
        whether a minimum key length of 128 :term:`bits` is enforced. This
        exists to work around the fact that as documented in `Issue #2915`_,
        the Google Authenticator PAM module by default generates 80 bit keys.
        If this flag is set to False, the application developer should
        implement additional checks of the key length before passing it into
        :class:`~cryptography.hazmat.primitives.twofactor.hotp.HOTP`.

        .. versionadded:: 1.5

    :raises ValueError: This is raised if the provided ``key`` is shorter than
        128 :term:`bits` or if the ``length`` parameter is not 6, 7 or 8.
    :raises TypeError: This is raised if the provided ``algorithm`` is not
        :class:`~cryptography.hazmat.primitives.hashes.SHA1()`,
        :class:`~cryptography.hazmat.primitives.hashes.SHA256()` or
        :class:`~cryptography.hazmat.primitives.hashes.SHA512()` or if the
        ``length`` parameter is not an integer.

    .. method:: generate(counter)

        :param int counter: The counter value used to generate the one time
            password.
        :return bytes: A one time password value.

    .. method:: verify(hotp, counter)

        :param bytes hotp: The one time password value to validate.
        :param int counter: The counter value to validate against.
        :raises cryptography.hazmat.primitives.twofactor.InvalidToken: This
             is raised when the supplied HOTP does not match the expected HOTP.

    .. method:: get_provisioning_uri(account_name, counter, issuer)

        .. versionadded:: 1.0

        :param account_name: The display name of account, such as
            ``'Alice Smith'`` or ``'alice@example.com'``.
        :type account_name: str
        :param issuer: The optional display name of issuer. This is typically
            the provider or service the user wants to access using the OTP
            token.
        :type issuer: ``str`` or ``None``
        :param int counter: The current value of counter.
        :return: A URI string.

Throttling
~~~~~~~~~~

Due to the fact that the HOTP algorithm generates rather short tokens that are
6 - 8 digits long, brute force attacks are possible. It is highly recommended
that the server that validates the token implement a throttling scheme that
locks out the account for a period of time after a number of failed attempts.
The number of allowed attempts should be as low as possible while still
ensuring that usability is not significantly impacted.

Re-synchronization of the counter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The server's counter value should only be incremented on a successful HOTP
authentication. However, the counter on the client is incremented every time a
new HOTP value is requested. This can lead to the counter value being out of
synchronization between the client and server.

Due to this, it is highly recommended that the server sets a look-ahead window
that allows the server to calculate the next ``x`` HOTP values and check them
against the supplied HOTP value. This can be accomplished with something
similar to the following code.

.. code-block:: python

    def verify(hotp, counter, look_ahead):
        assert look_ahead >= 0
        correct_counter = None

        otp = HOTP(key, 6)
        for count in range(counter, counter + look_ahead):
            try:
                otp.verify(hotp, count)
                correct_counter = count
            except InvalidToken:
                pass

        return correct_counter

.. currentmodule:: cryptography.hazmat.primitives.twofactor.totp

.. class:: TOTP(key, length, algorithm, time_step, *, enforce_key_length=True)

    TOTP objects take a ``key``, ``length``, ``algorithm`` and ``time_step``
    parameter. The ``key`` should be :doc:`randomly generated bytes
    </random-numbers>` and is recommended to be as long as your hash function's
    output (e.g 256-bit for SHA256). The ``length`` parameter controls the
    length of the generated one time password and must be >= 6 and <= 8.

    This is an implementation of :rfc:`6238`.

    .. doctest::

        >>> import os
        >>> import time
        >>> from cryptography.hazmat.primitives.twofactor.totp import TOTP
        >>> from cryptography.hazmat.primitives.hashes import SHA1
        >>> key = os.urandom(20)
        >>> totp = TOTP(key, 8, SHA1(), 30)
        >>> time_value = time.time()
        >>> totp_value = totp.generate(time_value)
        >>> totp.verify(totp_value, time_value)

    :param key: Per-user secret key. This value must be kept secret
                and be at least 128 :term:`bits`. It is recommended that the
                key be 160 bits.
    :type key: :term:`bytes-like`
    :param int length: Length of generated one time password as ``int``.
    :param cryptography.hazmat.primitives.hashes.HashAlgorithm algorithm: A
        :class:`~cryptography.hazmat.primitives.hashes`
        instance.
    :param int time_step: The time step size. The recommended size is 30.
    :param enforce_key_length: A boolean flag defaulting to True that toggles
        whether a minimum key length of 128 :term:`bits` is enforced. This exists to
        work around the fact that as documented in `Issue #2915`_, the
        Google Authenticator PAM module by default generates 80 bit keys. If
        this flag is set to False, the application develop should implement
        additional checks of the key length before passing it into
        :class:`~cryptography.hazmat.primitives.twofactor.totp.TOTP`.

        .. versionadded:: 1.5
    :raises ValueError: This is raised if the provided ``key`` is shorter than
        128 :term:`bits` or if the ``length`` parameter is not 6, 7 or 8.
    :raises TypeError: This is raised if the provided ``algorithm`` is not
        :class:`~cryptography.hazmat.primitives.hashes.SHA1()`,
        :class:`~cryptography.hazmat.primitives.hashes.SHA256()` or
        :class:`~cryptography.hazmat.primitives.hashes.SHA512()` or if the
        ``length`` parameter is not an integer.

    .. method:: generate(time)

        :param int time: The time value used to generate the one time password.
        :return bytes: A one time password value.

    .. method:: verify(totp, time)

        :param bytes totp: The one time password value to validate.
        :param int time: The time value to validate against.
        :raises cryptography.hazmat.primitives.twofactor.InvalidToken: This
             is raised when the supplied TOTP does not match the expected TOTP.

    .. method:: get_provisioning_uri(account_name, issuer)

        .. versionadded:: 1.0

        :param account_name: The display name of account, such as
            ``'Alice Smith'`` or ``'alice@example.com'``.
        :type account_name: str
        :param issuer: The optional display name of issuer. This is typically
            the provider or service the user wants to access using the OTP
            token.
        :type issuer: ``str`` or ``None``
        :return: A URI string.

Provisioning URI
~~~~~~~~~~~~~~~~

The provisioning URI of HOTP and TOTP is a `feature of Google Authenticator`_
and not actually part of the HOTP or TOTP RFCs. However, it is widely supported
by web sites and mobile applications which are using Two-Factor authentication.

For generating a provisioning URI you can use the ``get_provisioning_uri``
method of HOTP/TOTP instances.

.. code-block:: python

    counter = 5
    account_name = 'alice@example.com'
    issuer_name = 'Example Inc'

    hotp_uri = hotp.get_provisioning_uri(account_name, counter, issuer_name)
    totp_uri = totp.get_provisioning_uri(account_name, issuer_name)

A common usage is encoding the provisioning URI into QR code and guiding users
to scan it with Two-Factor authentication applications in their mobile devices.

.. _`feature of Google Authenticator`: https://github.com/google/google-authenticator/wiki/Key-Uri-Format
.. _`Issue #2915`: https://github.com/pyca/cryptography/issues/2915
