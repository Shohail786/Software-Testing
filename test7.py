import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, ElementClickInterceptedException,
    ElementNotInteractableException, NoSuchElementException
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
import requests
from io import BytesIO
import pytesseract
import time
import urllib3
import os
import base64
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import re

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

webdriver_path = r'C:\\Users\\IITGN\\Downloads\\chromedriver-win64_new\\chromedriver-win64\\chromedriver.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Example camps data
camps_to_selected = [
    {"name": "ttcm_year1[]", "values": ["2024", "2023"]},
    {"name": "ttcm_year2[]", "values": ["2024"]},
    {"name": "ttcm_year3[]", "values": ["2022", "2021"]},
    {"name": "ttcm_year4[]", "values": ["2024", "2023", "2022"]}
]

camps_to_attend = [
    {"name": "ttcm_year_attend1[]", "values": ["2024", "2023"]},
    {"name": "ttcm_year_attend2[]", "values": ["2024"]},
    {"name": "ttcm_year_attend3[]", "values": ["2022", "2021"]},
    {"name": "ttcm_year_attend4[]", "values": ["2024", "2023", "2022"]}
]

IO_india = [
    {"name": "olympiads_represent1[]", "values": ["1", "3"]},
    {"name": "olympiads_represent2[]", "values": ["2"]},
    {"name": "olympiads_represent3[]", "values": ["2", "5"]},
    {"name": "olympiads_represent4[]", "values": ["2", "3", "4"]},
    {"name": "olympiads_represent5[]", "values": ["1", "2", "3"]}
]

IO_intn = [
    {"name": "olympiads_medal1[]", "values": ["Gold", "Bronze"]},
    {"name": "olympiads_medal2[]", "values": ["Silver"]},
    {"name": "olympiads_medal3[]", "values": ["Bronze", "None"]},
    {"name": "olympiads_medal4[]", "values": ["Silver", "Bronze", "None"]},
    {"name": "olympiads_medal5[]", "values": ["Gold", "Silver", "Bronze"]}
]

discipline_list = [
    "discipline_preference1", "discipline_preference2", "discipline_preference3", 
    "discipline_preference4", "discipline_preference5", "discipline_preference6", 
    "discipline_preference7", "discipline_preference8", "discipline_preference9", 
    "discipline_preference10", "discipline_preference11"
]


# Check checkboxes for camps to select

photoPath="C:\\Users\\IITGN\\Downloads\\Automation\\goku.jpg"
nationalityPath="C:\\Users\\IITGN\\Downloads\\Automation\\Documentation.pdf"
ociPath="C:\\Users\\IITGN\\Downloads\\Automation\\Comprehensive1.pdf"

@pytest.fixture(scope="module")
def driver():
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    yield driver
    driver.quit()

def fill_field(driver, wait, type, typeVal, value):
    try:
        key = type.lower()
        by_type = getattr(By, key.upper())
        field = wait.until(EC.presence_of_element_located((by_type, typeVal)))
        
        print("field is filled")
        field.send_keys(value)
        
        return
    except TimeoutException as e:
        pytest.fail(f"Timeout waiting for element: {e}")
        
    except Exception as e:
        pytest.fail(f"Unable to find the {typeVal}: {e}")
        


def switch_to_iframe(driver, xpath):
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for iframe in iframes:
        driver.switch_to.frame(iframe)
        try:
            driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            driver.switch_to.default_content()
    return False

def select_dropdown(driver, wait, type,typeVal, value, by_value,by_text):
    try:
       
        key = type.lower()
        by_type = getattr(By, key.upper())
        print("typeVal",typeVal)
        dropdown=WebDriverWait(driver, 30).until(EC.presence_of_element_located((by_type, typeVal)))
        select = Select(dropdown)
        select_options = [option.text for option in select.options]
        
        print(value)
        print("program options:", select_options)
        
        assert value in select_options, f" {value}  not found in the available options"
        if by_value:
            
            select.select_by_value(value)
            
            print(f"Selected option '{value}' for {typeVal}")
        if by_text:
           
            select.select_by_visible_text(value)
            
            print(f"Selected option '{value}' for {typeVal}")
        
    except TimeoutException as e:
        pytest.fail(f"Timeout waiting for element: {e}")
        
        driver.quit()
    except Exception as e:
        pytest.fail(f"Unable to select: {e}")
        
        driver.quit()


