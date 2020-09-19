from itsdangerous import TimestampSigner

from .env import SECRET


csrf_signer = TimestampSigner(SECRET)
