from tkinter import *
from tkinter import filedialog, messagebox

from tocadordemusicas.libs.audioplayer.abstractaudioplayer import AudioPlayerError
from tocadordemusicas.libs.audioplayer import AudioPlayer
from tocadordemusicas.libs.PIL import Image
from tocadordemusicas.libs.PIL import ImageTk

from tocadordemusicas.internal_dependecies.SliderVolume import SliderVolume


def atualizar_volume(valor):
    """Autaliza o volume do tocador de músicas"""

    volume = valor * 100
    tocador.volume = volume


def reiniciar_tocador(arquivo_caminho):
    """Reconfigura o tocador de músicas"""

    global tocador, tocador_estado, musica_iniciada

    tocador = AudioPlayer(arquivo_caminho)
    atualizar_volume(slider_volume.get())
    botao_pausar.configure(text="Começar", state=ACTIVE, image=imagem_despausar)
    tocador_estado = False
    musica_iniciada = False


def escolher_musica():
    """O usuário escolhe o arquivo duma música."""

    formatos_suportados = (("MP3", "*.mp3"),)
    arquivo_caminho = filedialog.askopenfilename(title="Selecione um arquivo de som",
                                                 filetypes=formatos_suportados)

    if arquivo_caminho == "":
        return

    try:  # Checa se o arquivo é válido, tocando um tocador-de=músicas-dummy
        tocador_teste = AudioPlayer(arquivo_caminho)
        tocador_teste.volume = 0
        tocador_teste.play()
    except AudioPlayerError:
        messagebox.showwarning(title="Tocador de Músicas", message=f"{arquivo_caminho}\nO Tocador de "
                                                                   "Músicas não pode ler o arquivo.\nEsse não é um "
                                                                   "arquivo váliado ou não há suporte para ele.")
    else:
        # Reinicia o tocador
        tocador_teste.close()
        reiniciar_tocador(arquivo_caminho)

        # Formatando o nome do arquivo
        arquivo_nome_list = []
        ponto_formato = True  # Se o primeiro ponto da direita para a esquerda já se encontrou
        for c in arquivo_caminho[-1::-1]:
            if c == "." and ponto_formato:
                arquivo_nome_list = []
                ponto_formato = False
            elif c != "/":
                arquivo_nome_list.append(c)
            else:
                break
        arquivo_nome = "".join(arquivo_nome_list[-1::-1])
        if len(arquivo_nome) > 26:  # If the song's name is too long
            arquivo_nome = arquivo_nome[0:23] + "..."
        label_nome_musica.configure(text=arquivo_nome)


def pausar_musica():
    """Pausa a música"""

    global tocador, tocador_estado

    tocador.pause()
    botao_pausar.configure(image=imagem_despausar)
    tocador_estado = False


def despausar_musica():
    """Despausa a música"""

    global tocador, tocador_estado

    tocador.resume()
    botao_pausar.configure(image=imagem_pausar)
    tocador_estado = True


def iniciar_musica():
    """Inicia uma música que não se iniciara"""

    global tocador, tocador_estado, musica_iniciada

    tocador.play()
    botao_pausar.configure(image=imagem_pausar)
    tocador_estado = True
    musica_iniciada = True


def pausar_despausar():
    """Pausa ou despausa a música"""

    global tocador_estado, musica_iniciada

    if tocador_estado:  # Se tocando
        pausar_musica()
    elif not musica_iniciada:
        iniciar_musica()
    else:
        despausar_musica()


def parar_musica(event):
    """Para a música"""

    global tocador_estado, musica_iniciada

    tocador.stop()
    botao_pausar.configure(image=imagem_despausar)
    tocador_estado = False
    musica_iniciada = False


bg_cor = "white"  # Cor de fundo da aplicação
in_cor = "light green"  # Cor-tema
fonte_cor = "black"  # Cor da fonte

root = Tk()
root.title("Tocador de Músicas")
root.configure(bg=bg_cor)
root.iconbitmap("icon.ico")
root.geometry("300x115+26+26")
root.resizable(width=False, height=False)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(3, weight=1)

tocador = AudioPlayer("")
tocador_estado = False  # Se está tocando música
musica_iniciada = False  # Se a música atual já foi iniciada

# Botão para escolher a música
botao_escolher_musica = Button(root, text="Escolher Música", command=escolher_musica, anchor=CENTER,
                               activebackground=bg_cor, bg=in_cor, fg=fonte_cor, bd=1, relief=SOLID)
botao_escolher_musica.grid(row=0, column=0, pady=7)

# Botão para controlar a música
imagem_despausar = ImageTk.PhotoImage(Image.open("internal_dependecies/img/play-button.png"))
imagem_pausar = ImageTk.PhotoImage(Image.open("internal_dependecies/img/pause-button.png"))
botao_pausar = Button(root, command=pausar_despausar, state=DISABLED, image=imagem_despausar, bd=0, anchor=CENTER,
                      bg=bg_cor, activebackground=bg_cor)
botao_pausar.place(x=121, y=38)

# Botão para parar a música
imagem_parar = ImageTk.PhotoImage(Image.open("internal_dependecies/img/stop-button.png"))
botao_parar = Label(root, image=imagem_parar, bd=0, bg=bg_cor, activebackground=bg_cor)
botao_parar.bind("<Button-1>", parar_musica)
botao_parar.place(x=153, y=39)

# Slider para controlar o volume
slider_volume = SliderVolume(root, largura_linha=80, x=110, y=67, func=atualizar_volume, cor=in_cor)
slider_volume.set(1)

# Label mostrando o nome da música
label_nome_musica = Label(root, text="Nenhuma Música", anchor=S, relief=SUNKEN, bg=in_cor, bd=0, pady=3,
                          activebackground=bg_cor, fg=fonte_cor)
label_nome_musica.grid(row=3, column=0, sticky=W+E+S)


root.mainloop()
