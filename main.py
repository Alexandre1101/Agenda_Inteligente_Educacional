#arquivo central do projeto, vamos deixar o mvp.py de lado, ou para testes pontuais ... 

from audio.transcriber import transcriber
from ai.extractor import extractor


audio = "aula.mp3"

texto = transcriber(audio)

resultado = extractor(texto)

print(resultado)
