import time
import webbrowser
from datetime import datetime, timedelta
import pyautogui

# Specify the path to your Chrome executable
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Replace with your Chrome executable path

# Execute a JavaScript script in the opened tab
script = """
    console.log('Hello from the content script!');
"""

keyword = "HiruSinhalaNews"
since = "2023-06-30"
until = "2023-07-07"
date_format = "%Y-%m-%d"
time_delta = 1


def run_script(start_date, end_date):
    # Your script logic goes here
    print("Running script for window:", start_date, "-", end_date)
    url = f"https://twitter.com/search?q=%23{keyword}%20until%3A{end_date}%20since%3A{start_date}&src=typed_query&f=live"

    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open(url)

    # Wait for the page to load
    time.sleep(5)

    # Adjust the delay according to your system's performance
    pyautogui.PAUSE = 1

    # # Locate the extension button on the screen
    # extension_button_location = pyautogui.locateOnScreen('icon-2.jpg')
    # if extension_button_location is None:
    #     print("Extension button not found.")
    #     exit()

    # print current mouse position
    print(pyautogui.position())

    # set location manually (x=1647, y=67)
    extension_button_location = pyautogui.Point(x=1647, y=67)

    # # Get the center coordinates of the extension button
    # button_x, button_y, button_width, button_height = pyautogui.center(extension_button_location)

    # Move the mouse to the center of the extension button and click
    pyautogui.moveTo(extension_button_location)
    pyautogui.click()

    # Wait for the extension to load (adjust the delay if needed)
    time.sleep(1)

    # move to Point(x=1422, y=181)
    pyautogui.moveTo(pyautogui.Point(x=1422, y=181))

    # Click on the extension's text box
    pyautogui.click()

    # Wait for the text box to load (adjust the delay if needed)
    time.sleep(3)


start_date = datetime.strptime(since, date_format)
end_date = datetime.strptime(until, date_format)

delta = timedelta(days=time_delta)
current_date = start_date

while current_date <= end_date:
    next_date = current_date + delta
    run_script(current_date.strftime(date_format), next_date.strftime(date_format))
    current_date = next_date
