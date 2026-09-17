#gpt sugeriu mas estou achando inutil 

from audio.transcriber import transcriber
from ai.extractor import extractor


def process_lesson(audio_path):

    texto = transcriber(audio_path)

    aula = extractor(texto)

    return texto, aula
