import requests
import simplejson

from model import Model

class GLMModel(Model):
    def __init__(self, model_url: str, timeout: int):
        self.model_url = model_url
        self.timeout = timeout

    def make_request(self, prompt):
        try:
            payload = {
                "prompt": prompt,
                "history": []
            }
            response = requests.post(self.model_url, json=payload, timeout=self.timeout)
            response.raise_for_status() # 检查响应的状态码，如果不是 200，则抛出一个异常。
            response_dict = response.json() # 从响应中解析出 JSON 格式的数据
            translation = response_dict["response"] # 从响应数据中提取出翻译结果。
            return translation, True # 返回翻译结果以及一个标志表示请求是否成功。
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求异常：{e}")
        except requests.exceptions.Timeout as e:
            raise Exception(f"请求超时：{e}")
        except simplejson.errors.JSONDecodeError as e:
            raise Exception("Error: response is not valid JSON format.")
        except Exception as e:
            raise Exception(f"发生了未知错误：{e}")
        return "", False # 如果发生异常，则返回空字符串和一个标志表示请求失败。
