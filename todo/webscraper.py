from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from queries import add_new_book
from const import const


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

driver.get(const.site1)

isNextDisabled = False

while not isNextDisabled:
    try:
        
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#list-slide1003")))
        
        elem_list = driver.find_element(
            By.CSS_SELECTOR, "#list-slide1003")

        items = elem_list.find_elements(
            By.CLASS_NAME, "productItem")

        for item in items:
            bname = item.find_element(By.CLASS_NAME,"text-description").text
            bpublisher = "No publisher found"
            bauthor = "No author found"
            bprice = "No price found"
            try:
                bpublisher = item.find_element(By.CLASS_NAME,"mt").text
                bauthor = item.find_element(By.ID,"productModelText").text
                bprice = item.find_element(By.CLASS_NAME,"currentPrice").text
                
                if "." and " TL" in bprice:
                    bprice = bprice.replace(' TL', '').replace('.', '', 1)
                    bprice = bprice.replace(',', '.', 1)
                else:
                    bprice = bprice.replace(' TL', '').replace(',', '.')
               
            except:
                pass    
            
            add_new_book(bname, bauthor, bpublisher, float(bprice))

            print("BookName:" + bname)
            print("Publisher:" + bpublisher)
            print("Author:" + bauthor)
            print("Price:" + bprice)

        next_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "next")))


        next_class = next_btn.get_attribute('class')

        if "next passive" in next_class:
            isNextDisabled = True
        else:
            driver.find_element(By.CLASS_NAME, 'next').click()

        

    except Exception as e:
        print(e,"Main Error")

#####################################################################################################

driver.get(const.site2)

for i in range(8):
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "prd_list_container")))

        elem_list = driver.find_element(
            By.CLASS_NAME, "prd_list_container")

        items = elem_list.find_elements(
            By.TAG_NAME, "li")

        for item in items:
            bname = item.find_element(By.CLASS_NAME,"name").text
            bpublisher = "No publisher found"
            bauthor = "No author found"
            bprice = "-1.0"

            try:
                bpublisher = item.find_element(By.CLASS_NAME,"publisher").text
                bauthor = item.find_element(By.CLASS_NAME,"writer").text
                bprice = item.find_element(By.CLASS_NAME,"price_sale").text
                if "." and "," in bprice:
                    bprice = bprice.replace('.', '', 1)
                    bprice = bprice.replace(',', '.', 1)
                elif "," in bprice:
                    bprice = bprice.replace(',', '.')
                
            except: 
                pass
            
            add_new_book(bname, bauthor, bpublisher, float(bprice))

            print("BookName:" + bname)
            print("Publisher:" + bpublisher)
            print("Author:" + bauthor)
            print("Price:" + bprice)

        
        if  i != 8:
            element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "button_pager_next")))
            
            driver.find_element(By.CLASS_NAME, "button_pager_next").click() 
    
             
    except Exception as e:
        print(e,"Main Error")
    
    if i == 7: driver.quit()

