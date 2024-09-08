from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument('--disable-search-engine-choice-screen')

def calculate_benefit_costs(num_dependants):
    benefit_cost_per_year = 38.46 #1000/26
    dependant_cost_per_year = 19.23 #500/26
    total_benefit_cost = benefit_cost_per_year + (num_dependants * dependant_cost_per_year)
    return total_benefit_cost

# Setup chromedriver
driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

# 1. Open the login page
driver.get("https://wmxrwq14uc.execute-api.us-east-1.amazonaws.com/Prod/Account/Login")

# 2. Login using credentials
username_input = driver.find_element(By.ID, 'Username')
username_input.send_keys('TestUser434')
password_input = driver.find_element(By.ID, 'Password')
password_input.send_keys('}*rbRiNAjf^H')
login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
login_button.click()

# 3. Confirm that Dashboard page is open
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'employeesTable')))

# 4. Click Add Employee
add_employee_button = driver.find_element(By.XPATH,'//button[@id="add"]')
add_employee_button.click()

# 5. Check that Add Employee dialog box is open
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[@id="employeeModal"]//div[@class="modal-content"]')))

# 6. Enter the first name - Automation
first_name_input = driver.find_element(By.XPATH,'//input[@id="firstName"]')
first_name_input.send_keys('Automation')

#7. Enter last name - Testing
last_name_input = driver.find_element(By.XPATH,'//input[@id="lastName"]')
last_name_input.send_keys('Testing')

#8. Enter the number of dependants - 3
dependants_input = driver.find_element(By.XPATH,'//input[@id="dependants"]')
dependants_input.send_keys('3')

#9. Click Add button
add_button = driver.find_element(By.XPATH,'//button[@id="addEmployee"]')
add_button.click()

#10. Confirm that Employee has been added and that salary, gross and Benefit cost are added correctly
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//table[@id="employeesTable"]//td[text()="Automation"]/following-sibling::td[3][text()="52000.00"]'))) #salary
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//table[@id="employeesTable"]//td[text()="Automation"]/following-sibling::td[4][text()="2000.00"]'))) #gross
num_dependants = 3
benefit_cost = calculate_benefit_costs(num_dependants)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,f'//table[@id="employeesTable"]//td[text()="Automation"]/following-sibling::td[5][text()="{benefit_cost}"]'))) #benefits

#11. Edit Employee. Click Edit button next to Automation Testing employee
edit_button = driver.find_element(By.XPATH,'//td[text()="Automation"]/following-sibling::td[7]/i[@class="fas fa-edit"]')
edit_button.click()

#12. Make sure Add employee dialog box is open
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[@id="employeeModal"]//div[@class="modal-content"]')))

#13.Change first name to Paylocity
first_name_input.clear()
first_name_input.send_keys('Paylocity')

#14. Change last name to Dashboard
last_name_input.clear()
last_name_input.send_keys('Dashboard')

#15. Change the number of dependants to 1
dependants_input.clear()
dependants_input.send_keys('1')

#16. Click Update button
add_button = driver.find_element(By.XPATH,'//button[@id="updateEmployee"]')
add_button.click()

#17. Confirm that Employee has been updated and that Benefit cost is also updated correctly
num_dependants = 1
benefit_cost = calculate_benefit_costs(num_dependants)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,f'//table[@id="employeesTable"]//td[text()="Paylocity"]/following-sibling::td[5][text()="{benefit_cost}"]'))) #benefits

#18. Delete Employee. Click Delete button next to Paylocity Dashboard employee
delete_employee = driver.find_element(By.XPATH,'//td[text()="Paylocity"]/following-sibling::td[7]/i[@class="fas fa-times"]')
delete_employee.click()

#19. Delete employee dialog box should open
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[@id="deleteModal"]//div[@class="modal-content"]')))

#20. Click Delete button in dialog box
delete_button = driver.find_element(By.XPATH,'//button[@id="deleteEmployee"]')
delete_button.click()

#21. Check that employee Paylocity Dashboard has been deleted successfully
WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH,'//table[@id="employeesTable"]//td[text()="Paylocity"]')))

# Wait for a few seconds to see the result
time.sleep(10)

# quit driver
driver.quit()
