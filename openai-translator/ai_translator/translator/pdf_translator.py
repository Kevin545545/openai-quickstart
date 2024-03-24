from typing import Optional
from model import Model
from translator.pdf_parser import PDFParser
from translator.writer import Writer
from utils import LOG
from book import ContentType

class PDFTranslator:
    def __init__(self, model: Model):
        self.model = model
        self.pdf_parser = PDFParser()
        self.writer = Writer()

    def translate_pdf(self, pdf_file_path: str, file_format: str , target_language :str, output_file_path: str = None, pages: Optional[int] = None):
        self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages = 2) # : 使用 PDFParser 对象解析给定的 PDF 文件，将结果保存在实例变量 book 中。

        for page_idx, page in enumerate(self.book.pages): # 迭代解析后的每一页。
            for content_idx, content in enumerate(page.contents):
                if content.content_type == ContentType.IMAGE:  # 如果内容是图像，则跳过翻译步骤
                    continue

                prompt = self.model.translate_prompt(content, target_language) #  使用模型对象创建一个翻译提示，该提示由原始内容和目标语言组成。
                LOG.debug(prompt)
                translation, status = self.model.make_request(prompt) # 使用模型对象向 API 发送请求，并获取翻译结果和状态。
                LOG.info(translation)
                
                # Update the content in self.book.pages directly
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status) # 将翻译结果和状态设置到相应的内容块中。

        self.writer.save_translated_book(self.book, output_file_path, file_format) # 将翻译后的书籍保存到文件中，可以指定输出文件的格式和路径。
