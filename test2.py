import pygetwindow as gw
from pywinauto import Application

class WindowManager:
    def __init__(self):
        pass

    def list_windows(self):
        """List all open windows."""
        windows = gw.getAllTitles()
        return [win for win in windows if win]  # Filter out empty window titles

    def get_window(self, window_title):
        """Get a window by title."""
        window = gw.getWindowsWithTitle(window_title)
        if window:
            return window[0]
        else:
            raise Exception(f"No window found with title: {window_title}")

    def minimize_window(self, window_title):
        """Minimize a window by its title."""
        window = self.get_window(window_title)
        window.minimize()

    def maximize_window(self, window_title):
        """Maximize a window by its title."""
        window = self.get_window(window_title)
        window.maximize()

    def close_window(self, window_title):
        """Close a window by its title."""
        app = Application().connect(title=window_title)
        app.window(title=window_title).close()

    def list_and_manipulate(self):
        """List open windows, let the user select one, and then manipulate it."""
        open_windows = self.list_windows()
        if not open_windows:
            print("No open windows found.")
            return
        
        print("Open Windows:")
        for idx, title in enumerate(open_windows):
            print(f"{idx + 1}. {title}")
        
        window_index = int(input(f"Select a window by entering its number (1-{len(open_windows)}): ")) - 1
        if window_index < 0 or window_index >= len(open_windows):
            print("Invalid window selection.")
            return

        window_title = open_windows[window_index]
        print(f"You selected: {window_title}")
        
        action = input("Enter the action you want to perform (minimize, maximize, restore, move, resize, close): ").lower()

        try:
            if action == 'minimize':
                self.minimize_window(window_title)
                print(f"Minimized {window_title}.")
            elif action == 'maximize':
                self.maximize_window(window_title)
                print(f"Maximized {window_title}.")
            elif action == 'close':
                self.close_window(window_title)
                print(f"Closed {window_title}.")
            else:
                print("Invalid action choice.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    wm = WindowManager()
    wm.list_and_manipulate()
