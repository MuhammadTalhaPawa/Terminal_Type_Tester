#!/usr/bin/env python3
"""
Terminal Typing Test Game - Simple Version
Uses ANSI escape codes, no curses library required
All output remains in terminal after completion
"""

import sys
import time
import random
import threading
import os

# Platform-specific imports for keyboard input
if os.name == 'nt':  # Windows
    import msvcrt
else:  # Unix/Linux/Mac
    import termios
    import tty

# ANSI Color Codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_WHITE = '\033[47m'

# Word list
WORD_LIST = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
    "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
    "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
    "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
    "even", "new", "want", "because", "any", "these", "give", "day", "most", "us",
    "python", "code", "programming", "terminal", "typing", "speed", "test", "game", "cursor", "ghost",
    "quick", "brown", "fox", "jump", "lazy", "dog", "keyboard", "screen",
    "monitor", "mouse", "laptop", "window", "system", "input", "output",
    "error", "debug", "function", "variable", "loop", "list", "string",
    "number", "boolean", "random", "import", "print", "while", "break",
    "continue", "return", "class", "object", "method", "value", "true",
    "false", "start", "stop", "reset", "score", "level", "player",
    "enemy", "challenge", "practice", "focus", "learn", "build",
    "create", "design", "develop", "improve", "fast", "slow",
    "accuracy", "reaction", "skill", "challenge", "press", "enter",
    "space", "shift", "control", "escape", "tab", "command",
    "power", "logic", "data", "file", "folder", "network",
    "internet", "server", "client", "cloud", "secure", "login"
]

class KeyboardInput:
    """Handle keyboard input for different platforms"""
    
    def __init__(self):
        self.is_windows = os.name == 'nt'
        if not self.is_windows:
            self.old_settings = None
    
    def __enter__(self):
        if not self.is_windows:
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        return self
    
    def __exit__(self, *args):
        if not self.is_windows and self.old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
    
    def kbhit(self):
        """Check if a key has been pressed"""
        if self.is_windows:
            return msvcrt.kbhit()
        else:
            import select
            return select.select([sys.stdin], [], [], 0)[0] != []
    
    def getch(self):
        """Get a single character"""
        if self.is_windows:
            if msvcrt.kbhit():
                char = msvcrt.getch()
                # Handle special keys
                if char == b'\xe0' or char == b'\x00':  # Special key prefix
                    msvcrt.getch()  # Consume the second byte
                    return None
                try:
                    return char.decode('utf-8')
                except:
                    return None
            return None
        else:
            if self.kbhit():
                char = sys.stdin.read(1)
                # Handle escape sequences
                if char == '\x1b':
                    if self.kbhit():
                        sys.stdin.read(1)  # Consume [
                        if self.kbhit():
                            sys.stdin.read(1)  # Consume the rest
                    return None
                return char
            return None

