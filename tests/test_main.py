"""Unit tests for the command line interface."""
from unittest import mock

from app.main import main, print_table, render_menu, resolve_choice


def test_render_menu_shows_placeholder_when_empty():
    menu = render_menu([])

    assert "No queries available yet." in menu
    assert "0. Exit" in menu


def test_render_menu_lists_query_titles():
    queries = [{"title": "First query"}, {"title": "Second query"}]

    menu = render_menu(queries)

    assert "1. First query" in menu
    assert "2. Second query" in menu
    assert "0. Exit" in menu


def test_resolve_choice_exit_values():
    queries = [{"title": "Only query"}]

    assert resolve_choice("0", queries) == "exit"
    assert resolve_choice("q", queries) == "exit"
    assert resolve_choice("Q", queries) == "exit"


def test_resolve_choice_valid_selection():
    queries = [{"title": "First"}, {"title": "Second"}]

    assert resolve_choice("1", queries) == 0
    assert resolve_choice("2", queries) == 1


def test_resolve_choice_rejects_invalid_input():
    queries = [{"title": "Only query"}]

    assert resolve_choice("x", queries) is None
    assert resolve_choice("", queries) is None
    assert resolve_choice("5", queries) is None
    assert resolve_choice("-1", queries) is None
    assert resolve_choice("1", []) is None


def test_print_table_aligns_columns(capsys):
    columns = ["id", "name"]
    rows = [(1, "Alice"), (22, "Bob")]

    print_table(columns, rows)

    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 4
    line_lengths = {len(line) for line in lines}
    assert len(line_lengths) == 1
    assert lines[0].startswith("id")
    assert set(lines[1]) == {"-", " "}


def test_print_table_handles_empty_rows(capsys):
    print_table(["id", "name"], [])

    output = capsys.readouterr().out
    assert output.strip() == "No results found."


def test_invalid_choice_reprompts_then_exits(capsys):
    with mock.patch("builtins.input", side_effect=["x", "0"]):
        main()

    output = capsys.readouterr().out
    assert "Please choose a valid option from the menu." in output
    assert "Goodbye." in output


def test_exit_choice_returns_cleanly(capsys):
    with mock.patch("builtins.input", side_effect=["0"]):
        main()

    output = capsys.readouterr().out
    assert "Goodbye." in output


def test_letter_quit_choice_exits(capsys):
    with mock.patch("builtins.input", side_effect=["q"]):
        main()

    output = capsys.readouterr().out
    assert "Goodbye." in output


def test_keyboard_interrupt_exits_cleanly(capsys):
    with mock.patch("builtins.input", side_effect=KeyboardInterrupt):
        main()

    output = capsys.readouterr().out
    assert "Goodbye." in output
