from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

with open("data.json", "w") as f:
    json.dump([],f)



def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

#PATH = "/home/barkin/Desktop/chromedriver.exe"




driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--disable-notifications")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 2 }
)
driver = webdriver.Chrome(options=options)

driver.maximize_window()

site1 = "https://www.bkmkitap.com/bilim-kurgu-kitaplari"
site2 = "https://www.ilknokta.com/index.php?p=Products&q_field_active=0&q=bilimkurgu&search=&q_field=&sort_type=prd_id-desc&page=1"


driver.get(site1)


isNextDisabled = False
ID = 0

while not isNextDisabled:
    try:
        
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#list-slide1003")))
        
        elem_list = driver.find_element(
            By.CSS_SELECTOR, "#list-slide1003")

        items = elem_list.find_elements(
            By.CLASS_NAME, "productItem")

        for item in items:
            name = item.find_element(By.CLASS_NAME,"text-description").text
            publisher = "No publisher found"
            author = "No author found"
            price = "No price found"
            try:
                publisher = item.find_element(By.CLASS_NAME,"mt").text
            except:
                pass    
            try:    
                author = item.find_element(By.ID,"productModelText").text
            except:
                pass    
            try:    
                price = item.find_element(By.CLASS_NAME,"currentPrice").text
            except:
                pass
            
            
            print("BookName:" + name)
            print("Publisher:" + publisher)
            print("Author:" + author)
            print("Price:" + price)

            write_json({
                "ID":ID,
                "BookName": name,
                "Publisher": publisher,
                "Author": author,
                "Price": price
            })
            ID = ID + 1

        next_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "next")))


        next_class = next_btn.get_attribute('class')

        if "next passive" in next_class:
            isNextDisabled = True
        else:
            driver.find_element(By.CLASS_NAME, 'next').click()

        

    except Exception as e:
        print(e,"Main Error")



#####################################################################################################


driver.get(site2)


for i in range(8):
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "prd_list_container")))

        elem_list = driver.find_element(
            By.CLASS_NAME, "prd_list_container")

        items = elem_list.find_elements(
            By.TAG_NAME, "li")

        for item in items:
            name = item.find_element(By.CLASS_NAME,"name").text
            publisher = "No publisher found"
            author = "No author found"
            price = "No price found"

            try:
                publisher = item.find_element(By.CLASS_NAME,"publisher").text
            except: 
                pass    
            try:
                author = item.find_element(By.CLASS_NAME,"writer").text
            except:
                pass
            try:
                price = item.find_element(By.CLASS_NAME,"price_sale").text
            except:
                pass

              
            print("BookName:" + name)
            print("Publisher:" + publisher)
            print("Author:" + author)
            print("Price:" + price)
            
            write_json({
                "ID":ID,
                "BookName": name,
                "Publisher": publisher,
                "Author": author,
                "Price": price
            })
            ID = ID + 1

        
        if  i != 8:
            element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "button_pager_next")))
            
            driver.find_element(By.CLASS_NAME, "button_pager_next").click() 
        else:
                driver.close()
             
    except Exception as e:
        print(e,"Main Error")

