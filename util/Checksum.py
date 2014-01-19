import hashlib


class Checksum:
    def __init__(self):
        pass

    @staticmethod
    def get_md5(local_path):
        md5 = hashlib.md5()
        with open(local_path, 'rb') as f:
            for chunk in iter(lambda: f.read(128*md5.block_size), b''):
                md5.update(chunk)
        return md5.hexdigest()
