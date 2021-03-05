from utils import download_file
import os

models = {
    "morph-models-1.5.0/de/de-lemma-perceptron-conll09.bin": "https://drive.google.com/uc?export=download&id=1JlXYiHsCnzvvdLAeJlbh6WujbNgzlkkh",
    "morph-models-1.5.0/de/de-pos-perceptron-autodict01-conll09.bin": "https://drive.google.com/uc?export=download&id=1PaEkC2faiiXlL3mGxFbr46MymRB3SgbA",
    "morph-models-1.5.0/en/en-lemma-perceptron-conll09.bin": "https://drive.google.com/uc?export=download&id=1CSSfpn7Uf_lyJpNiIfhEkKIAAMhXENOt",
    "morph-models-1.5.0/en/en-pos-perceptron-autodict01-conll09.bin": "https://drive.google.com/uc?export=download&id=1AwxhRBKsYf8ziBtUG9QpMoghIrDtzs6d",
    "morph-models-1.5.0/es/es-lemma-perceptron-ancora-2.0.bin": "https://drive.google.com/uc?export=download&id=1cHfxNB8mJu91d6QKgMw-yj-rtvAXIxgH",
    "morph-models-1.5.0/es/es-pos-perceptron-autodict01-ancora-2.0.bin": "https://drive.google.com/uc?export=download&id=19Y8pQ7OeN5LaWOjyCmyPselsfId234gD",
    "morph-models-1.5.0/eu/eu-lemma-perceptron-epec.bin": "https://drive.google.com/uc?export=download&id=1wsZXNjq9ICiy2yEstzanppV8j1mGJoOe",
    "morph-models-1.5.0/eu/eu-pos-perceptron-epec.bin": "https://drive.google.com/uc?export=download&id=1vHBt6fFRrNbn2gsFm8aAVYB_kq7m5RgI",
    "morph-models-1.5.0/fr/fr-lemma-perceptron-sequoia.bin": "https://drive.google.com/uc?export=download&id=13qoEpeAnsDs0FUj6KbO6CJaxsAfO9kvw",
    "morph-models-1.5.0/fr/fr-pos-perceptron-autodict01-sequoia.bin": "https://drive.google.com/uc?export=download&id=1nEP_HI3jbwuo6JDIFXzHFrEq3q5I4ozk",
    "morph-models-1.5.0/gl/gl-lemma-perceptron-autodict05-ctag.bin": "https://drive.google.com/uc?export=download&id=1tTQdqD5N6nt9HrtHquts2V7k_ocq9bMg",
    "morph-models-1.5.0/gl/gl-pos-perceptron-autdict05-ctag.bin": "https://drive.google.com/uc?export=download&id=1TLri0YqSIydTF6w09qN5xZshUhmHqXrU",
    "morph-models-1.5.0/nl/nl-lemma-perceptron-alpino.bin": "https://drive.google.com/uc?export=download&id=1Oatj_OJrTbk-gQUM0hc8oTJ2EXH5nOZK",
    "morph-models-1.5.0/nl/nl-pos-perceptron-autodict01-alpino.bin": "https://drive.google.com/uc?export=download&id=1jaMQPD8NML9zAw_iCUjmnqMmYFs-P9Et",
}


def get_model(model_name_or_path: str) -> str:
    if model_name_or_path in models:
        cache_path = os.path.join(
            os.path.expanduser("~/.cache/python-ixa-pipes/"), model_name_or_path
        )

        if os.path.exists(cache_path):
            return cache_path
        else:
            print(f"Downloading model to: {cache_path}")
            download_file(url=models[model_name_or_path], output_path=cache_path)

        return cache_path

    else:
        print(
            f"{model_name_or_path} not found in model list, assuming that it is a path to a model"
        )

        return model_name_or_path
