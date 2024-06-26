import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
import schedule
import os
load_dotenv()
import os

next_tuesday = (datetime.today() + timedelta( (1-datetime.today().weekday()) % 7 )).strftime('%Y-%m-%d')
booking_time = "19:00-20:00"
url = '{}/{}/by-time/slot/{}'.format((os.environ.get("url")), next_tuesday, booking_time)

def attempt_court_booking(url):
  # browser + chrome_options for production version
  chrome_options = add_chrome_options_for_heroku()
  browser = webdriver.Chrome(service=Service(os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)

  # browser for dev env
  # service = Service('./chromedriver')
  # browser = webdriver.Chrome(service=service)
  browser.get(url)

  if is_court_confirmed(browser):
    confirm_payment(browser)
  else:
    return

def add_chrome_options_for_heroku():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  return chrome_options

def get_list_of_courts(browser):
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class=' css-thk6w-control']"))).click()
  time.sleep(2)

def login(browser):
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(os.environ.get("username"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(os.environ.get("password"))
  showmore_link = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, ".//button[contains(@class,'Button__StyledButton-sc-5h7i9w-1 cEQnin SharedLoginComponent__LoginButton-sc-hdtxi2-5 htvyQa') and @type='submit']")))
  showmore_link.click()
  time.sleep(2)

def is_court_available(browser):
  for x in range(1, 11):
    court_div = '//div[text()="{} {}"]'.format(os.environ.get("court-name"), x)
    if len(browser.find_elements(By.XPATH, court_div)) > 0:
      print("court found")
      browser.find_element(By.XPATH, court_div).click()
      time.sleep(2)
      return True
  print("court unavailable")
  return False

def confirm_booking(browser):
  showmore_link2 = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, ".//button[contains(@class,'Button__StyledButton-sc-5h7i9w-1 cEQnin') and @type='button']")))
  showmore_link2.click()
  time.sleep(2)

def agree_to_terms_and_conditions(browser):
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Continue')]"))).click()

  ele = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='TermsModalComponent__Background-sc-1g34mtg-4 kARssu']")))
  browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", ele)

  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'I Agree')]"))).click()

def fill_out_payment_details_old(browser):
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingFirstName']"))).send_keys(os.environ.get("first-name"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingLastName']"))).send_keys(os.environ.get("last-name"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingAddressLineOne']"))).send_keys(os.environ.get("billing-address-line-one"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingCity']"))).send_keys(os.environ.get("billing-city"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='billingPostcode']"))).send_keys(os.environ.get("billing-postcode"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='cardholderName']"))).send_keys(os.environ.get("cardholder-name"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='cardNumber']"))).send_keys(os.environ.get("card-number"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='expiryDate']"))).send_keys(os.environ.get("expiry-date"))
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='securityCode']"))).send_keys(os.environ.get("security-code"))

def fill_out_payment_details(browser):
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='securityCode']"))).send_keys(os.environ.get("security-code"))

def pay_for_booking(browser):
  WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='PayNowButton__PayText-sc-1wm3jnf-2 fNBsUK']"))).click()

def click_cookies_button(browser):
  try:
    cookies_button = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    cookies_button.click()
    return True
  except Exception as e:
    print(f"Error clicking cookies button: {e}")
    return False

def is_court_confirmed(browser):
  click_cookies_button(browser)
  get_list_of_courts(browser)
  if is_court_available(browser):
    confirm_booking(browser)  
    login(browser)
    # booking must be confirmed again after logging in
    get_list_of_courts(browser)
    is_court_available(browser)
    confirm_booking(browser)
    time.sleep(2)
    return True  
  else:
    return False

def can_amount_be_paid_with_credit(browser):
  if len(browser.find_elements(By.XPATH, '//span[text()="Use full credit balance"]')) > 0:
    print("credit available to pay for court")
    return True
  return False

def pay_for_court_with_credit(browser):
    browser.find_element(By.XPATH, '//span[text()="Use full credit balance"]').click()
    print("paying using credit")
    time.sleep(2)
    browser.find_element(By.XPATH, '//span[text()="Confirm booking"]').click()
    time.sleep(10)
    print("booking confirmed")
      
def confirm_payment(browser):
  print("confirming payment")
  if (can_amount_be_paid_with_credit(browser)):
    pay_for_court_with_credit(browser)
    return
  print("not enough credit available to pay for court")
  fill_out_payment_details(browser)
  time.sleep(2)
  pay_for_booking(browser)
  print("paying for booking....")
  time.sleep(10)

def schedule_job():
 schedule.every(2).minutes.do(book_court)
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

# book_court()
schedule_job()
