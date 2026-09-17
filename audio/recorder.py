#arquivo para tentar implementar gravador de áudio

from pathlib import Path


def save_audio(audio_data: bytes, filepath: str | Path) -> Path:
    filepath = Path(filepath)

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    filepath.write_bytes(audio_data)

    return filepath
