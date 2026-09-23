#!/usr/init/env python3
"""D&D Initiative Tracker - Interactive Textual TUI Version with Initiative, Damage, Healing & Overheal Reset"""

from typing import Dict, List, Any
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Button, DataTable, Static, Input, Label
from textual.screen import ModalScreen


class Combatant:
    """Represents any combatant (Player or Enemy) in the initiative order."""
    def __init__(self, key: str, name: str, hp: int, ac: int, initiative: int, is_player: bool):
        self.key = key
        self.name = name
        self.hp = hp
        self.base_max_hp = hp  # Permanent starting max HP for resets
        self.max_hp = hp        # Dynamic max HP (can expand via overheal/temp buffs)
        self.ac = ac
        self.initiative = initiative
        self.is_player = is_player  # True for persistent players, False for temporary enemies

    def reset_for_new_battle(self):
        """Resets combatant health and max HP back to original baseline for a new battle."""
        self.max_hp = self.base_max_hp
        self.hp = self.base_max_hp


class BatailleTracker:
    """Manages players, enemies, initiative, damage, and healing handling."""
    def __init__(self):
        self.players: Dict[str, Combatant] = {}
        self.enemies: Dict[str, Combatant] = {}

    def reset(self):
        """Reset battle: clears ALL enemies, and resets all player HP & max HP back to baseline."""
        self.enemies.clear()
        for player in self.players.values():
            player.reset_for_new_battle()
        return True

    def get_all_combatants(self) -> List[Combatant]:
        """Returns all players and enemies sorted by Initiative (highest first)."""
        all_c = list(self.players.values()) + list(self.enemies.values())
        return sorted(all_c, key=lambda c: c.initiative, reverse=True)

    def apply_damage_by_key(self, key: str, damage: int) -> bool:
        """Applies damage directly using the unique combatant key."""
        if key in self.players:
            p = self.players[key]
            p.hp = max(0, p.hp - damage)
            return True
        elif key in self.enemies:
            e = self.enemies[key]
            e.hp = max(0, e.hp - damage)
            if e.hp <= 0:
                del self.enemies[key]  # Remove defeated enemy
            return True
        return False

    def apply_damage(self, target_name: str, damage: int) -> bool:
        """Applies damage to a player or enemy by name (fallback)."""
        target_lower = target_name.strip().lower()
        
        # Check players
        for p in self.players.values():
            if p.name.lower() == target_lower:
                p.hp = max(0, p.hp - damage)
                return True
                
        # Check enemies
        for key, e in list(self.enemies.items()):
            if e.name.lower() == target_lower:
                e.hp = max(0, e.hp - damage)
                if e.hp <= 0:
                    del self.enemies[key]  # Remove defeated enemy
                return True
        return False

    def apply_healing_by_key(self, key: str, amount: int) -> bool:
        """Applies healing with full overheal support (raises current HP, allows temporarily exceeding max HP)."""
        if key in self.players:
            p = self.players[key]
            p.hp += amount
            if p.hp > p.max_hp:
                p.max_hp = p.hp
            return True
        elif key in self.enemies:
            e = self.enemies[key]
            e.hp += amount
            if e.hp > e.max_hp:
                e.max_hp = e.hp
            return True
        return False

    def apply_healing(self, target_name: str, amount: int) -> bool:
        """Applies healing with full overheal support by name (fallback)."""
        target_lower = target_name.strip().lower()
        
        # Check players
        for p in self.players.values():
            if p.name.lower() == target_lower:
                p.hp += amount
                if p.hp > p.max_hp:
                    p.max_hp = p.hp
                return True
                
        # Check enemies
        for e in self.enemies.values():
            if e.name.lower() == target_lower:
                e.hp += amount
                if e.hp > e.max_hp:
                    e.max_hp = e.hp
                return True
        return False


