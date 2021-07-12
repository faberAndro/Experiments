#!/usr/bin/python
# website with 10M password: https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt

import hashlib
import crypt #applies a 'salt' to hashes from encryption


def getting_pwd_from_hash(hashvalue_to_decode):
    enc_word = hashvalue_to_decode.encode('utf-8')
    clean_hash = hashlib.md5(enc_word.strip()).hexdigest()


hashvalue = input("Enter a string to hash: ")


hashobj1 = hashlib.md5()
hashobj1.update(hashvalue.encode())
print(hashobj1.hexdigest())

hashobj2 = hashlib.sha1()
hashobj2.update(hashvalue.encode())
print(hashobj2.hexdigest())

hashobj3 = hashlib.sha224()
hashobj3.update(hashvalue.encode())
print(hashobj3.hexdigest())

hashobj4 = hashlib.sha256()
hashobj4.update(hashvalue.encode())
print(hashobj4.hexdigest())

hashobj5 = hashlib.sha512()
hashobj5.update(hashvalue.encode())
print(hashobj5.hexdigest())

salt = 'DL'
cryptWord = crypt.crypt(hashvalue, salt)
print(cryptWord)
getsalt = cryptWord[:2]