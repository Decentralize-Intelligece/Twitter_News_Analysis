import time
import webbrowser
from datetime import datetime, timedelta

# Specify the path to your Chrome executable
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Replace with your Chrome executable path

# Execute a JavaScript script in the opened tab
script = """
    console.log('Hello from the content script!');

// Retrieve elements with class="css-1dbjc4n r-1jgb5lz r-1ye8kvj r-13qz1uu"
var elements = document.querySelectorAll('.css-1dbjc4n.r-1jgb5lz.r-1ye8kvj.r-13qz1uu');

// Function to add a random delay
function addRandomDelay() {
    var delay = Math.random() * 2000; // Adjust the delay range as needed
    return new Promise(function(resolve) {
        setTimeout(resolve, delay);
    });
}

// Function to scroll to the bottom of the page
async function scrollToBottom() {
    window.scrollTo(0, document.body.scrollHeight);
    await addRandomDelay(); // Add a random delay after scrolling
}

// Function to scroll until reaching the end
async function scrollUntilEnd() {
    var previousScrollHeight = 0;
    var currentScrollHeight = document.body.scrollHeight;

    // Scroll until reaching the end
    while (currentScrollHeight !== previousScrollHeight) {
        previousScrollHeight = currentScrollHeight;
        await scrollToBottom();
        currentScrollHeight = document.body.scrollHeight;
    }
}

// Start scrolling until reaching the end
scrollUntilEnd().then(async function() {
    // count the number of elements
    console.log('Number of elements: ' + elements.length);

    console.log(elements[0].outerHTML)

    // Output the HTML code of the matched elements to the console and download them
    for (let i = 0; i < 1; i++) {
        await addRandomDelay(); // Add a random delay before downloading

        var url = window.location.href;
        var urlObj = new URL(url);
        var q = urlObj.searchParams.get('q');
        var until = urlObj.searchParams.get('until');
        var since = urlObj.searchParams.get('since');
        var fileName = 'twitter_scrape-content';
        if (q) {
            fileName += '-' + q.replace(/[^\w-]/g, '_');
        }
        if (until) {
            fileName += '-until-' + until;
        }
        if (since) {
            fileName += '-since-' + since;
        }
        fileName += '-' + (i + 1) + '.txt';

        var link = document.createElement('a');
        link.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(elements[i].outerHTML);
        link.download = fileName;
        link.style.display = 'none';

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
});

"""

keyword = "HiruSinhalaNews"
since = "2023-06-30"
until = "2023-07-07"
date_format = "%Y-%m-%d"


def run_script(start_date, end_date):
    # Your script logic goes here
    print("Running script for window:", start_date, "-", end_date)
    url = f"https://twitter.com/search?q=%23{keyword}%20until%3A{end_date}%20since%3A{start_date}&src=typed_query&f=live"

    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open(url)

    # Wait for the page to load
    time.sleep(10)


start_date = datetime.strptime(since, date_format)
end_date = datetime.strptime(until, date_format)

delta = timedelta(days=2)
current_date = start_date

while current_date <= end_date:
    next_date = current_date + delta
    run_script(current_date.strftime(date_format), next_date.strftime(date_format))
    current_date = next_date
