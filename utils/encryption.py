from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# 32-byte key for AES-256
KEY = b'12345678901234567890123456789012'

def encrypt_vote(candidate_id):
    cipher = AES.new(KEY, AES.MODE_CBC)
    ciphertext = cipher.encrypt(
        pad(candidate_id.encode(), AES.block_size)
    )

    # Combine IV + ciphertext
    encrypted_data = base64.b64encode(cipher.iv + ciphertext).decode()
    return encrypted_data


def decrypt_vote(encrypted_vote):
    raw_data = base64.b64decode(encrypted_vote)

    iv = raw_data[:16]        # First 16 bytes = IV
    ciphertext = raw_data[16:]  # Remaining = actual encrypted vote

    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted_data = unpad(
        cipher.decrypt(ciphertext),
        AES.block_size
    )

    return decrypted_data.decode()
