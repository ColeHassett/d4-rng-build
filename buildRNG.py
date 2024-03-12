from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

def any_waiters(driver, locator):
    return WebDriverWait(driver, timeout=10).until(expected_conditions.presence_of_element_located(locator))

def main():
    
    class_choice = "" #input("Choose a class(empty = random): ")
    
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--start-maximized")
    browser = webdriver.Chrome(options=opts)
    browser.get('https://d4builds.gg/build-planner/')
    
    any_waiters(browser, (By.ID, 'tyche_trendi_video_container'))
    browser.execute_script("""
        document.querySelector('#tyche_trendi_video_container').remove()
        """)

    # select class
    class_drp = browser.find_element(By.CLASS_NAME, 'builder__header__arrow')
    class_drp.click()
    
    class_choice.lower()
    if class_choice == 'd' or 'dru' in class_choice:
        class_choice = 0
    elif class_choice == 'n' or 'necro' in class_choice:
        class_choice = 1
    elif class_choice == 'r' or 'rog' in class_choice:
        class_choice = 2
    elif class_choice == 's' or 'sorc' in class_choice:
        class_choice = 3
    elif class_choice == 'n' or 'barb' in class_choice:
        class_choice = 4
    else:
        class_choice = randint(0, 4)
        
    classes = browser.find_elements(By.CLASS_NAME, 'builder__header__dropdown__item')
    if class_choice != 4:
        classes[class_choice].click()
    else:
        class_drp.click()

    # select aspects
    gear_slots = browser.find_elements(By.CSS_SELECTOR, 'button.builder__gear__icon__wrapper')
    for slot in gear_slots:
        slot.click()
        any_waiters(browser, (By.CSS_SELECTOR, 'button.gear__modal__item'))
        gear_items = browser.find_elements(By.CSS_SELECTOR, 'button.gear__modal__item:not(.selected)')
        random_num_gear = randint(0, len(gear_items)-1)
        gear_items[random_num_gear].click()
        
    # select gems
    gem_slots = browser.find_elements(By.CSS_SELECTOR, 'button.builder__gem__icon__wrapper')
    for slot in gem_slots:
        slot.click()
        any_waiters(browser, (By.CSS_SELECTOR, 'button.spec__modal__item'))
        gem_items = browser.find_elements(By.CSS_SELECTOR, 'button.spec__modal__item')
        random_num_gem = randint(0, len(gem_items)-1)
        gem_items[random_num_gem].click()
        
    # switch to tree
    skill_tree_tab = browser.find_elements(By.CLASS_NAME, 'builder__navigation__link')[1]
    skill_tree_tab.click()
    
    notes_tab = browser.find_elements(By.CLASS_NAME, 'builder__navigation__link')[4]
    notes_txt = ""

    view_btn = browser.find_elements(By.CLASS_NAME, 'game__filters__btn')[1]
    view_btn.click()

    max_points = 60
    used_points = 0
    
    max_skills = 6
    used_skills = 0

    while used_points < max_points:
        print(f'iterating... max_points:{max_points}; used_points:{used_points}\nmax_skills:{max_skills}; used_skills:{used_skills}')
        # get total options
        skills = browser.find_elements(By.CLASS_NAME, 'skill__tree__item--active')
        active_sections = browser.find_elements(By.CSS_SELECTOR, '.skill__tree__section.active')
        filtered_skills = []
        for s in skills:
            if len(active_sections) <= used_skills and "large" in s.get_attribute("class"):
                continue
            if "full" not in s.get_attribute("class"):
                if "fill" in s.get_attribute("class") or ("large" not in s.get_attribute("class") or used_skills < max_skills):
                    filtered_skills.append(s)
        print(f'number skills available: {len(filtered_skills)}')
        # generate random option
        random_num = randint(0, len(filtered_skills)-1)
        # select option
        print(f'selecting skill: {filtered_skills[random_num].get_attribute("class").split()[-1]}')
        if "large" in filtered_skills[random_num].get_attribute("class") and "fill" not in filtered_skills[random_num].get_attribute("class"):
            used_skills += 1
        notes_txt += f'{filtered_skills[random_num].get_attribute("class").split()[-1]}\n'
        filtered_skills[random_num].click()
        # increment counters
        used_points += 1

    # put pick order in notes tab
    notes_tab.click()
    any_waiters(browser, (By.ID, 'myTextArea'))
    notes_txtarea = browser.find_element(By.ID, 'myTextArea')
    notes_txtarea.send_keys(notes_txt)

    share_btn = browser.find_elements(By.CLASS_NAME, 'builder__header__button')[0]
    share_btn.click()
    
    any_waiters(browser, (By.CLASS_NAME, 'builder__modal__button'))
    copy_btn = browser.find_elements(By.CLASS_NAME, 'builder__modal__button')[0]
    copy_btn.click()
    
    WebDriverWait(browser, timeout=10).until(expected_conditions.text_to_be_present_in_element((By.CLASS_NAME, 'builder__modal__input--share'), 'd4builds'))
    build_link = browser.find_elements(By.CLASS_NAME, 'builder__modal__input--share')[0].text
    print(f'ENJOY YOUR BUILD: {build_link}')

if __name__ == "__main__":
    main()