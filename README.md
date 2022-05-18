# GovDeals-Scraper
This Python script allows you find profitable products from the website govdeals.com using eBay's finding API. 
##### Dm me on Discord if you have any questions or if you have any suggestions on how to make it better!
#### asf#6352
---

## Requirements
Go to  [Python Downloads](https://www.python.org/downloads/) page and install Python 3 if you do not already have it. 



### 1. Get the files.

Clone the repository **https://github.com/DavIdEscalant/GovDeals-Scraper.git** or download the [ZIP](https://github.com/DavIdEscalant/GovDeals-Scraper/archive/refs/heads/main.zip) file



### 2. Install the following libraries using pip: 
```
 pip install requests
 pip install bs4
 pip install xlsxwriter
 pip install ebaysdk
 
```

### 3. Obtain private eBay API key.
You will need a private eBay API key, follow these steps to get one!

- Go to the [developers](https://developer.ebay.com/signin) portal, create an account and wait for it to be approved.
- Navigate to [Application Keys](https://developer.ebay.com/my/keys) and create a key.

**Note: You might have agree to eBay's Event Notifications. In this case, click on (I do not persist eBay data) and submit your application since we do not need this**


---

## Tutorial

### 1. Change the `EBAY_API_kEY` variable inside the `govdeals.py` file to your private API key.
    
    EBAY_API_KEY = 'YOUR-API-KEY`
  
### 2. Open command promt and go to your file's directory.

    `cd /path/to/directory/`

### 3. Run the python file

    python govdeals.py
   
### 4. Follow cmd instructions:
- You will be asked to input a link. Go to [govdeals.com](https://www.govdeals.com/), copy the link of the category you wish to scrape and paste it into the terminal.
- Complete the following instrucitons.
- Name your file

    *** An Excel file will be crated if these previous steps were followed correctly ***

### 5. Enjoy!
