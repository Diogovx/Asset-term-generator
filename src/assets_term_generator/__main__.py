import logging

from jinja2.exceptions import TemplateSyntaxError, UndefinedError
from requests.exceptions import RequestException
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from assets_term_generator.api import snipeit_client
from assets_term_generator.core.config_handler import load_config
from assets_term_generator.core.document_processor import DocumentProcessor
from assets_term_generator.ui.cli_main import Menu
from assets_term_generator.util.exceptions import AssetNotFoundError, UserNotFoundError
from assets_term_generator.util.history_logging import log_generation_history
from assets_term_generator.util.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)
console = Console()


def main() -> None:
    welcome_panel = Panel.fit(
        Text("Bom-vindo ao Gerador de Termos", justify="center"),
        title="[bold cyan]Assets Term Generator v2.1.0[/bold cyan]",
        padding=(1, 2),
    )
    console.print(Align.center(welcome_panel))

    app_config = load_config()
    document_processor = DocumentProcessor(config=app_config)
    menu = Menu(config=app_config)

    while True:
        try:
            document_key = menu.select_document_type()

            selected_template_config = app_config.document.templates[document_key]

            employee_number = menu.input_employee_number()
            if not employee_number:
                raise ValueError("Matrícula não pode ser vazia")
            with console.status(
                "[bold green]Buscando dados na API do Snipe-IT...[/bold green]", spinner="dots"
            ):
                user, assets = snipeit_client.get_user_and_assets(employee_number)
            if not assets:
                raise AssetNotFoundError(f"Nenhum ativo encontrado para o usuário '{user.name}'.")

            user_categories_set = {
                asset.category.name for asset in assets if asset.category and asset.category.name
            }

            allowed_categories = selected_template_config.target_categories

            final_categories = set()
            if allowed_categories:
                allowed_categories_set = set(allowed_categories)
                final_categories = user_categories_set & allowed_categories_set
            else:
                final_categories = user_categories_set

            categories_to_show = sorted(list(final_categories))

            if not categories_to_show:
                raise ValueError(
                    f"O usuário não possui ativos compatíveis com o template '{document_key}'."
                )

            selected_category = menu.select_asset_category(categories_to_show)
            logger.info(f"Categoria selecionada para o termo: '{selected_category}'")

            assets_in_category = [
                asset
                for asset in assets
                if asset.category and asset.category.name == selected_category
            ]

            if len(assets_in_category) > 1:
                asset_table = Table(title="Ativos encontrados para a categoria")
                asset_table.add_column("Asset_tag", style="cyan", no_wrap=True)
                asset_table.add_column("Model", style="magenta")
                asset_table.add_column("Serial", justify="right", style="green")

                for asset in assets_in_category:
                    asset_table.add_row(asset.asset_tag, asset.model.name, asset.serial or "N/A")

                console.print(asset_table)

                selected_asset = menu.select_asset(assets_in_category)
            else:
                selected_asset = assets_in_category[0]

            logger.info(f"Ativo principal selecionado para o termo: {selected_asset.asset_tag}")

            summary_text = (
                f"Usuário: [bold]{user.name}[/bold] ({user.employee_num})\n"
                f"Ativo: [bold]{selected_asset.asset_tag}[/bold] - {selected_asset.model.name}\n"
                f"Template: [bold]{document_key}[/bold]"
            )
            summary_panel = Panel(
                summary_text, title="[yellow]Confirmar Geração[/yellow]", border_style="yellow"
            )

            console.print(summary_panel)

            confirm = menu.confirm_action()

            if not confirm:
                console.print("[bold red]Operação cancelada pelo usuário[/bold red]")
                continue

            document_processor.load_template(document_key)

            document_processor.process_document(user, selected_asset)

            file_path = document_processor.save(user.name, selected_asset.asset_tag, document_key)

            log_generation_history(user, selected_asset, document_key, file_path)
            document_processor.open_file(file_path)

            console.print("[bold green]Termo gerado com sucesso![/bold green]")

        except (UserNotFoundError, AssetNotFoundError, ValueError) as e:
            console.print(f"[bold red]ERRO:[/bold red] {e}")
            logger.error(e)
        except RequestException as e:
            console.print(
                "[bold red]NETWORK ERROR: Erro de comunicação com a API do Snipe-IT[/bold red]."
            )
            logger.error(e)
        except TemplateSyntaxError as e:
            console.print("[bold red]SYNTAX ERROR[/bold red]: Template preenchido incorretamente.")
            console.print("Por favor verifique as etiquetas '{{ ... }}', '{% ... %}'.")
            console.print(f"[bold yellow]WARNING: Detalhe técninco: {e.message}")
            logger.error(e)
        except UndefinedError as e:
            console.print(
                "[bold red]UNDEFINED ERROR[/bold red]:"
                "O programa encontrou um erro ao preencher o template"
            )
            console.print(f"[bold yellow] WARNING[/bold yellow]: Detalhe técnico: {e.message}")
        except Exception as e:
            console.print("[bold red]UNEXPECTED ERROR[/bold red]: Ocorreu uma falha inesperada.")
            logger.critical({e}, exc_info=True)

        input("\nPressione Enter para continuar...")

        selected_action = menu.select_action()
        if selected_action == "Exit":
            break


if __name__ == "__main__":
    main()
