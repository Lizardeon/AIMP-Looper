import time
import threading
import os
import sys
from pyaimp import Client, PlayBackState

class AimpLooper:
    def __init__(self, config_file):
        try:
            self.client = Client()
        except RuntimeError as e:
            print(f"Error: {e}")
            sys.exit(1)

        self.config_file = config_file
        self.tracks_data = {}  # Storage: { 'Track Title': [list of loops] }
        self.current_track = ""
        self.active_loops = []
        
        self.current_idx = 0   # Index of the loop currently playing
        self.next_idx = 0      # Index of the loop to transition to next
        self.running = True

        self.load_config()

    def parse_time(self, t_str):
        # Converts MM:SS.mmm to milliseconds
        try:
            t_str = t_str.strip()
            # Split by dot into (minutes:seconds) and (milliseconds)
            min_sec, ms = t_str.split('.')
            minutes, seconds = min_sec.split(':')
            return (int(minutes) * 60000) + (int(seconds) * 1000) + int(ms)
        except Exception:
            return 0

    def load_config(self):
        # Parses the loops.txt file
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.write("// Format: # Track Title\n// 00:01.000 | 00:05.000 | Loop Name\n")
            return

        new_data = {}
        last_track = None

        with open(self.config_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('//'):
                    continue
                
                # Lines starting with # are track titles
                if line.startswith('#'):
                    last_track = line[1:].strip()
                    new_data[last_track] = []
                    continue
                
                # Lines with pipe separators are loop data
                if '|' in line and last_track:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        new_data[last_track].append({
                            'start': self.parse_time(parts[0]),
                            'end': self.parse_time(parts[1]),
                            'name': parts[2].strip()
                        })
        
        self.tracks_data = new_data
        print(f"[SYSTEM] Config updated. Tracks in database: {len(self.tracks_data)}")

    def monitor_aimp(self):
        # Background thread to monitor playback position
        while self.running:
            try:
                # 1. Check what's playing
                info = self.client.get_current_track_info()
                title = info.get('title', 'Unknown')

                # If track changed, load new loops
                if title != self.current_track:
                    self.current_track = title
                    self.active_loops = self.tracks_data.get(title, [])
                    self.current_idx = 0
                    self.next_idx = 0
                
                # 2. If loops exist and player is playing
                if self.active_loops and self.client.get_playback_state() == PlayBackState.Playing:
                    pos = self.client.get_player_position()
                    current_loop = self.active_loops[self.current_idx]

                    # If current position exceeds loop end boundary
                    if pos >= current_loop['end']:
                        # Transition: apply the user-selected next loop
                        self.current_idx = self.next_idx
                        target_pos = self.active_loops[self.current_idx]['start']
                        self.client.set_player_position(target_pos)

                time.sleep(0.05) # Poll frequency (50ms)
            except Exception:
                time.sleep(1)

    def run(self):
        # Start background process
        threading.Thread(target=self.monitor_aimp, daemon=True).start()

        while self.running:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=== AIMP LOOPER ===")
            print(f"Current Track: {self.current_track}")
            print("-" * 25)

            if not self.active_loops:
                print("No loops found for this track.")
            else:
                for i, lp in enumerate(self.active_loops):
                    prefix = ">>" if i == self.current_idx else "  "
                    suffix = " (NEXT)" if i == self.next_idx and i != self.current_idx else ""
                    print(f"{prefix} [{i+1}] {lp['name']} ({lp['start']}ms -> {lp['end']}ms){suffix}")

            print("-" * 25)
            print("CONTROLS: [Number] - Select Loop | [R] - Reload File | [Q] - Quit")
            
            cmd = input("\nCommand: ").strip().lower()

            if cmd == 'q':
                self.running = False
            elif cmd == 'r':
                self.load_config()
            elif cmd.isdigit():
                val = int(cmd) - 1
                if 0 <= val < len(self.active_loops):
                    self.next_idx = val
                    print(f"Waiting for cycle to finish before switching to {val+1}...")
                else:
                    print("Invalid loop number!")
                    time.sleep(1)

if __name__ == "__main__":
    looper = AimpLooper('loops.txt')
    looper.run()
