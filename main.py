import tkinter as tk
from tkinter import filedialog, ttk
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

def transcrever_azure(audio_file_path, progress_bar, duracao_audio):
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
        progresso = (speech_recognizer.properties[speechsdk.PropertyId.SpeechServiceConnection_AudioLength] / duracao_audio) * 100
        progress_bar['value'] = progresso
        root.update_idletasks()

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

def select_video_file():
    video_file_path.set(filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")]))
    progress_bar['value'] = 0  # Reset progress bar

def process_video():
    video_file = video_file_path.get()
    if video_file:
        print(f"Processing video: {video_file}")
        audio_file_path = "audio_extraido.wav"
        duracao_audio = extrair_audio(video_file, audio_file_path)
        
        transcricao = transcrever_azure(audio_file_path, progress_bar, duracao_audio)
        if transcricao:
            palavras_chave = ["corta", "voltando", "parou", "retomando"]
            momentos = identificar_palavras_chave(transcricao, palavras_chave, duracao_audio)
            salvar_transcricao_em_txt(transcricao, momentos, output_txt_path)
            
            print(f"Texto completo transcrito: {transcricao['text']}")
            print("Momentos das palavras-chave identificadas:")
            for momento in momentos:
                print(f"Palavra: {momento['palavra']}, Timestamp: {momento['timestamp']}")
    else:
        print("Please select a video file.")

root = tk.Tk()
root.title("Video Processing")

output_txt_path = r"C:\Users\fabri\OneDrive\Desktop\transcricoes-fiap\transcricao.txt"

video_file_path = tk.StringVar()
video_file_entry = tk.Entry(root, textvariable=video_file_path, width=50)
video_file_entry.grid(row=0, column=0, padx=10, pady=10)

select_video_button = tk.Button(root, text="Select Video", command=select_video_file)
select_video_button.grid(row=0, column=1, padx=10, pady=10)

process_button = tk.Button(root, text="Process Video", command=process_video)
process_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

if __name__ == "__main__":
    video_file_path.set(r"C:/Users/fabri/Downloads/riverside_aula_2 - vídeo 1 * oct 3, 2024 001*[aula_7_8_2] 1mlet .mp4")