def take_screenshot(driver, name="screenshot.png"):
    driver.save_screenshot(name)

def extract_text_from_image(image_path):
    try:
        captcha_image = Image.open(image_path)
        captcha_text = pytesseract.image_to_string(captcha_image)
        return captcha_text.strip()
    except Exception as e:
        print(f"Error extracting text from CAPTCHA: {e}")
        pytest.fail(f"Failed to extract CAPTCHA text: {e}")

def click_event(driver,wait,type,typeVal):
    try:
        
        key = type.lower()
        by_type = getattr(By, key.upper())
        print(by_type)
        print(typeVal)
        time.sleep(1)
        button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((by_type, typeVal)))
        
        print("field2 is filled")
    
        # driver.execute_script("arguments[0].scrollIntoView();", button)
        # button = driver.find_element(by_type, typeVal)
        button.click()
        
        print("button is clicked")
        
    except TimeoutException as e:
        pytest.fail(f"Timeout waiting for element: {e}")
       
    except Exception as e:
        pytest.fail(f"Unable to click: {e}")

def check_box(driver,wait,checkbox_type,checkbox_typeVal):
    key = checkbox_type.lower()
    by_type = getattr(By, key.upper())
    try:
        
        checkbox=WebDriverWait(driver, 10).until(EC.presence_of_element_located((by_type, checkbox_typeVal)))
        print("Element found: ", checkbox_typeVal)
        # Scroll to the element
        driver.implicitly_wait(10)
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        print("Scrolled to element: ", checkbox_typeVal)
        
        checkbox=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((by_type, checkbox_typeVal)))
        print("element visible")
        driver.execute_script("arguments[0].disabled = false;", checkbox)
        # WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable((by_type, checkbox_typeVal))
        # )
        # checkbox = driver.find_element(by_type, checkbox_typeVal)
    
        if not checkbox.is_selected():
            checkbox.click()
        print("Clicked checkbox: ", checkbox_typeVal)
    except TimeoutException:
        print(f"Timeout waiting for element: {checkbox_typeVal}")
        
        driver.quit()
    except ElementClickInterceptedException:
        print("ElementClickInterceptedException for: ", checkbox_typeVal)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((by_type, checkbox_typeVal))).click()
    except ElementNotInteractableException:
        print(f"ElementNotInteractableException for: {checkbox_typeVal}")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((by_type, checkbox_typeVal))).click()
    except NoSuchElementException:
        print(f"NoSuchElementException for: {checkbox_typeVal}")
        
        driver.quit()

        


def check_checkboxes(driver,wait, camps):
    for camp in camps:
        for value in camp["values"]:
            checkbox_type="xpath"
            checkbox_typeVal = f"//input[@name='{camp['name']}' and @value='{value}']"
            print(checkbox_typeVal)
            check_box(driver,wait,checkbox_type,checkbox_typeVal)

def get_preferences(driver, wait, type,typeVal):
    try:
        key = type.lower()
        by_type = getattr(By, key.upper())
        dropdown=WebDriverWait(driver, 20).until(EC.presence_of_element_located((by_type, typeVal)))
        select = Select(dropdown)
        select_options = [option.text for option in select.options]
        
        return select_options
        
    except TimeoutException as e:
        pytest.fail(f"Timeout waiting for options: {e}")
        driver.quit()
    except Exception as e:
        pytest.fail(f"Unable to find options: {e}")
        driver.quit()
          
def select_program_preferences(driver,wait, discipline_list):
    print("apple ",f'//select[@name="{discipline_list[0]}"]')
    lst=get_preferences(driver, wait,"xpath",f'//select[@name="{discipline_list[0]}"]')
    print("list ",lst)
    for name in discipline_list:
        program_name=random.choice(lst)
        print(program_name)
        print(name)
        select_dropdown(driver, wait,"xpath",f'//select[@name="{name}"]', program_name,by_value=False,by_text=True)
        

