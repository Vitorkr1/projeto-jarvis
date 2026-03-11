import speech_recognition as sr
import webbrowser
import os
import time
from datetime import datetime
import requests
import pandas as pd
import pyautogui
import pytesseract
import base64
from groq import Groq
import asyncio
import edge_tts

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

WEATHER_API_KEY = "sua api"
GROQ_API_KEY = "sua api"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pygame.mixer.init()

def speak(text):
    print(f"\n🔊 {text}")
    voice = "pt-BR-AntonioNeural"
    output_file = "temp_voz.mp3"
    
    async def _gerar_audio():
        communicate = edge_tts.Communicate(text, voice, rate="+20%")
        await communicate.save(output_file)
        
    asyncio.run(_gerar_audio())
    
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.05)
        
    pygame.mixer.music.unload()
    try:
        if os.path.exists(output_file):
            os.remove(output_file)
    except Exception:
        pass

def listen():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 1500  
    recognizer.dynamic_energy_threshold = True 
    recognizer.pause_threshold = 0.5 
    
    with sr.Microphone() as source:
        print("\r🎤 Ouvindo...     ", end="", flush=True)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            print("\rProcessando...  ", end="", flush=True)
            query = recognizer.recognize_google(audio, language='pt-BR')
            print(f"\r✓ Você disse: {query}                  ")
            return query.lower().strip()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            print("\r✗ Não entendi a frase.    ", end="", flush=True)
            return ""
        except sr.RequestError:
            print(f"\r✗ Sem conexão com a internet. Aguarde...")
            time.sleep(2)
            return ""
        except Exception:
            return ""
def send_whatsapp_automation():
    try:
        speak("Para quem devo enviar a mensagem?")
        contato = listen()
        if not contato: return False

        speak(f"O que devo dizer para {contato}?")
        mensagem = listen()
        if not mensagem: return False

        speak(f"Buscando {contato} no sistema. Aguarde.")
        
        webbrowser.open("https://web.whatsapp.com")
        time.sleep(18) 

       
        pyautogui.hotkey('ctrl', 'alt', '/') 
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        

        pyautogui.write(contato, interval=0.1)
        time.sleep(4)

        pyautogui.press('enter')
        time.sleep(2)
        
        pyautogui.write(mensagem)
        time.sleep(1)
        pyautogui.press('enter')
        
        speak(f"Mensagem enviada para {contato}.")
        return True
    except Exception as e:
        print(f"Erro: {e}")
        speak("Falha na automação.")
        return False
def extract_city_from_command(command):
    palavras_chave = ['em ', 'de ', 'na ', 'no ', 'para ', 'por ']
    for palavra in palavras_chave:
        if palavra in command:
            idx = command.find(palavra) + len(palavra)
            city = command[idx:].strip()
            if city and len(city) > 0:
                return city
    return None

def get_weather(city_input):
    try:
        if not city_input:
            speak("Qual cidade?")
            city_input = listen()
        if not city_input:
            speak("Cidade não encontrada.")
            return False
        city = city_input.strip()
        url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no&lang=pt"
        response = requests.get(url, timeout=5)
        data = response.json()
        if 'current' in data:
            temp = data['current']['temp_c']
            desc = data['current']['condition']['text']
            speak(f"Em {city}, a temperatura é de {temp} graus com {desc}.")
            return True
        else:
            speak(f"Não encontrei a cidade {city}.")
            return False
    except Exception:
        speak("Erro ao consultar clima.")
        return False

def get_weather_forecast(city_input):
    try:
        if not city_input:
            speak("Qual cidade?")
            city_input = listen()
        if not city_input:
            return False
        city = city_input.strip()
        speak(f"Buscando previsão para {city}.")
        url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=yes&lang=pt"
        response = requests.get(url, timeout=5)
        data = response.json()
        if 'current' in data:
            temp = data['current']['temp_c']
            desc = data['current']['condition']['text']
            humidity = data['current']['humidity']
            wind = data['current']['wind_kph']
            speak(f"A temperatura será de {temp} graus, com {desc}. Umidade em {humidity} porcento e vento a {wind} quilômetros por hora.")
            return True
    except Exception:
        speak("Erro ao consultar previsão.")
        return False

