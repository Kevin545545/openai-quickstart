import pdfplumber
from typing import Optional
from book import Book, Page, Content, ContentType, TableContent ,ImageContent
from translator.exceptions import PageOutOfRangeException
from utils import LOG


class PDFParser:
    def __init__(self):
        pass

    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None) -> Book: # 定义了 parse_pdf 方法，接受一个参数 pdf_file_path 表示 PDF 文件的路径，
        book = Book(pdf_file_path) # 还有一个可选参数 pages 表示要解析的页数，默认为 None。在方法内部创建了一个 Book 对象，用于存储解析后的书籍内容。

        with pdfplumber.open(pdf_file_path) as pdf:
            if pages is not None and pages > len(pdf.pages): # 检查 pages 参数是否超出 PDF 文件的总页数，如果超出则抛出 PageOutOfRangeException 异常。
                raise PageOutOfRangeException(len(pdf.pages), pages)

            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]

            for pdf_page in pages_to_parse: # 遍历要解析的页数范围，并为每一页创建一个 Page 对象。
                page = Page()

                # Store the original text content
                raw_text = pdf_page.extract_text(layout=True)
                tables = pdf_page.extract_tables()
                images = pdf_page.images

                # Remove each cell's content from the original text 遍历表格数据，从原始文本内容中删除每个单元格的内容，以避免重复解析。
                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            raw_text = raw_text.replace(cell, "", 1)

                # Handling text
                if raw_text: # 处理原始文本内容，去除空行和首尾空白字符，并创建 Content 对象表示文本内容，然后将其添加到页面中。
                    # Remove empty lines and leading/trailing whitespaces
                    '''
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)
                    '''
                    text_content = Content(content_type=ContentType.TEXT, original=raw_text)
                    page.add_content(text_content)
                    LOG.debug(f"[raw_text]\n {raw_text}")



                # Handling tables 处理表格数据，创建 TableContent 对象表示表格内容，并将其添加到页面中。
                if tables: 
                    table = TableContent(tables)
                    page.add_content(table)
                    LOG.debug(f"[table]\n{table}")
                    
                if images:
                    image_content = ImageContent(image_list=[])
                    for img in images:
                        bbox = (img["x0"], img["top"], img["x1"], img["bottom"])
                        cropped_page = pdf_page.crop(bbox)
                        im = cropped_page.to_image(antialias=True)
                        image_content.original.append(im)
                    page.add_content(image_content)
                    LOG.debug(f"[image]\n{image_content}")

                book.add_page(page) # 将每一页添加到书籍对象中

        return book
