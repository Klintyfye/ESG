# About

This is a product made by ESG for Softhouse © 2022.
Using this product, you can upload or select a Chrome web extension in order to receive a risk analysis of it.

It is designed to be run on Ubuntu Linux.

# Manual

## First Time Setup

The first time you use this product, begin by running installscript.sh to ensure you have all the necessary libraries. Additionally, you must make sure the APIKEY in constants.py has the key for a mongoDB database.

## Usage

1. While in the ESG-Master folder, run ``python3 server.py``
2. In your browser, navigate to <http://127.0.0.1:5000>.
3. You will be presented with a home page. Here, you can either manually upload a .crx file, or you can use the search bar to navigate through the Chrome webstore.
    1. After you have uploaded a .crx file, press the "submit" button.
    2. If you chose to use the search bar, press "select" next to the desired extension.
4. If the file has already been previously scanned in the database, you will be presented with an option to re-scan it. Select Yes to re-scan, or No to view the data of the previous scan.
5. You should now see the results screen.
    1. In the center, there is a pie chart displaying what vulnerabilities were detected.
    2. On the right, there is a chart. If the extension has been scanned multiple times over various dates, you will see how the amount of risks in the extension have changed over time.
    3. On the left, there is information about the extension. There is also an "advanced view" button, which displays the output of the retireJS algorithm.
