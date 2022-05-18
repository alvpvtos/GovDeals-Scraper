import bs4
import requests
import xlsxwriter
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

cat_list = ['Agriculture Equip/Commodities','Aircraft','Aircraft Parts and Components','Alarm and Fire Protection Systems','All Terrain Vehicles','All Vehicles (Restricted Vehicles)','Ambulance/Rescue','Animal Equipment, Cages and Feed','Archery and Crossbows','Arts and Crafts','Arts, Crafts, and Collectibles','Asphalt Equipment','Audio/Visual Equipment','Automobiles','Automobiles (Classic/Custom)','Aviation','Aviation Ground Support Equipment','Bags, All Types','Barber and Beauty Shop Equipment','Barrels and Drums','Batteries, All Types','BB Guns and Air Rifles','Bicycles','Boats, Marine Vessels and Supplies','Books/Manuals','Builders Supplies','Buses, Transit and School','Cafeteria and Kitchen Equipment','Chemicals, All Types','Clocks','Clothing/Linens','Coin Collections','Collectibles','Commercial Catering and Restaurant','Commercial Furnaces','Commodities / General Merchandise','Communication/Electronic Equipment','Compressor Parts and Accessories','Compressors','Computer accessories','Computer Hardware','Computer Monitors','Computer Printers, Scanners, and Copiers','Computer Software','Computers, Parts, and Supplies','Computers: Desktops and All-In-Ones','Computers: Laptops','Confiscated/Forfeited/Personal Property','Consumer Kitchen','Containers - Storage/Shipping','Cranes','Currency and Financial Products','Dental Equipment and Supplies','Displays and Exhibit Stands','Educational','Election Equipment','Electrical Supplies','Electronics, Personal','Engineering Equipment and Supplies','Exercise Equipment','Fine Art','Fire and Police Equipment','Fire Trucks','Firearm Accessories','Firearms and Live Ammunition','First Aid','Food','Forklifts','Fueling Equipment','Furniture/Furnishings','Garbage','Garbage and Refuse Containers','Garbage Trucks','Generators','Glass','Golf Course Equipment','Grandstands and bleachers','Health and Beauty','Heavy Equipment and Construction','Heavy Equipment Components and Accessories','Highway Equipment','Holiday/Seasonal Items','HVAC Equipment','Industrial Compressors','Industrial Equipment, General','Industrial Pumps','Industrial Pumps and Compressors','iPads, Tablets, and eReaders','Janitorial Equipment','Jewelry and Watches','Knives / Multi-Tools','Laboratory Equipment','Laboratory Pumps and Tubing','Laundry Equipment','Library Equipment','Lighting/Fixtures','Lost/Abandoned Property','Lumber','Machinery','Mailing Equipment','Material Handling Equipment','Medical Equipment and Supplies','Metal, Scrap','Metals, Precious','Miscellaneous Vehicles','Motor Homes / Travel Trailers','Motorcycles','Mowing Equipment','Music/Musical Equipment','Networking and Wireless Devices','Nursery/Horticulture/Landscaping','Office Equipment/Supplies','Outdoor Living','Paper and Paper Products','Permanent Buildings','Photographic Equipment','Pipe, Valves, and Fittings, Industrial','Playground / Amusement Park Equipment','Plumbing Equipment and Supplies','Pool Supplies and Equipment','Portable Buildings and structures','Printing and Binding Equipment','Public Safety and Control','Public Utility Equipment','Pump','Pump Parts and Accessories','Rail Equipment and Accessories','Real Estate / Land Parcels','Real Estate Tax Liquidations - Illinois','Recovered Items','Recyclable Materials','Remediation Equipment','Road/Highway/Bridge Supplies','Scales and Weighing Apparatus','School Equipment','Security Equipment','Simulators','Snow Removal Equipment','Sporting Equipment','Survey Equipment','SUV','Sweeper - Parking Lot/Warehouse','Sweeper - Street','Tanks','Televisions','Tires and Tubes','Tools, All Types','Tractor - Farm','Traffic Signals and Controls','Trailers','Trucks, Heavy Duty 1 ton and Over','Trucks, Light Duty under 1 ton','Vans','Vehicle Equipment/Parts','Vending Equipment','Welding Equipment','Woodworking Equipment']

def get_soup(base_url):
    requ = requests.get(base_url)
    soup = bs4.BeautifulSoup(requ.text, 'html.parser')
    return soup

def total_items_to_scrape(url):
    requ = requests.get(url)
    soup = bs4.BeautifulSoup(requ.text, 'html.parser')
    total_items = int(soup.select('.col-sm-6.col-md-6.col-lg-4.col-xl-4')[0].text.split()[-1])
    items = 0
    while items == 0 or items > total_items :
        try:
            items = int(input(f'There are {total_items} available to scrape.\nHow many items would you like to scrape? '))
            if items > total_items:
                print(f'Number should be lower or equal to {total_items}')
        except ValueError:
            print(f'Value must be an integer greater or equal to 1 and lower or equal to {total_items}')
            continue
    return int(items)


