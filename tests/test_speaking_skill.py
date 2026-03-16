# import os
# import time
#
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.common import NoSuchElementException, TimeoutException
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.support.wait import WebDriverWait
#
#
# def test_speaking_skill_ai(driver):
#     email = "testuser5203@gmail.com"
#     try:
#         google_button = WebDriverWait(driver, 10).until(
#             expected_conditions.visibility_of_element_located((AppiumBy.XPATH,
#                                                                '//android.widget.TextView[@text="By clicking continue I agree to the"]/preceding-sibling::android.view.ViewGroup[6]')))
#         google_button.click()
#     except (TimeoutException, NoSuchElementException):
#         driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
#                             'new UiScrollable(new UiSelector().scrollable(true))'
#                             '.scrollIntoView(new UiSelector().text("By clicking continue I agree to the"))')
#         WebDriverWait(driver, 20).until(
#             expected_conditions.element_to_be_clickable((AppiumBy.XPATH,
#                                                          '//android.widget.TextView[@text="By clicking continue I agree to the"]/preceding-sibling::android.view.ViewGroup[@clickable="true" and @enabled="true"]'))).click()
#     WebDriverWait(driver, 10).until(
#         expected_conditions.visibility_of_element_located((AppiumBy.ID, "com.google.android.gms:id/main_title")))
#     driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{email}")').click()
#     WebDriverWait(driver, 20).until(
#         expected_conditions.visibility_of_element_located(
#             (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Let\'s start your learning journey")')))
#     driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'AI Tutor').click()
#     WebDriverWait(driver,10).until(
#         expected_conditions.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Speaking, Practice speaking skills with AI'))).click()
#     # Mute Mic
#     for i in range(5):
#         try:
#             mic_off = WebDriverWait(driver,20,poll_frequency=0.3).until(lambda d:d.find_element(AppiumBy.ACCESSIBILITY_ID,'Microphone listening'))
#             mic_off.click()
#             break
#         except (TimeoutException, NoSuchElementException):
#             print(f"Mic muted on retrying {i+1} time")
#             continue
#     bot_reply_locator = (AppiumBy.XPATH,'((//android.widget.ScrollView)[2]//android.widget.TextView)[position() mod 2 = 1]')
#     first_reply = WebDriverWait(driver, 30,poll_frequency=0.3).until(
#         expected_conditions.visibility_of_element_located(bot_reply_locator))
#     print(first_reply.text)
#     time.sleep(5)
#     # Unmute Mic
#     for i in range(5):
#         try:
#             mic_on = WebDriverWait(driver,20,poll_frequency=0.3).until(lambda d:d.find_element(AppiumBy.ACCESSIBILITY_ID,'Microphone muted'))
#             mic_on.click()
#             break
#         except (TimeoutException, NoSuchElementException):
#             print(f"Mic umuted on retrying {i+1} time")
#             continue
#     os.system(
#         'adb shell am start -a android.intent.action.VIEW -d "file:///sdcard/Recordings/i_dont_have_any_question.wav" -t audio/wav'
#     )
#     time.sleep(3)
#     pass