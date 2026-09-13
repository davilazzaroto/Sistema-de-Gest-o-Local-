# English - Package that extract time...
# Português - Pacote para extrair tempo...
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
PROJECT_DIR = Path(__file__).resolve().parent


def show_product_table(products, title="Produtos"):
    table = Table(title=title, header_style="bold cyan", border_style="blue")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Nome", style="bold white")
    table.add_column("Categoria", style="magenta")
    table.add_column("Preço", justify="right", style="green")
    table.add_column("Estoque", justify="right", style="yellow")
    for product in products:
        table.add_row(
            str(product["id"]),
            product["name"],
            product["category"],
            f"R$ {product['price']:.2f}",
            str(product["stock"]),
        )
    console.print(table)


def show_message(message, style="white", title=None):
    console.print(Panel(message, title=title, border_style=style))


# English - Function to create the next product's ID in the list...
# Português - Função para gerar o próximo ID do produto que será colocado na lista...
def next_id(products):
    if not products:
        return 1
    return max(product["id"] for product in products) + 1


# English - Function to search the product by ID in the list...
# Português - Função para estar procurando um produto pelo ID em nossa lista...
def find_product_by_id(products, product_id):
    for p in products:
        if str(p["id"]) == str(product_id):
            return p
    return None


# English - Function that show all the products that are registered in the system...
# Português - Função para estar mostrando todos os produtos cadastrados no sistema...
def list_products(products):
    if not products:
        show_message(
            "Não há produtos cadastrados no sistema no momento.", "yellow", "Atenção"
        )
        return
    show_product_table(products, "Inventário de Produtos")
    print("Deseja Exportar o Relatório de Produtos Para um Arquivo TXT?")
    choice = input(
        "Escolha a Opção '1' Para Exportar ou '2' Para Não Exportar:"
    ).strip()
    if choice == "1":
        export_TXT_PR(products, PROJECT_DIR / "product_inventory.txt")

    # English - Option to show all products in the ordered form...
    # Português - Opção para mostrar os produtos de forma ordenada...
    print("Deseja Listar Produtos Por Nome?")
    choice = input(
        "Escolha a Opção '1' Para Mostrar Produtos em Ordem ou '2' Para Não Mostrar: "
    )
    if choice == "1":
        sorted_products = sorted(products, key=lambda p: p["name"])
        show_product_table(sorted_products, "Produtos em Ordem Alfabética")


# English - Function that register the products...
# Português - Função para registrar os produtos...
def register_product(products):
    name = input("Nome do Produto: ")
    category = input("Categoria do Produto: ")
    price = read_float_validation("Preço do Produto: ")
    stock = read_int_validation("Quantidade de Estoque: ")
    product_id = next_id(products)
    new_product = {
        "id": product_id,
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
    }
    products.append(new_product)
    print(f"Produto '{name}' Cadastrado no Sistema com ID '{product_id}'.")


# English - Function that update a product's information...
# Português - Função para atualizar informações de um produto...
def update_product(products):
    product_id = read_int_validation("ID do Produto para Alteração: ")
    product = find_product_by_id(products, product_id)

    if not product:
        print("Produto Não Encontrado!")
        return
    print(
        f"Editando: {product['name']} | Categoria: {product['category']} | Preço: R${product['price']:.2f}"
    )

    new_name = input("Novo Nome ou Deixe em Branco Para Não Alterar: ").strip()
    new_category = input("Nova Categoria ou Deixe em Branco Para Não Alterar: ").strip()
    new_price_str = input("Novo Preço ou Deixe em Branco Para Não Alterar: ").strip()
    if new_name:
        product["name"] = new_name
    if new_category:
        product["category"] = new_category
    if new_price_str:
        product["price"] = float(new_price_str.replace(",", "."))
    print("Produto Atualizado com Sucesso!")


# English - Function that search products by ID...
# Português - Função para procurar produtos por ID...
def search_product_by_id(products):
    search_id = input("Digite o ID Exato do Produto: ").strip()
    product = find_product_by_id(products, search_id)

    if product:
        show_product_table([product], "Produto Encontrado")
    else:
        print("Produto Não Encontrado com Esse ID!")


# English - Function that search products by name ou category...
# Português - Função para procurar produtos por nome ou categoria...
def search_product(products):
    search_term = input("Digite o Nome ou Categoria do Produto: ").strip().lower()
    found_products = [
        p
        for p in products
        if search_term in p["name"].lower() or search_term in p["category"].lower()
    ]
    if not found_products:
        print("Nenhum Produto Encontrado!")
        return
    show_product_table(found_products, "Resultados da Busca")


# English - Function that register procucts´s entrys in the system...
# Português - Função para registrar entradas de produtos no sistemas...
def register_stock_entry(products, stock_movements):
    product_id = read_int_validation("ID do Produto Para Entrada de Estoque: ")
    product = find_product_by_id(products, product_id)
    if not product:
        print("Produto Não Encontrado!")
        return
    quantity = read_int_validation("Quantidade a Adicionar: ")
    product["stock"] += quantity
    stock_movements.append(
        {
            "id": next_id(stock_movements),
            "product_id": product_id,
            "type": "Entrada",
            "quantity": quantity,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "observation": input("Observação da Entrada (Opcional): "),
        }
    )
    print(
        f"Entrada de {quantity} Unidades Registrada Para o Produto '{product['name']}'."
    )


