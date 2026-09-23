*DISCLAIMER*
I am not a programmer. This is vibe coded completely. That was the experiment. I did this to prove that I could vibe code.

# === Initial Attempt ===

I wanted to see what locally hosted AI could generate in terms of a python initiative tracker for DnD battles

Used Gemma4 to generate a prompt to feed into Aider which was configured to use Qwen3.5:latest through Ollama on my personal rig.

<img width="1201" height="619" alt="Screenshot" src="https://github.com/user-attachments/assets/bf95de29-9a10-4896-9593-fec8ef716ac9" />


# === Tried again ===

This time, I used a mix of Gemma4 and Qwen 2.5 Coder via my personal hermes agent.

Gave it the basic idea to create an initiative battle tracker for D&D 5e and had it go! Few little clarifications to add Damage and healing and some small tweaks made myself to fix some syntax and other basic things. This time, I wanted to make it prettier as well so I chose to use Textual.

Final draft uploaded in the folder titled Final

## Requirements
Python
  `<package_manager> install python`
Python Textual
  `pip install textual`

## To Run
- Open terminal
- Navigate to your directory with the init_tracker.py file
- Run `python3 init_tracker.py`


<img width="1196" height="602" alt="image" src="https://github.com/user-attachments/assets/97ab344a-ce5f-4a29-b11a-16aab8048ccd" />

### In App Controls
a - Add a player </br>
e - Add an Enemy </br>
d - Damage the currently selected Player/Enemy </br>
h - Heal or Overheal the currently selected Player/Enemy </br>
r - Reset the field (This resets all the enemies and resets the Overhealing to players) </br>
q - Quit the App (This will reset your players as well)