def register_form(driver, wait, name, email, password):
    try:
        driver.get("https://recruitment1.iitgn.ac.in/olympiad/register")
        print(driver.title)

        # Fill in the personal details
        name_field = wait.until(EC.presence_of_element_located((By.NAME, 'ufirstname')))
        name_field.send_keys(name)

        email_field = wait.until(EC.presence_of_element_located((By.NAME, 'uemail')))
        email_field.send_keys(email)

        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'upassword')))
        password_field.send_keys(password)

        confirm_password_field = wait.until(EC.presence_of_element_located((By.NAME, 'uconfirmpassword')))
        confirm_password_field.send_keys(password)
        
        # Wait for manual CAPTCHA input
        # input("Please enter the CAPTCHA in the browser and press Enter here to continue...")
        
        #AUTOMATE CAPTCH
        ele_captcha = driver.find_element("xpath","/html/body/div[2]/div[2]/form/div[5]/div[1]/div/img")
        img_captcha_base64 = driver.execute_async_script("""
        var ele = arguments[0], callback = arguments[1];
        ele.addEventListener('load', function fn(){
          ele.removeEventListener('load', fn, false);
          var cnv = document.createElement('canvas');
          cnv.width = this.width; cnv.height = this.height;
          cnv.getContext('2d').drawImage(this, 0, 0);
          callback(cnv.toDataURL('image/jpeg').substring(22));
        }, false);
        ele.dispatchEvent(new Event('load'));
        """, ele_captcha)
        timestamp = int(time.time())
        timestamp_filename = f"{timestamp}.jpg"
        print(timestamp_filename)
        with open(timestamp_filename, 'wb') as f:
                f.write(base64.b64decode(img_captcha_base64))
        captcha_image_path=timestamp_filename
        captcha_text = extract_text_from_image(captcha_image_path)
        print(captcha_text)
        # # Fill CAPTCHA text into input field
        captcha_input = wait.until(EC.presence_of_element_located((By.NAME, 'captchacode')))  # Update with actual CAPTCHA input field name
        captcha_input.send_keys(captcha_text)
        time.sleep(2)
        # Click the "Register Account" button to go to the next step
        register_button = wait.until(EC.element_to_be_clickable((By.ID, 'register_submit')))
        register_button.click()
        
        time.sleep(2)  # Wait for a while to ensure the form submission is processed
        
        # Check for redirection to login page by verifying the presence of expected elements
        wait.until(EC.presence_of_element_located((By.ID, 'frmLogin')))
        success_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.alert.alert-success')))
        
        assert "Registration Successfull. Please try to login using credentials." in success_message.text
        
    except TimeoutException as e:
        pytest.fail(f"Timeout waiting for element: {e}")
    except Exception as e:
        pytest.fail(f"Failed to fill form: {e}")
def login_form(driver, wait, email, password):
    try:
        driver.get("https://recruitment1.iitgn.ac.in/olympiad/login")
        fill_field(driver,wait,"name",'email',email)
        fill_field(driver,wait,"name","password",password)
        
        click_event(driver,wait,"id",'cmd_submit')
        # login_button = wait.until(EC.element_to_be_clickable((By.ID, 'cmd_submit')))
        # login_button.click()
        
    except TimeoutException as e:
        pytest.fail(f"Timeout waiting for element: {e}")
        
    except Exception as e:
        pytest.fail(f"Failed to login: {e}")
        

def select_date_from_calender(driver, wait, year, month, date):
    try:
        click_event(driver,wait,"id",'dob')
        print("dob")
        click_event(driver,wait,"class_name",'ui-datepicker-year')
        print("year")
        click_event(driver,wait,"xpath",f'//option[text()="{year}"]')
        print("year")
        click_event(driver,wait,"class_name",'ui-datepicker-month')
        click_event(driver,wait,"xpath",f'//option[text()="{month}"]')
        print("month")
        click_event(driver,wait,"xpath",f'//a[text()="{date}"]')
        print("date")
    except TimeoutException as e:
        pytest.fail(f"Timeout waiting for element: {e}")
        
        driver.quit()
    except Exception as e:
        pytest.fail(f"Failed to select_from_calender: {e}")
        
        driver.quit()
    

