# drf-pyseto

[![PyPI version](https://img.shields.io/pypi/v/drf-pyseto.svg)](https://pypi.org/project/drf-pyseto/)
[![Python versions](https://img.shields.io/pypi/pyversions/drf-pyseto.svg)](https://pypi.org/project/drf-pyseto/)
[![Django versions](https://img.shields.io/pypi/djversions/drf-pyseto.svg)](https://pypi.org/project/drf-pyseto/)

A simple, secure, and modern [PASETO (Platform-Agnostic Security Tokens)](https://paseto.io/) authentication backend for Django REST Framework (DRF).

`drf-pyseto` utilizes the **v4.local** (symmetric encryption) PASETO specification, providing a more secure alternative to JWTs by preventing cryptographic agility attacks and minimizing misconfigurations. It is heavily inspired by SimpleJWT but focuses purely on PASETO.

## Why PASETO over JWT?
JSON Web Tokens (JWT) have historically been the default for modern REST API authentication, but they give developers too many choices regarding algorithms (including the infamous `none` signature scheme), which often lead to security vulnerabilities.

PASETO limits these choices intentionally. By demanding specific, modern cryptographic practices, it heavily reduces the chance of misconfiguration. `drf-pyseto` implements the **v4.local** standard which uses **XChaCha20-Poly1305** for symmetric encryption, meaning token claims are fully encrypted and hidden from the client, not just signed.

## Features

- **Secure by Default:** Implements PASETO `v4.local` ensuring robust, symmetric encryption.
- **Seamless Integration:** Built specifically for Django REST Framework. Drop-in replacement for traditional token or JWT authentication.
- **Configurable Lifetimes:** Easily manage separate lifetimes for access and refresh tokens.
- **Modern Ecosystem Compatibility:** Supports Python 3.10–3.14 and Django 4.2–6.0.
