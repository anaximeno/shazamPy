# It is here to avoid circular imports
import hashlib

# List with all hashlist usable
hashes = {
    "md5": hashlib.md5(),
    "sha1": hashlib.sha1(),
    "sha224": hashlib.sha224(),
    "sha256": hashlib.sha256(),
    "sha384": hashlib.sha384(),
    "sha512": hashlib.sha512()
}

hashes_n2 = {
    "md5": hashlib.md5(),
    "sha1": hashlib.sha1(),
    "sha224": hashlib.sha224(),
    "sha256": hashlib.sha256(),
    "sha384": hashlib.sha384(),
    "sha512": hashlib.sha512()
}