class AddPlayerScreen(ModalScreen):
    """Modal dialog to add/update a persistent player."""
    BINDINGS = [("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog"):
            yield Label("[bold cyan]Add/Update Player[/bold cyan]")
            yield Input(placeholder="Character Name", id="name-input")
            yield Input(placeholder="HP (default 20)", id="hp-input")
            yield Input(placeholder="AC (default 15)", id="ac-input")
            yield Input(placeholder="Initiative Roll (default 10)", id="init-input")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Save", variant="success", id="save-btn")
                yield Button("Cancel", variant="error", id="cancel-btn")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.process_save()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-btn":
            self.process_save()
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)

    def process_save(self) -> None:
        name = self.query_one("#name-input", Input).value.strip() or "Hero"
        hp = int(self.query_one("#hp-input", Input).value.strip() or 20)
        ac = int(self.query_one("#ac-input", Input).value.strip() or 15)
        init = int(self.query_one("#init-input", Input).value.strip() or 10)
        self.dismiss((name, hp, ac, init))


class AddEnemyScreen(ModalScreen):
    """Modal dialog to add a temporary enemy."""
    BINDINGS = [("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog"):
            yield Label("[bold red]Add Enemy[/bold red]")
            yield Input(placeholder="Enemy Name (e.g., Goblin)", id="name-input")
            yield Input(placeholder="HP (default 10)", id="hp-input")
            yield Input(placeholder="AC (default 12)", id="ac-input")
            yield Input(placeholder="Initiative Roll (default 10)", id="init-input")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Save", variant="success", id="save-btn")
                yield Button("Cancel", variant="error", id="cancel-btn")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.process_save()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-btn":
            self.process_save()
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)

    def process_save(self) -> None:
        name = self.query_one("#name-input", Input).value.strip() or "Goblin"
        hp = int(self.query_one("#hp-input", Input).value.strip() or 10)
        ac = int(self.query_one("#ac-input", Input).value.strip() or 12)
        init = int(self.query_one("#init-input", Input).value.strip() or 10)
        self.dismiss((name, hp, ac, init))


class DamageScreen(ModalScreen):
    """Modal dialog to apply damage to any combatant."""
    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, target_name: str = ""):
        super().__init__()
        self.target_name = target_name

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog"):
            yield Label("[bold yellow]Apply Damage[/bold yellow]")
            yield Input(value=self.target_name, placeholder="Target Name", id="target-input")
            yield Input(placeholder="Damage Amount", id="dmg-input")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Apply", variant="warning", id="apply-btn")
                yield Button("Cancel", variant="error", id="cancel-btn")

    def on_mount(self) -> None:
        if self.target_name:
            self.query_one("#dmg-input", Input).focus()
        else:
            self.query_one("#target-input", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.process_save()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "apply-btn":
            self.process_save()
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)

    def process_save(self) -> None:
        target = self.query_one("#target-input", Input).value.strip()
        try:
            dmg = int(self.query_one("#dmg-input", Input).value.strip() or 0)
        except ValueError:
            dmg = 0
        self.dismiss((target, dmg))


class HealingScreen(ModalScreen):
    """Modal dialog to apply healing / overheal to any combatant."""
    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, target_name: str = ""):
        super().__init__()
        self.target_name = target_name

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog"):
            yield Label("[bold green]Apply Healing / Overheal[/bold green]")
            yield Input(value=self.target_name, placeholder="Target Name", id="target-input")
            yield Input(placeholder="Healing Amount", id="heal-input")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Heal", variant="success", id="heal-btn")
                yield Button("Cancel", variant="error", id="cancel-btn")

    def on_mount(self) -> None:
        if self.target_name:
            self.query_one("#heal-input", Input).focus()
        else:
            self.query_one("#target-input", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.process_save()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "heal-btn":
            self.process_save()
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)

    def process_save(self) -> None:
        target = self.query_one("#target-input", Input).value.strip()
        try:
            heal = int(self.query_one("#heal-input", Input).value.strip() or 0)
        except ValueError:
            heal = 0
        self.dismiss((target, heal))


