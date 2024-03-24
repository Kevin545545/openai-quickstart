from book import ContentType

class Model:
    def make_text_prompt(self, text: str, target_language: str) -> str:
        return f"你现在是一个语言翻译领域的专家，请将以下内容翻译为{target_language},并且保持原格式返回（务必保留原始文本的空行，间距等格式）：{text}"

    def make_table_prompt(self, table: str, target_language: str) -> str:
        return f"你现在是一个语言翻译领域的专家，请你对表格做以下处理：1.将表格内所有内容翻译为{target_language}（务必检查是所有内容均翻译完成）2. 保持间距（空格，分隔符），其中表格每列分隔符为|，以表格形式返回：\n{table}"

    def translate_prompt(self, content, target_language: str) -> str:
        if content.content_type == ContentType.TEXT:
            return self.make_text_prompt(content.original, target_language)
        elif content.content_type == ContentType.TABLE:
            return self.make_table_prompt(content.get_original_as_str(), target_language)
        elif content.content_type == ContentType.IMAGE:
            pass

    def make_request(self, prompt):
        raise NotImplementedError("子类必须实现 make_request 方法")
