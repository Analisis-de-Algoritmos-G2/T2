import os

from usecases import usecase_extraction, usecase_diagrams, usecase_mining, usecase_neo4j
from utils import files, transforms
from dotenv import load_dotenv
import threading

load_dotenv()


def process_video(video_id):

    transcript = usecase_extraction.extract_transcript(video_id)
    files.create_file((os.getenv("TRANSCRIPT_DEBATE_FILE")) + video_id + ".txt", transcript)

    print(f"\n Se ha generado el Transcript para el Video con ID: {video_id}")
    print(f"\n ---------------------------- Se procede a resumir, limpiar y Procesar el Transcript del debate con ID {video_id}--------------------")

    summarize = usecase_mining.get_summarize(usecase_mining.get_frases(transcript))
    files.create_file((os.getenv("SUMMARIZE_DEBATE_FILE")) + video_id + ".txt", summarize)

    clean_transcript = usecase_mining.process_text(transcript, usecase_mining.get_political_stopwords(transcript))
    files.create_file((os.getenv("CLEAN_DEBATE_FILE")) + video_id + ".txt", clean_transcript)

    topics = usecase_mining.get_principal_topics(' '.join(clean_transcript))
    entities = usecase_mining.get_entities(' '.join(clean_transcript))
    vocabulary = usecase_mining.get_vocabulary(' '.join(clean_transcript))
    wordcount = usecase_mining.get_word_frequency(' '.join(clean_transcript))
    feeling = usecase_mining.get_data_feeling(usecase_mining.get_feelings(' '.join(clean_transcript)))

    print(f"\n ---------------------------- Resultado del debate con ID {video_id}--------------------\n"
          f"Los temas principales son: {topics}\n"
          f"Las entidades mencionadas son: {entities}\n"
          f"El vocabulario principal fue: {vocabulary}\n"
          f"El sentimiento del debate es: {feeling}")

    print(f"\n ---------------------------- Gráficas del debate con ID {video_id}--------------------\n")
    usecase_diagrams.create_cloud_words((os.getenv("CLEAN_DEBATE_FILE")) + video_id + ".txt", usecase_mining.get_political_stopwords(transcript), video_id)


if __name__ == '__main__':

    ids = ["fxXU1vvbQyA", "6_Cs1tKzzbE", "uLC0dJhQ1d0&t=3775s"]
    threads = []

    for video_id in ids:
        t = threading.Thread(target=process_video, args=(video_id,))
        t.start()
        threads.append(t)

    # Espera a que todos los hilos terminen
    for t in threads:
        t.join()


