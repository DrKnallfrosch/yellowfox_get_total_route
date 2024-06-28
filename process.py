from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from tkinter import ttk
import tkinter as tk
import os


def ttk_window():
    def destroy():
        failure.destroy()

    failure = tk.Tk()
    failure.title("Your LOGIN Failed!")
    failure.geometry("400x110")
    failure.attributes('-topmost', True)

    fail = ttk.Label(failure, text="WRONG LOGIN DATA!!! TRY AGAIN!", foreground="red")
    fail.pack()

    bb = ttk.Button(failure, text='OK', command=destroy)
    bb.pack()
    bb.place(x=165, y=60)

    failure.mainloop()


def process_main(start_day: str = "1", start_month: str = "1", start_year: str = "2022", end_day: str = "31",
                 end_month: str = "1", end_year: str = "2022", user_data: [str, str, str] = "" "" ""):
    # URL to Stalking Website
    url = ('https://map.yellowfox.de/gprsv2/index.asp?_gl=1*5e3dfl*_ga*NDY1Nzg0NjMwLjE3MTgxNzYwMjI.*_ga_6V25G7EE5M'
           '*MTcxODI2NTEyMi4yLjAuMTcxODI2NTEyMi42MC4wLjA.*_ga_MR88EXWMNQ*MTcxODI2NTEyMi4yLjAuMTcxODI2NTEyMi42MC4wLjA'
           '.*_gcl_au*Mzc4NDA1NzY0LjE3MTgxNzYwMjI.')

    __user_code = ""
    __user_name = ""
    __password = ""

    # Login data
    try:
        __user_code = user_data[0]
        __user_name = user_data[1]
        __password = user_data[2]
    except IndexError:
        pass
    # define the webbrowser 
    currentpath = os.getcwd()
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": fr"{currentpath}\csv_file"}  # change the download directory
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)

    # open the URL
    driver.get(url)
    # find box and write into
    client_id_box = driver.find_element(By.ID, 'clientid')
    client_id_box.send_keys(__user_code)
    # find box and write into
    login_id_box = driver.find_element(By.ID, 'loginname')
    login_id_box.send_keys(__user_name)
    # find box and write into
    password_id_box = driver.find_element(By.ID, 'password')
    password_id_box.send_keys(__password)  # password is to decode into string
    # click on the button
    try:
        login_button = driver.find_element(By.CLASS_NAME, 'arrowRight')
        login_button.click()
        sleep(2)
        submit_buton = driver.find_element(By.ID, 'cboxClose')
        submit_buton.click()
    except:
        driver.close()
        ttk_window()
    # wait 1 sec
    sleep(1)
    # open tab Reports
    report = driver.find_element(By.XPATH, '//*[@id="report_main"]/a')
    report.click()
    # wait 2 secs
    sleep(2)
    # clicked on new report
    new_report = driver.find_element(By.XPATH, '//*[@id="report_main"]/ul/table/tbody/tr/td[1]/ul[1]/li[1]/a')
    new_report.click()
    # wait 3 secs
    sleep(3)
    # opened in this tab the iframe/site
    driver.get('https://map.yellowfox.de/gprsv2/reportcenterv2/?action=edit_draft_inputmask')
    # wait 3 secs
    sleep(3)
    # write into to set the Report name
    report_name = driver.find_element(By.XPATH, '/html/body/form/div/table/tbody/tr[1]/td[2]/input')
    report_name.send_keys("Report")
    # wait 1 sec
    sleep(1)
    # click on the Report-type field
    report_type = driver.find_element(By.ID, 'report_type_title')
    report_type.click()
    # wait 1 sec
    sleep(1)
    # choose day-drive-report
    report_type = driver.find_element(By.XPATH, '/html/body/form/div/table/tbody/tr[2]/td[2]/div[2]/div[2]/a[2]')
    report_type.click()
    # wait 1 sec
    sleep(1)
    # write in from date a value
    driver.execute_script("date = document.getElementById('report_from')", "")
    driver.execute_script(f"date.value = '{start_day}.{start_month}.{start_year}'", "")
    # write in to date a value
    driver.execute_script("date = document.getElementById('report_to')", "")
    driver.execute_script(f"date.value = '{end_day}.{end_month}.{end_year}'", "")
    # open cars list
    wheelers = driver.find_element(By.XPATH, '//*[@id="textShowCarSelection"]/a')
    wheelers.click()
    # select all not virtuell cars
    b = driver.find_elements(By.NAME, 'units_single_member[]')
    a = 1  # couter set to 1 because to use in the html xpath to select all cars
    for a in range(a, len(b) - 10):
        wheeler_sign = driver.find_element(By.XPATH,
                                           f'/html/body/form/div/table/tbody/tr[28]/td[2]/div/div/div[1]/div/div'
                                           f'[{a}]/input')
        wheeler_sign.click()
    wheeler_sign = driver.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[28]/td[2]/div/div/div[2]/h3/input")
    wheeler_sign.click()
    # click on the output format csv
    output_format = driver.find_element(By.ID, 'report_format_title')
    output_format.click()
    output_format = driver.find_element(By.ID, 'report_format_msa_3')
    output_format.click()
    # disable any notification for the status of operation
    disable_notification = driver.find_element(By.XPATH,
                                               '/html/body/form/div/table/tbody/tr[58]/td/div/div[2]/p/input[1]')
    disable_notification.click()
    # semd the formula to yellow fox
    send_preset = driver.find_element(By.ID, 'saveButton')
    send_preset.click()
    # wait 10 secs
    sleep(10)
    # go to the main website
    driver.get("https://map.yellowfox.de/gprsv2/module/framework/3.0/index.php")
    # wait 5 secs
    sleep(5)
    # close first pop-up window on website
    submit_buton = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/div[2]/div[2]/div[1]/div/button")
    submit_buton.click()
    # wait 2 secs
    sleep(2)
    # open report options
    report = driver.find_element(By.XPATH, '//*[@id="report_main"]/a')
    report.click()
    sleep(0.7)  # wait 0.7 secs
    # open the lists from all created reports
    organise_report = driver.find_element(By.XPATH, '//*[@id="report_main"]/ul/table/tbody/tr/td[1]/ul[1]/li[2]/a')
    organise_report.click()

    sleep(1440)
    # reload website
    driver.refresh()
    sleep(5)
    # navigate again to the report list
    submit_buton = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/div[2]/div[2]/div[1]/div/button")
    submit_buton.click()
    sleep(0.2)  # wait 0.2 secs
    report = driver.find_element(By.XPATH, '//*[@id="report_main"]/a')
    report.click()
    sleep(2)  # wait 2 secs
    organise_report = driver.find_element(By.XPATH, '//*[@id="report_main"]/ul/table/tbody/tr/td[1]/ul[1]/li[2]/a')
    organise_report.click()
    sleep(2)  # wait 2 secs
    iframe = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/iframe")
    driver.switch_to.frame(iframe)
    sleep(0.5)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/form/table/tbody/tr[2]/td[10]/span').click()
    sleep(90)
