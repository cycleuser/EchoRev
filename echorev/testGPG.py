from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

def MagicCrype(self):
    plaintext = self.textbox_decrypt.toPlainText()

    if not plaintext:
        print("No text to encrypt.")
        return

    # 加载公钥
    try:
        with open(self.public_key_path, 'rb') as pub_file:
            public_key = serialization.load_pem_public_key(pub_file.read(), backend=default_backend())
    except FileNotFoundError:
        print(f"Public key file not found: {self.public_key_path}")
        return

    # 分块加密
    max_length = 190  # 对于2048位RSA密钥和OAEP填充，最大输入长度约为190字节
    encrypted_chunks = []
    for i in range(0, len(plaintext), max_length):
        chunk = plaintext[i:i + max_length].encode('utf-8')
        encrypted_chunk = public_key.encrypt(
            chunk,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        encrypted_chunks.append(encrypted_chunk)

    # 将所有加密的小块组合在一起
    encrypted_message = b''.join(encrypted_chunks)

    # 将加密后的文本显示在textbox_crype
    self.textbox_crype.setPlainText(encrypted_message.hex())

    print("Text encrypted successfully.")