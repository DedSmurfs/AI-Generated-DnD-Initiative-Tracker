#!/usr/bin/env python3
"""
D&D 5e Initiative Tracker - Main Entry Point
Run with: python3 main.py
"""

import sys
from combatant import Combatant, Condition
from initiative_tracker import InitiativeTracker


def print_banner():
    """Print the application banner."""
    print("\n" + "=" * 80)
    print("                    D&D 5E INITIATIVE TRACKER")
    print("=" * 80)
    print("Track initiative, manage HP/Temp HP, conditions, and more!")
    print("=" * 80 + "\n")


def print_help():
    """Print available commands."""
    print("\n--- Available Commands ---")
    print("  q - Quit")
    print("  n - Next turn")
    print("  p - Previous turn")
    print("  a <name> <damage> - Apply damage")
    print("  h <name> <amount> - Heal")
    print("  t <name> <amount> - Add temp HP")
    print("  c <name> <condition> - Add condition (Poisoned, Stunned, Prone, etc.)")
    print("  r <name> <condition> - Remove condition")
    print("  e <name> <value> - Edit AC/HP/Initiative")
    print("  s - Save party to file")
    print("  l - Load/reset encounter from saved party")
    print("  d - Display all combatants")
    print("  help - Show this help message")
    print("=" * 80 + "\n")


def main():
    """Main function to run the initiative tracker."""
    tracker = InitiativeTracker()
    
    # Load existing party if available
    if tracker.load_party():
        print("✓ Loaded existing party from party.json")
    else:
        print("ℹ No existing party found. Starting fresh.")
    
    # Add some example combatants for demonstration
    print("\n--- Adding Combatants ---")
    tracker.add_player("Player 1", initiative=15, ac=16, max_hp=45, current_hp=45)
    tracker.add_player("Player 2", initiative=12, ac=14, max_hp=38, current_hp=38)
    tracker.add_monster("Goblin Scout", initiative_modifier=4, ac=13, max_hp=7)
    tracker.add_monster("Orc Warrior", initiative_modifier=5, ac=16, max_hp=28)
    
    # Display initial state
    print("\n--- Battle Order ---")
    tracker.display_battle_order()
    
    print_help()
    
    while True:
        try:
            command = input("Command: ").strip().lower()
            
            if command == "q":
                print("\nGoodbye! Your party has been saved.")
                break
            
            elif command == "n":
                tracker.advance_turn()
                tracker.display_battle_order()
            
            elif command == "p":
                tracker.previous_turn()
                tracker.display_battle_order()
            
            elif command.startswith("a"):
                parts = command.split(maxsplit=2)
                if len(parts) >= 3:
                    name, damage_str = parts[1], parts[2]
                    try:
                        damage = int(damage_str)
                        tracker.apply_damage(name, damage)
                        tracker.display_battle_order()
                    except ValueError:
                        print("✗ Error: Damage must be a number")
            
            elif command.startswith("h"):
                parts = command.split(maxsplit=2)
                if len(parts) >= 3:
                    name, amount_str = parts[1], parts[2]
                    try:
                        amount = int(amount_str)
                        tracker.heal(name, amount)
                        tracker.display_battle_order()
                    except ValueError:
                        print("✗ Error: Amount must be a number")
            
            elif command.startswith("t"):
                parts = command.split(maxsplit=2)
                if len(parts) >= 3:
                    name, amount_str = parts[1], parts[2]
                    try:
                        amount = int(amount_str)
                        tracker.add_temp_hp(name, amount)
                        tracker.display_battle_order()
                    except ValueError:
                        print("✗ Error: Amount must be a number")
            
            elif command.startswith("c"):
                parts = command.split(maxsplit=2)
                if len(parts) >= 3:
                    name, cond_str = parts[1], parts[2]
                    try:
                        condition = Condition[cond_str.upper()]
                        tracker.add_condition(name, condition)
                        tracker.display_battle_order()
                    except (KeyError, ValueError):
                        print(f"✗ Error: Unknown condition '{cond_str}'. Use: Poisoned, Stunned, Prone, Concentrating, Blind, Deaf, Frozen, Grappled, Paralyzed, Petrified")
            
            elif command.startswith("r"):
                parts = command.split(maxsplit=2)
                if len(parts) >= 3:
                    name, cond_str = parts[1], parts[2]
                    try:
                        condition = Condition[cond_str.upper()]
                        tracker.remove_condition(name, condition)
                        tracker.display_battle_order()
                    except (KeyError, ValueError):
                        print(f"✗ Error: Unknown condition '{cond_str}'")
            
            elif command.startswith("e"):
                parts = command.split(maxsplit=2)
                if len(parts) >= 3:
                    name, value_str = parts[1], parts[2]
                    try:
                        value = int(value_str)
                        tracker.edit_ac(name, value)
                        tracker.display_battle_order()
                    except ValueError:
                        print("✗ Error: Value must be a number")
            
            elif command == "s":
                if tracker.save_party():
                    print("✓ Party saved successfully!")
                else:
                    print("✗ Failed to save party.")
            
            elif command == "l":
                if tracker.reset_encounter():
                    print("✓ Encounter reset. Party loaded from file.")
                    tracker.display_battle_order()
                else:
                    print("✗ No party file found or error loading.")
            
            elif command == "d":
                tracker.display_battle_order(show_all=True)
            
            elif command == "help":
                print_help()
            
            else:
                print(f"✗ Unknown command: {command}")
        
        except KeyboardInterrupt:
            print("\n\n⚠ Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"✗ Error: {e}")


if __name__ == "__main__":
    print_banner()
    main()
