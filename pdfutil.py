import io
import pycurl
import tempfile

import certifi
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdftypes import PDFException

from .log import Log


# PDFから情報を取ってくるユーティリティ
class PDFUtil:
    @classmethod
    def parse_text_from_buffer(cls, buffer: io.BytesIO, password='') -> str:
        ret = ""
        try:
            parser = PDFParser(buffer)
            document = PDFDocument()
            parser.set_document(document)  # set document to parser

            # Create a PDF document object that stores the document structure.
            # Supply the password for initialization.
            document.set_parser(parser)  # set parser to document
            document.initialize(password)

            # Check if the document allows text extraction. If not, abort.
            if not document.is_extractable:
                Log.e('pdf file is not extractable')
                return ''

            manager = PDFResourceManager()
            page_a = PDFPageAggregator(manager, laparams=LAParams())
            interpreter = PDFPageInterpreter(manager, page_a)

            # Process each page contained in the document.
            for page in document.get_pages():
                interpreter.process_page(page)
                layout = page_a.get_result()
                for obj in layout:
                    if isinstance(obj, LTTextBox):
                        ret += obj.get_text()
                        print(obj.get_text())

        except PDFException:
            pass

        return PDFUtil.wrap_content_tag(ret)

    @classmethod
    def parse_text_from_bytes(cls, _bytes: bytes, password='') -> str:
        buffer = io.BytesIO(_bytes)
        return cls.parse_text_from_buffer(buffer, password)

    @classmethod
    def parse_text_from_file(cls, destination: str, password='') -> str:
        if destination.startswith('http'):
            curl = pycurl.Curl()
            fp = tempfile.TemporaryFile()
            curl.setopt(pycurl.URL, destination)
            curl.setopt(pycurl.CAINFO, certifi.where())
            curl.setopt(pycurl.WRITEFUNCTION, fp.write)
            curl.perform()
            fp.seek(0)
        else:
            fp = open(destination, 'rb')

        return PDFUtil.parse_text_from_buffer(fp, password)

    @classmethod
    def wrap_content_tag(cls, instr: str) -> str:
        return "<html><head></head><body><main>%s</main></body></html>" % instr
