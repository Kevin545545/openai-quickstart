# 导入了 Python 的 sys 和 os 模块，用于处理系统路径等操作。

import sys
import os

# 这行代码将当前文件所在的目录添加到 Python 模块搜索路径中。
# 这样做的目的是确保 Python 解释器可以找到当前目录下的其他模块。

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG # 这些类分别用于解析命令行参数、加载配置文件和记录日志。
from model import GLMModel, OpenAIModel
from translator import PDFTranslator # 这个类可能是用来实现 PDF 文件的翻译功能。

if __name__ == "__main__":
    argument_parser = ArgumentParser() # 创建了一个 ArgumentParser 对象，用于解析命令行参数。
    args = argument_parser.parse_arguments() # 解析命令行参数，并将结果存储在 args 变量中。
    config_loader = ConfigLoader(args.config) # 创建了一个 ConfigLoader 对象，用于加载配置文件。

    config = config_loader.load_config() # 加载配置文件，并将配置信息存储在 config 变量中。

    model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
    api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
    model = OpenAIModel(model=model_name, api_key=api_key) # 根据确定的翻译模型名称和 API 密钥，创建了一个 OpenAIModel 对象。

    pdf_file_path = args.book if args.book else config['common']['book'] # 根据命令行参数或配置文件中的设置，确定要翻译的 PDF 文件路径。
    file_format = args.file_format if args.file_format else config['common']['file_format'] # 确定翻译后的文件格式
    target_language = args.language

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file_path, file_format, target_language)
