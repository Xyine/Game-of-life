import click
from game_of_life import GameOfLife
from gui import GameGUI
from rules import classic_rules, zombie_rules, von_neumann_rules, respawn_rules

RULES_MAP = {
    "classic": classic_rules,
    "zombie": zombie_rules,
    "neumann": von_neumann_rules,
    "respawn": respawn_rules,
}


@click.group()
def cli():
    """Game of Life launcher"""
    pass


@cli.command()
def gui():
    """Launch pygame GUI"""
    GameGUI().run()


@cli.command()
@click.option("--width", type=int, default=None)
@click.option("--height", type=int, default=None)
@click.option("--file", type=str, default=None)
@click.option("--interval", "interval_s", type=float, default=0.5)
@click.option("--fill-mode", default="DEAD")
@click.option("--placement", default="topleft")
@click.option("--rules", type=click.Choice(RULES_MAP.keys()), default=None)
@click.option("--patterns", is_flag=True)
def terminal(
    width,
    height,
    file,
    interval_s,
    fill_mode,
    placement,
    rules,
    patterns,
):
    """Launch terminal version"""

    selected_rules = RULES_MAP.get(rules) if rules else None

    game = GameOfLife(
        width=width,
        height=height,
        file=file,
        interval_s=interval_s,
        fill_mode=fill_mode,
        placement=placement,
        rules=selected_rules,
        paterns=patterns,
    )

    game.start()


if __name__ == "__main__":
    cli()
