import functions as fun



EBAY_API_KEY = 'YOUR-API-KEY'
cat_list = ['Agriculture Equip/Commodities','Aircraft','Aircraft Parts and Components','Alarm and Fire Protection Systems','All Terrain Vehicles','All Vehicles (Restricted Vehicles)','Ambulance/Rescue','Animal Equipment, Cages and Feed','Archery and Crossbows','Arts and Crafts','Arts, Crafts, and Collectibles','Asphalt Equipment','Audio/Visual Equipment','Automobiles','Automobiles (Classic/Custom)','Aviation','Aviation Ground Support Equipment','Bags, All Types','Barber and Beauty Shop Equipment','Barrels and Drums','Batteries, All Types','BB Guns and Air Rifles','Bicycles','Boats, Marine Vessels and Supplies','Books/Manuals','Builders Supplies','Buses, Transit and School','Cafeteria and Kitchen Equipment','Chemicals, All Types','Clocks','Clothing/Linens','Coin Collections','Collectibles','Commercial Catering and Restaurant','Commercial Furnaces','Commodities / General Merchandise','Communication/Electronic Equipment','Compressor Parts and Accessories','Compressors','Computer accessories','Computer Hardware','Computer Monitors','Computer Printers, Scanners, and Copiers','Computer Software','Computers, Parts, and Supplies','Computers: Desktops and All-In-Ones','Computers: Laptops','Confiscated/Forfeited/Personal Property','Consumer Kitchen','Containers - Storage/Shipping','Cranes','Currency and Financial Products','Dental Equipment and Supplies','Displays and Exhibit Stands','Educational','Election Equipment','Electrical Supplies','Electronics, Personal','Engineering Equipment and Supplies','Exercise Equipment','Fine Art','Fire and Police Equipment','Fire Trucks','Firearm Accessories','Firearms and Live Ammunition','First Aid','Food','Forklifts','Fueling Equipment','Furniture/Furnishings','Garbage','Garbage and Refuse Containers','Garbage Trucks','Generators','Glass','Golf Course Equipment','Grandstands and bleachers','Health and Beauty','Heavy Equipment and Construction','Heavy Equipment Components and Accessories','Highway Equipment','Holiday/Seasonal Items','HVAC Equipment','Industrial Compressors','Industrial Equipment, General','Industrial Pumps','Industrial Pumps and Compressors','iPads, Tablets, and eReaders','Janitorial Equipment','Jewelry and Watches','Knives / Multi-Tools','Laboratory Equipment','Laboratory Pumps and Tubing','Laundry Equipment','Library Equipment','Lighting/Fixtures','Lost/Abandoned Property','Lumber','Machinery','Mailing Equipment','Material Handling Equipment','Medical Equipment and Supplies','Metal, Scrap','Metals, Precious','Miscellaneous Vehicles','Motor Homes / Travel Trailers','Motorcycles','Mowing Equipment','Music/Musical Equipment','Networking and Wireless Devices','Nursery/Horticulture/Landscaping','Office Equipment/Supplies','Outdoor Living','Paper and Paper Products','Permanent Buildings','Photographic Equipment','Pipe, Valves, and Fittings, Industrial','Playground / Amusement Park Equipment','Plumbing Equipment and Supplies','Pool Supplies and Equipment','Portable Buildings and structures','Printing and Binding Equipment','Public Safety and Control','Public Utility Equipment','Pump','Pump Parts and Accessories','Rail Equipment and Accessories','Real Estate / Land Parcels','Real Estate Tax Liquidations - Illinois','Recovered Items','Recyclable Materials','Remediation Equipment','Road/Highway/Bridge Supplies','Scales and Weighing Apparatus','School Equipment','Security Equipment','Simulators','Snow Removal Equipment','Sporting Equipment','Survey Equipment','SUV','Sweeper - Parking Lot/Warehouse','Sweeper - Street','Tanks','Televisions','Tires and Tubes','Tools, All Types','Tractor - Farm','Traffic Signals and Controls','Trailers','Trucks, Heavy Duty 1 ton and Over','Trucks, Light Duty under 1 ton','Vans','Vehicle Equipment/Parts','Vending Equipment','Welding Equipment','Woodworking Equipment']


url = fun.url_check()
link,total = fun.master_url(url)



file_soup = fun.get_soup(link)

item_dict = {}

for item in range(total):
    try:
        #print("\033[Style(0-5);Color(30-37);backrnd(40-47)m Bright Green  \n") (adds color) (ANSI Codes:https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#color-codes)
        print('\033[33m' + str(item) + '/' ' Scraping: ' + fun.get_title(item,file_soup))

        search = fun.ebay_search(item,file_soup,EBAY_API_KEY)
        item_dict[item]=search #assigns a the value of (search) to the (item_dict) dictionary 
        item_dict[item]['name']= fun.get_title(item,file_soup) # assigns the title  to an element of item_dict
        #item_dict[item]['govd_url'] = get_url(item,file_soup)
        print('\033[32m' 'Done')
        
    
    except:
        print('\033[31m' 'There is an error with this item')
        continue

print("Removing empty searches")
fun.remove_unwanted(item_dict)

print('Creating Excel file')
fun.create_xlsx(item_dict,file_soup)

