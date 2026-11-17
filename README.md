# AndriStock — Sistema de Controle de Estoque

## 1. Sobre o projeto

O **AndriStock** é um sistema de controle de estoque desenvolvido em Python, utilizando a biblioteca Tkinter para a criação da interface gráfica e arquivos JSON para o armazenamento dos dados.

O sistema foi desenvolvido com o objetivo de facilitar o gerenciamento de produtos, permitindo registrar entradas e saídas, acompanhar quantidades disponíveis e identificar produtos com estoque baixo.

A interface possui um menu lateral e um design compacto e minimalista, buscando oferecer uma utilização simples e organizada, inclusive em notebooks com telas menores.

## 2. Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento do sistema.
- **Tkinter:** biblioteca utilizada para construir a interface gráfica.
- **JSON:** formato utilizado para armazenar os dados dos produtos e das movimentações.
- **DateTime:** utilizado para registrar as datas e os horários das movimentações.

## 3. Funcionalidades

O AndriStock possui as seguintes funcionalidades:

### Gerenciamento de produtos
- Cadastrar novos produtos.
- Editar informações dos produtos.
- Excluir produtos cadastrados.
- Listar todos os produtos.
- Pesquisar produtos pelo código ou nome.

### Controle de movimentações
- Registrar entradas de produtos no estoque.
- Registrar saídas de produtos.
- Atualizar automaticamente as quantidades disponíveis.
- Registrar a data e o horário de cada movimentação.
- Impedir saídas com quantidade superior ao estoque disponível.

### Controle de estoque
- Consultar os produtos cadastrados.
- Identificar produtos com estoque baixo.
- Comparar a quantidade disponível com o estoque mínimo definido para cada produto.

### Relatórios
- Consultar informações gerais do estoque.
- Visualizar dados sobre produtos e movimentações.

## 4. Armazenamento dos dados

O sistema utiliza arquivos JSON para salvar as informações, sem a necessidade de um banco de dados.

Os dados são armazenados localmente, permitindo que os registros permaneçam disponíveis mesmo após o fechamento do programa.

São utilizados dois arquivos principais:

- `produtos.json`: armazena os dados dos produtos cadastrados.
- `movimentacoes.json`: armazena o histórico de entradas e saídas.

## 5. Estrutura do projeto

```text
AndriStock/
│
├── Dados/
│   ├── produtos.json
│   └── movimentacoes.json
│
├── main.py
│
└── README.md
```

## 6. Como executar o projeto

Para executar o AndriStock, é necessário ter o Python instalado no computador.

**Passo 1:** Baixe ou clone o repositório.

**Passo 2:** Abra a pasta do projeto no Visual Studio Code ou em outro editor de código.

**Passo 3:** Abra o terminal na pasta do projeto.

**Passo 4:** Execute o comando:

```bash
python main.py
```

O sistema será iniciado e a janela principal ficará disponível para utilização.

## 7. Validações do sistema

Para evitar erros durante a utilização, o
 AndriStock possui algumas validações:

- Não permite cadastrar produtos com códigos repetidos.
- Exige o preenchimento do nome do produto.
- Não permite quantidades negativas.
- Exige que o preço unitário seja maior que zero.
- Não permite retirar uma quantidade maior do que a disponível no estoque.
- Trata situações como arquivos inexistentes ou problemas na leitura dos dados.

## 8. Objetivo educacional

O desenvolvimento deste projeto possibilitou aplicar conhecimentos de lógica de programação, estruturas condicionais, funções, orientação a objetos, manipulação de arquivos, tratamento de exceções e desenvolvimento de interfaces gráficas.

Além disso, permitiu compreender a importância de um sistema de controle de estoque para a organização de produtos e o acompanhamento das movimentações de uma empresa.

---

**Projeto:** AndriStock — Sistema de Controle de Estoque  
**Linguagem:** Python  
**Interface gráfica:** Tkinter  
**Armazenamento:** JSON