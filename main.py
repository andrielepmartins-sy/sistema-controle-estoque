
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# -------------------------- CORES --------------------------

# Cores utilizadas para manter o mesmo padrão em todas as telas.
FUNDO = "#FEEDDD"
CARD = "#FFF8F2"
CAMPO = "#FCE2DC"
ROSA_CLARO = "#FEC1B6"
ROSA = "#F3A6BA"
ROSA_ESCURO = "#DF678F"
LAVANDA = "#9391BC"
AZUL = "#7ABCC4"
TEXTO = "#49384F"
CINZA = "#806F83"
BRANCO = "#FFFFFF"

# Os arquivos JSON ficam dentro da pasta Dados.
PASTA_DADOS = "Dados"
ARQUIVO_PRODUTOS = os.path.join(PASTA_DADOS, "produtos.json")
ARQUIVO_MOVIMENTACOES = os.path.join(PASTA_DADOS, "movimentacoes.json")


class AndriStock:

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("AndriStock - Controle de Estoque")
        self.janela.configure(bg=FUNDO)

        # Organiza o tamanho da janela de acordo com a tela disponível.
        self.definir_tamanho_janela()

        # Prepara os arquivos e carrega os dados salvos anteriormente.
        self.criar_pastas()
        self.carregar_dados()
        self.configurar_estilo()

        self.pagina_atual = "Produtos"
        self.pesquisa_atual = ""

        # Monta a estrutura principal do programa.
        self.criar_interface()
        self.mostrar_produtos()

    # -------------------------- JANELAS --------------------------

    def definir_tamanho_janela(self):
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()

        # Define um tamanho que não ocupe a tela inteira em notebooks.
        largura = min(1050, largura_tela - 40)
        altura = min(680, altura_tela - 80)

        largura = max(700, largura)
        altura = max(500, altura)

        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2

        self.janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        self.janela.minsize(700, 480)

    def centralizar_janela(self, janela, largura, altura):
        janela.update_idletasks()

        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()

        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2

        janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # -------------------------- ARQUIVOS JSON --------------------------

    def criar_pastas(self):
        # Cria a pasta de dados caso ela ainda não exista.
        os.makedirs(PASTA_DADOS, exist_ok=True)

        # Também cria os arquivos vazios na primeira execução.
        for arquivo in [ARQUIVO_PRODUTOS, ARQUIVO_MOVIMENTACOES]:
            if not os.path.exists(arquivo):
                try:
                    with open(arquivo, "w", encoding="utf-8") as f:
                        json.dump([], f, ensure_ascii=False, indent=4)
                except OSError as erro:
                    messagebox.showerror(
                        "Erro",
                        f"Não foi possível criar o arquivo:\n{erro}"
                    )

    def carregar_arquivo(self, caminho):
        # Lê o conteúdo do JSON e retorna uma lista com os registros.
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)

            if isinstance(dados, list):
                return dados

            return []

        except FileNotFoundError:
            return []

        except (json.JSONDecodeError, OSError, ValueError) as erro:
            messagebox.showerror(
                "Erro ao carregar",
                f"Não foi possível carregar os dados:\n{erro}"
            )
            return []

    def salvar_arquivo(self, caminho, dados):
        # Primeiro salva em um arquivo temporário para evitar perder
        # os dados caso aconteça algum problema durante a gravação.
        temporario = caminho + ".tmp"

        try:
            with open(temporario, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)

            # Depois substitui o arquivo antigo pelo arquivo atualizado.
            os.replace(temporario, caminho)
            return True

        except (OSError, TypeError, ValueError) as erro:
            messagebox.showerror(
                "Erro ao salvar",
                f"Não foi possível salvar os dados:\n{erro}"
            )

            if os.path.exists(temporario):
                try:
                    os.remove(temporario)
                except OSError:
                    pass

            return False

    def carregar_dados(self):
        self.produtos = self.carregar_arquivo(ARQUIVO_PRODUTOS)
        self.movimentacoes = self.carregar_arquivo(
            ARQUIVO_MOVIMENTACOES
        )

        # Confere se os registros possuem os campos necessários.
        # Assim, dados incompletos não causam erros nas outras telas.
        campos_produto = {
            "codigo", "nome", "quantidade",
            "estoque_minimo", "preco"
        }

        self.produtos = [
            produto for produto in self.produtos
            if isinstance(produto, dict)
            and campos_produto.issubset(produto.keys())
        ]

        campos_movimentacao = {
            "tipo", "codigo", "produto",
            "quantidade", "data", "hora"
        }

        self.movimentacoes = [
            movimento for movimento in self.movimentacoes
            if isinstance(movimento, dict)
            and campos_movimentacao.issubset(movimento.keys())
        ]

    def salvar_produtos(self):
        return self.salvar_arquivo(
            ARQUIVO_PRODUTOS,
            self.produtos
        )

    def salvar_movimentacoes(self):
        return self.salvar_arquivo(
            ARQUIVO_MOVIMENTACOES,
            self.movimentacoes
        )

    # -------------------------- ESTILO --------------------------

    def configurar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Personaliza a tabela para combinar com as outras telas.
        estilo.configure(
            "Treeview",
            background=CARD,
            foreground=TEXTO,
            fieldbackground=CARD,
            rowheight=29,
            font=("Arial", 9)
        )

        estilo.configure(
            "Treeview.Heading",
            background=ROSA_CLARO,
            foreground=TEXTO,
            font=("Arial", 9, "bold"),
            relief="flat"
        )

        estilo.map(
            "Treeview",
            background=[("selected", LAVANDA)],
            foreground=[("selected", BRANCO)]
        )

        estilo.configure(
            "Vertical.TScrollbar",
            background=ROSA_CLARO,
            troughcolor=FUNDO,
            arrowcolor=TEXTO
        )

        estilo.configure(
            "Horizontal.TScrollbar",
            background=ROSA_CLARO,
            troughcolor=FUNDO,
            arrowcolor=TEXTO
        )

    # -------------------------- INTERFACE PRINCIPAL --------------------------

    def criar_interface(self):
        self.container = tk.Frame(self.janela, bg=FUNDO)
        self.container.pack(fill="both", expand=True)

        # Menu lateral com largura fixa para não ocupar muito espaço.
        self.menu_lateral = tk.Frame(
            self.container,
            bg=CARD,
            width=155
        )
        self.menu_lateral.pack(side="left", fill="y")
        self.menu_lateral.pack_propagate(False)

        tk.Label(
            self.menu_lateral,
            text="AndriStock",
            font=("Arial", 17, "bold"),
            bg=CARD,
            fg=ROSA_ESCURO
        ).pack(pady=(22, 3))

        tk.Label(
            self.menu_lateral,
            text="CONTROLE DE ESTOQUE",
            font=("Arial", 7, "bold"),
            bg=CARD,
            fg=CINZA
        ).pack(pady=(0, 25))

        # Cada botão abre uma parte diferente do sistema.
        self.botoes_menu = {}

        opcoes = [
            ("Produtos", self.mostrar_produtos),
            ("Movimentações", self.mostrar_movimentacoes),
            ("Estoque baixo", self.mostrar_estoque_baixo),
            ("Relatórios", self.mostrar_relatorios)
        ]

        for nome, comando in opcoes:
            botao = tk.Button(
                self.menu_lateral,
                text=nome,
                command=comando,
                font=("Arial", 9),
                bg=CARD,
                fg=TEXTO,
                activebackground=ROSA_CLARO,
                activeforeground=TEXTO,
                relief="flat",
                anchor="w",
                padx=18,
                pady=11,
                cursor="hand2"
            )
            botao.pack(fill="x", padx=8, pady=2)

            self.botoes_menu[nome] = botao

        # Informação sobre onde os dados ficam armazenados.
        tk.Label(
            self.menu_lateral,
            text="Dados salvos localmente\nem arquivos JSON",
            font=("Arial", 8),
            bg=CARD,
            fg=CINZA,
            justify="left"
        ).pack(side="bottom", pady=18)

        # Área onde o conteúdo das páginas será exibido.
        self.area_principal = tk.Frame(
            self.container,
            bg=FUNDO
        )
        self.area_principal.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20,
            pady=18
        )

    def atualizar_menu(self, pagina):
        self.pagina_atual = pagina

        # Destaca o botão da página que está aberta no momento.
        for nome, botao in self.botoes_menu.items():
            if nome == pagina:
                botao.configure(
                    bg=ROSA_CLARO,
                    fg=TEXTO,
                    font=("Arial", 9, "bold")
                )
            else:
                botao.configure(
                    bg=CARD,
                    fg=TEXTO,
                    font=("Arial", 9)
                )

    def limpar_area(self):
        # Remove os widgets da página anterior antes de abrir outra.
        for widget in self.area_principal.winfo_children():
            widget.destroy()

    def criar_cabecalho(self, titulo, descricao):
        tk.Label(
            self.area_principal,
            text=titulo,
            font=("Arial", 19, "bold"),
            bg=FUNDO,
            fg=TEXTO
        ).pack(anchor="w")

        tk.Label(
            self.area_principal,
            text=descricao,
            font=("Arial", 9),
            bg=FUNDO,
            fg=CINZA
        ).pack(anchor="w", pady=(3, 16))

    def criar_area_tabela(self, parent, colunas, larguras=None):
        quadro = tk.Frame(parent, bg=CARD)
        quadro.pack(fill="both", expand=True)

        tabela = ttk.Treeview(
            quadro,
            columns=colunas,
            show="headings"
        )

        # Define os nomes e as larguras das colunas.
        for indice, coluna in enumerate(colunas):
            tabela.heading(coluna, text=coluna)

            largura = 120
            if larguras and indice < len(larguras):
                largura = larguras[indice]

            tabela.column(
                coluna,
                width=largura,
                minwidth=70,
                anchor="center"
            )

        barra_vertical = ttk.Scrollbar(
            quadro,
            orient="vertical",
            command=tabela.yview
        )

        barra_horizontal = ttk.Scrollbar(
            quadro,
            orient="horizontal",
            command=tabela.xview
        )

        tabela.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        tabela.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")

        quadro.grid_rowconfigure(0, weight=1)
        quadro.grid_columnconfigure(0, weight=1)

        return tabela

    def criar_botao(self, parent, texto, comando, cor=ROSA):
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            font=("Arial", 9, "bold"),
            bg=cor,
            fg=TEXTO,
            activebackground=ROSA_ESCURO,
            activeforeground=BRANCO,
            relief="flat",
            padx=13,
            pady=8,
            cursor="hand2"
        )

    # -------------------------- PRODUTOS --------------------------

    def mostrar_produtos(self):
        self.limpar_area()
        self.atualizar_menu("Produtos")

        self.criar_cabecalho(
            "Produtos",
            "Consulte, cadastre e organize os produtos do estoque."
        )

        # Barra de pesquisa e botões de ação.
        barra = tk.Frame(self.area_principal, bg=FUNDO)
        barra.pack(fill="x", pady=(0, 12))

        self.campo_pesquisa = tk.Entry(
            barra,
            font=("Arial", 9),
            bg=BRANCO,
            fg=TEXTO,
            relief="flat"
        )
        self.campo_pesquisa.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8,
            padx=(0, 6)
        )

        self.campo_pesquisa.insert(0, self.pesquisa_atual)

        self.criar_botao(
            barra,
            "Pesquisar",
            self.pesquisar_produtos,
            LAVANDA
        ).pack(side="left", padx=3)

        self.criar_botao(
            barra,
            "Limpar",
            self.limpar_pesquisa,
            CAMPO
        ).pack(side="left", padx=3)

        self.criar_botao(
            barra,
            "+ Novo produto",
            self.formulario_produto,
            ROSA
        ).pack(side="right", padx=(8, 0))

        # Tabela principal com os dados cadastrados.
        colunas = (
            "Código",
            "Nome",
            "Quantidade",
            "Estoque mínimo",
            "Preço"
        )

        self.tabela_produtos = self.criar_area_tabela(
            self.area_principal,
            colunas,
            [80, 190, 100, 120, 100]
        )

        self.atualizar_tabela_produtos()

        # Os botões ficam separados da tabela para deixar a tela mais limpa.
        acoes = tk.Frame(self.area_principal, bg=FUNDO)
        acoes.pack(fill="x", pady=12)

        self.criar_botao(
            acoes,
            "Editar selecionado",
            self.editar_produto,
            LAVANDA
        ).pack(side="left", padx=(0, 6))

        self.criar_botao(
            acoes,
            "Excluir selecionado",
            self.excluir_produto,
            ROSA_CLARO
        ).pack(side="left")

    def atualizar_tabela_produtos(self, lista=None):
        # Limpa os registros antigos antes de preencher a tabela novamente.
        for item in self.tabela_produtos.get_children():
            self.tabela_produtos.delete(item)

        if lista is None:
            lista = self.produtos

        for produto in lista:
            self.tabela_produtos.insert(
                "",
                "end",
                values=(
                    produto["codigo"],
                    produto["nome"],
                    produto["quantidade"],
                    produto["estoque_minimo"],
                    f'R$ {produto["preco"]:.2f}'
                )
            )

    def pesquisar_produtos(self):
        termo = self.campo_pesquisa.get().strip().lower()
        self.pesquisa_atual = termo

        # A pesquisa procura tanto pelo código quanto pelo nome.
        # O uso de lower() permite pesquisar sem diferenciar maiúsculas.
        resultado = [
            produto for produto in self.produtos
            if termo in str(produto["codigo"]).lower()
            or termo in produto["nome"].lower()
        ]

        self.atualizar_tabela_produtos(resultado)

    def limpar_pesquisa(self):
        self.campo_pesquisa.delete(0, "end")
        self.pesquisa_atual = ""
        self.atualizar_tabela_produtos()

    def obter_produto_selecionado(self):
        selecionado = self.tabela_produtos.selection()

        if not selecionado:
            messagebox.showwarning(
                "Atenção",
                "Selecione um produto na tabela."
            )
            return None

        valores = self.tabela_produtos.item(
            selecionado[0],
            "values"
        )

        codigo = str(valores[0])

        # Busca na lista original o produto que possui esse código.
        for produto in self.produtos:
            if str(produto["codigo"]) == codigo:
                return produto

        return None

    # -------------------------- CADASTRO E EDIÇÃO --------------------------

    def formulario_produto(self, produto=None):
        # Quando recebe um produto, o formulário é aberto para edição.
        editando = produto is not None

        janela = tk.Toplevel(self.janela)
        janela.title("Editar produto" if editando else "Novo produto")
        janela.configure(bg=FUNDO)
        janela.resizable(False, False)

        self.centralizar_janela(janela, 370, 430)

        titulo = "Editar produto" if editando else "Cadastrar produto"

        tk.Label(
            janela,
            text=titulo,
            font=("Arial", 16, "bold"),
            bg=FUNDO,
            fg=TEXTO
        ).pack(anchor="w", padx=22, pady=(20, 15))

        campos = {}

        campos_info = [
            ("codigo", "Código"),
            ("nome", "Nome do produto"),
            ("quantidade", "Quantidade"),
            ("estoque_minimo", "Estoque mínimo"),
            ("preco", "Preço (R$)")
        ]

        for chave, rotulo in campos_info:
            tk.Label(
                janela,
                text=rotulo,
                font=("Arial", 9, "bold"),
                bg=FUNDO,
                fg=TEXTO
            ).pack(anchor="w", padx=22)

            entrada = tk.Entry(
                janela,
                font=("Arial", 10),
                bg=BRANCO,
                fg=TEXTO,
                relief="flat"
            )
            entrada.pack(
                fill="x",
                padx=22,
                pady=(4, 12),
                ipady=6
            )

            campos[chave] = entrada

            # Se estiver editando, preenche os campos com os dados atuais.
            if editando:
                entrada.insert(0, str(produto[chave]))

                # O código não pode ser alterado durante a edição.
                if chave == "codigo":
                    entrada.configure(state="disabled")

        def salvar():
            try:
                # Primeiro, pega os valores digitados e converte
                # cada um para o tipo de dado necessário.
                if editando:
                    codigo = int(produto["codigo"])
                else:
                    codigo = int(campos["codigo"].get().strip())

                nome = campos["nome"].get().strip()
                quantidade = int(campos["quantidade"].get().strip())
                estoque_minimo = int(
                    campos["estoque_minimo"].get().strip()
                )
                preco = float(
                    campos["preco"].get().strip().replace(",", ".")
                )

            except ValueError:
                messagebox.showerror(
                    "Dados inválidos",
                    "Confira os campos numéricos e tente novamente.",
                    parent=janela
                )
                return

            # Verifica se os dados estão corretos antes de continuar.
            # Isso evita cadastrar produtos com informações inválidas.
            if codigo <= 0:
                messagebox.showwarning(
                    "Atenção",
                    "O código deve ser maior que zero.",
                    parent=janela
                )
                return

            if not nome:
                messagebox.showwarning(
                    "Atenção",
                    "Informe o nome do produto.",
                    parent=janela
                )
                return

            if quantidade < 0 or estoque_minimo < 0:
                messagebox.showwarning(
                    "Atenção",
                    "As quantidades não podem ser negativas.",
                    parent=janela
                )
                return

            if preco <= 0:
                messagebox.showwarning(
                    "Atenção",
                    "O preço deve ser maior que zero.",
                    parent=janela
                )
                return

            # Confere se o código já está sendo utilizado por outro produto.
            codigo_existe = any(
                int(item["codigo"]) == codigo
                for item in self.produtos
                if not editando or item is not produto
            )

            if codigo_existe:
                messagebox.showwarning(
                    "Código existente",
                    "Já existe um produto com esse código.",
                    parent=janela
                )
                return

            novo_produto = {
                "codigo": codigo,
                "nome": nome,
                "quantidade": quantidade,
                "estoque_minimo": estoque_minimo,
                "preco": preco
            }

            # Guarda uma cópia da lista para recuperar os dados
            # caso aconteça algum problema ao salvar o arquivo.
            produtos_anteriores = [item.copy() for item in self.produtos]

            if editando:
                indice = self.produtos.index(produto)
                self.produtos[indice] = novo_produto
            else:
                self.produtos.append(novo_produto)

            if self.salvar_produtos():
                messagebox.showinfo(
                    "Sucesso",
                    "Produto salvo com sucesso!",
                    parent=janela
                )
                janela.destroy()
                self.mostrar_produtos()
            else:
                # Se o salvamento falhar, volta para a lista anterior.
                self.produtos = produtos_anteriores

        self.criar_botao(
            janela,
            "Salvar produto",
            salvar,
            ROSA
        ).pack(fill="x", padx=22, pady=(5, 18))

    def editar_produto(self):
        produto = self.obter_produto_selecionado()

        if produto:
            self.formulario_produto(produto)

    def excluir_produto(self):
        produto = self.obter_produto_selecionado()

        if not produto:
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja excluir o produto '{produto['nome']}'?"
        )

        if not confirmar:
            return

        # Guarda a lista antes da exclusão para conseguir recuperar
        # o produto caso não seja possível atualizar o arquivo JSON.
        produtos_anteriores = [item.copy() for item in self.produtos]

        self.produtos.remove(produto)

        if self.salvar_produtos():
            messagebox.showinfo(
                "Sucesso",
                "Produto excluído com sucesso!"
            )
            self.mostrar_produtos()
        else:
            self.produtos = produtos_anteriores

    # -------------------------- MOVIMENTAÇÕES --------------------------

    def mostrar_movimentacoes(self):
        self.limpar_area()
        self.atualizar_menu("Movimentações")

        self.criar_cabecalho(
            "Movimentações",
            "Acompanhe as entradas e saídas de produtos."
        )

        barra = tk.Frame(self.area_principal, bg=FUNDO)
        barra.pack(fill="x", pady=(0, 12))

        self.criar_botao(
            barra,
            "+ Nova movimentação",
            self.formulario_movimentacao,
            ROSA
        ).pack(side="right")

        colunas = (
            "Tipo",
            "Código",
            "Produto",
            "Quantidade",
            "Data",
            "Hora"
        )

        self.tabela_movimentacoes = self.criar_area_tabela(
            self.area_principal,
            colunas,
            [90, 75, 150, 90, 100, 85]
        )

        self.atualizar_tabela_movimentacoes()

    def atualizar_tabela_movimentacoes(self):
        for item in self.tabela_movimentacoes.get_children():
            self.tabela_movimentacoes.delete(item)

        # Inverte a lista para mostrar as movimentações mais recentes primeiro.
        for movimento in reversed(self.movimentacoes):
            self.tabela_movimentacoes.insert(
                "",
                "end",
                values=(
                    movimento["tipo"],
                    movimento["codigo"],
                    movimento["produto"],
                    movimento["quantidade"],
                    movimento["data"],
                    movimento["hora"]
                )
            )

    def formulario_movimentacao(self):
        if not self.produtos:
            messagebox.showwarning(
                "Atenção",
                "Cadastre pelo menos um produto antes de registrar uma movimentação."
            )
            return

        janela = tk.Toplevel(self.janela)
        janela.title("Nova movimentação")
        janela.configure(bg=FUNDO)
        janela.resizable(False, False)

        self.centralizar_janela(janela, 370, 330)

        tk.Label(
            janela,
            text="Nova movimentação",
            font=("Arial", 16, "bold"),
            bg=FUNDO,
            fg=TEXTO
        ).pack(anchor="w", padx=22, pady=(20, 15))

        tk.Label(
            janela,
            text="Tipo de movimentação",
            font=("Arial", 9, "bold"),
            bg=FUNDO,
            fg=TEXTO
        ).pack(anchor="w", padx=22)

        tipo = ttk.Combobox(
            janela,
            values=["Entrada", "Saída"],
            state="readonly",
            font=("Arial", 10)
        )
        tipo.pack(fill="x", padx=22, pady=(4, 12))
        tipo.set("Entrada")

        tk.Label(
            janela,
            text="Produto",
            font=("Arial", 9, "bold"),
            bg=FUNDO,
            fg=TEXTO
        ).pack(anchor="w", padx=22)

        # Mostra o código e o nome para facilitar a escolha do produto.
        opcoes_produtos = [
            f'{produto["codigo"]} - {produto["nome"]}'
            for produto in self.produtos
        ]

        escolha_produto = ttk.Combobox(
            janela,
            values=opcoes_produtos,
            state="readonly",
            font=("Arial", 10)
        )
        escolha_produto.pack(fill="x", padx=22, pady=(4, 12))

        tk.Label(
            janela,
            text="Quantidade",
            font=("Arial", 9, "bold"),
            bg=FUNDO,
            fg=TEXTO
        ).pack(anchor="w", padx=22)

        campo_quantidade = tk.Entry(
            janela,
            font=("Arial", 10),
            bg=BRANCO,
            fg=TEXTO,
            relief="flat"
        )
        campo_quantidade.pack(
            fill="x",
            padx=22,
            pady=(4, 12),
            ipady=6
        )

        def registrar():
            try:
                quantidade = int(campo_quantidade.get().strip())
            except ValueError:
                messagebox.showerror(
                    "Quantidade inválida",
                    "Informe uma quantidade inteira.",
                    parent=janela
                )
                return

            if quantidade <= 0:
                messagebox.showwarning(
                    "Atenção",
                    "A quantidade deve ser maior que zero.",
                    parent=janela
                )
                return

            if not escolha_produto.get():
                messagebox.showwarning(
                    "Atenção",
                    "Selecione um produto.",
                    parent=janela
                )
                return

            indice = opcoes_produtos.index(escolha_produto.get())
            produto = self.produtos[indice]

            quantidade_anterior = produto["quantidade"]

            # Na saída, não permite retirar mais unidades do que existem.
            if tipo.get() == "Saída":
                if quantidade > produto["quantidade"]:
                    messagebox.showwarning(
                        "Estoque insuficiente",
                        "Não há quantidade suficiente para essa saída.",
                        parent=janela
                    )
                    return

                produto["quantidade"] -= quantidade

            else:
                produto["quantidade"] += quantidade

            agora = datetime.now()

            # Registra as informações da movimentação para manter o histórico.
            nova_movimentacao = {
                "tipo": tipo.get(),
                "codigo": produto["codigo"],
                "produto": produto["nome"],
                "quantidade": quantidade,
                "data": agora.strftime("%d/%m/%Y"),
                "hora": agora.strftime("%H:%M:%S")
            }

            self.movimentacoes.append(nova_movimentacao)

            # Os dois arquivos precisam ser atualizados: o estoque atual
            # e o histórico de movimentações.
            produtos_salvos = self.salvar_produtos()

            if produtos_salvos:
                movimentacoes_salvas = self.salvar_movimentacoes()
            else:
                movimentacoes_salvas = False

            if produtos_salvos and movimentacoes_salvas:
                messagebox.showinfo(
                    "Sucesso",
                    "Movimentação registrada com sucesso!",
                    parent=janela
                )
                janela.destroy()
                self.mostrar_movimentacoes()

            else:
                # Se algum arquivo não for salvo, desfaz a alteração
                # para não deixar o estoque e o histórico diferentes.
                produto["quantidade"] = quantidade_anterior

                if self.movimentacoes:
                    self.movimentacoes.pop()

                self.salvar_produtos()
                self.salvar_movimentacoes()

        self.criar_botao(
            janela,
            "Registrar movimentação",
            registrar,
            ROSA
        ).pack(fill="x", padx=22, pady=(5, 18))

    # -------------------------- ESTOQUE BAIXO --------------------------

    def mostrar_estoque_baixo(self):
        self.limpar_area()
        self.atualizar_menu("Estoque baixo")

        self.criar_cabecalho(
            "Estoque baixo",
            "Produtos que precisam de reposição."
        )

        # Compara a quantidade atual com o limite mínimo de cada produto.
        produtos_baixos = [
            produto for produto in self.produtos
            if produto["quantidade"] <= produto["estoque_minimo"]
        ]

        if not produtos_baixos:
            tk.Label(
                self.area_principal,
                text="Nenhum produto com estoque baixo.",
                font=("Arial", 12),
                bg=FUNDO,
                fg=CINZA
            ).pack(anchor="center", pady=60)
            return

        colunas = (
            "Código",
            "Nome",
            "Quantidade",
            "Estoque mínimo",
            "Preço"
        )

        self.tabela_estoque_baixo = self.criar_area_tabela(
            self.area_principal,
            colunas,
            [80, 190, 100, 120, 100]
        )

        for produto in produtos_baixos:
            self.tabela_estoque_baixo.insert(
                "",
                "end",
                values=(
                    produto["codigo"],
                    produto["nome"],
                    produto["quantidade"],
                    produto["estoque_minimo"],
                    f'R$ {produto["preco"]:.2f}'
                )
            )

    # -------------------------- RELATÓRIOS --------------------------

    def mostrar_relatorios(self):
        self.limpar_area()
        self.atualizar_menu("Relatórios")

        self.criar_cabecalho(
            "Relatórios",
            "Resumo das informações do estoque."
        )

        # Calcula algumas informações gerais para mostrar no relatório.
        total_produtos = len(self.produtos)

        # Soma a quantidade de unidades de todos os produtos cadastrados.
        total_unidades = sum(
            produto["quantidade"] for produto in self.produtos
        )

        # Calcula o valor estimado de todos os produtos em estoque.
        valor_total = sum(
            produto["quantidade"] * produto["preco"]
            for produto in self.produtos
        )

        # Conta quantos produtos estão no limite mínimo ou abaixo dele.
        total_baixo = sum(
            1 for produto in self.produtos
            if produto["quantidade"] <= produto["estoque_minimo"]
        )

        # Soma separadamente as quantidades de entradas e saídas.
        total_entradas = sum(
            movimento["quantidade"]
            for movimento in self.movimentacoes
            if movimento["tipo"] == "Entrada"
        )

        total_saidas = sum(
            movimento["quantidade"]
            for movimento in self.movimentacoes
            if movimento["tipo"] == "Saída"
        )

        # Organiza os indicadores em cartões para facilitar a leitura.
        indicadores = [
            ("Produtos cadastrados", total_produtos, ROSA_CLARO),
            ("Unidades em estoque", total_unidades, LAVANDA),
            ("Produtos com estoque baixo", total_baixo, AZUL),
            ("Valor estimado do estoque", f"R$ {valor_total:.2f}", ROSA)
        ]

        quadro_indicadores = tk.Frame(
            self.area_principal,
            bg=FUNDO
        )
        quadro_indicadores.pack(fill="x", pady=(0, 15))

        for indice, (titulo, valor, cor) in enumerate(indicadores):
            linha = indice // 2
            coluna = indice % 2

            cartao = tk.Frame(
                quadro_indicadores,
                bg=CARD,
                padx=15,
                pady=13
            )
            cartao.grid(
                row=linha,
                column=coluna,
                sticky="nsew",
                padx=5,
                pady=5
            )

            tk.Label(
                cartao,
                text=titulo,
                font=("Arial", 9),
                bg=CARD,
                fg=CINZA
            ).pack(anchor="w")

            tk.Label(
                cartao,
                text=str(valor),
                font=("Arial", 17, "bold"),
                bg=CARD,
                fg=TEXTO
            ).pack(anchor="w", pady=(5, 0))

            # Uma pequena faixa colorida ajuda a diferenciar os indicadores.
            tk.Frame(
                cartao,
                bg=cor,
                height=4
            ).pack(fill="x", pady=(10, 0))

        quadro_indicadores.grid_columnconfigure(0, weight=1)
        quadro_indicadores.grid_columnconfigure(1, weight=1)

        # Mostra também os totais de movimentações registrados.
        quadro_movimentacoes = tk.Frame(
            self.area_principal,
            bg=CARD,
            padx=18,
            pady=15
        )
        quadro_movimentacoes.pack(fill="x", padx=5, pady=5)

        tk.Label(
            quadro_movimentacoes,
            text="Resumo das movimentações",
            font=("Arial", 11, "bold"),
            bg=CARD,
            fg=TEXTO
        ).pack(anchor="w", pady=(0, 12))

        tk.Label(
            quadro_movimentacoes,
            text=f"Total de unidades que entraram: {total_entradas}",
            font=("Arial", 10),
            bg=CARD,
            fg=TEXTO
        ).pack(anchor="w", pady=3)

        tk.Label(
            quadro_movimentacoes,
            text=f"Total de unidades que saíram: {total_saidas}",
            font=("Arial", 10),
            bg=CARD,
            fg=TEXTO
        ).pack(anchor="w", pady=3)

        tk.Label(
            quadro_movimentacoes,
            text=f"Valor estimado do estoque: R$ {valor_total:.2f}",
            font=("Arial", 10, "bold"),
            bg=CARD,
            fg=ROSA_ESCURO
        ).pack(anchor="w", pady=(8, 3))


# -------------------------- INÍCIO DO PROGRAMA --------------------------

if __name__ == "__main__":
    # Cria a janela principal e inicia o sistema.
    janela = tk.Tk()
    sistema = AndriStock(janela)
    janela.mainloop()
