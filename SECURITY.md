# Security policy

## Supported versions

| Version | Supported |
|---------|-----------|
| Latest on `main` | Yes |

## Reporting a vulnerability

If you discover a security vulnerability in this repository, please report it responsibly:

1. **Do not** open a public issue
2. Email Joseph.Raetano@gmail.com with a description of the vulnerability
3. Include steps to reproduce if possible

You should receive a response within 7 days. We will work with you to understand and address the issue before any public disclosure.

## Scope

This repository contains research datasets, pre-trained classifiers (pickle files), and Jupyter notebooks. The primary security concerns are:

- Malicious content in pickle files (classifiers are trained and committed by the maintainer only)
- Notebook outputs containing unintended data exposure
- Dependencies with known vulnerabilities

## Dependencies

If you notice a dependency with a known CVE, please open an issue or email directly.
