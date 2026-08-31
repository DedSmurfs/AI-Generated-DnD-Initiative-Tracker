The previous implementation has broken input loops—I cannot add new participants mid-combat, and the edit function does not trigger or work. Let's fix this and upgrade how player data is handled.

Rebuild the Python D&D 5e Initiative Tracker script with the following structure and functionality:
1. Separate Player Persistence (CSV Support)

    Player Database (players.csv):

        Store permanent party stats in a local players.csv file with columns: Name, AC, MaxHP, InitModifier.

        On startup, the program automatically reads players.csv and prompts whether to pull the party into combat.

        Add a helper option or command to quickly append new players to players.csv.

2. Reliable Command Loop & Interactivity (Fixing Add/Edit)

    Fix the Input/Edit Bugs:

        Ensure the program runs a reliable, non-blocking main command loop (e.g., using a prompt loop or clear keyboard navigation menu) so commands are always active and responsive.

        Editing Mid-Combat: Allow selecting a participant by number/index or name to edit any field: Current HP, Temp HP, AC, Initiative, or Condition Tags.

        Adding Mid-Combat: Add a dedicated add command to add reinforcement monsters or new combatants on the fly without breaking the active turn order or round state.

3. Core Combat Tracking Features

    Initiative & Turn Order:

        Prompts for initiative rolls for players (or uses defaults) and auto-rolls initiative for monsters.

        Automatically sorts in descending order (handling ties).

        Keeps track of the active turn and round counter with next / prev controls.

    HP & Status Management:

        Live damage/healing inputs that correctly reduce Temp HP before Current HP.

        Apply/remove status condition tags (e.g., Poisoned, Stunned, Concentrating).

        Clear visual indicator for 0 HP / Unconscious state.

4. Technical Requirements & Linux Usability

    Write the application using Python 3 with rich for formatting.

    Keep the terminal display clear and readable by redrawing the table cleanly on every state change.

    Place all code in a clean file structure with an updated requirements.txt and a example players.csv template.

Please review the input handling logic carefully to guarantee that both add and edit work reliably without freezing or ignoring terminal input.
