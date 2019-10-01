def encrypt_caesar(plaintext) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''
    shift = 3
    for ch in plaintext:
        if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
            if ord('Z') < ord(ch) + shift < ord('a') or ord(ch) + shift > ord('z'):
                ciphertext += chr(ord(ch) + shift - 26)
            else:
                ciphertext += chr(ord(ch) + shift)
        else:
            ciphertext += ch
    return ciphertext


def decrypt_caesar(ciphertext) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ''
    shift = 3
    for ch in ciphertext:
        if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
            if ord('Z') < ord(ch) - shift < ord('a') or ord(ch) - shift < ord('A'):
                plaintext += chr(ord(ch) - shift + 26)
            else:
                plaintext += chr(ord(ch) - shift)
        else:
            plaintext += ch
    return plaintext