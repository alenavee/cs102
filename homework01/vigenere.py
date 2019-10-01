def encrypt_vigenere(plaintext, keyword) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    for i, ch in enumerate(plaintext):
        key_ch = keyword[i % len(keyword)]
        if "A" <= key_ch <= "Z":
            shift = ord(key_ch) - ord('A')
        else:
            shift = ord(key_ch) - ord('a')

        if "A" <= ch <= "Z":
            ciphertext += chr(ord("A") + (ord(ch) - ord("A") + shift) % 26)
        else:
            ciphertext += chr(ord("a") + (ord(ch) - ord("a") + shift) % 26)

    return ciphertext


def decrypt_vigenere(ciphertext, keyword) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    for i, ch in enumerate(ciphertext):
        key_ch = keyword[i % len(keyword)]
        if 'A' <= key_ch <= 'Z':
            shift = ord(key_ch) - ord('A')
        else:
            shift = ord(key_ch) - ord('a')

        if 'A' <= ch <= 'Z':
            plaintext += chr(ord('A') + (26 + ord(ch) - ord('A') - shift) % 26)
        else:
            plaintext += chr(ord("a") + (26 + ord(ch) - ord("a") - shift) % 26)

    return plaintext
