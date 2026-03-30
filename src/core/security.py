"""
PDF security operations: lock and unlock PDFs.
Uses pikepdf for encryption/decryption.
"""

import os
import pikepdf


def lock_pdf(
    pdf_path: str,
    output_path: str,
    user_password: str,
    owner_password: str = "",
) -> str:
    """
    Add password protection to a PDF.

    user_password  – password required to open the document
    owner_password – password for full permissions (defaults to user_password if empty)
    Returns output path.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if not owner_password:
        owner_password = user_password

    with pikepdf.open(pdf_path) as pdf:
        pdf.save(
            output_path,
            encryption=pikepdf.Encryption(
                user=user_password,
                owner=owner_password,
                R=6,  # AES-256
            ),
        )
    return output_path


def unlock_pdf(pdf_path: str, output_path: str, password: str) -> str:
    """
    Remove password protection from a PDF.

    password – the password required to open the document.
    Returns output path.
    Raises pikepdf.PasswordError if the password is wrong.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    with pikepdf.open(pdf_path, password=password) as pdf:
        pdf.save(output_path)
    return output_path
