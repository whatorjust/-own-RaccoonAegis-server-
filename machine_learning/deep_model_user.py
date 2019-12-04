from konlpy.tag import Okt
import os.path
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import json
from keras.models import load_model

# import tensorflow as tf
from keras import backend

def deep_learn(arr):

    backend.clear_session()

    okt = Okt()

    maxlen = 50
    max_words = 10000

    tokenizer = Tokenizer(num_words=max_words)

    with open(os.path.abspath("machine_learning/wordIndex.json")) as json_file:
        word_index = json.load(json_file)
        tokenizer.word_index = word_index

    model = load_model(os.path.abspath("machine_learning/a_model.h5"))

    examples = arr

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
    # for i in range(0, len(x_test)):
    #     print(examples[i], ":", round(value_predicted[i][0] * 100, 1), "%의 확률로 악플입니다.")
    return_value = []

    for i in range(0, len(x_test)):
        return_value.append(str(round(value_predicted[i][0], 3)))

    return return_value