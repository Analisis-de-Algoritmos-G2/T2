from youtube_transcript_api import YouTubeTranscriptApi


def extract_transcript(video_id):

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['es'])

    transcript_text = ' '.join([d['text'] for d in transcript.fetch()])

    return transcript_text


def extract_keywords(texts):
    vectorizer = TfidfVectorizer(max_features=10)  # Cambia el número de palabras clave
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    return feature_names
