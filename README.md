🤖 J.A.R.V.I.S - Assistente Virtual em Python

Um assistente virtual inteligente inspirado no J.A.R.V.I.S do Homem de Ferro, capaz de controlar o computador usando voz, automação, inteligência artificial e visão de tela.

O sistema pode ouvir comandos, falar respostas, abrir aplicativos, enviar mensagens, analisar a tela e muito mais.

🚀 Funcionalidades

✔ Reconhecimento de voz
✔ Respostas faladas com Edge TTS
✔ Integração com IA (Groq + Llama)
✔ Automação do computador
✔ Controle do navegador
✔ Envio de mensagens no WhatsApp
✔ Captura e análise da tela com IA
✔ OCR para leitura de texto da tela
✔ Criação automática de planilhas
✔ Pesquisa no Google / YouTube / Wikipedia
✔ Sistema de lembretes

🧠 Tecnologias usadas

Python

SpeechRecognition

Edge TTS

Groq AI

PyAutoGUI

Pytesseract

Pandas

Requests

Pygame

📥 Como clonar o projeto
1️⃣ Instalar o Git

Baixe e instale:

https://git-scm.com/downloads

Verifique:

git --version
2️⃣ Clonar o repositório
git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git

Exemplo:

git clone https://github.com/vitorguiljerme1-max/jarvis-ai.git
3️⃣ Entrar na pasta do projeto
cd jarvis-ai
🧪 Criar ambiente virtual (recomendado)
python -m venv venv

Ativar no Windows:

venv\Scripts\activate
📦 Instalar dependências
pip install SpeechRecognition requests pandas pyautogui pytesseract groq edge-tts pygame openpyxl pyaudio pillow
⚙️ Instalar programas obrigatórios
1️⃣ Tesseract OCR

Baixe:

https://github.com/UB-Mannheim/tesseract/wiki

Instale em:

C:\Program Files\Tesseract-OCR
2️⃣ FFmpeg

Baixe:

https://ffmpeg.org/download.html

Adicione ao PATH do Windows.

🔑 Configurar API Keys

No código jarvis.py adicione suas chaves:

WEATHER_API_KEY = "SUA_CHAVE"
GROQ_API_KEY = "SUA_CHAVE"
▶️ Rodar o J.A.R.V.I.S

Execute:

python jarvis.py
🎤 Exemplos de comandos

Você pode falar:

que horas são
qual o clima em recife
abrir youtube
pesquisar inteligência artificial
tocar música
tirar print
analisar minha tela
ler texto da tela
criar planilha
enviar mensagem no whatsapp
📂 Estrutura do projeto
jarvis-ai
│
├── jarvis.py
├── memoria_jarvis.txt
├── README.md
└── requirements.txt
⚠️ Aviso

Este projeto é educacional e demonstra automação com IA, reconhecimento de voz e visão computacional.

👨‍💻 Autor

Desenvolvido por Vitor Guilherme

GitHub:
https://github.com/vitorkr1
