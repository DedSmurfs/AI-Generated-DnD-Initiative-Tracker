"""Core Initiative Tracker logic for D&D 5e."""

import json
import os
from typing import List, Optional
from datetime import datetime

from combatant import Combatant, Condition, create_combatant_from_json, combatant_to_json


class InitiativeTracker:
    """Manages D&D 5e initiative order and combat state."""
    
    def __init__(self, party_file: str = "party.json"):
        self.combatants: List[Combatant] = []
        self.current_turn_index: int = -1
        self.round: int = 1
        self.party_file = party_file
    
    def add_combatant(self, name: str, initiative_modifier: int, ac: int, 
                      max_hp: int, current_hp: Optional[int] = None,
                      temp_hp: int = 0) -> Combatant:
        """Add a new combatant to the battle."""
        combatant = Combatant(
            name=name,
            initiative_modifier=initiative_modifier,
            ac=ac,
            max_hp=max_hp,
            current_hp=current_hp if current_hp is not None else max_hp,
            temp_hp=temp_hp
        )
        self.combatants.append(combatant)
        return combatant
    
    def add_monster(self, name: str, initiative_modifier: int, ac: int, 
                    max_hp: int, auto_roll_initiative: bool = True) -> Combatant:
        """Add a monster with optional auto-roll for initiative."""
        if auto_roll_initiative:
            import random
            init_roll = random.randint(1, 20)
            initiative_modifier += init_roll
        
        return self.add_combatant(name, initiative_modifier, ac, max_hp)
    
    def add_player(self, name: str, initiative: int, ac: int, 
                   max_hp: int, current_hp: Optional[int] = None,
                   temp_hp: int = 0) -> Combatant:
        """Add a player with explicit initiative value."""
        return self.add_combatant(name, initiative, ac, max_hp, current_hp, temp_hp)
    
    def remove_combatant(self, name: str) -> bool:
        """Remove a combatant from the battle."""
        for i, combatant in enumerate(self.combatants):
            if combatant.name.lower() == name.lower():
                del self.combatants[i]
                return True
        return False
    
    def advance_turn(self) -> Optional[Combatant]:
        """Advance to next turn, return the active combatant."""
        alive_combatants = [c for c in self.combatants if c.is_alive]
        
        if not alive_combatants:
            return None
        
        # Sort by initiative descending
        sorted_combatants = sorted(alive_combatants, 
                                   key=lambda x: x.initiative, 
                                   reverse=True)
        
        # Find next active combatant
        for i in range(len(sorted_combatants)):
            if sorted_combatants[i].is_alive:
                self.current_turn_index = i
                return sorted_combatants[i]
        
        return None
    
    def previous_turn(self) -> Optional[Combatant]:
        """Go back to previous turn."""
        alive_combatants = [c for c in self.combatants if c.is_alive]
        
        if not alive_combatants:
            return None
        
        sorted_combatants = sorted(alive_combatants, 
                                   key=lambda x: x.initiative, 
                                   reverse=True)
        
        # Find previous active combatant
        for i in range(len(sorted_combatants) - 1, -1, -1):
            if sorted_combatants[i].is_alive:
                self.current_turn_index = i
                return sorted_combatants[i]
        
        return None
    
    def get_active_combatant(self) -> Optional[Combatant]:
        """Get the currently active combatant."""
        if self.current_turn_index < 0 or self.current_turn_index >= len(self.combatants):
            return None
        
        return self.combatants[self.current_turn_index]
    
    def get_sorted_combatants(self) -> List[Combatant]:
        """Get all combatants sorted by initiative."""
        alive_combatants = [c for c in self.combatants if c.is_alive]
        return sorted(alive_combatants, 
                      key=lambda x: x.initiative, 
                      reverse=True)
    
    def apply_damage(self, name: str, damage: int) -> None:
        """Apply damage to a combatant."""
        for combatant in self.combatants:
            if combatant.name.lower() == name.lower():
                combatant.take_damage(damage)
                break
    
    def heal(self, name: str, amount: int) -> None:
        """Heal a combatant."""
        for combatant in self.combatants:
            if combatant.name.lower() == name.lower():
                combatant.heal(amount)
                break
    
    def add_temp_hp(self, name: str, amount: int) -> None:
        """Add temporary HP to a combatant."""
        for combatant in self.combatants:
            if combatant.name.lower() == name.lower():
                combatant.add_temp_hp(amount)
                break
    
    def add_condition(self, name: str, condition: Condition) -> None:
        """Add a condition to a combatant."""
        for combatant in self.combatants:
            if combatant.name.lower() == name.lower():
                combatant.add_condition(condition)
                break
    
    def remove_condition(self, name: str, condition: Condition) -> bool:
        """Remove a condition from a combatant."""
        for combatant in self.combatants:
            if combatant.name.lower() == name.lower():
                return combatant.remove_condition(condition)
        return False
    
    def edit_ac(self, name: str, new_ac: int) -> bool:
        """Edit AC of a combatant."""
        for combatant in self.combatants:
            if combatant.name.lower() == name.lower():
                combatant.ac = new_ac
                return True
        return False
    
    def edit_hp(self, name: str, max_hp: int, current_hp: Optional[int] = None) -> bool:
        """Edit HP of a combatant."""
        for combatant in self.combatants:
            if combatant.name.lower() == name.lower():
                combatant.max_hp = max_hp
                if current_hp is not None:
                    combatant.current_hp = min(max_hp, current_hp)
                return True
        return False
    
    def edit_initiative(self, name: str, new_initiative: int) -> bool:
        """Edit initiative of a combatant."""
        for combatant in self.combatants:
            if combatant.name.lower() == name.lower():
                combatant.initiative_modifier = new_initiative
                return True
        return False
    
    def save_party(self) -> bool:
        """Save party to JSON file."""
        try:
            data = {
                "party": [combatant_to_json(c) for c in self.combatants],
                "last_saved": datetime.now().isoformat()
            }
            
            with open(self.party_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving party: {e}")
            return False
    
    def load_party(self) -> bool:
        """Load party from JSON file."""
        if not os.path.exists(self.party_file):
            return False
        
        try:
            with open(self.party_file, 'r') as f:
                data = json.load(f)
            
            self.combatants = [create_combatant_from_json(c) for c in data.get("party", [])]
            return True
        except Exception as e:
            print(f"Error loading party: {e}")
            return False
    
    def reset_encounter(self) -> bool:
        """Reset to a new encounter, keeping party definitions."""
        if not os.path.exists(self.party_file):
            return False
        
        try:
            with open(self.party_file, 'r') as f:
                data = json.load(f)
            
            self.combatants = [create_combatant_from_json(c) for c in data.get("party", [])]
            self.round = 1
            self.current_turn_index = -1
            
            return True
        except Exception as e:
            print(f"Error resetting encounter: {e}")
            return False
    
    def display_battle_order(self, show_all: bool = False) -> None:
        """Display the current battle order."""
        print("\n" + "=" * 80)
        print("                    D&D 5E INITIATIVE TRACKER")
        print("=" * 80)
        
        if not self.combatants:
            print("No combatants in battle.")
            return
        
        sorted_combatants = self.get_sorted_combatants()
        
        # Header
        print(f"\n{'Round':<6} {'Position':<12} {'Name':<25} {'AC':<4} {'HP':<10} {'Init':<8}")
        print("-" * 80)
        
        for i, combatant in enumerate(sorted_combatants):
            position = f"{i+1}. " if combatant.is_alive else f"{i+1}. (DEFEATED)"
            
            # Highlight active turn
            if self.current_turn_index == i and combatant.is_alive:
                indicator = " [ACTIVE TURN]"
            elif not combatant.is_alive:
                indicator = ""
            else:
                indicator = ""
            
            print(f"{self.round:<6} {position:<12} {combatant.name:<25} "
                  f"{combatant.ac:<4} {combatant.get_hp_status():<10} "
                  f"{combatant.initiative_modifier:<8}{indicator}")
        
        # Active turn indicator
        active = self.get_active_combatant()
        if active:
            print("-" * 80)
            print(f"Current Turn: {active.name} (Initiative: {active.initiative})")
        
        print("=" * 80 + "\n")
    
    def display_summary(self) -> None:
        """Display a summary of the battle state."""
        alive_count = sum(1 for c in self.combatants if c.is_alive)
        total_combatants = len(self.combatants)
        
        print(f"\nBattle Summary:")
        print(f"  Round: {self.round}")
        print(f"  Alive Combatants: {alive_count}/{total_combatants}")
        print(f"  Active Turn: {self.get_active_combatant().name if self.get_active_combatant() else 'None'}")


def main():
    """Main function to run the initiative tracker."""
    tracker = InitiativeTracker()
    
    # Load existing party if available
    if tracker.load_party():
        print("Loaded existing party from party.json")
    else:
        print("No existing party found. Starting fresh.")
    
    # Add some example combatants
    print("\n--- Adding Combatants ---")
    tracker.add_player("Player 1", initiative=15, ac=16, max_hp=45, current_hp=45)
    tracker.add_player("Player 2", initiative=12, ac=14, max_hp=38, current_hp=38)
    tracker.add_monster("Goblin Scout", initiative_modifier=4, ac=13, max_hp=7)
    tracker.add_monster("Orc Warrior", initiative_modifier=5, ac=16, max_hp=28)
    
    # Display initial state
    tracker.display_battle_order()
    
    print("\n--- Available Commands ---")
    print("  q - Quit")
    print("  n - Next turn")
    print("  p - Previous turn")
    print("  a <name> <damage> - Apply damage")
    print("  h <name> <amount> - Heal")
    print("  t <name> <amount> - Add temp HP")
    print("  c <name> <condition> - Add condition")
    print("  r <name> <condition> - Remove condition")
    print("  e <name> <new_value> - Edit AC/HP/Initiative")
    print("  s - Save party")
    print("  l - Load/reset encounter")
    print("  d - Display all combatants")


if __name__ == "__main__":
    main()
