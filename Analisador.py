from youtube_transcript_api import YouTubeTranscriptApi

from pytube import extract
import pandas as pd

import tkinter as tk
from tkinter import messagebox

def functionResume_video():
    try:
        # Link do video pela entrada
        link_videoYT = entrada.get()

        # Valida link
        if not link_videoYT:
            raise ValueError("Nenhum link foi inserido...")

        # Extra ID
        video_Id = extract.video_id(link_videoYT)

        srt=YouTubeTranscriptApi.get_transcript(video_Id, languages=['pt']) # Obtem legenda

        lista = [linha for linha in srt]
        df = pd.DataFrame(lista)

        # Salva resumo em CSV
        df.to_csv("dados.csv", encoding='utf-8', index=False)

        saida.config(text="Resumo feito com sucesso!") #TEMPORARIO
        print(df) # Temporario
    
    except Exception as e:
        messagebox.showerror("Erro", f"Erro no processamento do vídeo: {e}")

# Cria uma janela
janela = tk.Tk()
janela.title("Analisador de Videos")

# Permite entrada do link
tk.Label(janela, text="Digite o link do video:").pack()
entrada = tk.Entry(janela, width=40)
entrada.pack()

# Botão que inicia resumo
botao = tk.Button(janela, text="Resumir", command=functionResume_video) #Colocar a função que faz o resumo do video
botao.pack()

saida = tk.Label(janela, text="", fg="blue")
saida.pack()

janela.mainloop()