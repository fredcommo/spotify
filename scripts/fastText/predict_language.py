import fasttext
import os

# Load fasttext pretrained bin from: https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
# Change path_to_pretrained_model according to your bin location
path_to_pretrained_model = f"{os.path.dirname(__file__)}/lid.176.bin"
fmodel = fasttext.load_model(path_to_pretrained_model)

def predict_language(text):
    predictions = fmodel.predict(text)
    label = [pred[0].split("_")[-1] for pred in predictions[0]]
    prob = [pred[0] for pred in predictions[1]]
    return label, prob


if __name__ == "__main__":

    text = {
        "en": "Hello everybody",
        "fr": "Bonjour à tous",
        "de": "Hallo zusammen",
        "es": "Hola a todos",
        "it": "Ciao a tutti",
        "ja": "皆さん、こんにちは。",
        "ru": "Привет всем",
        "pt": "Olá a todos"
    }

    label, prob = predict_language(list(text.values()))

    for t, l0, l1, p in zip(text.values(), text.keys(), label, prob):
        print(f"{t} ({l0});\tpredicted: {l1};\tprob: {'%.3f' % p}")
    