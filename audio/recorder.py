#arquivo para tentar implementar gravador de áudio

from pathlib import Path
from datetime import datetime


def save_audio(audio_data: bytes) -> Path:

    audio_dir = Path("data/audio")
    audio_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filepath = audio_dir / f"aula_{timestamp}.wav"

    filepath.write_bytes(audio_data)

    return filepath
