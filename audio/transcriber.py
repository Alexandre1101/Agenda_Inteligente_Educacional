# Arquivo para deixar funções de transcrição de áudio para texto

import whisper


def transcriber(audio):
    model = whisper.load_model("large")

    result = model.transcribe(
        audio,
        language="pt",
        fp16=False
    )

    texto = result["text"]

    return texto