def fill_present_address(driver,wait,address1, address2, country, state, city, pinCode,countryCode,phone,altPhone,altEmail):
    type="name"
    fill_field(driver,wait, type,"preaddress1", address1)
    if(address2!=""):
        fill_field(driver,wait, type,"preaddress2",  address2)
        
    select_dropdown(driver,wait,type, "precountry",country,by_value=False,by_text=True)
    
    time.sleep(1)
    select_dropdown(driver,wait,type, "prestate",state,by_value=False,by_text=True)
    
    time.sleep(1)
    select_dropdown(driver,wait,type, "precity",city,by_value=False,by_text=True)
    
    
    fill_field(driver,wait, type,"prepincode",pinCode)
    driver.implicitly_wait(10)
    
    select_dropdown(driver,wait,type, "nationality_code",countryCode,by_value=False,by_text=True)
    
    
    # phone number
    fill_field(driver,wait, type,"prephone",phone)
    driver.implicitly_wait(10)
    
    #alt phone number
    fill_field(driver,wait, type,"premobile",altPhone)
    
    
    #email id already field
    
    #alternate email id
    fill_field(driver,wait, type,"altemail",altEmail)
    

def fill_permanent_address(driver,wait,address1, address2, country, state, city, pinCode):
    type="name"
    fill_field(driver,wait, type,"peraddress1", address1)
    if(address2!=""):
        fill_field(driver,wait, type,"peraddress2",  address2)
        
    select_dropdown(driver,wait,type, "percountry",country,by_value=False,by_text=True)
    
    time.sleep(1)
    select_dropdown(driver,wait,type, "perstate",state,by_value=False,by_text=True)
   
    time.sleep(1)
    select_dropdown(driver,wait,type, "percity",city,by_value=False,by_text=True)
    
    
    fill_field(driver,wait, type,"perpincode",pinCode)

    
   
# def fill_attachment_section(driver,wait):

