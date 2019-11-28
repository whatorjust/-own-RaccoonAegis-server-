from konlpy.tag import Okt

okt = Okt()

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

maxlen = 20
max_words = 10000

tokenizer = Tokenizer(num_words=max_words)

import json

with open("wordIndex.json") as json_file:
    word_index = json.load(json_file)
    tokenizer.word_index = word_index

from keras.models import load_model

model = load_model("model.h5")

examples = [
    "여기에 원하는 문장을 입력하세요.",
    "그러면 각각의 문장이 악플일 확률을 출력합니다.",
    "힘내세요! 응원합니다",
]

ex_morpheme = []

for text in examples:
    union = ""
    for word_tag in okt.pos(text, norm=True, stem=True):
        if word_tag[1] in [
            "Noun",
            "Verb",
            "VerbPrefix",
            "Adjective",
            "Determiner",
            "Adverb",
            "Exclamation",
            "KoreanParticle",
        ]:
            union += word_tag[0]
            union += " "
    ex_morpheme.append(union)

sequences = tokenizer.texts_to_sequences(ex_morpheme)
x_test = pad_sequences(sequences, maxlen=maxlen)

value_predicted = model.predict(x_test)
for i in range(0, len(x_test)):
    print(examples[i], ":", round(value_predicted[i][0] * 100, 1), "%의 확률로 악플입니다.")
