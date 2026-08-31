"""Combatant data model for D&D 5e Initiative Tracker."""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class Condition(Enum):
    """Standard D&D 5e conditions."""
    NONE = "None"
    POISONED = "Poisoned"
    STUNNED = "Stunned"
    PRONE = "Prone"
    CONCENTRATING = "Concentrating"
    BLIND = "Blind"
    DEAF = "Deaf"
    FROZEN = "Frozen"
    GRAPPLED = "Grappled"
    PARALYZED = "Paralyzed"
    PETRIFIED = "Petrified"
    RESTRICTED_MOVEMENT = "Restricted Movement"
    ADVANTAGE = "Advantage"
    DISADVANTAGE = "Disadvantage"


@dataclass
class Combatant:
    """Represents a combatant in D&D 5e combat."""
    
    name: str
    initiative_modifier: int
    ac: int
    max_hp: int
    current_hp: int
    temp_hp: int = 0
    conditions: List[Condition] = field(default_factory=list)
    is_alive: bool = True
    
    def __post_init__(self):
        """Ensure HP values are valid."""
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
        if self.current_hp < 0:
            self.current_hp = 0
    
    @property
    def initiative(self) -> int:
        """Get initiative value (roll + modifier)."""
        return self.initiative_modifier
    
    def take_damage(self, damage: int) -> None:
        """Apply damage, absorbing into temp HP first."""
        if not self.is_alive:
            return
        
        # Absorb damage into temp HP first
        temp_hp_needed = min(damage, self.temp_hp)
        self.temp_hp -= temp_hp_needed
        remaining_damage = damage - temp_hp_needed
        
        # Apply remaining damage to current HP
        if remaining_damage > 0:
            self.current_hp -= remaining_damage
        
        # Check for unconsciousness or death
        if self.current_hp <= 0:
            self.current_hp = 0
            self.is_alive = False
    
    def heal(self, amount: int) -> None:
        """Apply healing to current HP."""
        if not self.is_alive:
            return
        
        self.current_hp = min(self.max_hp, self.current_hp + amount)
    
    def add_temp_hp(self, amount: int) -> None:
        """Add temporary hit points."""
        if not self.is_alive:
            return
        
        self.temp_hp += amount
    
    def remove_condition(self, condition: Condition) -> bool:
        """Remove a condition from the combatant."""
        if condition in self.conditions:
            self.conditions.remove(condition)
            return True
        return False
    
    def add_condition(self, condition: Condition) -> None:
        """Add a condition to the combatant."""
        if condition not in self.conditions:
            self.conditions.append(condition)
    
    def get_hp_status(self) -> str:
        """Get HP status string for display."""
        if not self.is_alive:
            return "DEAD"
        
        temp_indicator = f" (Temp: {self.temp_hp})" if self.temp_hp > 0 else ""
        hp_str = f"{self.current_hp}/{self.max_hp}"
        
        if self.current_hp <= 0:
            return f"UNCONSCIOUS ({hp_str}{temp_indicator})"
        elif self.current_hp < self.max_hp // 2:
            return f"DAMAGED ({hp_str}{temp_indicator})"
        else:
            return f"OK ({hp_str}{temp_indicator})"
    
    def get_conditions_display(self) -> str:
        """Get condition string for display."""
        if not self.conditions:
            return ""
        
        cond_names = [c.value for c in self.conditions]
        return " | ".join(cond_names)
    
    def __str__(self) -> str:
        """String representation for display."""
        hp_status = self.get_hp_status()
        conditions = self.get_conditions_display()
        
        status = ""
        if not self.is_alive:
            status = " [DEFEATED]"
        
        return f"{self.name:<25} | AC:{self.ac:<3} | {hp_status:<15} | {conditions}"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"Combatant(name={self.name!r}, initiative={self.initiative_modifier}, ac={self.ac}, hp={self.current_hp}/{self.max_hp})"


def create_combatant_from_json(data: dict) -> Combatant:
    """Create a combatant from JSON data."""
    conditions = []
    for cond in data.get("conditions", []):
        try:
            conditions.append(Condition[cond.upper()])
        except KeyError:
            pass
    
    return Combatant(
        name=data["name"],
        initiative_modifier=data["initiative_modifier"],
        ac=data["ac"],
        max_hp=data["max_hp"],
        current_hp=data.get("current_hp", data["max_hp"]),
        temp_hp=data.get("temp_hp", 0),
        conditions=conditions,
        is_alive=data.get("is_alive", True)
    )


def combatant_to_json(combatant: Combatant) -> dict:
    """Convert combatant to JSON-serializable dict."""
    return {
        "name": combatant.name,
        "initiative_modifier": combatant.initiative_modifier,
        "ac": combatant.ac,
        "max_hp": combatant.max_hp,
        "current_hp": combatant.current_hp,
        "temp_hp": combatant.temp_hp,
        "conditions": [c.value for c in combatant.conditions],
        "is_alive": combatant.is_alive
    }
