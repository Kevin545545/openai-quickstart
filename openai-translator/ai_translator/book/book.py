from .page import Page

class Book:
    def __init__(self, pdf_file_path):
        self.pdf_file_path = pdf_file_path # 保存 PDF 文件路径
        self.pages = [] # 初始化了一个空列表 self.pages 来保存书籍的页面对象。

    def add_page(self, page: Page):
        self.pages.append(page) # page表示要添加的页面对象，将该页面对象添加到 self.pages 列表中。