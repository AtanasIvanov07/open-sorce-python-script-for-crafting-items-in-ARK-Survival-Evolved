# open-sorce-python-script-for-crafting-items-in-ARK-Survival-Evolved
ARK Crafting Automation Script is a Python-based tool designed to automate the crafting process in ARK by simulating keyboard and mouse actions. This script streamlines repetitive tasks by automating interactions at multiple crafting stations—such as the Fabricator and Chemistry Bench—while offering configurable delays.
# ARK Crafting Automation Script

This repository contains a Python automation script designed to simplify the crafting process in ARK by simulating keyboard and mouse actions. The script automates crafting at multiple stations (such as the Fabricator and Chemistry Bench) by performing a series of actions including moving between stations, opening interfaces, and crafting items.

## Features

- **Automated Crafting Loop**: Cycle through multiple crafting stations and craft items continuously.
- **Configurable Item Positions**: Capture and store screen coordinates for various items in the crafting interface.
- **Customizable Delays**: Adjust timing settings for interface interactions, crafting actions, and movement.
- **Real-Time Controls**: Pause/resume the script, adjust movement speed, or terminate the automation using hotkeys.
- **Error Handling & Recovery**: Built-in retry logic and error management to handle failed crafting attempts.

## Requirements

- Python 3.x
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)
- [keyboard](https://github.com/boppreh/keyboard)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/ark-crafting-automation.git
   cd ark-crafting-automation
