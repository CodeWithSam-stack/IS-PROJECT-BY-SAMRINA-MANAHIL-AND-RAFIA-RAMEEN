import os
import hashlib

# ── Key Pad: pre-shared between Alpha and Bravo units ──
class OTPKeyPad:
    def __init__(self, mission_id, num_messages, msg_size=128):
        self.keys = [os.urandom(msg_size) for _ in range(num_messages)]
        self.index = 0  # pointer to next unused key

    def get_key(self):
        key = self.keys[self.index]
        self.keys[self.index] = bytes(len(key))  # destroy after use
        self.index += 1
        return key

# ── OTP Encrypt / Decrypt (XOR) ──
def otp_encrypt(plaintext: bytes, key: bytes) -> bytes:
    return bytes(p ^ k for p, k in zip(plaintext, key))

def otp_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    return bytes(c ^ k for c, k in zip(ciphertext, key))

# ── TACS Battlefield Message ──
class BattlefieldMessage:
    def __init__(self, sender, receiver, text, key_pad):
        self.sender = sender
        self.receiver = receiver
        raw = text.encode().ljust(128, b'\x00')
        key = key_pad.get_key()
        self.cipher = otp_encrypt(raw, key)
        self._key = key  # held for demo

    def decrypt(self):
        raw = otp_decrypt(self.cipher, self._key)
        return raw.rstrip(b'\x00').decode()

# ── Simulation ──
pad_alpha = OTPKeyPad('MISSION-DELTA', 50)
msg = BattlefieldMessage(
    'Alpha-6', 'Bravo-4',
    'GRID 3847-N ENEMY SPOTTED. REQUEST FIRE SUPPORT.',
    pad_alpha)
print('Sender:   ', msg.sender)
print('Receiver: ', msg.receiver)
print('Cipher:   ', msg.cipher.hex()[:32] + '...')
print('Decrypted:', msg.decrypt())