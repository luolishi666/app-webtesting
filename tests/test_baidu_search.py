import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestBaiduSearch:
    def test_search_pytest(self, app_driver):
        driver = app_driver

        # 检查是否在百度APP中
        try:
            current_package = driver.current_package
            if current_package != "com.baidu.searchbox":
                print(f"当前不在百度APP中，正在启动...")
                driver.start_activity("com.baidu.searchbox", "com.baidu.searchbox.MainActivity")
                time.sleep(5)
        except:
            # 如果无法获取当前包名，尝试启动百度APP
            driver.start_activity("com.baidu.searchbox", "com.baidu.searchbox.MainActivity")
            time.sleep(5)

        try:
            # 步骤1: 点击搜索框 - 使用文本定位
            search_box = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView'))
            )
            search_box.click()

            # 步骤2: 输入关键词 - 使用EditText类定位输入框
            input_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
            )
            input_field.clear()
            input_field.send_keys("pytest")

            # 步骤3: 点击搜索按钮 - 通过文本"搜索"定位
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@text="搜索"]'))
            )
            search_button.click()

            # 步骤4: 验证搜索结果
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@text, 'pytest')]"))
            )

            results = driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, 'pytest')]")
            assert len(results) > 0, "搜索结果中未找到关键词'pytest'"

        except Exception as e:
            driver.save_screenshot("search_pytest_error.png")
            raise e

    def test_search_empty_keyword(self, app_driver):
        driver = app_driver

        # 检查是否在百度APP中
        try:
            current_package = driver.current_package
            if current_package != "com.baidu.searchbox":
                print(f"当前不在百度APP中，正在启动...")
                driver.start_activity("com.baidu.searchbox", "com.baidu.searchbox.MainActivity")
                time.sleep(5)
        except Exception as e:
            print(f"检查包名时出错: {e}")
            driver.start_activity("com.baidu.searchbox", "com.baidu.searchbox.MainActivity")
            time.sleep(5)
        try:
            # 确保回到首页 - 按返回键直到回到主页
            for _ in range(5):
                try:
                    # 检查是否在首页（有搜索框）
                    search_box = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView'))
                    )
                    print("已在首页，继续测试")
                    break
                except:
                    # 如果不在首页，按返回键
                    driver.back()
                    time.sleep(3)
            else:
                # 如果循环结束还没有回到首页，重启应用
                print("无法回到首页，重启应用")
                driver.start_activity("com.baidu.searchbox", "com.baidu.searchbox.MainActivity")
                time.sleep(5)

            # 点击搜索框
            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView'))
            )
            search_box.click()

            # 清空输入框（确保没有内容）
            input_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
            )
            input_field.clear()
            time.sleep(1)  # 等待清空完成

            search_button_found = False
            try:
                # 方式1: 通过文本定位
                search_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, '//*[@text="搜索"]'))
                )
                search_button_found = True
            except:
                try:
                    # 方式2: 通过content-desc定位
                    search_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((AppiumBy.XPATH, '//*[@content-desc="搜索"]'))
                    )
                    search_button_found = True
                except:
                    try:
                        # 方式3: 通过类名和文本定位
                        search_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((AppiumBy.XPATH,
                                                        '//android.widget.Button[contains(@text, "搜索")]'))
                        )
                        search_button_found = True
                    except:
                        print("未找到搜索按钮，尝试使用键盘回车键")

            if search_button_found:
                search_button.click()
            else:
                # 如果没有找到搜索按钮，使用键盘回车键进行搜索
                # 确保输入框获得焦点
                input_field = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
                )
                input_field.click()
                time.sleep(1)

                # 定位输入框并清除可能存在的自动填充内容
                input_field = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
                )

                # 先清除输入框内容
                input_field.clear()
                time.sleep(1)

                # 再次清除，确保没有自动填充内容
                input_field.clear()
                time.sleep(1)

                # 按回车键执行搜索
                driver.press_keycode(66)  # 66是回车键的键码
                print("使用键盘回车键执行搜索")

            time.sleep(3)  # 等待错误提示出现

            # 检查错误提示
            error_tip = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((AppiumBy.XPATH,
                                                  "//*[contains(@text, '请输入') or contains(@text, '搜索') or contains(@text, '空') or contains(@content-desc, '请输入')]"))
            )
            assert error_tip.is_displayed(), "空关键词搜索未提示错误信息"

        except Exception as e:
            driver.save_screenshot("search_empty_error.png")
            raise e