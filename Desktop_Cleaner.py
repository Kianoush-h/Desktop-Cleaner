
from time import sleep
from watchdog.observers import Observer
import shutil
from datetime import date
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from ext import extension_paths
from win10toast import ToastNotifier 

def add_date_to_path(path: Path):
    dated_path = path / f'{date.today().year}' / f'{date.today().month:02d}'
    dated_path.mkdir(parents=True, exist_ok=True)
    return dated_path


def rename_file(source: Path, destination_path: Path):
    if Path(destination_path / source.name).exists():
        increment = 0

        while True:
            increment += 1
            new_name = destination_path / f'{source.stem}_{increment}{source.suffix}'

            if not new_name.exists():
                return new_name
    else:
        return destination_path / source.name


class EventHandler(FileSystemEventHandler):
    def __init__(self, watch_path: Path, destination_root: Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

    def on_modified(self, event):
        for child in self.watch_path.iterdir():
            # skips directories and non-specified extensions
            if child.is_file() and child.suffix.lower() in extension_paths:
                destination_path = self.destination_root / extension_paths[child.suffix.lower()]
                destination_path = add_date_to_path(path=destination_path)
                destination_path = rename_file(source=child, destination_path=destination_path)
                shutil.move(src=child, dst=destination_path)
                
                result = 'File is moved to:\n' + str(destination_path)
                toaster.show_toast("Desktop Cleaner", result, duration = 5, icon_path="icon1.ico", threaded=True) 




if __name__ == '__main__':
    toaster = ToastNotifier() 
    
    watch_path = Path.home() / 'Desktop/aa/'
    # watch_path = 'C:/Users/Admin/Desktop/aa'
    
    destination_root = Path.home() / 'Desktop/bb/'
    # destination_root = 'C:/Users/Admin/Desktop/bb'
    
    event_handler = EventHandler(watch_path=watch_path, destination_root=destination_root)

    observer = Observer()
    observer.schedule(event_handler, f'{watch_path}', recursive=True)
    observer.start()
    
    result = 'Desktop cleaner is on'
    toaster.show_toast("Desktop Cleaner", result, duration = 5, icon_path="icon1.ico", threaded=True) 
        
    print('Starting...')
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()