def get_title(item_id,file_soup):
    name = file_soup.select(".col-6.col-sm-6.col-md-6.col-lg-2.col-xl-2")[item_id].a.text
    return name

def get_make_brand(item_id,file_soup):
    att_list = list(file_soup.select(".col-6.col-sm-6.col-md-6.col-lg-2.col-xl-2")[item_id].stripped_strings)

    empty = [] == list(filter(lambda x: "Make" in x, att_list))
    
    if empty == False:
        return list(filter(lambda x: "Make" in x, att_list))[0][12:]


    elif empty == True:
        return 'No Make/Brand'
    

def get_closing_time(item_id,file_soup):
    name = file_soup.select('.col-10.col-sm-10.col-md-10.col-lg-2.col-xl-2.px-1')[item_id].stripped_strings
    return list(name)

def get_url(item_id,file_soup):
    url = file_soup.select('.col-6.col-sm-6.col-md-6.col-lg-2.col-xl-2')[item_id].a['href']
    # https://www.govdeals.com/index.cfm?fa=Main.Item&itemid=69&acct
    return 'https://www.govdeals.com/'+url

def get_model(item_id,file_soup):
    att_list = list(file_soup.select(".col-6.col-sm-6.col-md-6.col-lg-2.col-xl-2")[item_id].stripped_strings)
    empty = [] == list(filter(lambda x: "Model" in x, att_list))
    
    if empty == False:
        return list(filter(lambda x: "Model" in x, att_list))[0][7:]


    elif empty == True:
        return 'No Model'

def get_params(item_id,file_soup):

    parameters = {
            'keywords': '',
            'paginationInput': {'pageNumber': '1',
                'entriesPerPage': '100',  
                }}

    no_brand = 'No Make/Brand'
    no_model = 'No Model'
    #changes the keywords 
    if get_make_brand(item_id,file_soup) != no_brand and get_model != no_model: #if both brand and model are present
        parameters['keywords'] = get_make_brand(item_id,file_soup) + ' ' + get_model(item_id, file_soup) 

    elif get_make_brand(item_id,file_soup) != no_brand and get_model == no_model: # if only model is present
         parameters['keywords'] = get_model(item_id, file_soup) 

    elif get_make_brand(item_id,file_soup) == no_brand and get_model != no_model: # if only brand is present
         parameters['keywords'] = get_title(item_id, file_soup)

    else:
        parameters['keywords'] = get_title(item_id, file_soup) # to the title if both brand and model arent present

    return parameters


def ebay_search(item_id,file_soup,API_KEY):
    api = Finding(appid=API_KEY, config_file=None)
    response = api.execute('findItemsByKeywords', get_params(item_id,file_soup)) 
    return response.dict()

def average_price(item,filtered_file):
    prices = []
    for p in filtered_file[item]['searchResult']['item']:
        prices.append(float(p['sellingStatus']['currentPrice']['value']))
    
    return sum(prices)/ 100

def url_check():

    while True:
        try:

            link = input('Please enter the link to the category you would like to scrape: ')
            requ = requests.get(link)
            soup = bs4.BeautifulSoup(requ.text, 'html.parser')

            if soup.title.text[15:-19] not in  cat_list:
                #if there is a new category, add it to cat_list
                print('Category link not found, please visit https://www.govdeals.com/, click a desired category and paste its link here ')
                continue
            else:
                print(f'Category {soup.title.text[15:-19]} selected')
                return link
                break
        except:
            print('This is an invalid link.\nPlease go to https://www.govdeals.com/, click a desired category and paste its link here')


def master_url(url):
    requ = requests.get(url)
    soup = bs4.BeautifulSoup(requ.text, 'html.parser')
    total_items = int(soup.select('.col-sm-6.col-md-6.col-lg-4.col-xl-4')[0].text.split()[-1])
    items = 0
    while items == 0 or items > total_items :
        try:
            items = int(input(f'There are {total_items} total items.\nHow many items would you like to scrape? '))
            if items > total_items:
                print(f'Number should be lower or equal to {total_items}')
        except ValueError:
            print(f'Value must be an integer greater or equal to 1 and lower or equal to {total_items}')
            continue
    return url[:157] + f'&rowCount={items}&StartRow=1', items

def remove_unwanted(item_dict):
    for i in list(item_dict):
        if item_dict[i]['paginationOutput']['totalEntries'] == '0':
            print('Empty search found')
            item_dict.pop(i)

def create_xlsx(item_dict,file_soup):
    while True:
        try:
            name = str(input('Chose a name for your Excel file'))
            workbook = xlsxwriter.Workbook(f'{name}.xlsx')

            worksheet = workbook.add_worksheet("My sheet")
            row = 0
            column = 0
            for i in item_dict:
                worksheet.write(row,column,item_dict[i]['name'])
                worksheet.write(row,column+1,average_price(i,item_dict))
                worksheet.write(row,column+2,item_dict[i]['itemSearchURL'])
                worksheet.write(row,column+3,get_url(i,file_soup))
                row+= 1 
            workbook.close()
        except:
            print("There has been an error, please choose another file name:")
        else:
            break


