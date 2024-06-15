from transformers import pipeline
import fasttext

# remove annoying warning
fasttext.FastText.eprint = lambda x: None
# enforce consistent results for lang detection
pretrained_lang_model = "models/lid218e.bin" # Path of model file


def detect_language(text: str):
    model = fasttext.load_model(pretrained_lang_model)

    return model.predict(text, k=1)[0][0].replace('__label__', '')


def translate(text: str):
    textLang = detect_language(text)
    print(textLang)
    translator = pipeline(task='translation', model='facebook/nllb-200-distilled-600M')
    result = translator(text, src_lang=textLang, tgt_lang="eng_Latn")
    return [textLang, result[0]['translation_text']]



