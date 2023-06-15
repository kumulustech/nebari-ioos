import json
from pathlib import Path
from typing import Tuple

import typer

from _nebari.keycloak import do_keycloak, export_keycloak_users
from nebari.hookspecs import hookimpl


@hookimpl
def nebari_subcommand(cli: typer.Typer):
    app_keycloak = typer.Typer(
        add_completion=False,
        no_args_is_help=True,
        rich_markup_mode="rich",
        context_settings={"help_option_names": ["-h", "--help"]},
    )

    cli.add_typer(
        app_keycloak,
        name="keycloak",
        help="Interact with the Nebari Keycloak identity and access management tool.",
        rich_help_panel="Additional Commands",
    )

    @app_keycloak.command(name="adduser")
    def add_user(
        add_users: Tuple[str, str] = typer.Option(
            ..., "--user", help="Provide both: <username> <password>"
        ),
        config_filename: str = typer.Option(
            ...,
            "-c",
            "--config",
            help="nebari configuration file path",
        ),
    ):
        """Add a user to Keycloak. User will be automatically added to the [italic]analyst[/italic] group."""
        if isinstance(config_filename, str):
            config_filename = Path(config_filename)

        args = ["adduser", add_users[0], add_users[1]]

        do_keycloak(config_filename, *args)

    @app_keycloak.command(name="listusers")
    def list_users(
        config_filename: str = typer.Option(
            ...,
            "-c",
            "--config",
            help="nebari configuration file path",
        )
    ):
        """List the users in Keycloak."""
        if isinstance(config_filename, str):
            config_filename = Path(config_filename)

        args = ["listusers"]

        do_keycloak(config_filename, *args)

    @app_keycloak.command(name="export-users")
    def export_users(
        config_filename: str = typer.Option(
            ...,
            "-c",
            "--config",
            help="nebari configuration file path",
        ),
        realm: str = typer.Option(
            "nebari",
            "--realm",
            help="realm from which users are to be exported",
        ),
    ):
        """Export the users in Keycloak."""
        if isinstance(config_filename, str):
            config_filename = Path(config_filename)

        r = export_keycloak_users(config_filename, realm=realm)

        print(json.dumps(r, indent=4))