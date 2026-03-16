from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from utils.crash_detector import check_for_crash_or_anr
from utils.handel_reading_section import handel_input_in_reading, check_radio_button_from_reading
from utils.safe_actions import safe_gesture_click


def test_learning_journey(driver):
    email = "testuser5203@gmail.com"
    try:
        google_button = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located((AppiumBy.XPATH,
                                                               '//android.widget.TextView[@text="By clicking continue I agree to the"]/preceding-sibling::android.view.ViewGroup[6]')))
        google_button.click()
    except (TimeoutException, NoSuchElementException):
        driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiScrollable(new UiSelector().scrollable(true))'
                            '.scrollIntoView(new UiSelector().text("By clicking continue I agree to the"))')
        WebDriverWait(driver, 20).until(
            expected_conditions.element_to_be_clickable((AppiumBy.XPATH,
                                                         '//android.widget.TextView[@text="By clicking continue I agree to the"]/preceding-sibling::android.view.ViewGroup[@clickable="true" and @enabled="true"]'))).click()
    WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located((AppiumBy.ID, "com.google.android.gms:id/main_title")))
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{email}")').click()
    WebDriverWait(driver, 20).until(
        expected_conditions.visibility_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Let\'s start your learning journey")')))
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Start learning").click()
    try:
        WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Choose Your Tutor")')))
        driver.find_element(AppiumBy.XPATH,'//android.widget.TextView[@text="Non Native English"]/following-sibling::android.view.ViewGroup[2]').click()
        driver.find_element(AppiumBy.XPATH,'//android.widget.TextView[@text="Non Native English"]/following-sibling::android.view.ViewGroup[4]').click()
    except (NoSuchElementException,TimeoutException):
        WebDriverWait(driver,10).until(expected_conditions.invisibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Please wait…")')))
    WebDriverWait(driver,20).until(expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID,'Start Now'))).click()
    WebDriverWait(driver,30,poll_frequency=0.2).until(
        expected_conditions.invisibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().textContains("Loading PDF")')))
    WebDriverWait(driver,20).until(
        expected_conditions.visibility_of_element_located((AppiumBy.XPATH,'//android.view.ViewGroup[@content-desc="View Transcript"]/preceding-sibling::android.view.ViewGroup[1]'))).click()
    input_notes = WebDriverWait(driver,20).until(
        expected_conditions.element_to_be_clickable((AppiumBy.CLASS_NAME,'android.widget.EditText')))
    print("Founddddddd................")
    input_notes.send_keys("test to notes")
    driver.find_element(AppiumBy.ACCESSIBILITY_ID,'Save Notes').click()
    WebDriverWait(driver,20).until(expected_conditions.element_to_be_clickable((AppiumBy.XPATH,'//android.view.ViewGroup[@content-desc="View Transcript"]/preceding-sibling::android.view.ViewGroup[2]'))).click()
    WebDriverWait(driver,30,poll_frequency=0.3).until(
        expected_conditions.visibility_of_element_located((AppiumBy.XPATH,'(//android.widget.TextView)[6]')))
    xpath = '((//android.widget.ScrollView)[2]//android.view.ViewGroup//android.view.ViewGroup/following-sibling::android.widget.TextView)[position() mod 2 = 0]'
    bot_replies1 = driver.find_elements(AppiumBy.XPATH,xpath)
    current_count = len(bot_replies1)
    print("Updated Count1",current_count)
    if current_count == 0:
        bot_replies1 = WebDriverWait(driver, 40,poll_frequency=0.2).until(
            lambda d: elements1 if (elements1 := d.find_elements(AppiumBy.XPATH, xpath)) and len(elements1) > current_count else False)  # walrus operator (:=)
        current_count = len(driver.find_elements(AppiumBy.XPATH,xpath))
    print("Updated Count2",current_count)
    question1 = "1st question asked"
    driver.find_element(AppiumBy.CLASS_NAME,'android.widget.EditText').send_keys(question1)
    driver.find_element(AppiumBy.XPATH,f'//android.widget.EditText[@text="{question1}"]/following-sibling::android.view.ViewGroup[1]').click()
    # When you want to wait for a custom condition (not just element visible/clickable), you use:
    bot_replies2 = WebDriverWait(driver, 40).until(
        lambda d: elements1 if (elements1 := d.find_elements(AppiumBy.XPATH, xpath)) and len(
            elements1) > len(bot_replies1) else False)
    print("Final Updated Count3",len(bot_replies2))
    if len(bot_replies2) > len(bot_replies1):
        bot_reply = bot_replies2[-1].text
        print(bot_reply)
        assert bot_reply.strip() !=""
    print("ready to lower hand")
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Lower hand")').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID,'Finish').click()
    if_text = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Lesson is still pending to be completed")').text
    print(if_text)
    if if_text:
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Yes').click()
    WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Move on to excercises")'))).click()
    for i in range(5):
        WebDriverWait(driver, 20).until(expected_conditions.visibility_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Reading Passage")')))
        edit_text = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        if edit_text:
            handel_input_in_reading(driver)
        else:
            check_radio_button_from_reading(driver)
    print("Lesson 1 Completed.............")
    WebDriverWait(driver,20).until(
        expected_conditions.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID,'Start reading practice')))
    driver.find_element(AppiumBy.ACCESSIBILITY_ID,'Let\'s start').click()
    WebDriverWait(driver,20).until(expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID,'Start Now'))).click()
    try:
        WebDriverWait(driver, 20,poll_frequency=0.2).until(expected_conditions.invisibility_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Loading PDF")')))
    except TimeoutException:
        print("Loading PDF did not disappear, continuing anyway...")
    WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Finish'))).click()
    try:
        popup = WebDriverWait(driver,10).until(
            expected_conditions.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Lesson is still pending to be completed")')))
        print(popup.text)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Yes').click()
    except(TimeoutException,NoSuchElementException):
        print("Popup not displayed, moving forward...")
    WebDriverWait(driver,20).until(expected_conditions.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Move on to excercises")'))).click()
    for _ in range(5):
        mic_start_locator = (AppiumBy.XPATH,
                       '(//android.widget.TextView[@text="Recording will start in"]/preceding-sibling::android.view.ViewGroup[@clickable="true"])[1]')
        try:
            mic_start = WebDriverWait(driver, 5).until(
                expected_conditions.visibility_of_element_located(mic_start_locator))
        except (TimeoutException, NoSuchElementException):
            driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                'new UiScrollable(new UiSelector().scrollable(true))'
                                '.scrollIntoView(new UiSelector().text("Recording will start in"))')
            mic_start = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located(mic_start_locator))
        """This is an Appium mobile command.
        It tells Android:
        Perform a REAL touch gesture on this element.
        """
        safe_gesture_click(driver, mic_start)
        check_for_crash_or_anr(driver)
        for attempt in range(3):
            try:
                mic_stop_locator = (AppiumBy.XPATH,'(//android.widget.TextView[contains(@text,"QUESTION")]/following-sibling::android.view.ViewGroup[@clickable="true"])[last()]')
                mic_stop_element = WebDriverWait(driver, 20, poll_frequency=0.3).until(
                    expected_conditions.visibility_of_element_located(mic_stop_locator))
                print(mic_stop_element,"..................id")
                safe_gesture_click(driver, mic_stop_element)
                print(f"Mic stopped successfully on attempt{attempt+1}")
                break
            except (NoSuchElementException,TimeoutException,StaleElementReferenceException):
                if attempt ==2:
                    raise Exception("Mic stop failed after retries")
        submit_locator = (AppiumBy.ACCESSIBILITY_ID, 'Submit')
        try:
            submit_button = WebDriverWait(driver, 30).until(
                expected_conditions.element_to_be_clickable(submit_locator))
        except TimeoutException:
            driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                'new UiScrollable(new UiSelector().scrollable(true))'
                                '.scrollIntoView(new UiSelector().description("Submit"))')
            submit_button = WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable(submit_locator))
        submit_button.click()
    print("Lesson 2 Completed.........")
    WebDriverWait(driver, 20).until(
        expected_conditions.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Start speaking practice')))
    driver.find_element(AppiumBy.ACCESSIBILITY_ID,'Let\'s start').click()
    WebDriverWait(driver,20).until(expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID,'Start Now'))).click()
    try:
        WebDriverWait(driver, 20, poll_frequency=0.2).until(expected_conditions.invisibility_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Loading PDF")')))
    except TimeoutException:
        print("Loading PDF did not disappear, continuing anyway...")
    WebDriverWait(driver, 20).until(
        expected_conditions.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Finish'))).click()
    try:
        popup = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Lesson is still pending to be completed")')))
        print(popup.text)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Yes').click()
    except(TimeoutException, NoSuchElementException):
        print("Popup not displayed, moving forward...")
    WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Move on to excercises")'))).click()
    question_locator = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().textContains("QUESTION")')
    for i in range(5):
        question_element =  WebDriverWait(driver, 20, poll_frequency=0.3).until(
        expected_conditions.visibility_of_element_located(question_locator))
        previous_question = question_element.text
        edit_text = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        print("EditText count:", len(edit_text))
        if edit_text:
            handel_input_in_reading(driver)
        else:
            check_radio_button_from_reading(driver)
        if i<4:
            WebDriverWait(driver,15).until(lambda d:d.find_element(*question_locator).text !=previous_question)
    print("Lesson 3 Completed..............")
    WebDriverWait(driver,20).until(expected_conditions.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID,'Go to home'))).click()
    print("Day1 Complete Successfully")

