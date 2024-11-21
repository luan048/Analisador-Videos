from youtube_transcript_api import YouTubeTranscriptApi

from pytube import extract
import pandas as pd

import tkinter as tk
from tkinter import simpledialog

# Cria uma janela
root = tk.Tk()
root.withdraw()

# Lista para leganda do video
lista = []

link_videoYT = simpledialog.askstring("Analisador video", "Insira o link do video")
video_Id = extract.video_id(link_videoYT) # Extrai legenda

srt = YouTubeTranscriptApi.get_transcript(video_Id, languages=['pt'])

# Repetição para pegar linha por linha
for i in srt:
    lista.append(i)

# Cria o dataframe
df = pd.DataFrame(lista)
df

# Baixa as transcrições
df_download = df.to_csv("dados.csv", encoding= 'utf-8')
df_download

print(df) #Temporário