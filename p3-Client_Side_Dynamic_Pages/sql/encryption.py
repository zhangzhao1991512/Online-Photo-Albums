import hashlib
import uuid
algorithm = 'sha512' # name of the algorithm to use for

password = 'bob1pass' # unencrypted password
salt = uuid.uuid4().hex # salt as a hex string for storage in db
m = hashlib.new(algorithm)
m.update(salt + password)
password_hash = m.hexdigest()

print "$".join([algorithm,salt,password_hash])