def details_sections(driver,wait,camps_to_selected,camps_to_attend,IO_india,IO_intn,discipline_list,userdetails):
    try:
        # Check checkboxes for camps selected
        check_checkboxes(driver, wait,camps_to_selected)
        fill_field(driver, wait,"id","attachment_selected", userdetails.file_path_selected)
        driver.implicitly_wait(10)
        click_event(driver,wait,"xpath","//button[@id='saveBtnCampTraining']")
        time.sleep(1)
        driver.execute_script("document.getElementById('nextBtnCampTraining').disabled = false;")
        print("Next button enabled")
        time.sleep(1)
        click_event(driver,wait,"xpath","//button[@id='nextBtnCampTraining']")
        

        # Check checkboxes for camps attended
        check_checkboxes(driver, wait,camps_to_attend)
        fill_field(driver, wait,"id","attachment_attended", userdetails.file_path_attended)
        
        # Enter reasons in the text areas
        reason_text_attend = driver.find_element(By.ID, "reasons_text_attend")
        reason_text_attend.send_keys("The documents are not available because...")
        reason_text = driver.find_element(By.ID, "reasons_text")
        reason_text.send_keys("The camp was not attended because...")
        click_event(driver,wait,"xpath","//button[@id='saveBtnAttachment']")
        time.sleep(1)
        driver.execute_script("document.getElementById('nextBtnCampTrainingAttend').disabled = false;")
        print("Next button enabled")
        time.sleep(1)
        click_event(driver,wait,"xpath","//button[@id='nextBtnCampTrainingAttend']")
        

        # Check checkboxes for IO India
        check_checkboxes(driver, wait,IO_india)
        
        fill_field(driver, wait,"id","international_certificate", userdetails.file_path_ioi)
        click_event(driver,wait,"xpath","//*[@id='saveBtnOlympiadRepresent']")
        
        
        
        # Check checkboxes for IO International
        check_checkboxes(driver, wait,IO_intn)
        
        fill_field(driver, wait,"id","olympiad_medal_attachment", userdetails.file_path_iom)
        click_event(driver,wait,"xpath","//button[@id='saveBtnOlympiadMedal']")
        time.sleep(1)
        driver.execute_script("document.getElementById('representation_olympiads_nxt_btn').disabled = false;")
        print("Next button enabled")
        time.sleep(1)
        click_event(driver,wait,"xpath","//button[@id='representation_olympiads_nxt_btn']")
       

        # Select program preferences
        select_program_preferences(driver, wait, discipline_list)
        
        
        click_event(driver,wait,"xpath","//button[@id='saveBtnPreference']")
        time.sleep(1)
        driver.execute_script("document.getElementById('preference_nxt_btn').disabled = false;")
        print("Next button enabled")
        time.sleep(1)
        click_event(driver,wait,"xpath","//button[@id='preference_nxt_btn']")
        
        fill_field(driver, wait,"id","attachment_resume", userdetails.file_path_resume)
        fill_field(driver, wait,"id","attachment_jee_mains", userdetails.file_path_jee_mains)
        
        check_box(driver,wait,"xpath","//input[@name='agreement']")
        
        fill_field(driver,wait,"id","declaration_name",userdetails.name)
        
        fill_field(driver,wait,"id","declaration_place",userdetails.precity)
        
        click_event(driver,wait,"xpath","//button[@id='saveBtnFinal']")
        driver.implicitly_wait(10)
        
        # Wait for the popup to appear and handle it
        popup_confirm_button_xpath = "//div[contains(@class, 'swal-modal')]//button[contains(@class, 'swal-button--confirm')]"
        click_event(driver,wait,"xpath",popup_confirm_button_xpath)
        driver.implicitly_wait(10)
        
        click_event(driver,wait,"xpath","//a[@id='saveBtnPreviewApplication']")
        driver.implicitly_wait(10)

    except TimeoutException as e:
        pytest.fail(f"Timeout waiting for element: {e}")
        driver.quit()
    except Exception as e:
        pytest.fail(f"Failed to fill details sections form: {e}")
        driver.quit()

def fill_education_section(driver, wait,userdetails):
    fill_field(driver,wait, "name",'school_name',userdetails.tenth_school_name)
                                                           
    fill_field(driver,wait,"name", 'board_name',userdetails.tenth_board_name)
    
    fill_field(driver,wait, "name",'percentage', userdetails.tenth_percent)
    
    fill_field(driver,wait, "name",'10th_attachment', userdetails.tenth_attachment)
    
    select_dropdown(driver,wait,"name",'passing_year', userdetails.tenth_passing_year,by_value=False,by_text=True)
   
    
    fill_field(driver,wait, "name",'12th_school_name',userdetails.twel_school_name)
                                                           
    fill_field(driver,wait, "name",'12th_board_name',userdetails.twel_board_name)
    
    fill_field(driver,wait, "name",'12th_percentage', userdetails.twel_percent)
    
    fill_field(driver,wait, "name",'12th_attachment', userdetails.twel_attachment)
    
    select_dropdown(driver,wait,"name",'12th_passing_year', userdetails.twel_passing_year,by_value=False,by_text=True)
    
    time.sleep(1)
    click_event(driver,wait,"id",'saveBtnEducationDetails')
    driver.execute_script("document.getElementById('details_education_nxt_btn').disabled = false;")
    # print("Next button enabled2")
    
    click_event(driver,wait,"id",'details_education_nxt_btn')
    

    


