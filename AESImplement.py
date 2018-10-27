import os, random, struct
from Crypto.Cipher import AES
from Crypto import Random
import sys

class AESImplement:

    def generateKey(self):
        key = ''.join(chr(random.randint(0, 100)) for i in range(16))
        fd = open("AES_key.pem", "wb")
        fd.write(bytes(str(key), 'utf-8'))
        fd.close()
        return bytes(str(key), 'utf-8')

    #################################################################################################################
    def encrypt_file(self,key, in_filename, out_filename=None, chunksize=64*1024):
        if not out_filename:
            out_filename = in_filename + '.enc'

        iv = Random.get_random_bytes(16)
        print(type(key))
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))

    #####################################################################################################

    def decrypt_file(self,key, in_filename, out_filename=None, chunksize=24*1024):

        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)


# aes = AESImplement()
# aes.generateKey()
# fd = open('AES_key.pem','rb')
# key1 = fd.read()
# aes.encrypt_file(key1, 'received_file', 'enc_file')
# print("File encryption done")
# aes.decrypt_file(key1, 'enc_file', 'dec_file',)
# print("File decrypted")
