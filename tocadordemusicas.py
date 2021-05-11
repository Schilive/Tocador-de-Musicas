from tkinter import *
from tkinter import filedialog, messagebox

import audioplayer.abstractaudioplayer
from audioplayer import AudioPlayer
from PIL import ImageTk, Image


def reiniciar_tocador(arquivo_caminho):
    global tocador, tocador_estado, musica_iniciada

    tocador = AudioPlayer(arquivo_caminho)
    botao_pausar.configure(text="Começar", state=ACTIVE, image=imagem_despausado)
    tocador_estado = False
    musica_iniciada = False


def escolher_musica():
    """O usuário escolhe o arquivo duma música."""

    formatos_suportados = (("MP3", "*.mp3"),)
    arquivo_caminho = filedialog.askopenfilename(title="Selecione um arquivo de som",
                                                 filetypes=formatos_suportados)

    if arquivo_caminho == "":
        return

    try:  # Checa se o arquivo é válido
        tocador_teste = AudioPlayer(arquivo_caminho)
        tocador_teste.volume = 0
        tocador_teste.play()
    except audioplayer.abstractaudioplayer.AudioPlayerError:
        messagebox.showwarning(title="Tocador de Músicas", message=f"{arquivo_caminho}\nO Tocador de "
                                                                   "Músicas não pode ler o arquivo.\nEsse não é um "
                                                                   "arquivo váliado ou não há suporte para ele.")
    else:
        # Reinicia o tocador
        tocador_teste.close()
        reiniciar_tocador(arquivo_caminho)

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
    global tocador, tocador_estado, musica_iniciada

    if tocador_estado:
        tocador.pause()
        botao_pausar.configure(image=imagem_despausado)
        tocador_estado = False
    elif not musica_iniciada:
        tocador.play()
        botao_pausar.configure(image=imagem_pausado)
        tocador_estado = True
        musica_iniciada = True
    else:
        tocador.resume()
        botao_pausar.configure(image=imagem_pausado)
        tocador_estado = True


bg_cor = "white"  # Cor de fundo da aplicação

root = Tk()
root.title("Tocador de Músicas")
root.configure(bg=bg_cor)
root.iconbitmap("icon.ico")
root.geometry("300x100+26+26")
root.resizable(width=False, height=False)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)

tocador = AudioPlayer("")
tocador_estado = False  # Se está tocando música
musica_iniciada = False  # Se já

# Botão para escolher a música
botao_escolher_musica = Button(root, text="Escolher Música", command=escolher_musica, anchor=CENTER,
                               activebackground=bg_cor)
botao_escolher_musica.grid(row=0, column=0, pady=7)

# Botão para controlar a música
imagem_despausado = ImageTk.PhotoImage(Image.open("play-button-arrowhead.png"))
imagem_pausado = ImageTk.PhotoImage(Image.open("pause-button.png"))
botao_pausar = Button(root, command=pausar_despausar, state=DISABLED, image=imagem_despausado, bd=0, anchor=CENTER,
                      bg=bg_cor, activebackground=bg_cor)
botao_pausar.grid(row=1, column=0, sticky=N+S, pady=3)

# Label mostrando o nome da música
label_nome_musica = Label(root, text="Nenhuma Música", anchor=S, relief=SUNKEN, bg="orange", bd=0, pady=3,
                          activebackground=bg_cor)
label_nome_musica.grid(row=2, column=0, sticky=W+E+S)

escolher_musica()

root.mainloop()
