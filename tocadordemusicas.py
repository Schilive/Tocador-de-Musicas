from tkinter import *
from tkinter import filedialog, messagebox

import audioplayer.abstractaudioplayer
from audioplayer import AudioPlayer
from PIL import ImageTk, Image


def escolher_musica():
    """O usuário escolhe o arquivo duma música."""
    global tocador, tocador_estado

    formatos_suportados = (("MP3", "*.mp3"),)
    arquivo_caminho = filedialog.askopenfilename(title="Selecione um arquivo de som",
                                                 filetypes=formatos_suportados)

    if arquivo_caminho == "":
        return

    try:  # Checa se o caminho é válido
        tocador = AudioPlayer(arquivo_caminho)
        tocador.volume = 0
        tocador.play()
    except audioplayer.abstractaudioplayer.AudioPlayerError:
        botao_pausar.configure(state=DISABLED)
        messagebox.showwarning(title="Tocador de Músicas", message=f"{arquivo_caminho}\nO Tocador de "
                                                                   "Músicas não pode ler o arquivo.\nEsse não é um "
                                                                   "arquivo váliado ou não há suporte para ele.")
    else:
        # Reinicia o tocador
        tocador.stop()
        tocador.volume = 100
        botao_pausar.configure(text="Começar", state=ACTIVE)
        tocador_estado = False

        # Formatando o nome do arquivo
        arquivo_nome_list = []
        ponto_formato = True
        for c in arquivo_caminho[-1::-1]:
            if c == "." and ponto_formato:
                arquivo_nome_list = []
                ponto_formato = False
            elif c != "/":
                arquivo_nome_list.append(c)
            else:
                break
        arquivo_nome = "".join(arquivo_nome_list[-1::-1])
        label_nome_musica.configure(text=arquivo_nome)


def pausar_despausar():
    global tocador, tocador_estado

    print(root.winfo_geometry())

    if tocador_estado:
        tocador.pause()
        botao_pausar.configure(text="Despausar", image=imagem_despausado)
        tocador_estado = False
    else:
        tocador.resume()
        botao_pausar.configure(text="Pausar", image=imagem_pausado)
        tocador_estado = True


root = Tk()
root.title("Tocador de Músicas")
root.iconbitmap("icon.ico")
root.geometry("283x73+26+26")
root.resizable(width=False, height=False)

frame_principal = Frame(root)
frame_principal.pack()

tocador = AudioPlayer
tocador_estado = False  # Se está tocando música

# Botão para escolher a música
botao_escolher_musica = Button(frame_principal, text="Escolher Música", command=escolher_musica)
botao_escolher_musica.grid(row=0, column=0)

# Botão para controlar a música
imagem_despausado = ImageTk.PhotoImage(Image.open("play-button-arrowhead.png"))
imagem_pausado = ImageTk.PhotoImage(Image.open("pause-button.png"))
botao_pausar = Button(frame_principal, command=pausar_despausar, state=DISABLED, image=imagem_despausado, bd=0)
botao_pausar.grid(row=1, column=0)

# Label mostrando o nome da música
label_nome_musica = Label(frame_principal, text="Nenhuma Música")
label_nome_musica.grid(row=2, column=0)

escolher_musica()

root.mainloop()
