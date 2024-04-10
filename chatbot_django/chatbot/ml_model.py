import os
import replicate
from translate import Translator


txt = open("D:\ALLPyProjacts\project\chatbot_django\chatbot\TOKEN.txt", 'r').readline()
os.environ["REPLICATE_API_TOKEN"] = txt

assert len(txt) != 0, "Invalid token"

ML_MODEL = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])
translator = Translator(to_lang="ru")


def answer_print(iterator):
    answer = ""
    for i in iterator:
        answer += i
    translated = ""
    count = len(answer) // 500 + 1
    for i in range(count):
        if i == count - 1:
            translated += translator.translate(answer[500 * i:])
        else:
            translated += translator.translate(answer[500 * i: 500 * (i + 1)])
    return translated # translator.translate()s