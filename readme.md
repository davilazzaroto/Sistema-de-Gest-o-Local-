# Sistema de Gestão de Estoque — Prática em Python

Este projeto foi desenvolvido com fins de prática e estudos em Python. A ideia é aplicar conceitos fundamentais da linguagem em um sistema simples de gestão de estoque executado pelo terminal.

O projeto não pretende ser uma aplicação comercial ou um sistema pronto para produção. Ele serve como exercício para experimentar organização de código, entrada de dados, persistência local e criação de relatórios.

## Objetivos de estudo

Durante o desenvolvimento, são praticados:

- criação e utilização de funções;
- listas e dicionários para representar dados;
- estruturas condicionais, laços de repetição e `match/case`;
- validação e conversão de entradas do usuário;
- leitura e gravação de arquivos JSON;
- manipulação de arquivos TXT;
- organização de um projeto em diferentes módulos;
- uso de datas com `datetime`;
- instalação e utilização de uma biblioteca externa (`Rich`);
- construção de tabelas e relatórios no terminal.

## Recursos

- Cadastro e alteração de produtos com nome, categoria, preço e estoque.
- Busca por ID, nome ou categoria.
- Registro de entradas e saídas com data, quantidade e observação.
- Validação de números negativos e prevenção de saídas maiores que o estoque.
- Relatórios de produtos, movimentações e indicadores gerenciais.
- Exportação dos relatórios para arquivos TXT.
- Interface aprimorada com a biblioteca [Rich](https://rich.readthedocs.io/), usando tabelas, painéis e cores.

## Requisitos para estudar e executar

- Python 3.10 ou superior, necessário para a estrutura `match/case`.
- Conhecimentos básicos de lógica de programação são recomendados, mas não obrigatórios.
- A biblioteca utilizada está listada em `../requirements.txt`.

## Instalação

Para praticar de forma organizada, recomenda-se criar um ambiente virtual na pasta raiz e instalar a dependência do projeto:

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

No Linux/macOS:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Como executar para estudar

Na raiz do projeto:

```bash
python workPython/main.py
```

Ou dentro da pasta `workPython`:

```bash
cd workPython
python main.py
```

O programa sempre usa os arquivos JSON de `workPython`, independentemente da pasta de onde for iniciado. Escolha a opção `0` para salvar e sair.

Ao estudar o código, uma boa sequência é começar por `main.py`, acompanhar as funções chamadas no menu e depois observar como `storage.py` salva e carrega os dados.

## Estrutura

| Arquivo                | Responsabilidade                                       |
| ---------------------- | ------------------------------------------------------ |
| `main.py`              | Menu interativo e fluxo principal.                     |
| `functions.py`         | Regras de negócio, buscas, movimentações e relatórios. |
| `storage.py`           | Leitura e gravação dos JSONs.                          |
| `products.json`        | Produtos persistidos localmente.                       |
| `stock_movements.json` | Histórico de movimentações.                            |
| `*.txt`                | Relatórios exportados sob demanda.                     |

## Fluxo básico de uso

1. Escolha `1` para cadastrar um produto.
2. Use `6` para entrada ou `7` para saída de estoque.
3. Consulte o inventário com `5`.
4. Acompanhe movimentações com `8`.
5. Visualize indicadores com `9`.
6. Escolha `0` para salvar e encerrar.

## Ideias para praticar

Algumas sugestões de exercícios para evoluir o projeto:

1. Adicionar uma opção para excluir produtos.
2. Melhorar a validação para não aceitar quantidades iguais a zero.
3. Separar os relatórios em funções menores.
4. Criar testes automatizados com `unittest` ou `pytest`.
5. Tratar erros de arquivos JSON vazios ou inválidos.
6. Adicionar filtros por período no relatório de movimentações.
7. Criar uma funcionalidade para localizar produtos com estoque baixo.
8. Melhorar o sistema de identificação dos produtos.

## Casos de teste manuais

- **Validação:** preços e quantidades negativas são rejeitados.
- **Busca:** `teclado`, `Teclado` e `TECLADO` encontram o mesmo produto.
- **Controle de saída:** uma saída maior que o estoque disponível é bloqueada.
- **Relatórios:** as opções `5`, `8` e `9` exibem tabelas/painéis no terminal e permitem exportação para TXT sem códigos de cor.

## Observações

Este é um projeto educacional e local. Os arquivos JSON funcionam como armazenamento apenas para facilitar os estudos, sem banco de dados externo. Faça cópias dos arquivos antes de testes que possam alterar os dados.
