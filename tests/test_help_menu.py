
from app.help_menu import get_help_menu
from app.operations import Addition, OperationFactory


def test_help_menu_lists_operations():
    """Verify the help menu displays registered operations."""
    menu = get_help_menu()

    for operation in OperationFactory._operations:
        assert operation in menu

    assert "Usage:" in menu
    assert "Commands:" in menu


def test_help_menu_updates_dynamically(monkeypatch):
    """Verify new operations appear without editing the menu."""
    monkeypatch.setitem(
        OperationFactory._operations,
        "new_operation",
        Addition,
    )

    menu = get_help_menu()

    assert "new_operation" in menu
