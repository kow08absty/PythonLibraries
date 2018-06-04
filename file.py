
class FileUtil:
    @classmethod
    def is_available_name(cls, name: str) -> bool:
        for letter in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\x00']:
            if name.find(letter) != -1:
                return False
        return True
