import os
import io
from abc import abstractmethod, ABC
from typing import Union, Tuple

from .log import Log


class _MimeGroupReflection(ABC):
    @abstractmethod
    def get_mime_str(self):
        raise NotImplementedError()


class _MimeEntryReflection(ABC):
    def __eq__(self, other):
        _clazz = other
        if isinstance(_clazz, self.__class__):
            _clazz = other.__class__
        return _clazz is self.__class__

    def __ne__(self, other):
        return not self.__eq__(other)

    @abstractmethod
    def get_mime_str(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_ext(self) -> Union[str, Tuple[str, ...]]:
        raise NotImplementedError()

    @abstractmethod
    def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
        raise NotImplementedError()

    @abstractmethod
    def is_str_decodable(self) -> bool:
        raise NotImplementedError()

    def __str__(self):
        return self.get_mime_str()

    def is_in(self, other: type) -> bool:
        _instance = other()
        return self.get_mime_str().startswith(_instance.get_mime_str())


class MimeTypes:
    _LIMIT_MAX_FILESIZE = 20971520  # 20MB

    class Application(_MimeGroupReflection):
        def get_mime_str(self) -> str:
            return "application"

        class OctetStream(_MimeEntryReflection):
            def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
                return ()

            def is_str_decodable(self) -> bool:
                return False

            def get_ext(self) -> Union[str, Tuple[str, ...]]:
                return ()

            def get_mime_str(self) -> str:
                return "application/octet-stream"

        class PDF(_MimeEntryReflection):
            def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
                return b'%PDF'

            def is_str_decodable(self) -> bool:
                return False

            def get_ext(self) -> Union[str, Tuple[str, ...]]:
                return ".pdf"

            def get_mime_str(self) -> str:
                return "application/pdf"

        class JSON(_MimeEntryReflection):
            def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
                return b'{', b'['

            def is_str_decodable(self) -> bool:
                return True

            def get_mime_str(self) -> str:
                return "application/json"

            def get_ext(self) -> Union[str, Tuple[str, ...]]:
                return '.json'

    class Text(_MimeGroupReflection):
        def get_mime_str(self) -> str:
            return "text"

        class HTML(_MimeEntryReflection):
            def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
                return b'<!DOCTYPE', b'<html', b'<HTML'

            def is_str_decodable(self) -> bool:
                return True

            def get_ext(self) -> Union[str, Tuple[str, ...]]:
                return ".htm", ".html", '.xhtm', '.xhtml'

            def get_mime_str(self) -> str:
                return "text/html"

        class Plain(_MimeEntryReflection):
            def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
                return ()

            def is_str_decodable(self) -> bool:
                return True

            def get_ext(self) -> Union[str, Tuple[str, ...]]:
                return ".txt"

            def get_mime_str(self) -> str:
                return "text/plain"

        class XML(_MimeEntryReflection):
            def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
                return b'<?xml'

            def is_str_decodable(self) -> bool:
                return True

            def get_ext(self) -> Union[str, Tuple[str, ...]]:
                return ".xml"

            def get_mime_str(self) -> str:
                return "text/xml"

    class Image(_MimeGroupReflection):
        def get_mime_str(self) -> str:
            return "image"

        class JPEG(_MimeEntryReflection):
            def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
                return b'\xFF\xD8'

            def is_str_decodable(self) -> bool:
                return False

            def get_ext(self) -> Union[str, Tuple[str, ...]]:
                return ".jpg", ".jpeg", '.jpe'

            def get_mime_str(self) -> str:
                return "image/jpeg"

        class PNG(_MimeEntryReflection):
            def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
                return b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'

            def is_str_decodable(self) -> bool:
                return False

            def get_ext(self) -> Union[str, Tuple[str]]:
                return ".png"

            def get_mime_str(self) -> str:
                return "image/png"

        class GIF(_MimeEntryReflection):
            def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
                return b'GIF87a', b'GIF89a'

            def is_str_decodable(self) -> bool:
                return False

            def get_ext(self) -> Union[str, Tuple[str, ...]]:
                return ".gif"

            def get_mime_str(self) -> str:
                return "image/gif"

        class TIFF(_MimeEntryReflection):
            def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
                return b'\x49\x49', b'\x4D\x4D'

            def is_str_decodable(self) -> bool:
                return False

            def get_ext(self) -> Union[str, Tuple[str, ...]]:
                return ".tif", ".tiff"

            def get_mime_str(self) -> str:
                return "image/tiff"

        class BMP(_MimeEntryReflection):
            def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
                return b'BM'

            def is_str_decodable(self) -> bool:
                return False

            def get_ext(self) -> Union[str, Tuple[str, ...]]:
                return ".bmp"

            def get_mime_str(self) -> str:
                return "image/bmp"

        class SVG(_MimeEntryReflection):
            def is_str_decodable(self) -> bool:
                return True

            def get_mime_str(self) -> str:
                return "image/svg+xml"

            def get_ext(self) -> Union[str, Tuple[str, ...]]:
                return '.svg', '.svgz'

            def get_header_bytes(self) -> Union[bytes, Tuple[bytes, ...]]:
                return b'<svg'

    @classmethod
    def set_max_filesize(cls, byte: int):
        MimeTypes._LIMIT_MAX_FILESIZE = byte

    @classmethod
    def guess_by_file_name(cls, file_name: str) -> _MimeEntryReflection:
        base, ext = os.path.splitext(file_name)
        for _clazz in _MimeEntryReflection.__subclasses__():
            _instance = _clazz()
            if ext in _instance.get_ext():
                return _instance
        return MimeTypes.Application.OctetStream()

    @classmethod
    def from_str(cls, mime_type_str: str) -> _MimeEntryReflection:
        for _clazz in _MimeEntryReflection.__subclasses__():
            _instance = _clazz()
            if mime_type_str == _instance.get_mime_str():
                return _instance
        return MimeTypes.Application.OctetStream()

    @classmethod
    def guess_by_file(cls, file_path: str):
        if os.path.isfile(file_path):
            try:
                fsize = os.path.getsize(file_path)
                if fsize > MimeTypes._LIMIT_MAX_FILESIZE:
                    Log.w(
                        '%s: %d bytes > limit %d bytes; not reading' %
                        (file_path, fsize, MimeTypes._LIMIT_MAX_FILESIZE)
                    )
                else:
                    with open(file_path, "rb") as f:
                        if f.readable():
                            return MimeTypes.guess_by_bytes(f.read())
            except OSError:
                Log.e(file_path + " - open error")
        else:
            Log.w(file_path + " - No such file")
        return MimeTypes.guess_by_file_name(os.path.basename(file_path))

    @classmethod
    def guess_by_buffer(cls, content: io.BufferedIOBase) -> _MimeEntryReflection:
        return MimeTypes.guess_by_bytes(content.read())

    @classmethod
    def guess_by_bytes(cls, content: bytes) -> _MimeEntryReflection:
        decode_ok = False
        try:
            content.decode('UTF-8')
            decode_ok = True
        except UnicodeDecodeError:
            pass
        for _clazz in _MimeEntryReflection.__subclasses__():
            _instance = _clazz()
            if content.startswith(_instance.get_header_bytes()):
                if _instance.is_str_decodable() and not decode_ok:
                    continue
                return _instance
        if decode_ok:
            return MimeTypes.Text.Plain()
        else:
            return MimeTypes.Application.OctetStream()