def create_spreadsheet():
    speak("Nome da planilha?")
    name = listen()
    if not name:
        speak("Cancelado.")
        return False
    try:
        data = {
            'Data': [datetime.now().strftime('%d/%m/%Y')],
            'Hora': [datetime.now().strftime('%H:%M')],
            'Status': ['OK']
        }
        df = pd.DataFrame(data)
        filename = f"{name.replace(' ', '_')}.xlsx"
        df.to_excel(filename, index=False)
        speak("Planilha criada com sucesso.")
        return True
    except Exception:
        speak("Erro ao criar a planilha.")
        return False

def open_application(app_name):
    app_name = app_name.strip().lower()
    apps = {
        'youtube': 'https://www.youtube.com',
        'whatsapp': 'https://web.whatsapp.com',
        'gmail': 'https://mail.google.com',
        'google': 'https://www.google.com',
        'navegador': 'https://www.google.com',
        'chrome': 'https://www.google.com',
        'spotify': 'https://open.spotify.com',
        'netflix': 'https://www.netflix.com',
        'instagram': 'https://www.instagram.com',
        'facebook': 'https://www.facebook.com',
        'github': 'https://www.github.com',
        'discord': 'https://discord.com',
    }
    if app_name in apps:
        webbrowser.open(apps[app_name])
        speak(f"Abrindo {app_name}.")
        return True
    elif 'calculadora' in app_name or 'calc' in app_name:
        os.system("calc" if os.name == 'nt' else "gnome-calculator")
        speak("Calculadora aberta.")
        return True
    elif 'bloco' in app_name or 'notas' in app_name:
        os.system("notepad" if os.name == 'nt' else "gedit")
        speak("Bloco de notas aberto.")
        return True
    else:
        speak(f"Não reconheço o aplicativo {app_name}.")
        return False

def take_screenshot():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        pyautogui.screenshot(filename)
        speak("Print salvo com sucesso.")
        return True
    except Exception:
        speak("Erro ao tirar print.")
        return False

def write_text(text):
    try:
        time.sleep(0.5)
        pyautogui.write(text, interval=0.02)
        speak("Texto digitado.")
        return True
    except Exception:
        speak("Erro ao digitar.")
        return False

def get_time():
    now = datetime.now().strftime("%H:%M")
    speak(f"Agora são {now}.")

def get_date():
    dias = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
    meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    hoje = datetime.now()
    speak(f"Hoje é {dias[hoje.weekday()]}, {hoje.day} de {meses[hoje.month - 1]}.")

def search_google(query):
    try:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak("Pesquisando.")
        return True
    except Exception:
        speak("Erro ao pesquisar.")
        return False

def search_youtube(query):
    try:
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        speak("Pesquisando no YouTube.")
        return True
    except Exception:
        speak("Erro ao pesquisar no YouTube.")
        return False

def search_wikipedia(query):
    try:
        webbrowser.open(f"https://pt.wikipedia.org/wiki/{query}")
        speak("Abrindo a Wikipedia.")
        return True
    except Exception:
        speak("Erro ao abrir a Wikipedia.")
        return False

def get_news():
    try:
        speak("Buscando notícias.")
        webbrowser.open("https://news.google.com/topstories?hl=pt-BR&gl=BR&ceid=BR:pt-419")
        return True
    except Exception:
        speak("Erro ao buscar notícias.")
        return False

def get_ip_info():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=3)
        ip = response.json()['ip']
        speak(f"Seu endereço de IP é {ip}.")
        return True
    except Exception:
        speak("Erro ao obter IP.")
        return False

def get_random_quote():
    try:
        response = requests.get("https://api.quotable.io/random", timeout=3)
        quote = response.json()['content']
        author = response.json()['author']
        speak(f"Citação: {quote}, por {author}.")
        return True
    except Exception:
        speak("Erro ao buscar citação.")
        return False

def play_music(song):
    try:
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        speak(f"Buscando {song} no YouTube.")
        return True
    except Exception:
        speak("Erro ao buscar a música.")
        return False

def set_reminder():
    speak("Em quantos minutos devo te lembrar?")
    minutes = listen()
    try:
        mins = int(''.join(filter(str.isdigit, minutes)))
        speak(f"Perfeito. Lembrete definido para {mins} minutos.")
        time.sleep(mins * 60)
        speak("Atenção! O tempo do seu lembrete acabou!")
        return True
    except Exception:
        speak("Não entendi o tempo.")
        return False