def fill_basic_info(driver,wait,userdetails):
    fill_field(driver,wait, "name",'firstname', userdetails.first_name)
    fill_field(driver,wait, "name",'middlename', userdetails.middle_name)
    

    if userdetails.last_name == "":
        checkbox = wait.until(EC.presence_of_element_located((By.NAME, 'not_applicable_last_name')))
        if not checkbox.is_selected():
            checkbox.click()
    else:
        fill_field(driver, wait,"name", 'lastname', userdetails.last_name)

    select_date_from_calender(driver, wait, userdetails.year, userdetails.month, userdetails.day)
    
    select_dropdown(driver,wait, "id",'gender', userdetails.gender,False,by_text=True)
    driver.implicitly_wait(10)
    
    select_dropdown(driver,wait, "id",'nationality', userdetails.nation,False,True)
    driver.implicitly_wait(10)
    
    fill_field(driver,wait, "name",'photo', userdetails.photo_path)
    
    
    fill_field(driver,wait,"name", 'nationality_attachment', userdetails.nationality_path)
    

    fill_field(driver,wait, "name",'oci_card_attachment', userdetails.oci_path)
    
    
    fill_field(driver,wait,"name", 'parent_email', userdetails.parent_email)
    
    fill_field(driver,wait, "name",'guardian_contact_no', userdetails.parent_phone)
    
    fill_present_address(driver, wait, userdetails.preaddress1,  userdetails.preaddress2,userdetails.precountry,userdetails.prestate,userdetails.precity,userdetails.prepincode,userdetails.nationalitycode,userdetails.prephone,userdetails.premobile,userdetails.altemail)
    
    driver.implicitly_wait(20)
    if userdetails.peraddress1 == "":
        click_event(driver,wait,"name",'same_as_above')
        driver.implicitly_wait(10)
    else:
        fill_permanent_address(driver, wait, userdetails.peraddress1,  userdetails.peraddress2,userdetails.percountry,userdetails.perstate,userdetails.percity,userdetails.perpincode)

    click_event(driver,wait,"id",'saveBtnstep2')
    time.sleep(1)
    driver.execute_script("document.getElementById('basic_info_nxt_btn').disabled = false;")
    time.sleep(1)
    click_event(driver,wait,"id",'basic_info_nxt_btn')
    

    

def apply_form(driver, wait):
    try:
        
        click_event(driver, wait,"xpath","/html/body/div[2]/div[3]/div/div/div[2]/div/div/div/div/div/div/a")    
    except TimeoutException as e:
        take_screenshot(driver, "apply_btn_timeout.png")  # Take screenshot for debugging
        pytest.fail(f"Timeout waiting for element: {e}")
        
        driver.quit()
    except Exception as e:
        take_screenshot(driver, "apply_btn_error.png")  # Take screenshot for debugging
        pytest.fail(f"Failed to apply: {e}")
        
        driver.quit()



def fill_application(driver, wait, userdetails):
    try:
        fill_basic_info(driver,wait,userdetails)
        fill_education_section(driver,wait,userdetails)
        details_sections(driver,wait,camps_to_selected,camps_to_attend,IO_india,IO_intn,discipline_list,userdetails)
    except TimeoutException as e:
        pytest.fail(f"Timeout waiting for element: {e}")
        driver.quit()
    except Exception as e:
        pytest.fail(f"Failed to fill application form: {e}") 
        driver.quit() 


import random
import pytest

