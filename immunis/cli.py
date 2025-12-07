import time

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


from . import core

from .app import get_attack_score
from .client import client

console = Console()


def main():

    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan] IMMUNIS CLI[/bold cyan]\n[dim]Active Defense System Initialized[/dim]"
        )
    )

    while True:
        status = core.get_status()
        if status.lock_down_mode:
            console.print(
                Panel(
                    "[bold white on red] SYSTEM IN LOCKDOWN [/bold white on red]",
                    expand=False,
                )
            )
            console.print(
                "[red]A critical threat was detected. All operations are halted.[/red]"
            )
            time.sleep(5)  # Pause to prevent spamming the check
            continue

        try:
            prompt = console.input("\n[bold green]➜ [/bold green]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Exiting Immunis CLI.[/yellow]")
            break

        with console.status("[blue]Analyzing prompt intent...[/blue]"):
            guard_response = get_attack_score(prompt)
            core.send_log_to_datadog(
                prompt, guard_response.score, guard_response.is_attack
            )

        if guard_response.is_attack:
            console.print(
                f"[bold red]Threat Detected![/bold red] Score: {guard_response.score} | Reason: {guard_response.reason}"
            )

        with console.status("[yellow]Generating response...[/yellow]"):
            response = client.models.generate_content(
                model="gemini-2.5-pro", contents=prompt
            )
            console.print(Markdown(response.text))