class DndTrackerApp(App):
    """Main Textual Application for D&D Tracker."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    #sidebar {
        dock: left;
        width: 30;
        background: $boost;
        padding: 1;
        border-right: solid $primary;
    }
    #main-content {
        padding: 1;
        width: 1fr;
    }
    Button {
        width: 100%;
        margin-bottom: 1;
    }
    .title {
        margin-bottom: 1;
    }
    .dialog {
        padding: 2;
        background: $panel;
        border: thick $primary;
        width: 44;
        height: 18;
        align: center middle;
    }
    .dialog-buttons {
        margin-top: 1;
    }
    .dialog-buttons Button {
        width: 50%;
        margin-right: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("p", "add_player", "Add Player"),
        ("e", "add_enemy", "Add Enemy"),
        ("d", "apply_damage", "Apply Damage"),
        ("h", "apply_healing", "Heal"),
        ("r", "reset_tracker", "Reset Battle"),
    ]

    def __init__(self):
        super().__init__()
        self.tracker = BatailleTracker()

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Static("[bold cyan]Controls[/bold cyan]", classes="title")
                yield Button("Add Player (P)", variant="success", id="btn-add-player")
                yield Button("Add Enemy (E)", variant="warning", id="btn-add-enemy")
                yield Button("Damage (D)", variant="error", id="btn-damage")
                yield Button("Heal (H)", variant="success", id="btn-heal")
                yield Button("Reset Battle (R)", variant="default", id="btn-reset")
                yield Button("Quit (Q)", variant="default", id="btn-quit")
            with Vertical(id="main-content"):
                yield Static("[bold]Initiative Order & Status[/bold]", classes="title")
                yield DataTable(id="tracker-table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#tracker-table", DataTable)
        table.add_columns("Initiative", "Type", "Name", "HP", "AC")
        table.cursor_type = "row"
        self.refresh_table()

    def refresh_table(self) -> None:
        table = self.query_one("#tracker-table", DataTable)
        table.clear()
        for c in self.tracker.get_all_combatants():
            c_type = "Player" if c.is_player else "Enemy"
            hp_display = f"{c.hp}/{c.max_hp}"
            table.add_row(str(c.initiative), c_type, c.name, hp_display, str(c.ac))

    def action_add_player(self) -> None:
        def handle_result(result):
            if result:
                name, hp, ac, init = result
                key = f"player_{name.lower()}"
                self.tracker.players[key] = Combatant(key, name, hp, ac, init, is_player=True)
                self.refresh_table()
        self.push_screen(AddPlayerScreen(), handle_result)

    def action_add_enemy(self) -> None:
        def handle_result(result):
            if result:
                name, hp, ac, init = result
                key = f"enemy_{name.lower()}_{len(self.tracker.enemies)}"
                self.tracker.enemies[key] = Combatant(key, name, hp, ac, init, is_player=False)
                self.refresh_table()
        self.push_screen(AddEnemyScreen(), handle_result)

    def action_apply_damage(self) -> None:
        table = self.query_one("#tracker-table", DataTable)
        combatants = self.tracker.get_all_combatants()
        
        selected_key = None
        selected_name = ""
        
        if table.row_count > 0 and table.cursor_row is not None and 0 <= table.cursor_row < len(combatants):
            selected = combatants[table.cursor_row]
            selected_key = selected.key
            selected_name = selected.name

        def handle_result(result):
            if result:
                target_name, dmg = result
                if selected_key and target_name.strip().lower() == selected_name.lower():
                    self.tracker.apply_damage_by_key(selected_key, dmg)
                else:
                    self.tracker.apply_damage(target_name, dmg)
                self.refresh_table()

        self.push_screen(DamageScreen(selected_name), handle_result)

    def action_apply_healing(self) -> None:
        table = self.query_one("#tracker-table", DataTable)
        combatants = self.tracker.get_all_combatants()
        
        selected_key = None
        selected_name = ""
        
        if table.row_count > 0 and table.cursor_row is not None and 0 <= table.cursor_row < len(combatants):
            selected = combatants[table.cursor_row]
            selected_key = selected.key
            selected_name = selected.name

        def handle_result(result):
            if result:
                target_name, heal = result
                if selected_key and target_name.strip().lower() == selected_name.lower():
                    self.tracker.apply_healing_by_key(selected_key, heal)
                else:
                    self.tracker.apply_healing(target_name, heal)
                self.refresh_table()

        self.push_screen(HealingScreen(selected_name), handle_result)

    def action_reset_tracker(self) -> None:
        self.tracker.reset()
        self.refresh_table()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-add-player":
            self.action_add_player()
        elif event.button.id == "btn-add-enemy":
            self.action_add_enemy()
        elif event.button.id == "btn-damage":
            self.action_apply_damage()
        elif event.button.id == "btn-heal":
            self.action_apply_healing()
        elif event.button.id == "btn-reset":
            self.action_reset_tracker()
        elif event.button.id == "btn-quit":
            self.exit()


if __name__ == "__main__":
    app = DndTrackerApp()
    app.run()
