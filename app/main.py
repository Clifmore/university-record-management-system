"""Command line interface entry point."""
from app.db import DatabaseError
from app.queries import QUERIES

EXIT_CHOICES = ("0", "q", "Q")
GOODBYE = "Goodbye."


def render_menu(queries):
    """Build the menu text for the given list of query entries."""
    lines = ["University Record Management System", "-" * 36]
    if queries:
        for index, query in enumerate(queries, start=1):
            lines.append("{0}. {1}".format(index, query["title"]))
    else:
        lines.append("No queries available yet.")
    lines.append("0. Exit")
    return "\n".join(lines)


def read_choice(prompt="\nSelect an option: "):
    """Read the user's raw menu choice as a stripped string."""
    return input(prompt).strip()


def resolve_choice(choice, queries):
    """Turn a raw menu choice into an action.

    :returns: ``"exit"`` if the user chose to quit, ``None`` if the
        choice is not a valid menu entry, otherwise the zero-based
        index of the selected query within ``queries``.
    """
    if choice in EXIT_CHOICES:
        return "exit"
    if not choice.isdigit():
        return None
    selection = int(choice)
    if selection < 1 or selection > len(queries):
        return None
    return selection - 1


def prompt_params(params):
    """Collect a value for each ``(prompt_text, param_name)`` pair."""
    values = {}
    for prompt_text, param_name in params:
        values[param_name] = input(prompt_text).strip()
    return values


def print_table(columns, rows):
    """Print query results as simple aligned columns."""
    if not rows:
        print("No results found.")
        return

    widths = []
    for index, column in enumerate(columns):
        cell_widths = [len(str(row[index])) for row in rows]
        widths.append(max([len(str(column))] + cell_widths))

    header = "  ".join(
        str(column).ljust(widths[index])
        for index, column in enumerate(columns)
    )
    separator = "  ".join("-" * width for width in widths)

    print(header)
    print(separator)
    for row in rows:
        print("  ".join(
            str(cell).ljust(widths[index])
            for index, cell in enumerate(row)
        ))


def main():
    """Run the interactive query menu until the user exits."""
    try:
        while True:
            print(render_menu(QUERIES))
            choice = read_choice()
            action = resolve_choice(choice, QUERIES)

            if action == "exit":
                print(GOODBYE)
                return
            if action is None:
                print("Please choose a valid option from the menu.")
                continue

            query = QUERIES[action]
            try:
                values = prompt_params(query["params"])
                columns, rows = query["func"](**values)
                print_table(columns, rows)
            except DatabaseError as exc:
                print(str(exc))
    except (KeyboardInterrupt, EOFError):
        print(GOODBYE)


if __name__ == "__main__":
    main()
