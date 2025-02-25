# Import required libraries for automation and timing
import pyautogui
import time
import keyboard

class CraftingConfig:
    def __init__(self):
        # Coordinates for the "Pull Materials" button in crafting interface
        self.pull_button_x = 1042  # X coordinate of the Pull button
        self.pull_button_y = 453   # Y coordinate of the Pull button
        
        # Dictionary storing screen coordinates for each craftable item
        # These coordinates are set using the get_item_position function
        self.item_positions = {
            'advanced_rifle_bullets': {'x': 0, 'y': 0},  # Coordinates in Fabricator
            'gunpowder': {'x': 0, 'y': 0},              # Coordinates in Chemistry Bench
            'cementing_paste': {'x': 0, 'y': 0},        # Coordinates in Chemistry Bench
            'sparkpowder': {'x': 0, 'y': 0}             # Coordinates in Chemistry Bench
        }
        
        # Delay settings for various actions
        self.craft_delay = 0.1        # Time between craft button presses
        self.interface_delay = 0.5    # Time to wait for interfaces to open/close
        self.movement_delay = 0.1     # Delay between movement actions

class ARKCrafter:
    def __init__(self, config: CraftingConfig = None):
        self.config = config or CraftingConfig()
        pyautogui.PAUSE = 0.5         # Set global delay between PyAutoGUI commands
        pyautogui.FAILSAFE = True     # Enable failsafe (move mouse to corner to stop)

    def move_to_next(self):
        """Moves character to the next crafting station"""
        try:
            # Align character forward briefly
            pyautogui.press('w')
            time.sleep(0.025)
            
            # Move right to next station
            pyautogui.keyDown('d')    # Start moving right
            time.sleep(0.025)           # Duration of movement
            pyautogui.keyUp('d')      # Stop moving right
            time.sleep(0.025)           # Pause before next action
        except Exception as e:
            print(f"Error moving to next station: {e}")
            pyautogui.keyUp('d')      # Ensure 'd' key is released on error

    def return_to_start(self, num_crafters: int):
        """Returns character to the first crafting station"""
        try:
            # Align character forward
            pyautogui.press('w')
            time.sleep(0.05)
            
            # Calculate total return movement time
            return_time = num_crafters * 1.1  # Time based on number of stations
            
            # Break movement into segments for smoothness
            segments = 4
            segment_time = return_time / segments
            
            # Execute movement in short bursts
            for _ in range(segments):
                pyautogui.keyDown('a')
                time.sleep(4.0)
                pyautogui.keyUp('a')
                time.sleep(0.05)
        except Exception as e:
            print(f"Error returning to start: {e}")
            pyautogui.keyUp('a')      # Ensure 'a' key is released on error

    def run_crafting_loop(self, item: str, num_crafters: int):
        """Main crafting loop with status tracking and error recovery"""
        # Print initial instructions and controls
        print(f"\nStarting crafting loop for {item} with {num_crafters} crafters")
        print("Press 'q' to stop the script")
        print("Move mouse to corner of screen for emergency stop")
        print("Controls:")
        print("- Press 'Q' to stop")
        print("- Press 'P' to pause/resume")
        print("- Press '+' to increase movement speed")
        print("- Press '-' to decrease movement speed")
        
        # Initialize tracking variables
        crafting_session = {
            'total_cycles': 0,
            'successful_crafts': 0,
            'failed_crafts': 0
        }

        paused = False
        movement_multiplier = 1.0    # Movement speed multiplier

        try:
            # Main loop - continues until 'q' is pressed
            while not keyboard.is_pressed('q'):
                # Handle pause toggle
                if keyboard.is_pressed('p'):
                    paused = not paused
                    print("Script PAUSED" if paused else "Script RESUMED")
                    time.sleep(0.5)  # Prevent multiple toggles
                    continue
                
                # Handle movement speed adjustments
                if keyboard.is_pressed('+'):
                    movement_multiplier *= 1.2
                    print(f"Movement speed increased: {movement_multiplier:.2f}x")
                    time.sleep(0.2)
                elif keyboard.is_pressed('-'):
                    movement_multiplier /= 1.2
                    print(f"Movement speed decreased: {movement_multiplier:.2f}x")
                    time.sleep(0.2)

                # Update movement timing
                self.move_time = 0.1 * movement_multiplier
                
                # Skip if paused
                if paused:
                    time.sleep(0.1)
                    continue

                # Start new crafting cycle
                crafting_session['total_cycles'] += 1
                print(f"\nStarting cycle {crafting_session['total_cycles']}")
                
                # Process each crafting station
                for i in range(num_crafters):
                    try:
                        print(f"Crafting at station {i+1}/{num_crafters}")
                        self.craft_at_station(item)
                        crafting_session['successful_crafts'] += 1
                        
                        # Move to next station if not at last one
                        if i < num_crafters - 1:
                            self.move_to_next()
                    except Exception as e:
                        print(f"Error at station {i+1}: {e}")
                        crafting_session['failed_crafts'] += 1
                        # Attempt recovery
                        pyautogui.press('esc')
                        time.sleep(0.5)
                
                # Return to starting position
                print("\nReturning to first station...")
                self.return_to_start(num_crafters)
                
                # Display current statistics
                print(f"\nSession Stats:")
                print(f"Cycles completed: {crafting_session['total_cycles']}")
                print(f"Successful crafts: {crafting_session['successful_crafts']}")
                print(f"Failed crafts: {crafting_session['failed_crafts']}")
        
        except KeyboardInterrupt:
            print("\nStopping crafting loop...")
        except Exception as e:
            print(f"Critical error in crafting loop: {e}")
        finally:
            # Display final statistics
            print("\nFinal Session Statistics:")
            print(f"Total cycles: {crafting_session['total_cycles']}")
            print(f"Total successful crafts: {crafting_session['successful_crafts']}")
            print(f"Total failed crafts: {crafting_session['failed_crafts']}")

    def craft_at_station(self, item: str):
        """Handles the crafting process at a single station"""
        max_retries = 3  # Number of retry attempts for failed crafts
        for attempt in range(max_retries):
            try:
                # Step 1: Open crafting interface
                print("Opening bench...")
                pyautogui.press('f')           # Interaction key
                time.sleep(0.5)                # Wait for interface

                # Step 2: Select item to craft
                print("Selecting item...")
                item_pos = self.config.item_positions[item]
                pyautogui.click(item_pos['x'], item_pos['y'])
                time.sleep(0.4)

                # Step 3: Pull required materials
                print("Pulling materials...")
                pyautogui.click(self.config.pull_button_x, self.config.pull_button_y)
                time.sleep(0.4)

                # Step 4: Click item again to ensure it's selected
                print("Re-selecting item...")
                pyautogui.click(item_pos['x'], item_pos['y'])
                time.sleep(0.4)

                # Step 5: Craft items (10 times)
                print("Crafting 10 items...")
                for i in range(10):
                    pyautogui.press('a')       # Craft key
                    time.sleep(0.05)            # Craft delay
                    print(f"Crafted item {i+1}/10")

                # Step 6: Wait for animations
                time.sleep(0.5)

                # Step 7: Close interface
                print("Closing interface...")
                pyautogui.press('esc')
                time.sleep(0.4)
                return  # Success - exit function

            except Exception as e:
                print(f"Error on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    pyautogui.press('esc')     # Try to close interface
                    time.sleep(1)
                else:
                    raise  # Max retries reached

def get_item_position(item_name: str):
    """Captures screen coordinates for items in crafting interface"""
    print(f"\nOpen the crafter and move your mouse to the {item_name} icon")
    print("You have 5 seconds...")
    time.sleep(5)                     # Wait for mouse positioning
    x, y = pyautogui.position()       # Capture coordinates
    print(f"Coordinates captured: X={x}, Y={y}")
    return x, y

def configure_delays(config: CraftingConfig):
    """Allows customization of timing delays"""
    print("\nCurrent delay settings (in seconds):")
    print(f"1. Interface open delay: {config.interface_delay}")
    print(f"2. Craft delay: {config.craft_delay}")
    print(f"3. Movement delay: {config.movement_delay}")
    
    if input("\nWould you like to adjust delays? (y/n): ").lower() == 'y':
        try:
            # Get user input for delays, use defaults if empty
            config.interface_delay = float(input("Enter interface delay (default 1.2): ") or 1.2)
            config.craft_delay = float(input("Enter craft delay (default 0.2): ") or 0.2)
            config.movement_delay = float(input("Enter movement delay (default 0.1): ") or 0.1)
        except ValueError:
            print("Invalid input, using default values")

def main():
    """Main program entry point"""
    print("ARK Crafting Automation Script")
    print("=============================")

    # Initialize configuration
    config = CraftingConfig()

    # Configure item positions if requested
    print("\nDo you want to set item positions? (y/n)")
    if input().lower() == 'y':
        print("\nWe'll capture the position of each item in the crafting interfaces.")
        print("Make sure you have access to both a Fabricator and Chemistry Bench.")
        
        # Configure Fabricator items
        print("\nFor Fabricator:")
        x, y = get_item_position("Advanced Rifle Bullets")
        config.item_positions['advanced_rifle_bullets'] = {'x': x, 'y': y}
        
        # Configure Chemistry Bench items
        print("\nFor Chemistry Bench:")
        for item in ['gunpowder', 'cementing_paste', 'sparkpowder']:
            x, y = get_item_position(item)
            config.item_positions[item] = {'x': x, 'y': y}
        
        print("\nItem positions captured!")

    try:
        # Configure timing delays
        configure_delays(config)
        crafter = ARKCrafter(config)

        # Select crafting station
        print("\nSelect crafting station:")
        print("1. Fabricator")
        print("2. Chemistry Bench")
        station_choice = input("\nEnter number (1-2): ")

        # Define available items for each station
        fabricator_items = {
            '1': 'advanced_rifle_bullets'
        }

        chemistry_items = {
            '1': 'gunpowder',
            '2': 'sparkpowder',
            '3': 'cementing_paste'
        }

        # Display appropriate crafting options based on station choice
        if station_choice == '1':
            print("\nWhat would you like to craft in Fabricator?")
            print("1. Advanced Rifle Bullets")
            items = fabricator_items
        elif station_choice == '2':
            print("\nWhat would you like to craft in Chemistry Bench?")
            print("1. Gunpowder")
            print("2. Sparkpowder")
            print("3. Cementing Paste")
            items = chemistry_items
        else:
            print("Invalid station choice!")
            return

        # Get item choice
        choice = input("\nEnter number (1-3): ")
       
        if choice not in items:
            print("Invalid choice!")
            return

        # Get number of crafting stations
        while True:
            try:
                num_crafters = int(input("\nHow many crafters in the line? "))
                if num_crafters > 0:
                    break
                print("Please enter a number greater than 0")
            except ValueError:
                print("Please enter a valid number")

        # Final setup instructions
        print("\nPreparing to start:")
        print("1. Position your character at the first crafter")
        print("2. Make sure you have materials in storage")
        print("3. Make sure you have Walls next to the first crafter and after the last crafter so your character can move between them without going out of the crafting stations position")
        print("4. Ensure your game window is active")
        input("\nPress Enter when ready...")

        # Countdown before starting
        print("\nStarting in:")
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        # Start crafting loop
        crafter.run_crafting_loop(items[choice], num_crafters)

    except Exception as e:
        print(f"\nError: {e}")
        print("Script terminated")

if __name__ == "__main__":
    main() 