def abrir_projeto_vscode(nome_projeto):
    base_dir = r"C:\Users\vitor\Downloads\sistemas"
    try:
        for pasta in os.listdir(base_dir):
            if nome_projeto.lower() in pasta.lower():
                caminho_completo = os.path.join(base_dir, pasta)
                if os.path.isdir(caminho_completo):
                    speak(f"Abrindo o projeto {pasta}.")
                    os.system(f'code "{caminho_completo}"')
                    return True
        speak(f"Não encontrei a pasta do projeto {nome_projeto}.")
        return False
    except Exception:
        speak("Erro ao abrir projeto.")
        return False

def analyze_screen_with_ai():
    try:
        speak("Analisando sua tela. Só um instante...")
        screenshot = pyautogui.screenshot()
        temp_path = "temp_screen.png"
        screenshot.save(temp_path)
        
        with open(temp_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        print("\n[IA] Processando imagem com Llama 4 Vision (Groq)...")
        
        client_groq = Groq(api_key=GROQ_API_KEY)
        completion = client_groq.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Descreva de forma curta o que você está vendo nesta imagem (se for código, diga qual linguagem. Se for papel de parede, descreva). Responda em português brasileiro."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                    ]
                }
            ],
            temperature=0.5,
            max_tokens=1024
        )
        
        resposta = completion.choices[0].message.content
        speak(resposta.replace('*', ''))
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return True
    except Exception as e:
        print(f"\n❌ ERRO NA VISÃO GROQ: {e}\n")
        speak("Tive um problema ao processar a imagem da tela.")
        return False

def read_text_from_screen():
    try:
        speak("Lendo o texto da tela...")
        screenshot = pyautogui.screenshot()
        texto_extraido = pytesseract.image_to_string(screenshot, lang='eng+por')
        if texto_extraido.strip():
            print("\n" + "="*40 + "\nTEXTO ENCONTRADO NA TELA:\n" + "="*40)
            print(texto_extraido[:800] + "\n... [Texto truncado]") 
            print("="*40)
            speak("Eu imprimi o texto da sua tela no terminal.")
        else:
            speak("Não encontrei texto legível.")
    except Exception:
        speak("Erro na visão OCR.")

def chat_with_jarvis(query):
    try:
        historico = ""
        arquivo_memoria = "memoria_jarvis.txt"
        
        if os.path.exists(arquivo_memoria):
            with open(arquivo_memoria, "r", encoding="utf-8") as f:
                linhas = f.readlines()
                historico = "".join(linhas[-10:]) 
                
        client_groq = Groq(api_key=GROQ_API_KEY)
        
        system_prompt = f"""Você é o J.A.R.V.I.S., um assistente virtual altamente inteligente e útil. 
O seu chefe se chama Vitor. Responda sempre em português do Brasil de forma natural, curta, direta e conversacional (pois sua resposta será falada em voz alta, evite textos longos ou listas gigantes).
Seja ligeiramente sarcástico e genial, como o Jarvis do Homem de Ferro. use palavras mais curtas
Aqui está a memória recente da conversa para você se contextualizar:
{historico}"""

        print("\n[IA] Pensando...")
        completion = client_groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        resposta = completion.choices[0].message.content
        
        with open(arquivo_memoria, "a", encoding="utf-8") as f:
            f.write(f"Vitor: {query}\nJarvis: {resposta}\n")
            
        speak(resposta.replace('*', '').replace('#', ''))
        
    except Exception as e:
        print(f"\n❌ ERRO NO CHAT: {e}")
        speak("Desculpe chefe, meus servidores de pensamento estão fora do ar.")

def greet_user():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        frase = "Bom dia"
    elif 12 <= hour < 18:
        frase = "Boa tarde"
    else:
        frase = "Boa noite"
    speak(f"{frase} chefe! Sou o Jarvis, manda as ordens")

def show_help():
    help_text = """
    COMANDOS DISPONÍVEIS:
    - Horas / Data / Clima / Previsão
    - Pesquisar / YouTube / Wikipedia
    - Abrir (app) / Abrir VS (projeto)
    - Criar planilha / Escrever / Digitar
    - Tirar print / Captura / Ler tela
    - Ler texto / Ler código / Lembrete
    - Calculadora / Bloco de notas
    - BATER PAPO NORMAL (Qualquer outra frase!)
    - Enviar mensagem (WhatsApp)
    """
    print(help_text)
    speak("Estes são os comandos. Mas agora você pode conversar comigo sobre qualquer coisa.")

