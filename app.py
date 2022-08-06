import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
import schedule
import os
load_dotenv()
import os

#booking_date_for_x_days_time = (datetime.today() + timedelta(days=5)).strftime('%Y-%m-%d')
next_monday = (datetime.today() + timedelta( (0-datetime.today().weekday()) % 7 )).strftime('%Y-%m-%d')
url = 'https://bookings.better.org.uk/location/islington-tennis-centre/highbury-tennis/{}/by-time/slot/19:00-20:00'.format(next_monday)

def attempt_court_booking(url):
  # browser + chrome_options for production version
  chrome_options = add_chrome_options_for_heroku()
  browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

  # browser for dev version
  #browser = webdriver.Chrome(executable_path='./chromedriver')
  browser.get(url)

  if is_court_confirmed(browser) == True:
    confirm_payment(browser)
  else:
    return False

def add_chrome_options_for_heroku():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  return chrome_options

def get_list_of_courts(browser):
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class=' css-xz6p7f']"))).click()
  time.sleep(2)

def login(browser):
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(os.environ.get("username"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(os.environ.get("password"))
  showmore_link = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, ".//button[contains(@class,'Button__StyledButton-sc-5h7i9w-1 fBHwHD SharedLoginComponent__LoginButton-sc-hdtxi2-5 fQXEJi') and @type='submit']")))
  showmore_link.click()
  time.sleep(2)

def is_court_available(browser):
  for x in range(1, 11):
    court_div = '//div[text()="Highbury Fields Tennis Court {}"]'.format(x)
    if len(browser.find_elements(By.XPATH, court_div)) > 0:
      browser.find_element(By.XPATH, court_div).click()
      time.sleep(2)
      return True
  print("court unavailable")
  return False

def confirm_booking(browser):
  showmore_link2 = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, ".//button[contains(@class,'Button__StyledButton-sc-5h7i9w-1 fBHwHD') and @type='button']")))
  showmore_link2.click()
  time.sleep(2)

def agree_to_terms_and_conditions(browser):
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Continue')]"))).click()

  ele = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='TermsModalComponent__Background-sc-1g34mtg-4 kARssu']")))
  browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", ele)

  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'I Agree')]"))).click()

def fill_out_payment_details(browser):
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingFirstName']"))).send_keys(os.environ.get("first-name"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingLastName']"))).send_keys(os.environ.get("last-name"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingAddressLineOne']"))).send_keys(os.environ.get("billing-address-line-one"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingCity']"))).send_keys(os.environ.get("billing-city"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingPostcode']"))).send_keys(os.environ.get("billing-postcode"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='cardholderName']"))).send_keys(os.environ.get("cardholder-name"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='cardNumber']"))).send_keys(os.environ.get("card-number"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='expiryDate']"))).send_keys(os.environ.get("expiry-date"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='securityCode']"))).send_keys(os.environ.get("security-code"))

def pay_for_booking(browser):
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Pay')]"))).click()

def is_court_confirmed(browser):
  get_list_of_courts(browser)
  if is_court_available(browser) == True:
    confirm_booking(browser)  
    login(browser)
    # above step must be repeated after logging in
    get_list_of_courts(browser)
    is_court_available(browser)
    confirm_booking(browser)
    time.sleep(2)
    return True  
  else:
    return False

def confirm_payment(browser):
  fill_out_payment_details(browser)
  #agree_to_terms_and_conditions(browser) // no longer needed
  pay_for_booking(browser)
  time.sleep(2)

def schedule_job():
 schedule.every(10).minutes.do(book_court)
 while True:
  schedule.run_pending()
  time.sleep(2)

def book_court():
  try:
    attempt_court_booking(url)
  except Exception as ex:
    # add proper error handling
    print(ex)
    sys.exit(0)

#book_court()
schedule_job()





