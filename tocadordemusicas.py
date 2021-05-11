from tkinter import *
from tkinter import filedialog, messagebox

import audioplayer.abstractaudioplayer
from audioplayer import AudioPlayer


def escolher_musica():
    """O usuário escolhe o arquivo duma música."""
    global tocador, tocador_estado

    formatos_suportados = (("MP3", "*.mp3"),)
    arquivo_caminho = filedialog.askopenfilename(title="Selecione um arquivo de som",
                                                 filetypes=formatos_suportados)

    try:  # Checa se o caminho é válido
        tocador = AudioPlayer(arquivo_caminho)
        tocador.volume = 0
        tocador.play()
    except audioplayer.abstractaudioplayer.AudioPlayerError:
        botao_pause.configure(state=DISABLED)
        messagebox.showwarning(title="Tocador de Músicas", message=f"{arquivo_caminho}\nO Tocador de "
                                                                   "Músicas não pode ler o arquivo.\nEsse não é um "
                                                                   "arquivo váliado ou não há suporte para ele.")
    else:  # Reinicia o tocador
        tocador.stop()
        tocador.volume = 100
        botao_pause.configure(text="Começar", state=ACTIVE)
        tocador_estado = False


def pausar_despausar():
    global tocador, tocador_estado

    if tocador_estado:
        tocador.pause()
        botao_pause.configure(text="Despausar")
        tocador_estado = False
    else:
        tocador.resume()
        botao_pause.configure(text="Pausar")
        tocador_estado = True


root = Tk()
root.title("Tocador de Músicas")
root.iconbitmap("icon.ico")

tocador = AudioPlayer
tocador_estado = False

botao_escolher_musica = Button(root, text="Escolhar Música", command=escolher_musica, anchor=E)
botao_escolher_musica.grid(row=0, column=0, sticky=W+E)

# Botão para controlar a música
botao_pause = Button(root, text="Começar", command=pausar_despausar, state=DISABLED, anchor=CENTER)
botao_pause.grid(row=1, column=0)

escolher_musica()

root.mainloop()
