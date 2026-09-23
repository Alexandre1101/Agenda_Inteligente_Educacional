# Arquivo para deixar funções de transcrição de áudio para texto

import whisper


model = whisper.load_model("medium")


def transcriber(audio_path):

    result = model.transcribe(
        str(audio_path),
        language="pt",
        fp16=False
    )

    return result["text"]
