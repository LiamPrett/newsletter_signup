from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random


def initiate_spam():
    """Takes the persons input(s) and runs the script for every input given"""

    print(f"Welcome to Liam's newsletter spammer. Lets hope your victim enjoys this as much as you do. \n")
    time.sleep(1)

    emails = input("Please enter the emails you wish to spam (separate by space): ")
    emails = emails.split(" ")

    for email in emails:
        message = evil_message_selection()
        spam_email(email, message)


def evil_message_selection():
    """Selects a random message from the list"""

    evil_messages = ["BOW TO THE NEWSLETTERS", "Oh? You want to be Christian", "Big oof incoming for",
                     "I have the high ground", "You have activated my trap card", "Your cheeks are about to be clapped"]

    message = random.choice(evil_messages)
    return message


def spam_email(email_to_spam="", evil_message=""):
    """
    Sets up a new driver, goes to the newsletter site, selects all of the tickboxes available,
    fills in the form and awaits confirmation that the user has been signed up
    :param email_to_spam: This is the email that you wish to spam. This is set in initiate_spam.
    :param evil_message: This is the message you wish to display to let the person know that you are spamming a user.
    This is set in evil_message_selection
    """

    print(f"{evil_message} {email_to_spam}")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("log-level=2")
    driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver.exe")

    driver.get("https://www.christianity.com/newsletters/")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "emailAddress")))

    boxes_ticked = 0

    categories = driver.find_elements_by_class_name("NewsletterColumn")
    print("Attempting to tick all newsletting checkboxes..")
    for _ in categories:
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_class_name("NewsletterCategoriesList"))
        checkboxes = _.find_elements_by_tag_name("input")

        for box in checkboxes:

            if "checkbox" in box.get_attribute("type"):
                box.click()
                boxes_ticked += 1

                if box.is_selected() is True:
                    continue
                else:
                    break

    print(f"I have ticked {boxes_ticked} checkboxes, meaning {boxes_ticked} newsletters will be sent.")

    email_input = driver.find_element_by_class_name("emailAddress")
    email_input.send_keys(f"{email_to_spam}")

    driver.find_element_by_class_name("SubmitButton").click()

    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "content")))
    assert "Thank you for your Newsletter request" in driver.find_element_by_tag_name("h1").text

    print(f"{email_to_spam} has been spammed \n")

    driver.quit()


initiate_spam()