def process_command(command):
    if not command:
        return True
        
    print(f"\n→ Você disse: {command}")
    
    # --- LOGICA WHATSAPP ---
    if 'enviar mensagem' in command or 'whatsapp' in command or 'mandar mensagem' in command:
        send_whatsapp_automation()
    
    elif 'horas' in command or 'hora' in command or 'que horas' in command:
        get_time()
    elif 'data' in command or 'dia' in command or 'hoje' in command:
        get_date()
    elif 'previsão' in command or 'forecast' in command:
        city = extract_city_from_command(command)
        get_weather_forecast(city)
    elif 'clima' in command or 'temperatura' in command or 'tempo' in command:
        city = extract_city_from_command(command)
        get_weather(city)
    elif 'pesquisar' in command or 'procurar' in command or 'buscar' in command:
        termo = command.replace('pesquisar', '').replace('procurar', '').replace('buscar', '').strip()
        if termo:
            search_google(termo)
        else:
            speak("O que pesquisar?")
            termo = listen()
            if termo: search_google(termo)
    elif 'youtube' in command:
        termo = command.replace('youtube', '').strip()
        if termo:
            search_youtube(termo)
        else:
            speak("O que procurar no YouTube?")
            termo = listen()
            if termo: search_youtube(termo)
    elif 'wikipedia' in command:
        termo = command.replace('wikipedia', '').strip()
        if termo:
            search_wikipedia(termo)
        else:
            speak("O que procurar na Wikipedia?")
            termo = listen()
            if termo: search_wikipedia(termo)
    elif 'notícia' in command or 'noticia' in command or 'news' in command:
        get_news()
    elif 'música' in command or 'musica' in command or 'tocar' in command:
        speak("Qual música tocar?")
        song = listen()
        if song: play_music(song)
    elif 'planilha' in command or 'excel' in command:
        create_spreadsheet()
    elif 'abrir vs' in command or 'abrir projeto' in command:
        nome_projeto = command.replace('abrir vs', '').replace('abrir projeto', '').replace('code', '').strip()
        if nome_projeto:
            abrir_projeto_vscode(nome_projeto)
        else:
            speak("Qual projeto abrir?")
            nome_projeto = listen()
            if nome_projeto: abrir_projeto_vscode(nome_projeto)
    elif 'abrir' in command:
        app = command.replace('abrir', '').strip()
        if app:
            open_application(app)
        else:
            speak("Qual aplicativo abrir?")
            app = listen()
            if app: open_application(app)
    elif 'escrever' in command or 'digitar' in command:
        texto = command.replace('escrever', '').replace('digitar', '').strip()
        if texto:
            write_text(texto)
        else:
            speak("O que devo escrever?")
            texto = listen()
            if texto: write_text(texto)
    elif 'tela' in command and ('ver' in command or 'analisar' in command or 'minha' in command or 'que' in command):
        analyze_screen_with_ai()
    elif 'ler texto' in command or 'ler código' in command:
        read_text_from_screen()
    elif 'tirar print' in command or 'captura' in command or 'screenshot' in command:
        take_screenshot()
    elif 'lembrete' in command or 'reminder' in command:
        set_reminder()
    elif 'ip' in command or 'endereço' in command:
        get_ip_info()
    elif 'citação' in command or 'citacao' in command or 'frase' in command:
        get_random_quote()
    elif 'calculadora' in command or 'calc' in command:
        open_application("calculadora")
    elif 'bloco' in command or 'notas' in command:
        open_application("bloco")
    elif 'desligar' in command or 'sair' in command or 'tchau' in command or 'encerrar' in command:
        speak("Até logo, chefe. Sistemas desligando.")
        return False
    elif 'ajuda' in command or 'comandos' in command or 'help' in command:
        show_help()
    else:
        chat_with_jarvis(command)
    
    return True

def main():
    print("\n" + "="*60)
    print("J.A.R.V.I.S")
    print("="*60 + "\n")
    
    greet_user()
    time.sleep(1)
    
    while True:
        try:
            query = listen()
            if not query:
                continue
            should_continue = process_command(query)
            if not should_continue:
                break
            time.sleep(0.3)
        except KeyboardInterrupt:
            print("\n⏹️  Encerrando...")
            speak("Até logo, chefe.")
            break
        except Exception:
            time.sleep(0.5)

if __name__ == "__main__":
    main()