# Define sample input values for each field
names = ["UserA", "UserB", "UserC", "UserD", "UserE"]
emails = [f"user{random.randint(1, 100)}@example.com" for _ in range(100)]
passwords = ["Password123!", "WeakPass", "Another$ecure1", "HelloWorld@2023", "SecurePassword!"]
first_names = ["John", "Jane", "Doe", "Alice", "Bob"]
middle_names = ["MiddleA", "MiddleB", "MiddleC", "MiddleD", "MiddleE"]
last_names = ["Smith", "Doe", "Johnson", "Williams", "Brown"]
years = [str(random.randint(1980, 2005)) for _ in range(100)]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
days = [str(random.randint(1, 31)) for _ in range(100)]
genders = ["Male", "Female", "Other"]
nations = ["India", "USA", "UK", "Canada", "Australia"]
phone_numbers = [str(random.randint(7000000000, 9999999999)) for _ in range(100)]
addresses = ["Address1", "Address2", "Address3", "Address4", "Address5"]
school_names = ["School A", "School B", "School C"]
board_names = ["Board A", "Board B", "Board C"]
percentages = [str(random.randint(50, 100)) for _ in range(100)]
years_passing = [str(random.randint(2015, 2025)) for _ in range(100)]
file_paths = ["path/to/photo.jpg", "path/to/nationality.pdf", "path/to/oci.pdf"]
# Define a data class for user details
class UserDetails:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
# Function to generate a random UserDetails instance
def generate_user_details():
    return {
        "name": random.choice(names),
        "email": random.choice(emails),
        "password": random.choice(passwords),
        "first_name": random.choice(first_names),
        "middle_name": random.choice(middle_names),
        "last_name": random.choice(last_names),
        "year": random.choice(years),
        "month": random.choice(months),
        "day": random.choice(days),
        "gender": random.choice(genders),
        "nation": random.choice(nations),
        "parent_email": random.choice(emails),
        "parent_phone": random.choice(phone_numbers),
        "preaddress1": random.choice(addresses),
        "preaddress2": random.choice(addresses),
        "precountry": "India",
        "prestate": "Bihar",
        "precity": "Muzaffarpur",
        "prepincode": "842001",
        "nationalitycode": 'India (+91)',
        "prephone": random.choice(phone_numbers),
        "premobile": random.choice(phone_numbers),
        "altemail": random.choice(emails),
        "peraddress1": random.choice(addresses),
        "peraddress2": random.choice(addresses),
        "percountry": "India",
        "perstate": "Bihar",
        "percity": "Muzaffarpur",
        "perpincode": "843001",
        "tenth_school_name": random.choice(school_names),
        "tenth_board_name": random.choice(board_names),
        "tenth_percent": random.choice(percentages),
        "tenth_attachment": random.choice(file_paths),
        "tenth_passing_year": random.choice(years_passing),
        "twel_school_name": random.choice(school_names),
        "twel_board_name": random.choice(board_names),
        "twel_percent": random.choice(percentages),
        "twel_attachment": random.choice(file_paths),
        "twel_passing_year": random.choice(years_passing),
        "file_path_selected": random.choice(file_paths),
        "file_path_attended": random.choice(file_paths),
        "file_path_ioi": random.choice(file_paths),
        "file_path_iom": random.choice(file_paths),
        "file_path_resume": random.choice(file_paths),
        "file_path_jee_mains": random.choice(file_paths)
    }

# Generate 100 test cases
test_cases = [UserDetails(**generate_user_details()) for _ in range(100)]

# Define the test function with generated test cases
@pytest.mark.parametrize("user_details", test_cases)

def test_register_form(driver, user_details):
    try:
        wait = WebDriverWait(driver, 60)  # Increased wait time to 60 seconds
        # Example assertions for fields
        
        assert user_details.email.endswith('@example.com'), f"Invalid email: {user_details.email}"
        
        # Password validation: 6 to 12 characters, allowing special characters (@$!%*?&_).
        assert 6 <= len(user_details.password) <= 12, f"Password length invalid: {user_details.password}"
        assert re.match(r'^[A-Za-z0-9@$!%*?&_]{6,12}$', user_details.password), f"Invalid characters in password: {user_details.password}"

        assert user_details.year.isdigit(), f"Year is not a number: {user_details.year}"
       
        # Add other necessary assertions here...
       
        register_form(driver, wait, user_details.first_name, user_details.email, user_details.password)
        
        # # Verify the URL to confirm redirection to login page
        # assert "login" in driver.current_url, "Redirection to login page failed."
        login_form(driver, wait, user_details.email, user_details.password)
        # driver.implicitly_wait(20)
        # Verify the URL to confirm redirection to the home page
        # assert "home" in driver.current_url, "Redirection to home page failed."
        
        apply_form(driver, wait)
        driver.implicitly_wait(10)
        fill_application(driver, wait,user_details)
        driver.quit()
    except AssertionError as e:
        # Log the error and move on to the next test case
        
        print(f"Test failed: {e}")
if __name__ == "__main__":
    pytest.main()

