from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import zlib
import base64, sys

class RSAImplement:
    #############################################################
    def generateKeyPair(self, username):
        new_key = RSA.generate(4096, e=65537)

        #The private key in PEM format
        private_key = new_key.exportKey("PEM")
        print(sys.getsizeof(private_key))
        print(len(private_key))
        #The public key in PEM Format
        public_key = new_key.publickey().exportKey("PEM")

        #print private_key
        fd = open(username + "_private_key.pem", "wb")
        fd.write(private_key)
        fd.close()

        #print public_key
        fd = open(username + "_public_key.pem", "wb")
        fd.write(public_key)
        fd.close()


###########################################################################333
    #Our Encryption Function
    def encrypt_blob(self, blob, public_key):
        #Import the Public Key and use for encryption using PKCS1_OAEP
        rsa_key = RSA.importKey(public_key)
        rsa_key = PKCS1_OAEP.new(rsa_key)

        #compress the data first
        blob = zlib.compress(blob)

        #In determining the chunk size, determine the private key length used in bytes
        #and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
        #in chunks
        chunk_size = 3200
        offset = 0
        end_loop = False
        encrypted =  ""

        while not end_loop:
            #The chunk
            chunk = blob[offset:offset + chunk_size]

            #If the data chunk is less then the chunk size, then we need to add
            #   padding with " ". This indicates the we reached the end of the file
            #so we end loop here
            if len(chunk) % chunk_size != 0:
                end_loop = True
                chunk += b' '* (chunk_size - len(chunk))

            #Append the encrypted chunk to the overall encrypted file
            encrypted += rsa_key.encrypt(chunk)

            #Increase the offset by chunk size
            offset += chunk_size

        #Base 64 encode the encrypted file
        return base64.b64encode(encrypted)


    def encryptFile(self, filename):

        #Use the public key for encryption
        fd = open("public_key.pem", "rb")
        public_key = fd.read()
        fd.close()

        #Our candidate file to be encrypted
        fd = open(filename, "rb")
        unencrypted_blob = fd.read()
        fd.close()

        encrypted_blob = self.encrypt_blob(unencrypted_blob, public_key)

        #Write the encrypted contents to a file
        fd = open("encrypted_"+filename, "wb")
        fd.write(encrypted_blob)
        fd.close()

#############################################################################

    #Our Decryption Function
    def decrypt_blob(self, encrypted_blob, private_key):

        #Import the Private Key and use for decryption using PKCS1_OAEP
        rsakey = RSA.importKey(private_key)
        rsakey = PKCS1_OAEP.new(rsakey)

        #Base 64 decode the data
        encrypted_blob = base64.b64decode(encrypted_blob)

        #In determining the chunk size, determine the private key length used in bytes.
        #The data will be in decrypted in chunks
        chunk_size = 512
        offset = 0
        decrypted = ""

        #keep loop going as long as we have chunks to decrypt
        while offset < len(encrypted_blob):
            #The chunk
            chunk = self.encrypted_blob[offset: offset + chunk_size]

            #Append the decrypted chunk to the overall decrypted file
            decrypted += rsakey.decrypt(chunk)

            #Increase the offset by chunk size
            offset += chunk_size

        #return the decompressed decrypted data
        return zlib.decompress(decrypted)

    def decryptFile(filename):
        #Use the private key for decryption
        fd = open("private_key.pem", "rb")
        private_key = fd.read()
        fd.close()

        #Our candidate file to be decrypted
        fd = open(filename, "rb")
        encrypted_blob = fd.read()
        fd.close()

        #Write the decrypted contents to a file
        fd = open("decrypted_"+filename, "wb")
        fd.write(self.decrypt_blob(encrypted_blob, private_key))
        fd.close()

###########################################################################

# rsa = RSAImplement()
# rsa.generateKeyPair()
# rsa.encryptFile()