class TypingTest:
    def __init__(self):
        self.duration = 60  # seconds
        self.words = [random.choice(WORD_LIST) for _ in range(200)]
        self.current_word_index = 0
        self.current_input = ""
        self.typed_words = []
        self.start_time = None
        self.running = True
        self.time_remaining = self.duration
        self.total_chars_typed = 0
    
    def calculate_stats(self):
        """Calculate WPM, CPM, and accuracy"""
        if not self.typed_words:
            return 0, 0, 0
        
        # Calculate actual elapsed time
        if self.start_time:
            elapsed = min(time.time() - self.start_time, self.duration)
        else:
            elapsed = self.duration
        
        if elapsed == 0:
            elapsed = 0.1  # Prevent division by zero
        
        words_typed = len(self.typed_words)
        wpm = (words_typed / elapsed) * 60
        cpm = (self.total_chars_typed / elapsed) * 60
        
        # Calculate accuracy
        correct_chars = 0
        total_chars = 0
        
        for typed, target in self.typed_words:
            total_chars += len(typed)
            for i in range(min(len(typed), len(target))):
                if typed[i] == target[i]:
                    correct_chars += 1
        
        accuracy = (correct_chars / total_chars * 100) if total_chars > 0 else 0
        
        return wpm, cpm, accuracy
    
    def timer_thread(self):
        """Background thread to update timer"""
        while self.running:
            if self.start_time:
                elapsed = time.time() - self.start_time
                self.time_remaining = max(0, self.duration - elapsed)
                if self.time_remaining <= 0:
                    self.running = False
                    break
            time.sleep(0.1)
    
    def display_current_state(self):
        """Display the current typing state - updates in place"""
        # Save cursor position and clear from here down
        print('\033[s', end='')  # Save cursor position
        
        # Stats at the top
        words_typed = len(self.typed_words)
        if self.start_time and words_typed > 0:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                current_wpm = (words_typed / elapsed) * 60
                current_cpm = (self.total_chars_typed / elapsed) * 60
                stats_text = f"WPM: {current_wpm:.1f} | CPM: {current_cpm:.1f} | Words: {words_typed}"
            else:
                stats_text = "WPM: 0.0 | CPM: 0.0 | Words: 0"
        else:
            stats_text = "WPM: 0.0 | CPM: 0.0 | Words: 0"
        
        print(f"\r{Colors.GREEN}{Colors.BOLD}{stats_text}{Colors.RESET}{'':50}", end='')
        
        # Timer line below stats
        if self.start_time:
            timer_text = f"Time: {self.time_remaining:.1f}s"
        else:
            timer_text = "Time: 60.0s (Timer starts when you type)"
        print(f"\n{Colors.CYAN}{timer_text}{Colors.RESET}{'':50}", end='')
        
        print(f"\n{'─' * 80}", end='')
        
        # More spacing before typing area
        print(f"\n\n\n", end='')
        
        target_word = self.words[self.current_word_index]
        
        # Show current word being typed
        print(f"\r{Colors.BOLD}{Colors.WHITE}", end='')
        
        # Display the typed portion with colors
        for i, char in enumerate(self.current_input):
            if i < len(target_word):
                if char == target_word[i]:
                    print(f"{Colors.GREEN}{char}", end='')
                else:
                    print(f"{Colors.RED}{char}", end='')
            else:
                print(f"{Colors.RED}{char}", end='')
        
        # Display remaining part of target word in dim
        if len(self.current_input) < len(target_word):
            remaining = target_word[len(self.current_input):]
            print(f"{Colors.DIM}{remaining}", end='')
        
        print(f"{Colors.RESET} ", end='')
        
        # Display ghost words (upcoming words) on the same line
        next_words = self.words[self.current_word_index + 1:self.current_word_index + 10]
        ghost_text = " ".join(next_words)
        print(f"{Colors.DIM}{ghost_text}{Colors.RESET}{'':50}", end='')
        
        # Instructions at bottom
        print(f"\n\n\n{'─' * 80}", end='')
        print(f"\n{Colors.DIM}SPACE=submit | BACKSPACE=delete | ESC=quit{Colors.RESET}{'':50}", end='')
        
        # Restore cursor position
        print('\033[u', end='', flush=True)
    
    def run(self):
        """Main game loop"""
        # Enable ANSI colors on Windows
        if os.name == 'nt':
            os.system('')
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║     TERMINAL TYPING SPEED TEST            ║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════╝{Colors.RESET}\n")
        
        print(f"{Colors.YELLOW}Instructions:{Colors.RESET}")
        print("• Type the word shown (green=correct, red=wrong)")
        print("• Ghost words show what's coming next")
        print("• Press SPACE to submit and move to next word")
        print("• BACKSPACE to correct mistakes in current word")
        print(f"\n{Colors.GREEN}Start typing to begin the 60-second test!{Colors.RESET}")
        
        input(f"{Colors.DIM}Press ENTER to see the words...{Colors.RESET}")
        
        with KeyboardInput() as kb:
            print("\n" + "=" * 80 + "\n")
            
            # Reserve space for the display (10 lines for new layout)
            print("\n" * 9)
            
            # Move cursor up to the display area
            print("\033[10A", end='', flush=True)
            
            # Show initial display (timer not started yet)
            self.display_current_state()
            
            last_update = time.time()
            timer_started = False
            
            # Main game loop
            while self.running:
                # Update display every 100ms for timer (only if started)
                if timer_started:
                    current_time = time.time()
                    if current_time - last_update >= 0.1:
                        self.display_current_state()
                        last_update = current_time
                    
                    # Check if time is up
                    if self.time_remaining <= 0:
                        break
                
                if kb.kbhit():
                    char = kb.getch()
                    
                    if char is None:
                        continue
                    
                    # Handle ESC (exit)
                    if char == '\x1b' or ord(char) == 27:
                        self.running = False
                        break
                    
                    # Handle SPACE (submit word)
                    elif char == ' ':
                        target_word = self.words[self.current_word_index]
                        self.typed_words.append((self.current_input, target_word))
                        self.total_chars_typed += len(self.current_input)
                        
                        self.current_word_index += 1
                        self.current_input = ""
                        
                        if self.current_word_index >= len(self.words):
                            break
                        
                        # Update display
                        self.display_current_state()
                    
                    # Handle BACKSPACE
                    elif char in ('\x7f', '\x08', '\b'):
                        if len(self.current_input) > 0:
                            self.current_input = self.current_input[:-1]
                            # Update display
                            self.display_current_state()
                    
                    # Handle regular characters
                    elif len(char) == 1 and 32 <= ord(char) <= 126:
                        # Start timer on first character typed
                        if not timer_started:
                            self.start_time = time.time()
                            timer = threading.Thread(target=self.timer_thread, daemon=True)
                            timer.start()
                            timer_started = True
                        
                        self.current_input += char
                        # Update display
                        self.display_current_state()
                
                time.sleep(0.01)  # Small delay to prevent CPU spinning
            
            self.running = False
            
            # Move cursor past the display area
            print("\n" * 11)
        
        # Show results
        self.show_results()
    
    def show_results(self):
        """Display final results"""
        wpm, cpm, accuracy = self.calculate_stats()
        
        # Calculate actual time taken
        if self.start_time:
            actual_time = min(time.time() - self.start_time, self.duration)
        else:
            actual_time = 0
        
        print("\n" + "=" * 80)
        print(f"{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║          TYPING TEST RESULTS              ║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════╝{Colors.RESET}\n")
        
        print(f"{Colors.YELLOW}Time Taken:{Colors.RESET} {actual_time:.1f} seconds")
        print(f"{Colors.YELLOW}Words Typed:{Colors.RESET} {len(self.typed_words)}")
        print(f"{Colors.YELLOW}Characters Typed:{Colors.RESET} {self.total_chars_typed}")
        print()
        print(f"{Colors.GREEN}{Colors.BOLD}Words Per Minute (WPM):{Colors.RESET} {Colors.GREEN}{wpm:.2f}{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}Characters Per Minute (CPM):{Colors.RESET} {Colors.GREEN}{cpm:.2f}{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}Accuracy:{Colors.RESET} {Colors.GREEN}{accuracy:.2f}%{Colors.RESET}")
        
        print("\n" + "=" * 80)
        
        # Performance rating
        if wpm >= 60:
            rating = "🔥 EXCELLENT!"
            color = Colors.GREEN
        elif wpm >= 40:
            rating = "👍 GOOD!"
            color = Colors.CYAN
        elif wpm >= 20:
            rating = "📝 KEEP PRACTICING!"
            color = Colors.YELLOW
        else:
            rating = "💪 ROOM FOR IMPROVEMENT!"
            color = Colors.YELLOW
        
        print(f"\n{color}{Colors.BOLD}{rating}{Colors.RESET}\n")

def main():
    try:
        game = TypingTest()
        game.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test interrupted!{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}\n")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
