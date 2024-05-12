import time
import ctypes
import psutil
import win32gui
import win32process
from pypresence import Presence

class Qobuz:
    def __init__(self, process_name="Qobuz.exe"):
        self.process_name = process_name

    def running_pids(self):
        """Generator that yields PIDs for all running instances of Qobuz."""
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == self.process_name:
                yield proc.pid

    def visible_windows(self, pid):
        """Generator that yields handles to all visible windows for a given PID."""
        def callback(hwnd, hwnds):
            _, win_pid = win32process.GetWindowThreadProcessId(hwnd)
            if win_pid == pid and ctypes.windll.user32.IsWindowVisible(hwnd):
                hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        for hwnd in hwnds:
            yield hwnd

    def get_titles(self, hwnd):
        """Retrieve the window title from a window handle."""
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff.value

    def get_valid_titles(self):
        """Generator that yields valid titles from all visible windows of running Qobuz processes."""
        for pid in self.running_pids():
            for hwnd in self.visible_windows(pid):
                title = self.get_titles(hwnd)
                if title and " - " in title and title != "Qobuz":
                    yield title


class DiscordRPC:
    def __init__(self, client_id="928957672907227147"):
        self.rpc = Presence(client_id)
        self.rpc.connect()
        self.current_song = {}

    def update_presence(self, song):
        if song != self.current_song:
            self.rpc.update(details=song['title'], state=f"by {song['artist']}", large_image="qobuz")
            print(f"Updated: {song['title']} - by {song['artist']}")
            self.current_song = song
        elif not song or song['title'] == "Qobuz":
            self.rpc.clear()
            print("Cleared Discord presence due to lack of title or default title.")

def main():
    qobuz = Qobuz()
    discord = DiscordRPC()
    while True:
        for title in qobuz.get_valid_titles():
            details, state = title.split(" - ", 1)
            discord.update_presence({'title': details, 'artist': state})
        time.sleep(5)

if __name__ == "__main__":
    main()
