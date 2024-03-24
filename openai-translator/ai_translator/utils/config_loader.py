import yaml

class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path

 # 定义了一个实例方法 load_config()，用于加载配置文件并返回配置信息。
 #       在这个方法中，使用 open 函数打开配置文件，然后使用 yaml.safe_load 函数将文件内容解析为一个 Python 字典，
 #       并将其存储在变量 config 中。最后，返回这个解析后的配置信息。
    def load_config(self):
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)
        return config