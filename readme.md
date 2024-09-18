# Voice recorder and transcribe (PyAudio & Whisper & MinIO)

## Configurando o ambiente (Windows)
- Para começar precisamos importar uma pasta do GitHub do próprio minio [(minio/minio-py)](https://github.com/minio/minio-py), na qual é obrigatório para conseguir conectar o Minio [(docker)](https://min.io/docs/minio/container/index.html) com o python e subir arquivos para os buckets ou resgata-los para a maquina.

- Ao entrar na pasta, terá alguns outros arquivos e pastas, porem o mais importante é o **setup.py**, ele irá realizar o download de alguns arquivos que faltam para rodar o Minio no python.

```bash
> python setup.py install
```

- Além disso é preciso baixar a biblioteca do Minio e clonar a pasta minio-py:

```bash
> pip install minio
> git clone https://github.com/minio/minio-py
```

- Para realizar a conexão no código python e realizar um **GET/PUT/UPDATE/DELETE**, é preciso importar a biblioteca do minio e criar um variável para passar os parâmetros de conexão:
```bash
from minio import Minio

client = Minio(
     "localhost:9000",
     access_key="",
     secret_key="",
     secure=False,
)
```
- Agora precisamos criar um container no Docker usando a imagem **minio/minio** para conseguirmos criar os buckets e subir os objetos (dados, txt, pdf, video, mp3...), após baixar o [Docker](https://www.docker.com/products/docker-desktop/) precisamos criar uma pasta para volume do container, no caso eu criei no disco local C: (C:\), você precisa de uma pasta e dentro dela criar outra chamada **'data'** e outra chamada **'config\.env'**, dentro do arquivo .env deve conter as seguintes informações:

```bash
MINIO_ROOT_USER=*****
MINIO_ROOT_PASSWORD=*****


MINIO_VOLUMES="C:\\minio\\data"

MINIO_OPTS="--console-address :9001"
```


Após configurar as pastas iremos para o PowerShell executar o comando do container:

```bash
> docker run -dt -p 9000:9000 -p 9001:9001 -v C:\minio\data -v C:\minio\config\.env:/etc/config.env -e "MINIO_CONFIG_ENV_FILE=/etc/config.env" --name 'minio_local' minio/minio server --console-address ":9001"
```
> [!WARNING]
> Ao criar um container do Minio, é definido 2 portas de sua escolha, na qual escolhi as portas 9000 e 9001, é importante saber qual porta você escolheu pois uma será para definir a porta de conexão API e outra porta para acesso WebUI, nesse caso a porta 9000 foi definida para API, para consultar para qual direção a porta está apontando basta dar o seguinte comando:

```bash
> docker logs (nome_do_container)

   WebUI: http://172.17.0.2:9001 http://127.0.0.1:9001
     RootUser: *****
     RootPass: *****

   API: http://172.17.0.2:9000 http://127.0.0.1:9000
     RootUser: *****
     RootPass: *****
```

- No caso o nome do container será definido no **--name** ao criar um container novo.

- Após isso o ambiente para utilizar o Minio com Python está pronto, para conseguirmos testar se a conexão foi feita com sucesso, você pode acessar o **WebUI** do Minio e criar um bucket e vermos com código Python se existe este bucket ou não, porém irei ensinar a criar um bucket a partir do Python e logo após verificar se ele existe ou não:

```bash
from minio import Minio

# Conexão com o minio
client = Minio(
    "localhost:9000",
    access_key=*****,
    secret_key=*****,
    secure=False,
)

# Nome do bucket que será criado
bucket_name = input("What name do u choose for your bucket: ")

client.make_bucket(bucket_name)
print(f"The bucket {bucket_name}, has been created")
```
****
```bash
from minio import Minio

# Conexão com o minio
client = Minio(
     "localhost:9000",
     access_key=*****,
     secret_key=*****,
     secure=False,
)

# Escolher o nome que quer consultar se existe
bucket = input("Whats the name of your buckt: ")

# Validar se o bucket já existe ou não
if client.bucket_exists(bucket):
  print(bucket, "exists!")
else:
  print(bucket, "doesn't exist!")
```
***
## fput_object & fget_object


- Existe vários outros parâmetros que servem para Consultar/Deletar/Alterar/Adicionar algo ao bucket ou o próprio bucket, como por exemplo:
  - ***fput_object()***   _Colocar um objeto dentro de um bucket de sua escolha e com o nome do arquivo e extensão (.txt, .mp3, .pdf ...) que você quiser._
  
  - ***fget_object()*** _Ao contrario do **PUT**, o GET ele vai até um bucket de sua escolha e trás o arquivo que você escolher, além disso você pode salvar na sua maquina com um nome diferente do nome que está dentro do bucket e pode salvar quantas vezes quiser._

> [!WARNING]
> Uma questão importante é que existe o **fget**/**fput** & **get**/**put**, a diferença entre eles é que o parâmetro que possui ***F*** tem o significado de "File" (arquivo), onde ele irá inserir o arquivo inteiro dentro do bucket, caso escolha um nome que já possua um arquivo criado ele irá tentar juntar os 2 em 1 sem perder conteúdo, caso seja um .TXT por exemplo, ele irá pegar todo conteúdo do .TXT que está sendo adicionado e inserir ao final do .TXT que está dentro do bucket escolhido, caso não esteja criado ele irá criar um novo arquivo com o nome e extensão que escolheu, já o parâmetro GET e PUT será apenas para inserir ou puxar dados do arquivo escolhido, ele não insere arquivos diretamente ou cria novos arquivos (Não testei, mas acredito que seja isso pelo que eu li).

- Segue um código de exemplo com fput & fget:

```bash
from minio import Minio

client = Minio(
     "localhost:9000",
     access_key=*****,
     secret_key=*****,
     secure=False,
)

put = client.fput_object(
    "test", # Nome do bucket.
    "test_put.txt", # Nome do arquivo + extensão que será salva dentro do bucket.
    "path/to/testing_put.txt", # Local do PC onde está o arquivo que deseja subir para o bucket.
)

print(
  "created {0} object; etag: {1}, version-id: {2}".format(
    result.object_name, result.etag, result.version_id,
 ),
)
```

```bash
from minio import Minio

client = Minio(
     "localhost:9000",
     access_key=*****,
     secret_key=*****,
     secure=False,
)

client.fget_object(
   "test", # Nome do bucket que irá acessar.
   "test_put.txt", # nome do arquivo dentro do bucket que deseja puxar para o PC.
   "testing_get.txt", # Escolha do nome que o arquivo irá ficar salvo no PC.
)

# Após rodar o código irá aparecer um arquivo com o nome "testing_put.txt" e 
# todo o conteúdo dentro, este arquivo ficara salvo na mesma pasta que você rodou o código (minio-py).
```

- Com isso da para começar a brincar um pouco com o Minio e realizar alguns testes, segue o link do artigo com vários comandos e funcionalidades do [Minio](https://min.io/docs/minio/linux/developers/python/API.html).
***
## Configurando o Gravador de audio & Transcrição (Whisper-OpenAI)

- Para começar precisamos baixar algumas bibliotecas na qual são necessárias para fazer o gravador e a transcrição com whisper da openai, segue a lista de bibliotecas:

  - pip install pyaudio wave
  - pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
  - [Chocolatey](https://chocolatey.org/install) (Instalar pelo PowerShell)
  - pip install openai-whisper ou pip install git+https://github.com/openai/whisper.git
  - [FFMPEG](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/) (Obrigatorio para rodar o whisper, no site tem o passo a passo, não se esqueça de colocar no PATH do windows)
  - pip install keyboard (opcional)
  - pip install pathlib (caso não tenha) (opcional)

- Após baixar essas poucas bibliotecas, está pronto para criar o gravador de audio + a transcrição do audio para texto com o whisper, a seguir é o código para criar o gravador, ao executar ele ficará rodando e gravando tudo, caso baixe a biblioteca "keyboard" será configurado para parar a gravação com o "q", caso não queira baixar e configurar uma tecla para isso basta clicar CTRL+C para interromper a gravação, segue o código:

```bash
import pyaudio
import wave
import whisper
import keyboard

nome_arquivo = input("Escolha um nome para salvar o arquivo: ")

audio = pyaudio.PyaAudio()

stream = audio.open(
    input=True, # Se irá receber audio ou enviar (True == Receber)
    format=pyaudio.paInt16, # Formato do audio reconhecido pelo python
    channels=1, # Mono ou Estero (1 == Mono / 2 == Estereo)
    rate=44000 # Mhz do audio (qualidade)
    frames_per_buffer=1024,
)

frames = []

try:
  while True:
      bloco = stream.read(1024)
      frames.append(bloco) # Ele ficará inserindo dados na lista Frames até que seja interrompido
      if keyboard.is_pressed('q'):
        print("Gravação parada!")
        break
except KeyboardInterrupt: # CTRL+C
  print("Gravação parada!")
  pass

stream.start_stream()
stream.close()
audio.terminate()
arquivo_final = wave.open(nome_arquivo+".mp3", "wb") # O 'wb' significa "Write bits" (Escrever bytes) é preciso desse b pois os dados salvos na lista "frames" são bytes.
arquivo_final.setchannels(1) # Mono
arquivo_final.setframerate(44000) # Mhz
arquivo_final.setsampwidth(audio.get_sample_size(pyaudio.paInt16))

arquivo_final.writeframes(b"".join(frames)) # Novamente o 'b' por conta que são bytes

arquivo_final.close()
```

- Após rodar esse código, você irá escolher um nome para o arquivo ser salvo e irá começar a gravar tudo que você falar ao apertar 'q' (caso tenha baixado a biblioteca 'keyboard') ou CTRL+C ele para de gravar e faz todo o processamento do arquivo para salvar no formato que desejar, eu escolhi .mp3, porem pode ser .wav também ou outro que seja compatível com áudio.

- Agora para conseguirmos transcrever iremos montar um código com a biblioteca Whisper, na qual usa a IA do chatgpt para conseguir realizar a transcrição, porem usa processamento do próprio computador, sendo assim existe níveis de processamento, quanto menor o nível de processamento, pior irá ser a transcrição, ele pode acabar transcrevendo coisas que nem foram ditas no áudio, segue a lista de processamentos do pior para o melhor:

|  Size  | Req. VRAM  | Relative speed |
|:------:|:----------:|:--------------:|
|  tiny  |  ~1 GB     |      ~32x      |
|  base  |  ~1 GB     |      ~16x      |
| small  |  ~2 GB     |      ~6x       |
| medium |  ~5 GB     |      ~2x       |
| large  | ~10 GB     |       1x       |

- O código é bem simples, são apenas 5 linhas de código (caso não queira salvar em um .txt), porem faremos algumas linhas a mais para estar salvando o que for dito em um arquivo TXT, segue o código:

```bash
import whisper

model = whisper.load_model("small") # Processamento para transcrição (lista acima)
result = model.transcribe("test.mp3") # Nome do arquivo que você deseja transcrever (deve ser áudio) caso ele não esteja
# na mesma página do código informe todo o caminho, caso surja algum erro tente passar com duas barras exemplo: path\\to\\audio.mp3

# print(result["text]) # Fica a criterio se quiser dar print, iremos salva-lo em um arquivo TXT então não influencia.

# Salvando em um .TXT
with open('teste.txt', '+a') as arquivo:
    arquivo.write(result['text'])
print("Áudio salvo em um arquivo TXT")
```

- Pronto, após o ultimo print ele irá criar um novo arquivo com o nome que você definiu .txt, ao abrir o arquivo terá todo o conteúdo do áudio transcrito nele, **obs:** como citei dependendo do nível de processamento pode ser que a transcrição não tenha nada haver com o aúdio.

> [!NOTE]
> Com essa pequena base de conhecimento sobre os 3 assuntos é possível junta-los e criar um programa que faz a captura do áudio, logo em seguida já transcreve salva em um arquivo .txt e manda para o Minio para manter salvo, caso queira dar uma olhada entre no [project_minio_whisper/minio-py/main.py](https://github.com/VitorAraujo63/project_minio_whisper/blob/main/minio-py/main.py) em meu GitHub, lá está montado tudo certinho já com conexão para o Minio.

> [!CAUTION]
> Em breve mais atualizações...