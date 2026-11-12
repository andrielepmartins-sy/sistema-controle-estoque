import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

# -------------------------- CORES --------------------------

FUNDO = "#0B0F14"
FUNDO_CARD = "#111820"
FUNDO_CARD_2 = "#151E28"
VERDE = "#00E5A0"
VERDE_ESCURO = "#00A878"
BRANCO = "#F5F7FA"
CINZA = "#8B98A8"
CINZA_ESCURO = "#202A35"
VERMELHO = "#FF5577"
AZUL = "#4DA6FF"

PASTA_DADOS = "Dados"
os.makedirs(PASTA_DADOS, exist_ok=True)

ARQUIVO_PRODUTOS = os.path.join(PASTA_DADOS, "produtos.json")
ARQUIVO_MOVIMENTACOES = os.path.join(PASTA_DADOS, "movimentacoes.json")


# -------------------------- ARQUIVOS JSON --------------------------

def carregar_arquivo(nome_arquivo):
    # Se o arquivo ainda não existir, começa com uma lista vazia.
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if not isinstance(dados, list):
            raise ValueError("O conteúdo do arquivo precisa ser uma lista.")

        return dados

    except FileNotFoundError:
        return []

    except (json.JSONDecodeError, OSError, ValueError) as erro:
        messagebox.showerror(
            "Erro ao carregar dados",
            f"Não foi possível ler {nome_arquivo}.\n\n{erro}"
        )
        return []


def salvar_arquivo(nome_arquivo, dados):
    # Salva os dados no formato JSON.
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        return True

    except (OSError, TypeError) as erro:
        messagebox.showerror(
            "Erro ao salvar",
            f"Não foi possível salvar os dados.\n\n{erro}"
        )
        return False


# -------------------------- JANELA PRINCIPAL --------------------------

