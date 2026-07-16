"""Unit tests for the command line interface."""
from unittest import mock

from app.main import (
    main,
    print_table,
    prompt_params,
    prompt_value,
    render_menu,
    resolve_choice,
    summarise_rows,
)


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


def test_resolve_choice_accepts_exit_words():
    queries = [{"title": "Only query"}]

    assert resolve_choice("exit", queries) == "exit"
    assert resolve_choice("QUIT", queries) == "exit"


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


def test_prompt_value_reprompts_until_non_empty(capsys):
    with mock.patch("builtins.input", side_effect=["", "   ", "CS101"]):
        value = prompt_value("Course code: ")

    assert value == "CS101"
    output = capsys.readouterr().out
    assert "cannot be blank" in output


def test_prompt_params_validates_each_field():
    with mock.patch("builtins.input", side_effect=["", "CS101", "Turing"]):
        values = prompt_params([
            ("Course code: ", "course_code"),
            ("Lecturer surname: ", "lecturer_last_name"),
        ])

    assert values == {
        "course_code": "CS101",
        "lecturer_last_name": "Turing",
    }


def test_summarise_rows_singular_and_plural():
    assert summarise_rows([(1,)]) == "1 row."
    assert summarise_rows([(1,), (2,)]) == "2 rows."


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


def test_main_runs_query_validates_and_shows_count(capsys):
    query = {
        "title": "Demo query",
        "params": [("Name: ", "name")],
        "func": lambda name: (["Name"], [("Alice",), ("Bob",)]),
    }
    # menu "1"; blank name (re-prompt); "Alice"; Enter to continue; "0"
    inputs = ["1", "", "Alice", "", "0"]
    with mock.patch("app.main.QUERIES", [query]):
        with mock.patch("builtins.input", side_effect=inputs):
            main()

    output = capsys.readouterr().out
    assert "> Demo query" in output
    assert "cannot be blank" in output
    assert "Alice" in output
    assert "2 rows." in output
    assert "Goodbye." in output
