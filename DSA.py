from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

class DSA:
    user=""
    def checkUser(self,username):
        self.user=username
    priv_fd=open('private_key.pem','rb')
    private_key=priv_fd.read()  
    
    pub_fd=open('public_key.pem','rb')
    public_key=pub_fd.read()
    #print(private_key)
    #print(public_key)
    def sign(self):
        priv_key=RSA.importKey(private_key)
        pub_key = RSA.importKey(public_key)
        #user = "Abhicruiser"
        h=SHA256.new(user.encode('utf-8'))
        #print(h)
        signer = PKCS1_v1_5.new(priv_key)
        signature = signer.sign(h)
        #print(signature)
    def verify(self):
        user_x="Abhicruiser"
        h_x = SHA256.new(user_x.encode('utf-8'))
        verifier = PKCS1_v1_5.new(pub_key)
        return(verifier.verify(h_x,signature))

#x = DSA()
#x.checkUser("Abhicruiser")
#x.sign()
#x.verify()

        