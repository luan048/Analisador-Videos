from youtube_transcript_api import YouTubeTranscriptApi

from pytube import extract
import pandas as pd

import tkinter as tk
from tkinter import messagebox

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string

nltk.download('punkt')
nltk.download('stopwords')

# Função para gerar resumo
def functionGerar_resumo(df, num_sentencas=5):
    try:
        # Legenda em um único texto
        texto = " ".join(df['text'])

        # Transforma tudo em Token
        sentencas = sent_tokenize(texto)

        # Deixa o Token somente em palavras, tira pontuação
        stop_words = set(stopwords.words("portuguese"))
        palavras = word_tokenize(texto.lower())
        palavras_limpas = [palavra for palavra in palavras if palavra not in stop_words and palavra not in string.punctuation]

        # Verifica fequencia das palavras para gerar um resumo baseado nas palavras mais importantes que mais se repetem
        frequencia_palavras = {}
        for palavra in palavras_limpas:
            frequencia_palavras[palavra] = frequencia_palavras.get(palavra, 0) + 1

        sentenca_pontuacao = {} # Armazena as palavras com maior pontuação, que mais se repetem
        for sentenca in sentencas:
            for palavra in word_tokenize(sentenca.lower()):
                if palavra in frequencia_palavras:
                    sentenca_pontuacao[sentenca] = sentenca_pontuacao.get(sentenca, 0) + frequencia_palavras[palavra]

        # Seleciona as sentenças com maior pontuação
        sentencas_resumo = sorted(sentenca_pontuacao, key=sentenca_pontuacao.get, reverse=True)[:num_sentencas]
        
        # Junta as sentenças
        resumo = " ".join(sentencas_resumo)
        return resumo
    except Exception as e:
        return f"Erro ao gerar resumo: {e}"

# Função principal para extrair e resumir o vídeo
def functionResume_video():
    try:
        # Obtem o link do vídeo pela entrada
        link_videoYT = entrada.get()

        # Valida link
        if not link_videoYT:
            raise ValueError("Nenhum link foi inserido...")

        # Extrai o ID do vídeo
        video_Id = extract.video_id(link_videoYT)

        # Obtém legendas do vídeo
        srt = YouTubeTranscriptApi.get_transcript(video_Id, languages=['pt'])

        # Cria uma lista com as legendas
        lista = [linha for linha in srt]
        df = pd.DataFrame(lista)

        # Aciona a função de gerar resumo
        resumo = functionGerar_resumo(df, num_sentencas=5)

        # Salva legendas em CSV
        df.to_csv("dados.csv", encoding='utf-8', index=False)

        # Exibe o resumo na interface
        saida.config(text="Resumo:\n" + resumo)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro no processamento do vídeo: {e}")

# Abre Janela
janela = tk.Tk()
janela.title("Analisador de Vídeos")

# Permite entrada do link
tk.Label(janela, text="Digite o link do vídeo:").pack()
entrada = tk.Entry(janela, width=40)
entrada.pack()

# Botão para iniciar o resumo
botao = tk.Button(janela, text="Resumir", command=functionResume_video)
botao.pack()

saida = tk.Label(janela, text="", fg="blue", wraplength=400, justify="left")
saida.pack()

janela.mainloop()