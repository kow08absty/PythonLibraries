from lib.external import Log


class Converter:
    @classmethod
    def to_unicode(cls, data: bytes, charset_order: list = ()):

        def f(d: bytes, enc: str) -> str:
            return d.decode(enc)

        if len(charset_order) == 0:
            charset_order = ['shift_jis', 'utf-8', 'euc_jp', 'cp932',
                             'euc_jis_2004', 'euc_jisx0213', 'iso2022_jp', 'iso2022_jp_1',
                             'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext',
                             'shift_jis_2004', 'shift_jisx0213', 'utf_16', 'utf_16_be',
                             'utf_16_le', 'utf_7', 'utf_8_sig']

        for codec in charset_order:
            try:
                return f(data, codec)
            except UnicodeError:
                continue
        Log.e('charset detection failed (in list: [' + str.join(',', charset_order) + '] )')
        return None
