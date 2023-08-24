def create_file(file, transcript):

    if isinstance(transcript, list):
        with open(file, "w") as archivo:
            for word in transcript:
                archivo.write(word + '\n')
    else:
        with open(file, "w") as archivo:
            archivo.write(transcript)


def read_file(file):

    text = ""
    with open(file, "r") as archivo:
        text = archivo.read()

    return text
