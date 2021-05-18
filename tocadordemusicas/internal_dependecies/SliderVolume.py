from tkinter import *


class SliderVolume(Frame):
    def __init__(self, parent, x=0, y=0, largura_linha=130, func=None, cor="gray", **options):
        Frame.__init__(self, parent, **options)

        self.min_botao = x  # Menor posição horizontal em que o botão do slider deve estar e sua posição inicial
        self.y = y  # A posição vertical do slider no programa
        self.largura = largura_linha  # A largura da linha do slider
        self.func = func  # Função chamada quando o valor do slider se altera
        self.cor = cor  # A cor do botão do slider

        # Desenha a linha do slider
        self.linha = Canvas(parent, highlightthickness=0, borderwidth=0, height=self.winfo_reqheight(),
                            width=self.largura)
        self.linha.create_line(0, 0, self.largura, 0, width=10)

        # O botão, que é o slider em si
        self.botao = Button(parent, text="", bg=self.cor, activebackground=self.cor, relief=SOLID, bd=0.2)
        self.max_button = self.largura + self.min_botao - self.botao.winfo_reqwidth()  # Maior posição horizontal em
        # que o slider deve estar
        self.botao.bind("<B1-Motion>", self.botao_pressionado)
        self.botao.bind("<ButtonRelease-1>", self.botao_solto)

        # Pões os widgets
        self.linha.place(x=self.min_botao, y=self.y + 12)
        self.botao.place(x=self.min_botao, y=self.y)

    def botao_pressionado(self, event):
        """Chamada quando o botão se pressiou e moveu. Move o slider aonde o mouse está"""

        posicao = max(self.botao.winfo_x() + event.x, self.min_botao)  # Vindoura posição do botão
        posicao = min(posicao, self.max_button)
        self.botao.place(x=posicao)

        if self.func is not None:
            self.func(self.get())

    def botao_solto(self, event):
        """Chamada quando o botão é solto. Chama a função dada como argumento."""

        if self.func is not None:
            self.func(self.get())

    def get(self):
        """O valor do slider em porcentagem (0%–100%), i.e., (0–1)"""

        posicao_atual = self.botao.winfo_x()
        posicao_porcentagem = (posicao_atual - self.min_botao) / (self.max_button - self.min_botao)
        return posicao_porcentagem

    def set(self, value_percentage):
        """Define o valor do slider em porcentagem"""

        posicao = value_percentage * (self.max_button - self.min_botao) + self.min_botao
        posicao = max(posicao, self.min_botao)
        posicao = min(posicao, self.max_button)
        self.botao.place(x=posicao)