# English - Function that register procucts´s exits in the system...
# Português - Função para registrar saídas de produtos no sistemas...
def register_stock_exit(products, stock_movements):
    product_id = read_int_validation("ID do Produto Para Saída de Estoque: ")
    product = find_product_by_id(products, product_id)
    if not product:
        print("Produto Não Encontrado!")
        return
    quantity = read_int_validation("Quantidade a Remover: ")
    if quantity > product["stock"]:
        print("Quantidade Insuficiente no Estoque!")
        return
    product["stock"] -= quantity
    stock_movements.append(
        {
            "id": next_id(stock_movements),
            "product_id": product_id,
            "type": "Saída",
            "quantity": quantity,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "observation": input("Observação de Saída (Opcional): "),
        }
    )
    print(
        f"Saída de {quantity} Unidades Registrada Para o Produto '{product['name']}'."
    )


# English - Function that show the ocurred movimentions in the stock...
# Português - Função para mostrar a movimentação que ocorreram no estoque...
def report_stock_movements(products, stock_movements):
    if not stock_movements:
        print("Nenhuma Movimentação de Estoque Registrada!")
        return
    table = Table(
        title="Movimentações de Estoque", header_style="bold cyan", border_style="blue"
    )
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Produto", justify="right")
    table.add_column("Nome", style="bold white")
    table.add_column("Tipo")
    table.add_column("Qtd.", justify="right", style="yellow")
    table.add_column("Data", style="dim")
    table.add_column("Observação")
    for movement in stock_movements:
        product = find_product_by_id(products, movement["product_id"])
        product_name = product["name"] if product else "Desconhecido"
        observation = movement.get("observation", "").strip() or "N/A"
        movement_style = "green" if movement["type"] == "Entrada" else "red"
        table.add_row(
            str(movement["id"]),
            str(movement["product_id"]),
            product_name,
            f"[{movement_style}]{movement['type']}[/{movement_style}]",
            str(movement["quantity"]),
            movement["date"],
            observation,
        )
    console.print(table)

    total_entries = sum(
        m["quantity"] for m in stock_movements if m["type"] == "Entrada"
    )
    total_exits = sum(m["quantity"] for m in stock_movements if m["type"] == "Saída")
    console.print(f"[green]Total de entradas:[/green] {total_entries} unidades")
    console.print(f"[red]Total de saídas:[/red] {total_exits} unidades")
    print("Deseja Exportar o Relatório de Movimentações Para um Arquivo TXT?")
    choice = input(
        "Escolha a Opção '1' Para Exportar ou '2' Para Não Exportar:"
    ).strip()
    if choice == "1":
        export_TXT_SM(products, stock_movements, PROJECT_DIR / "stock_movements.txt")


# English - Function that show a complete report about the stock...
# Português - Função para mostrar um relatório completo de estoque...
def managerial_report(products, stock_movements):
    if not products:
        print("Não Há Produtos Cadastrados Para Gerar o Relatório Gerencial!")
        return
    total_products = len(products)
    total_stock = sum(p["stock"] for p in products)
    total_entries = sum(
        m["quantity"] for m in stock_movements if m["type"] == "Entrada"
    )
    total_exits = sum(m["quantity"] for m in stock_movements if m["type"] == "Saída")
    max_stock_value = max(p["stock"] for p in products)
    min_stock_value = min(p["stock"] for p in products)
    max_stock_products = [p["name"] for p in products if p["stock"] == max_stock_value]
    min_stock_products = [p["name"] for p in products if p["stock"] == min_stock_value]
    max_stock_names = ", ".join(max_stock_products)
    min_stock_names = ", ".join(min_stock_products)
    values_total = sum(p["price"] * p["stock"] for p in products)
    quantity_category_products = {}
    for p in products:
        if p["category"] not in quantity_category_products:
            quantity_category_products[p["category"]] = 0
        quantity_category_products[p["category"]] += 1
    best_price_stock = sorted(
        products, key=lambda p: p["price"] * p["stock"], reverse=True
    )[:5]

    summary = Table.grid(padding=(0, 2))
    summary.add_column(style="bold cyan")
    summary.add_column(style="white")
    summary.add_row("Produtos cadastrados", str(total_products))
    summary.add_row("Itens em estoque", str(total_stock))
    summary.add_row("Entradas registradas", str(total_entries))
    summary.add_row("Saídas registradas", str(total_exits))
    summary.add_row("Maior estoque", f"{max_stock_names} ({max_stock_value} unidades)")
    summary.add_row("Menor estoque", f"{min_stock_names} ({min_stock_value} unidades)")
    summary.add_row("Valor total do estoque", f"R$ {values_total:.2f}")
    console.print(Panel(summary, title="Relatório Gerencial", border_style="green"))
    console.print("[bold cyan]Distribuição por categorias[/bold cyan]")
    for category, count in quantity_category_products.items():
        console.print(f"  • {category}: {count} produtos")
    console.print("[bold cyan]Top 5 produtos por valor em estoque[/bold cyan]")
    for product in best_price_stock:
        console.print(
            f"  • {product['name']} (ID: {product['id']}): R$ {product['price'] * product['stock']:.2f}"
        )
    print("Deseja Exportar o Relatório Gerencial Para um Arquivo TXT?")
    choice = input(
        "Escolha a Opção '1' Para Exportar ou '2' Para Não Exportar:"
    ).strip()
    if choice == "1":
        export_TXT_MR(
            products, stock_movements, PROJECT_DIR / "management_inventory.txt"
        )


