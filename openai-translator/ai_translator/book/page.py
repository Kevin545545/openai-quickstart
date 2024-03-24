from .content import Content

class Page:
    def __init__(self):
        self.contents = [] # 用于存储页面中的内容。

    def add_content(self, content: Content): # 添加内容到页面。接受一个参数 content，表示要添加的内容对象，并将其添加到 self.contents 列表中。
        self.contents.append(content)
