import azure.cognitiveservices.speech as speechsdk
from moviepy.editor import VideoFileClip
import threading

def extrair_audio(video_file_path, output_audio_path):
    video = VideoFileClip(video_file_path)
    video.audio.write_audiofile(output_audio_path, codec='pcm_s16le', ffmpeg_params=['-ar', '16000', '-ac', '1'])
    return video.duration  

def identificar_palavras_chave(transcricao, palavras_chave, duracao_audio):
    momentos = []
    
    for palavra in palavras_chave:
        if palavra.lower() in transcricao["text"].lower():
            index = transcricao["text"].lower().find(palavra.lower())
            segundos_aprox = (index / len(transcricao["text"])) * duracao_audio
            
            horas = int(segundos_aprox // 3600)
            minutos = int((segundos_aprox % 3600) // 60)
            segundos = int(segundos_aprox % 60)
            milissegundos = int((segundos_aprox - int(segundos_aprox)) * 1000)
            
            timestamp = f"{horas:02}:{minutos:02}:{segundos:02}:{milissegundos:03}"
            momentos.append({
                "palavra": palavra,
                "timestamp": timestamp
            })
    return momentos

def transcrever_azure(audio_file_path):
    speech_key = "EQWqe14P4vdBeFeJ8Ilq27hJ3sfsZ8zRkgsMwynvpDnp61WfUnIkJQQJ99AKACZoyfiXJ3w3AAAYACOGHPXg"
    service_region = "brazilsouth"
    
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = "pt-BR"
    
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    resultado_transcricao = []

    done = threading.Event()

    def handle_final_result(evt):
        resultado_transcricao.append(evt.result.text)

    def handle_session_stopped(evt):
        done.set()

    speech_recognizer.recognized.connect(handle_final_result)
    speech_recognizer.session_started.connect(lambda evt: print("Sessão de transcrição iniciada"))
    speech_recognizer.session_stopped.connect(handle_session_stopped)
    speech_recognizer.canceled.connect(lambda evt: print(f"Transcrição cancelada: {evt.reason}"))

    speech_recognizer.start_continuous_recognition()
    done.wait()  
    speech_recognizer.stop_continuous_recognition()

    texto_completo = ' '.join(resultado_transcricao)
    return {"text": texto_completo}

def salvar_transcricao_em_txt(transcricao, momentos, output_txt_path):
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write("Texto Completo da Transcrição:\n")
        f.write(transcricao["text"] + "\n\n")
        f.write("Momentos das Palavras-chave:\n")
        for momento in momentos:
            f.write(f"Palavra: {momento['palavra']}, Timestamp: {momento['timestamp']}\n")
    print(f"Transcrição e momentos salvos em {output_txt_path}")

if __name__ == "__main__":
    video_file_path = r"passa o caminho do vídeo aqui"
    audio_file_path = r"passa um caminho com o final desse\audio_extraido.wav"
    output_txt_path = r"C:passa um caminho\transcricao.txt"
    palavras_chave = ["corta", "voltando", "parou", "retomando"] #palavras reservadas

    duracao_audio = extrair_audio(video_file_path, audio_file_path)
    transcricao = transcrever_azure(audio_file_path)

    if transcricao:
        momentos = identificar_palavras_chave(transcricao, palavras_chave, duracao_audio)
        salvar_transcricao_em_txt(transcricao, momentos, output_txt_path)
        
        print(f"Texto completo transcrito: {transcricao['text']}")
        print("Momentos das palavras-chave identificadas:")
        for momento in momentos:
            print(f"Palavra: {momento['palavra']}, Timestamp: {momento['timestamp']}")
