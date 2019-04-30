import logging, os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import Config   # this imports the config file where the private data sits


# this logging code designed to output DEBUG to console, and INFO (and above) to file
logger = logging.getLogger('log')  # 'log' can be anything - it's just the name
logger.setLevel(logging.DEBUG)
# create file handler which logs only 'INFO and above' messages
fh = logging.FileHandler('Log_of_info.log', mode='a')
fh.setLevel(logging.INFO)
# create console handler with the DEBUG log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create console_formatter and file_formatter and add it to the handlers
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # when outputting to console, show date and time
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # when outputting to file, also show date and time
ch.setFormatter(console_formatter)
fh.setFormatter(file_formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

cfg = Config()  # create an instance of the Config class, essentially brings private config data into play
os.chdir(cfg.cwd)  # change the current working directory to the one stipulated in config file


def check_internet_connection(sites):
    results = []
    result = os.system("ping " + sites[0])  # result = 0 if net is up or 1 if net is down
    # logger.debug(result)
    results.append(result)
    if result == '1':
        result_2 = os.system("ping " + sites[1])  # result = 0 if net is up or 1 if net is down
        logger.debug(result_2)
        results.append(result_2)
        result_3 = os.system("ping " + sites[2])  # result = 0 if net is up or 1 if net is down
        logger.debug(result_3)
        results.append(result_3)
    if 0 in results:
        return 'up'
    else:
        return 'down'


def login_router_admin():
    driver.get(cfg.url)  # use selenium webdriver to open web browser and desired URL from config file
    driver.execute_script("document.getElementById('userName').value = '" + str(cfg.uname) + "';")  # insert username
    driver.execute_script("document.getElementById('pcPassword').value = '" + str(cfg.pwd) + "';")  # insert password
    pass_elem = driver.find_element_by_id('loginBtn')  # find the 'Login' button using its element ID
    pass_elem.click()  # submit password
    time.sleep(2)   # wait 2 seconds for the login process to take place
    reboot_elem = driver.find_element_by_id('button_reboot')  # find the 'Login' button using its element ID
    reboot_elem.click()  # click the reboot button
    alert = driver.switch_to.alert
    alert.accept()  # alert.dismiss() for test mode or alert.accept() for live mode
    logger.info('Initiating router reboot')


sites_to_check = ["google.com", "8.8.4.4", "8.8.8.8"]  # for live
dodgy_sites_to_check = ["asdasdasd", "asdwdaqwd", "asdasd"]  # for testing

result_of_check = check_internet_connection(sites_to_check)  # will be 'up' or 'down'
logger.info(f"Net is {result_of_check}")

if result_of_check == 'down':
    chrome_path = cfg.chrome_path  # location of chromedriver.exe on local drive
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # to disable notifications popup in Chrome (affects Zoho page)
    driver = webdriver.Chrome(chrome_path, options=chrome_options)  # specify webdriver (chrome via selenium)

    login_router_admin()


# TODO: schedule in windows task manager
# TODO: think about how/when to send email (as net will be down). Perhaps this means leaving program open til net is back and then re-testing / emailing
