from django.shortcuts import render
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from core.settings import DATABASES
from python_scripts.variables import *
# from python_scripts.header import header
# from python_scripts.footer import footer
from bs4 import BeautifulSoup

# Create your views here.

@csrf_protect
def scrape(request, template_name="tasks.html"):
    csrfContext = RequestContext(request)

    args = {}
    args['tasks'] = []
    args['date_titles'] = []
    args['dates'] = []

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    print('Sending get request to url')
    driver.get(url)

    driver.implicitly_wait(4)

    print('Finding fields...')
    print('Inputting login credentials...')
    driver.find_element(By.XPATH, un_field).send_keys(request.GET.get('username'))
    driver.find_element(By.XPATH, pw_field).send_keys(request.GET.get('password'))
    print('Logging in...')
    driver.find_element(By.XPATH, btn).click()

    print('Finding tasks...')

    driver.implicitly_wait(6)

    try:
        due_dates = driver.find_elements(By.CSS_SELECTOR, '#lstMyTasks > li')
    except:
        print('Tasks not found!')
        driver.quit()
        quit()

    for i, date in enumerate(due_dates):
        class Date:
            def __init__(self, date):
                self.date = date
        
        titles = date.find_elements(By.TAG_NAME, 'h2')
        tasks = date.find_elements(By.CSS_SELECTOR, 'ul > li')
        num_of_wc = 0
        for task in tasks:
            if task is not None:
                task_name = task.find_element(By.CSS_SELECTOR, '.mutedDark.pad-b-s').text
                if 'WC' in task_name and not 'WH' in task_name and not 'WP' in task_name:
                    num_of_wc += 1
        if num_of_wc <= 0:
            pass
        else:
            print('Tasks found...')
            for title in titles:
                d_obj = Date(title.get_attribute('innerHTML')) # KEEP THIS

        print('Adding ' + str(num_of_wc) + ' tasks for date ' + str(i + 1) + ' of ' + str(len(due_dates)))
        total_time = 0
        my_tasks = []
        for task in tasks:
            my_task = {}
            my_task['title'] = ''
            my_task['name'] = ''
            my_task['time'] = ''
            my_task['details'] = ''
            if task is not None:
                task_title = task.find_element(By.CSS_SELECTOR, 'button.btn-action.text.x10-12.wrap-text.bold').text
                task_name = task.find_element(By.CSS_SELECTOR, '.mutedDark.pad-b-s').text
                if 'WC' in task_name and not 'WH' in task_name and not 'WP' in task_name:
                    try:
                        task_dur = task.find_element(By.CSS_SELECTOR, 'icon.i-time.icon-l.italic.inline-block.pad-t-s.pad-r-l').get_attribute('innerHTML')
                    except:
                        task_dur = '0h'
                    try:
                        if task_dur is not None:
                            # args['tasks'] += '<div class="time-div"><p>{}</p></div>'.format(task_dur.split('h')[0])
                            total_time += float(task_dur.split('h')[0])
                            my_task_time = task_dur.split('h')[0]
                        task_deets = task.find_element(By.CSS_SELECTOR, '.pad-b-s.textflow > span').get_attribute('innerHTML')
                        my_task['title'] += task_title
                        my_task['name'] += task_name
                        my_task['time'] += my_task_time
                        my_task['details'] = task_deets.split('<br>')
                        my_tasks.append(my_task)
                    except:
                        print('This task has no details')
        d_obj.tasks = my_tasks
            
        args['dates'].append(d_obj)

        # if total_time > 0:
        #     args['tasks'] += 'Total Time: '.format(str(total_time))

    print('Ending task')

    driver.quit()

    return TemplateResponse(request, template_name, args)


def testing(request, template_name="test.html"):
    class Date:
        def __init__(self, date):
            self.date = date
        tasks = []

    args = {}
    args['dates'] = []

    task_dates = ['Date 01', 'Date 02']

    for date in task_dates:
        d = Date(date)
        task_arr = []
        for task in ['task 01', 'task 02', 'task 03', 'task 04', 'task 05 & stuff']:
            task_arr.append(task)
        d.tasks = task_arr
        args['dates'].append(d)


    
    return TemplateResponse(request, template_name, args)

# date
#     tasks
#         tasktitle
#         taskname
#         tasktime
#         taskdetails