class SistemaEstoque:

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("StockFlow | Controle de Estoque")
        self.janela.geometry("1100x700")
        self.janela.minsize(950, 620)
        self.janela.configure(bg=FUNDO)

        self.produtos = carregar_arquivo(ARQUIVO_PRODUTOS)
        self.movimentacoes = carregar_arquivo(ARQUIVO_MOVIMENTACOES)

        self.configurar_estilo()
        self.criar_interface()
        self.atualizar_telas()

    # -------------------------- ESTILO --------------------------

    def configurar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background=FUNDO_CARD,
            foreground=BRANCO,
            fieldbackground=FUNDO_CARD,
            rowheight=32,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "Treeview.Heading",
            background=FUNDO_CARD_2,
            foreground=VERDE,
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )

        estilo.map(
            "Treeview",
            background=[("selected", VERDE_ESCURO)],
            foreground=[("selected", BRANCO)]
        )

        estilo.map(
            "Treeview.Heading",
            background=[("active", CINZA_ESCURO)]
        )

    # -------------------------- COMPONENTES --------------------------

    def criar_botao(self, pai, texto, comando, cor=VERDE_ESCURO):
        return tk.Button(
            pai,
            text=texto,
            command=comando,
            bg=cor,
            fg=BRANCO,
            activebackground=VERDE,
            activeforeground=FUNDO,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=14,
            pady=9,
            cursor="hand2"
        )

    def criar_titulo(self, pai, texto):
        tk.Label(
            pai,
            text=texto,
            bg=FUNDO,
            fg=BRANCO,
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", pady=(0, 15))

    def criar_tabela(self, pai, colunas, larguras):
        tabela = ttk.Treeview(
            pai,
            columns=colunas,
            show="headings"
        )

        for coluna, largura in zip(colunas, larguras):
            tabela.heading(coluna, text=coluna)
            tabela.column(coluna, width=largura, anchor="center")

        tabela.pack(fill="both", expand=True)

        return tabela

    # -------------------------- INTERFACE --------------------------

    def criar_interface(self):
        topo = tk.Frame(
            self.janela,
            bg=FUNDO_CARD,
            height=85
        )
        topo.pack(fill="x")
        topo.pack_propagate(False)

        tk.Label(
            topo,
            text="StockFlow",
            bg=FUNDO_CARD,
            fg=VERDE,
            font=("Segoe UI", 23, "bold")
        ).pack(side="left", padx=25, pady=18)

        tk.Label(
            topo,
            text="CONTROLE DE ESTOQUE",
            bg=FUNDO_CARD,
            fg=CINZA,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=5, pady=27)

        self.resumo = tk.Label(
            topo,
            text="",
            bg=FUNDO_CARD,
            fg=BRANCO,
            font=("Segoe UI", 10)
        )
        self.resumo.pack(side="right", padx=25)

        corpo = tk.Frame(
            self.janela,
            bg=FUNDO,
            padx=22,
            pady=18
        )
        corpo.pack(fill="both", expand=True)

        menu = tk.Frame(corpo, bg=FUNDO)
        menu.pack(fill="x", pady=(0, 18))

        botoes = [
            ("PRODUTOS", self.mostrar_produtos),
            ("MOVIMENTAÇÕES", self.mostrar_movimentacoes),
            ("ESTOQUE BAIXO", self.mostrar_estoque_baixo),
            ("RELATÓRIOS", self.mostrar_relatorio)
        ]

        for texto, comando in botoes:
            self.criar_botao(
                menu,
                texto,
                comando,
                CINZA_ESCURO
            ).pack(side="left", padx=(0, 8))

        self.area = tk.Frame(corpo, bg=FUNDO)
        self.area.pack(fill="both", expand=True)

        self.mostrar_produtos()

    def limpar_area(self):
        for widget in self.area.winfo_children():
            widget.destroy()

    def atualizar_telas(self):
        total = len(self.produtos)

        unidades = sum(
            produto["quantidade"]
            for produto in self.produtos
        )

        baixos = sum(
            1 for produto in self.produtos
            if produto["quantidade"] <= produto["estoque_minimo"]
        )

        self.resumo.config(
            text=f"{total} produtos   |   {unidades} unidades   |   {baixos} com estoque baixo"
        )

    # -------------------------- CADASTRO DE PRODUTOS --------------------------

    def mostrar_produtos(self):
        self.limpar_area()
        self.criar_titulo(self.area, "Produtos cadastrados")

        barra = tk.Frame(self.area, bg=FUNDO)
        barra.pack(fill="x", pady=(0, 12))

        self.busca_produto = tk.StringVar()

        campo_busca = tk.Entry(
            barra,
            textvariable=self.busca_produto,
            bg=FUNDO_CARD,
            fg=BRANCO,
            insertbackground=BRANCO,
            relief="flat",
            font=("Segoe UI", 11)
        )

        campo_busca.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9,
            padx=(0, 8)
        )

        campo_busca.insert(
            0,
            "Digite código ou nome para pesquisar"
        )

        campo_busca.bind(
            "<FocusIn>",
            self.limpar_texto_busca
        )

        campo_busca.bind(
            "<KeyRelease>",
            lambda evento: self.atualizar_tabela_produtos()
        )

        self.criar_botao(
            barra,
            "NOVO PRODUTO",
            lambda: self.abrir_formulario_produto()
        ).pack(side="right")

        area_tabela = tk.Frame(self.area, bg=FUNDO)
        area_tabela.pack(fill="both", expand=True)

        colunas = (
            "Código",
            "Nome",
            "Quantidade",
            "Mínimo",
            "Preço unitário"
        )

        self.tabela_produtos = self.criar_tabela(
            area_tabela,
            colunas,
            (100, 350, 130, 110, 150)
        )

        acoes = tk.Frame(self.area, bg=FUNDO)
        acoes.pack(fill="x", pady=(12, 0))

        self.criar_botao(
            acoes,
            "ALTERAR",
            self.alterar_produto,
            AZUL
        ).pack(side="left", padx=(0, 8))

        self.criar_botao(
            acoes,
            "EXCLUIR",
            self.excluir_produto,
            VERMELHO
        ).pack(side="left")

        self.atualizar_tabela_produtos()

    def limpar_texto_busca(self, evento):
        if self.busca_produto.get() == "Digite código ou nome para pesquisar":
            self.busca_produto.set("")

    def atualizar_tabela_produtos(self):
        if not hasattr(self, "tabela_produtos"):
            return

        for item in self.tabela_produtos.get_children():
            self.tabela_produtos.delete(item)

        termo = self.busca_produto.get().strip().lower()

        for produto in self.produtos:
            codigo = str(produto["codigo"])
            nome = produto["nome"]

            if termo and termo not in codigo.lower() and termo not in nome.lower():
                continue

            self.tabela_produtos.insert(
                "",
                "end",
                values=(
                    f'{produto["codigo"]:03}',
                    nome,
                    produto["quantidade"],
                    produto["estoque_minimo"],
                    f'R$ {produto["preco"]:.2f}'
                )
            )

    def abrir_formulario_produto(self, produto=None):
        janela = tk.Toplevel(self.janela)

        janela.title(
            "Cadastrar produto"
            if produto is None
            else "Alterar produto"
        )

        janela.geometry("420x440")
        janela.resizable(False, False)
        janela.configure(bg=FUNDO_CARD)
        janela.transient(self.janela)
        janela.grab_set()

        tk.Label(
            janela,
            text="Dados do produto",
            bg=FUNDO_CARD,
            fg=VERDE,
            font=("Segoe UI", 17, "bold")
        ).pack(pady=(20, 15))

        campos = {}

        dados = produto or {
            "codigo": "",
            "nome": "",
            "quantidade": 0,
            "estoque_minimo": 0,
            "preco": ""
        }

        nomes = [
            ("Código", "codigo"),
            ("Nome", "nome"),
            ("Quantidade", "quantidade"),
            ("Estoque mínimo", "estoque_minimo"),
            ("Preço unitário", "preco")
        ]

        for rotulo, chave in nomes:
            linha = tk.Frame(janela, bg=FUNDO_CARD)
            linha.pack(fill="x", padx=35, pady=6)

            tk.Label(
                linha,
                text=rotulo,
                bg=FUNDO_CARD,
                fg=CINZA,
                font=("Segoe UI", 10)
            ).pack(anchor="w")

            entrada = tk.Entry(
                linha,
                bg=FUNDO_CARD_2,
                fg=BRANCO,
                insertbackground=BRANCO,
                relief="flat",
                font=("Segoe UI", 11)
            )

            entrada.pack(fill="x", ipady=7, pady=(3, 0))
            entrada.insert(0, str(dados[chave]))

            campos[chave] = entrada

            if chave == "codigo" and produto is not None:
                entrada.config(state="disabled")

        def salvar():
            try:
                codigo = int(campos["codigo"].get())
                nome = campos["nome"].get().strip()
                quantidade = int(campos["quantidade"].get())
                minimo = int(campos["estoque_minimo"].get())

                preco_texto = (
                    campos["preco"].get().strip().replace(",", ".")
                )

                preco = float(preco_texto)

                if codigo <= 0:
                    raise ValueError(
                        "O código precisa ser maior que zero."
                    )

                if not nome:
                    raise ValueError(
                        "O nome do produto é obrigatório."
                    )

                if quantidade < 0 or minimo < 0:
                    raise ValueError(
                        "Quantidade e estoque mínimo não podem ser negativos."
                    )

                if preco <= 0:
                    raise ValueError(
                        "O preço precisa ser maior que zero."
                    )

                if produto is None:
                    for item in self.produtos:
                        if item["codigo"] == codigo:
                            raise ValueError(
                                "Já existe um produto com esse código."
                            )

                    novo = {
                        "codigo": codigo,
                        "nome": nome,
                        "quantidade": quantidade,
                        "estoque_minimo": minimo,
                        "preco": preco
                    }

                    self.produtos.append(novo)

                else:
                    produto["nome"] = nome
                    produto["quantidade"] = quantidade
                    produto["estoque_minimo"] = minimo
                    produto["preco"] = preco

                if salvar_arquivo(ARQUIVO_PRODUTOS, self.produtos):
                    janela.destroy()
                    self.atualizar_telas()
                    self.atualizar_tabela_produtos()

                    messagebox.showinfo(
                        "Sucesso",
                        "Produto salvo com sucesso."
                    )

            except ValueError as erro:
                messagebox.showwarning(
                    "Verifique os dados",
                    str(erro)
                )

        self.criar_botao(
            janela,
            "SALVAR PRODUTO",
            salvar
        ).pack(pady=20)

    def produto_selecionado(self):
        selecao = self.tabela_produtos.selection()

        if not selecao:
            messagebox.showwarning(
                "Atenção",
                "Selecione um produto na tabela."
            )
            return None

        codigo = int(
            self.tabela_produtos.item(
                selecao[0],
                "values"
            )[0]
        )

        for produto in self.produtos:
            if produto["codigo"] == codigo:
                return produto

        return None

    def alterar_produto(self):
        produto = self.produto_selecionado()

        if produto:
            self.abrir_formulario_produto(produto)

    def excluir_produto(self):
        produto = self.produto_selecionado()

        if not produto:
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f'Deseja excluir o produto "{produto["nome"]}"?'
        )

        if confirmar:
            self.produtos.remove(produto)

            if salvar_arquivo(ARQUIVO_PRODUTOS, self.produtos):
                self.atualizar_telas()
                self.atualizar_tabela_produtos()

    # -------------------------- ENTRADAS E SAÍDAS --------------------------

    def mostrar_movimentacoes(self):
        self.limpar_area()

        self.criar_titulo(
            self.area,
            "Movimentação de mercadorias"
        )

        botoes = tk.Frame(self.area, bg=FUNDO)
        botoes.pack(fill="x", pady=(0, 15))

        self.criar_botao(
            botoes,
            "REGISTRAR ENTRADA",
            lambda: self.abrir_movimentacao("Entrada")
        ).pack(side="left", padx=(0, 8))

        self.criar_botao(
            botoes,
            "REGISTRAR SAÍDA",
            lambda: self.abrir_movimentacao("Saída"),
            VERMELHO
        ).pack(side="left")

        self.criar_titulo(
            self.area,
            "Histórico de movimentações"
        )

        self.tabela_movimentacoes = self.criar_tabela(
            self.area,
            ("Data", "Tipo", "Código", "Produto", "Quantidade"),
            (160, 130, 100, 350, 130)
        )

        self.atualizar_tabela_movimentacoes()

    def abrir_movimentacao(self, tipo):
        if not self.produtos:
            messagebox.showwarning(
                "Sem produtos",
                "Cadastre um produto antes de movimentar o estoque."
            )
            return

        janela = tk.Toplevel(self.janela)
        janela.title(f"Registrar {tipo.lower()}")
        janela.geometry("410x330")
        janela.resizable(False, False)
        janela.configure(bg=FUNDO_CARD)
        janela.transient(self.janela)
        janela.grab_set()

        tk.Label(
            janela,
            text=f"Registrar {tipo.lower()}",
            bg=FUNDO_CARD,
            fg=VERDE,
            font=("Segoe UI", 17, "bold")
        ).pack(pady=20)

        tk.Label(
            janela,
            text="Produto",
            bg=FUNDO_CARD,
            fg=CINZA
        ).pack(anchor="w", padx=35)

        opcoes = [
            f'{produto["codigo"]:03} - {produto["nome"]}'
            for produto in self.produtos
        ]

        escolha = tk.StringVar(value=opcoes[0])

        lista = ttk.Combobox(
            janela,
            textvariable=escolha,
            values=opcoes,
            state="readonly"
        )

        lista.pack(
            fill="x",
            padx=35,
            pady=(5, 15),
            ipady=5
        )

        tk.Label(
            janela,
            text="Quantidade",
            bg=FUNDO_CARD,
            fg=CINZA
        ).pack(anchor="w", padx=35)

        quantidade = tk.Entry(
            janela,
            bg=FUNDO_CARD_2,
            fg=BRANCO,
            insertbackground=BRANCO,
            relief="flat",
            font=("Segoe UI", 11)
        )

        quantidade.pack(
            fill="x",
            padx=35,
            pady=(5, 15),
            ipady=7
        )

        tk.Label(
            janela,
            text=f"Data: {date.today().strftime('%d/%m/%Y')}",
            bg=FUNDO_CARD,
            fg=CINZA
        ).pack(pady=3)

        def confirmar():
            try:
                qtd = int(quantidade.get())

                if qtd <= 0:
                    raise ValueError(
                        "Informe uma quantidade maior que zero."
                    )

                codigo = int(
                    escolha.get().split(" - ")[0]
                )

                produto = next(
                    item for item in self.produtos
                    if item["codigo"] == codigo
                )

                if tipo == "Saída" and qtd > produto["quantidade"]:
                    raise ValueError(
                        f'Estoque insuficiente. Disponível: {produto["quantidade"]}.'
                    )

                quantidade_anterior = produto["quantidade"]

                if tipo == "Entrada":
                    produto["quantidade"] += qtd
                else:
                    produto["quantidade"] -= qtd

                movimento = {
                    "tipo": tipo,
                    "codigo": codigo,
                    "produto": produto["nome"],
                    "quantidade": qtd,
                    "data": date.today().strftime("%d/%m/%Y"),
                    "registrado_em": datetime.now().strftime("%H:%M:%S")
                }

                self.movimentacoes.append(movimento)

                produtos_salvos = salvar_arquivo(
                    ARQUIVO_PRODUTOS,
                    self.produtos
                )

                movimentos_salvos = salvar_arquivo(
                    ARQUIVO_MOVIMENTACOES,
                    self.movimentacoes
                )

                if produtos_salvos and movimentos_salvos:
                    janela.destroy()

                    self.atualizar_telas()
                    self.atualizar_tabela_movimentacoes()

                    messagebox.showinfo(
                        "Movimentação registrada",
                        f"{tipo} registrada com sucesso."
                    )

                else:
                    produto["quantidade"] = quantidade_anterior
                    self.movimentacoes.pop()

            except StopIteration:
                    messagebox.showerror(
                        "Erro",
                        "O produto selecionado não foi encontrado."
                    )

            except ValueError as erro:
                messagebox.showwarning(
                    "Verifique os dados",
                    str(erro)
                )

        self.criar_botao(
            janela,
            "CONFIRMAR",
            confirmar
        ).pack(pady=18)

    def atualizar_tabela_movimentacoes(self):
        if not hasattr(self, "tabela_movimentacoes"):
            return

        for item in self.tabela_movimentacoes.get_children():
            self.tabela_movimentacoes.delete(item)

        for movimento in reversed(self.movimentacoes):
            self.tabela_movimentacoes.insert(
                "",
                "end",
                values=(
                    movimento.get("data", ""),
                    movimento.get("tipo", ""),
                    f'{movimento.get("codigo", 0):03}',
                    movimento.get("produto", ""),
                    movimento.get("quantidade", 0)
                )
            )

    # -------------------------- CONSULTA DE ESTOQUE BAIXO --------------------------

    def mostrar_estoque_baixo(self):
        self.limpar_area()

        self.criar_titulo(
            self.area,
            "Produtos com estoque baixo"
        )

        tk.Label(
            self.area,
            text="Produtos cuja quantidade atual está igual ou abaixo do estoque mínimo.",
            bg=FUNDO,
            fg=CINZA,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(0, 15))

        tabela = self.criar_tabela(
            self.area,
            ("Código", "Produto", "Quantidade atual", "Estoque mínimo"),
            (120, 400, 180, 180)
        )

        encontrados = [
            produto for produto in self.produtos
            if produto["quantidade"] <= produto["estoque_minimo"]
        ]

        for produto in encontrados:
            tabela.insert(
                "",
                "end",
                values=(
                    f'{produto["codigo"]:03}',
                    produto["nome"],
                    produto["quantidade"],
                    produto["estoque_minimo"]
                )
            )

        if not encontrados:
            tk.Label(
                self.area,
                text="Nenhum produto está com estoque baixo.",
                bg=FUNDO,
                fg=VERDE,
                font=("Segoe UI", 11, "bold")
            ).pack(anchor="w", pady=12)

    # -------------------------- RELATÓRIOS --------------------------

    def mostrar_relatorio(self):
        self.limpar_area()

        self.criar_titulo(
            self.area,
            "Relatórios"
        )

        total_produtos = len(self.produtos)

        total_unidades = sum(
            p["quantidade"] for p in self.produtos
        )

        valor_estoque = sum(
            p["quantidade"] * p["preco"]
            for p in self.produtos
        )

        baixos = [
            p for p in self.produtos
            if p["quantidade"] <= p["estoque_minimo"]
        ]

        resumo = (
            f"RESUMO DO ESTOQUE\n\n"
            f"Quantidade de produtos cadastrados: {total_produtos}\n"
            f"Total de unidades em estoque: {total_unidades}\n"
            f"Valor estimado do estoque: R$ {valor_estoque:.2f}\n"
            f"Produtos com estoque baixo: {len(baixos)}\n"
            f"Movimentações registradas: {len(self.movimentacoes)}\n\n"
            f"PRODUTOS COM ESTOQUE BAIXO\n\n"
        )

        if baixos:
            for produto in baixos:
                resumo += (
                    f'{produto["nome"]} - '
                    f'{produto["quantidade"]} unidade(s) '
                    f'(mínimo: {produto["estoque_minimo"]})\n'
                )

        else:
            resumo += "Nenhum produto no momento.\n"

        caixa = tk.Text(
            self.area,
            bg=FUNDO_CARD,
            fg=BRANCO,
            insertbackground=BRANCO,
            font=("Consolas", 11),
            relief="flat",
            padx=18,
            pady=18,
            wrap="word"
        )

        caixa.pack(fill="both", expand=True)
        caixa.insert("1.0", resumo)
        caixa.config(state="disabled")

        self.criar_botao(
            self.area,
            "ATUALIZAR RELATÓRIO",
            self.mostrar_relatorio
        ).pack(anchor="e", pady=12)


# -------------------------- INICIAR SISTEMA --------------------------

if __name__ == "__main__":
    janela = tk.Tk()
    app = SistemaEstoque(janela)
    janela.mainloop()