import os, os.path, pathlib, time, datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
DIR = '<enter path for plots here>' 
os.chdir(DIR)
delcount = 0
def countplots1():
    global count1
    count1 = 0
    for f in os.listdir(DIR):        
        if datetime.datetime(y,m,d,0,0).timestamp() > os.path.getmtime(f):
            count1+=1 
def deloldest():
    global delcount
    global oldest_file
    oldest_file = min(os.listdir(DIR), key=os.path.getmtime)
    os.remove(DIR+'/'+oldest_file)
    delcount+=1
if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
def on_moved(event):
    global delcount
    global count1
    oldest_file = min(os.listdir(DIR), key=os.path.getmtime)
    if (datetime.datetime(y,m,d,0,0).timestamp() > os.path.getmtime(DIR+'/'+oldest_file)):
        deloldest()
        print('Deleted '+ oldest_file)
        countplots1()
        print('Total files Deleted: '+ str(delcount))
        print('Left to replace: ' + str(count1 - 1))
dt=input('Enter cutoff date for plots: (YYYY-MM-DD)\n') #Any plots before this date will be deleted when a new one is added.
y,m,d = map(int,dt.split('-'))
my_event_handler.on_moved = on_moved
path = DIR
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)
my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()