# English - Function that validate the number typd in the system (Integer)...
# Português - Função para validar o número digitado no sistema (Inteiro)...
def read_int_validation(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("O Valor Não Pode Ser Negativo! Tente Novamente...")
                continue
            return value
        except ValueError:
            print("Digite um Número Inteiro Válido...")


# English - Function that validate the number typd in the system (Float)...
# Português - Função para validar o número digitado no sistema (Decimal)...
def read_float_validation(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("O Valor Não Pode Ser Negativo! Tente Novamente...")
                continue
            return value
        except ValueError:
            print("Digite um Número Decimal Válido...")


# English - Function that export gerencial report in format TXT...
# Português - Função para exportar relatório gerencial em formato TXT...
def export_TXT_PR(products, file_path):
    with open(file_path, "w", encoding="UTF-8") as f:
        f.write("ID | NOME | CATEGORIA | PREÇO | ESTOQUE\n")
        f.write("↓ =================================== ↓\n")
        for product in products:
            f.write(
                f"{product["id"]} | {product["name"]} | {product["category"]} | R${product["price"]:.2f} | {product["stock"]}\n"
            )
    print(f"Relatório Exportado Para {file_path}!")


# English - Function that export movement report in format TXT...
# Português - Função para exportar relatório de movimentações em formato TXT...
def export_TXT_SM(products, movement, file_path):
    with open(file_path, "w", encoding="UTF-8") as f:
        f.write(
            "ID DE MOVIMENTAÇÃO | ID DO PRODUTO | NOME | TIPO | QUANTIDADE | HORÁRIO | OBSERVAÇÃO\n"
        )
        f.write(
            "↓ ================================================================================ ↓\n"
        )
        for movement in movement:
            product = find_product_by_id(products, movement["product_id"])
            product_name = product["name"] if product else "Desconhecido"
            observation = movement.get("observation", "").strip() or "N/A"
            f.write(
                f"{movement['id']} | {movement['product_id']} | {product_name} | {movement['type']} | {movement['quantity']} | {movement['date']} | {observation}\n"
            )
    print(f"Relatório Exportado Para {file_path}!")


def export_TXT_MR(products, stock_movements, file_path):
    total_products = len(products)
    total_stock = sum(p["stock"] for p in products)
    total_entries = sum(
        m["quantity"] for m in stock_movements if m["type"] == "Entrada"
    )
    total_exits = sum(m["quantity"] for m in stock_movements if m["type"] == "Saída")

    max_stock_value = max(p["stock"] for p in products)
    min_stock_value = min(p["stock"] for p in products)
    max_stock_names = ", ".join(
        [p["name"] for p in products if p["stock"] == max_stock_value]
    )
    min_stock_names = ", ".join(
        [p["name"] for p in products if p["stock"] == min_stock_value]
    )

    values_total = sum(p["price"] * p["stock"] for p in products)

    quantity_category_products = {}
    for p in products:
        if p["category"] not in quantity_category_products:
            quantity_category_products[p["category"]] = 0
        quantity_category_products[p["category"]] += 1

    best_price_stock = sorted(
        products, key=lambda p: p["price"] * p["stock"], reverse=True
    )[:5]

    with open(file_path, "w", encoding="UTF-8") as f:
        f.write("Relatório Gerencial:\n")
        f.write(f"Total de Produtos Cadastrados → {total_products}\n")
        f.write(f"Total de Estoque → {total_stock}\n")
        f.write(f"Total de Entradas de Estoque → {total_entries}\n")
        f.write(f"Total de Saídas de Estoque → {total_exits}\n")
        f.write(
            f"Produto(s) de Maior Estoque → {max_stock_names} (Quantidade: {max_stock_value})\n"
        )
        f.write(
            f"Produto(s) de Menor Estoque → {min_stock_names} (Quantidade: {min_stock_value})\n"
        )
        f.write(f"Valor Total de Estoque → R${values_total:.2f}\n\n")

        f.write("→ Distribuição por Categorias ←\n")
        for category, count in quantity_category_products.items():
            f.write(f"{category}: {count} Produtos\n")

        f.write("\n→ Classificação dos 5 Produtos Pelo Valor Total em Estoque ←\n")
        for product in best_price_stock:
            f.write(
                f"{product["name"]} (ID: {product["id"]}): R${product["price"] * product["stock"]:.2f}\n"
            )

    print(f"\nRelatório Exportado Para {file_path} com Sucesso!")
