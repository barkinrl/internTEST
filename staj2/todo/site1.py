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
driver = webdriver.Chrome(options=options)

driver.maximize_window()

driver.get('https://www.amazon.com.tr/')


driver.find_element(By.ID,"twotabsearchtextbox").send_keys("kitap")
driver.find_element(By.ID, "nav-search-submit-button").click()



isNextDisable = False

while not isNextDisable:
    try:
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.XPATH, '//div[@data-component-type="s-search-result"]')))
        
        elem_list = driver.find_element(
            By.XPATH, '//div[@data-component-type="s-search-result"]')

        items = elem_list.find_elements(
            By.XPATH, '//div[@data-component-type="s-search-result"]' )

        for item in items:
            name = item.find_element(By.TAG_NAME, 'h2').text
            author = item.find_element(By.CSS_SELECTOR, '.a-size-base').text
            price = "No price found"

            try:
                price = item.find_element(By.CSS_SELECTOR, '.a-price').text.replace("\n",",")
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
            (By.CLASS_NAME, "s-pagination-next")))

        next_class = next_btn.get_attribute('class')

        if "s-pagination-disabled" in next_class:
            isNextDisabled = True
            break
        else:
            driver.find_element(By.CLASS_NAME, 's-pagination-next').click()
        

    except Exception as e:
        print(e,"Main Error")
        isNextDisable = True