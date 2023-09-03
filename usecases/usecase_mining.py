import os
import re
import spacy
from textblob import TextBlob
from gensim.summarization.summarizer import summarize
from gensim.models.ldamodel import LdaModel
from utils import transforms, files
from collections import Counter
from gensim import corpora

nlp = spacy.load('es_core_news_sm')


def process_text(text, stopwords):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)

    words = text.split()

    stopwords.update(transforms.create_set(files.read_file(os.getenv("STOPWORDS_FILE"))))

    words = [word for word in words if word not in stopwords]

    return words


def get_word_frequency(words):
    word_count = Counter(words)
    return word_count


def get_summarize(texto):
    return summarize(texto)


def get_principal_topics(texto):
    documents = [documento.split() for documento in texto.split('\n')]

    # Crear un diccionario y una matriz de términos-documento
    diccionario = corpora.Dictionary(documents)
    corpus = [diccionario.doc2bow(documento) for documento in documents]

    # Entrenar el modelo LDA
    modelo_lda = LdaModel(corpus, id2word=diccionario, num_topics=5)
    palabras = []
    for idx, topic in modelo_lda.print_topics(-1):
        palabras = re.findall(r'"(.*?)"', topic)

    return palabras


def get_entities(texto):
    doc = nlp(texto)
    entities = {''}
    for ent in doc.ents:
        entities.add(ent.text + " " + ent.label_)

    return entities


def get_frases(texto):
    segmentos = re.split(r'(?=\b[A-Z][a-z]*\b)', texto)
    segmentos = [seg for seg in segmentos if seg.strip()]

    return '. '.join(segmentos)


def get_political_stopwords(sample_text):
    doc = nlp(sample_text)

    # Generar una lista de palabras vacías basada en el análisis gramatical
    political_stop_words = set()
    for token in doc:
        if token.is_stop and token.is_alpha:
            political_stop_words.add(token.lemma_)

    return political_stop_words


def get_vocabulary(texto):
    palabras = [palabra for palabra in texto.split() if palabra.isalpha()]
    conteo = Counter(palabras)
    return conteo.most_common(20)


def get_feelings(texto):

    blob = TextBlob(texto)
    sentimiento = blob.sentiment

    # Imprimir el análisis
    print(f"Polaridad: {sentimiento.polarity}")
    print(f"Subjetividad: {sentimiento.subjectivity}")

    return sentimiento


def get_data_feeling(sentimiento):

    text = ""
    if sentimiento.polarity > 0:
        text = "El texto tiene un sentimiento positivo."
    elif sentimiento.polarity < 0:
        text = "El texto tiene un sentimiento negativo."
    else:
        text = "El texto es neutral."
    return text
