from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

with open("data2.json", "w") as f:
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
driver = webdriver.Chrome(options=options)

driver.maximize_window()

driver.get('https://blackwells.co.uk/bookshop/home')



driver.find_element(By.ID,"keyword").send_keys("avatar")
driver.find_element(By.CLASS_NAME, "visuallyhidden").click()



isNextDisable = False

while not isNextDisable:
    try:
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "container")))
        
        elem_list = driver.find_element(
            By.CLASS_NAME, "container")

        items = elem_list.find_elements(
            By.CLASS_NAME, "container" )

        for item in items:
            name = item.find_element(By.CLASS_NAME, 'product-name').text
            author = item.find_element(By.CLASS_NAME, 'product-author').text
            price = "No price found"

            try:
                price = item.find_element(By.CLASS_NAME, "product-price").text.replace("\n",",")
            except:
                pass


            print("Book Name:" + name)
            print("Author/Translator Name:" + author)
            print("Book Price:" + price)

            write_json({
                "Book Name": name,
                "Author/Translator Name": author,
                "Book Price": price
            })

        next_btn = WebDriverWait(driver, 17).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "btn btn--secondary js-search")))

        next_class = next_btn.get_attribute('class')

        if "null" in next_class:
            isNextDisabled = True
            break
        else:
            driver.find_element(By.ID, 'show-more-full-results-button').click()
        

    except Exception as e:
        print(e,"Main Error")
        isNextDisable = True