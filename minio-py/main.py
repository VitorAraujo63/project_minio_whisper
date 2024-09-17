import pyaudio
import wave
import whisper
from minio import Minio
import keyboard
from pathlib import Path


client = Minio(
        "localhost:9000",
        access_key="teste123",
        secret_key="teste123",
        secure=False,
    )

while True:
    nome_arquivo = input("Digite o nome do arquivo: ")
    object_1 = False
    object_2 = False
    try:
        object_1 = bool(client.stat_object("mp3", f'{nome_arquivo}.mp3'))
        object_2 = bool(client.stat_object("content", f'{nome_arquivo}.txt'))
    except:
        pass
    
    if object_1 == False or object_2 == False:
        print("Nome escolhido com sucesso!")
        break
    else:
        print("Já existe um arquivo salvo com esse nome, tente outro...")
        continue

audio = pyaudio.PyAudio()

stream = audio.open(
    input=True,
    format=pyaudio.paInt16,
    channels=1,
    rate=44000,
    frames_per_buffer=1024,
)

frames = []

try:
    while True:
        bloco = stream.read(1024)
        frames.append(bloco)
        if keyboard.is_pressed('q'):
            print("Reuniao finalizada!")
            break
except KeyboardInterrupt:
    print("Reuniao finalizada!")
    pass

stream.start_stream()
stream.close()
audio.terminate()
arquivo_final = wave.open(nome_arquivo+".mp3", "wb")
arquivo_final.setnchannels(1)
arquivo_final.setframerate(44000)
arquivo_final.setsampwidth(audio.get_sample_size(pyaudio.paInt16))

arquivo_final.writeframes(b"".join(frames))

arquivo_final.close()



while True:
    escolha = input("Você deseja realmente salvar essa reuniao? (s/n):")

    if escolha == 's':
        model = whisper.load_model("small")
        result = model.transcribe(nome_arquivo+".mp3")

        with open(nome_arquivo+".txt", "+a") as arq:
            arq.write(result['text'])

        mp3 = client.fput_object(
            "mp3", 
            f"{nome_arquivo}.mp3", 
            f"C:\\Users\\tonyb\\OneDrive\\Desktop\\minio\\minio-py\\{nome_arquivo}.mp3",
        )

        content = client.fput_object(
            "content", 
            f"{nome_arquivo}.txt",  
            f"C:\\Users\\tonyb\\OneDrive\\Desktop\\minio\\minio-py\\{nome_arquivo}.txt",
        )

        print("Reuniao salva no MiniIO")

        Path(nome_arquivo+".mp3").unlink()
        Path(nome_arquivo+".txt").unlink()
        break
    
    else:
        escolha2 = input("Você tem certeza que não deseja salvar a reunião? (s/n):")

        if escolha2 == 's':
            Path(nome_arquivo+".mp3").unlink()
            print("Excluindo os arquivos da reunião...")
            break
        else:
            pass