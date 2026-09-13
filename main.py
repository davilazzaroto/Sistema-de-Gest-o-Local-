from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from functions import (
    list_products,
    managerial_report,
    register_product,
    register_stock_entry,
    register_stock_exit,
    report_stock_movements,
    search_product_by_id,
    search_product,
    update_product,
)
from storage import load_json, save_json

console = Console()
PROJECT_DIR = Path(__file__).resolve().parent


def main():
    products_path = PROJECT_DIR / "products.json"
    movements_path = PROJECT_DIR / "stock_movements.json"
    products = load_json(products_path) or []
    stock_movements = load_json(movements_path) or []

    while True:
        menu = (
            "[bold cyan]1[/bold cyan]  Cadastrar produto\n"
            "[bold cyan]2[/bold cyan]  Alterar produto\n"
            "[bold cyan]3[/bold cyan]  Buscar produto por ID\n"
            "[bold cyan]4[/bold cyan]  Buscar por nome ou categoria\n"
            "[bold cyan]5[/bold cyan]  Relatório de produtos\n"
            "[bold cyan]6[/bold cyan]  Registrar entrada de estoque\n"
            "[bold cyan]7[/bold cyan]  Registrar saída de estoque\n"
            "[bold cyan]8[/bold cyan]  Relatório de movimentações\n"
            "[bold cyan]9[/bold cyan]  Relatório gerencial\n"
            "[bold cyan]0[/bold cyan]  Salvar e sair"
        )
        console.print(
            Panel(menu, title="📦 Sistema de Gestão de Estoque", border_style="cyan")
        )
        try:
            option = int(input("Escolha uma ação: ").strip())
        except ValueError:
            console.print("[bold red]Digite apenas números.[/bold red]")
            continue

        match option:
            case 1:
                register_product(products)
            case 2:
                update_product(products)
            case 3:
                search_product_by_id(products)
            case 4:
                search_product(products)
            case 5:
                list_products(products)
            case 6:
                register_stock_entry(products, stock_movements)
            case 7:
                register_stock_exit(products, stock_movements)
            case 8:
                report_stock_movements(products, stock_movements)
            case 9:
                managerial_report(products, stock_movements)
            case 0:
                save_json(products, products_path)
                save_json(stock_movements, movements_path)
                console.print(
                    "[bold green]Informações salvas! Saindo do sistema...[/bold green]"
                )
                break
            case _:
                console.print("[bold red]Opção inválida. Tente novamente.[/bold red]")


if __name__ == "__main__":
    main()
