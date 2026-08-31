Build a simple, interactive D&D 5e Initiative Tracker in Python designed to run in a Linux terminal.
Key Requirements

    Tech Stack & Libraries:

        Built with Python 3.

        Use rich or prompt_toolkit for a clean, highly readable, and easily navigable terminal user interface (TUI).

    Core Features:

        Participant Management:

            Add players and monsters with: Name, Initiative Roll/Modifier, Armor Class (AC), Max HP, Current HP, and Temporary HP.

            Option to automatically roll initiative for monsters using their modifier while accepting explicit initiative values for players.

        Initiative Order & Turn Tracking:

            Automatically sort participants in descending initiative order (handling ties cleanly).

            Active turn indicator showing whose turn it currently is.

            Advance (Next) or step back (Previous) turns, incrementing/decrementing a Round Counter automatically.

        HP, Temp HP & Health Status:

            Real-time HP tracking (apply damage/healing directly to Current or Temp HP).

            Automatically absorb damage into Temp HP before depleting Current HP.

            Visual indicators for unconsciousness (0 HP) or death.

        Status Condition Tags:

            Add, view, and clear standard D&D 5e condition tags (e.g., Poisoned, Stunned, Prone, Concentrating, Advantage/Disadvantage).

            Display active tags next to the character in the combat list.

        Live Mid-Combat Editing:

            Quick keyboard shortcuts or single-key commands to edit AC, HP, Temp HP, Conditions, or Initiative values on the fly.

            Ability to remove defeated monsters or add new combatants mid-encounter (e.g., reinforcements).

        Party Persistence & Encounter Setup:

            Save player profiles (Name, AC, Max HP) to a local JSON file so party stats persist between sessions.

            Fast reset command to start a new encounter without re-typing player details.

    Linux Compatibility & Usability:

        Ensure screen updates are smooth using terminal clearing or live table rendering.

        Keep interactions fast and low-friction so running combat during a session requires minimal typing.

Please organize the project cleanly, include a requirements.txt file for dependencies, and provide the command to launch the app.
