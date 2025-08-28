import pytest
from selenium import webdriver as web
from appium import webdriver as app
from appium.options.android import UiAutomator2Options  # 新增：导入Android选项类
import os

# 获取项目根目录
root_dir = os.path.dirname(os.path.abspath(__file__))


# ...（省略web_driver部分，保持不变）

@pytest.fixture(scope='session')
def app_driver():
    # Appium手机驱动配置（适配新版本客户端）
    chromedriver = os.path.join(root_dir, 'drivers\\chromedriver-win32\\appchromedriver.exe')

    # 1. 创建options对象（替代原来的desired_capabilities字典）
    options = UiAutomator2Options()

    # 2. 添加配置（用add_capability方法，参数名与之前一致）
    options.set_capability('platformName', 'Android')
    options.set_capability('udid', "MKB4C20622004049")  # 你的设备ID
    options.set_capability('automationName', 'UIAutomator2')
    options.set_capability('noReset', True)
    options.set_capability('fullReset', False)
    options.set_capability('chromedriverExecutable', chromedriver)
    options.set_capability('appPackage', "com.baidu.searchbox")  # 百度APP包名
    options.set_capability('appActivity', "com.baidu.searchbox.MainActivity")  # 启动活动名

    # 3. 连接Appium服务时，传入options参数（替代desired_capabilities）
    driver = app.Remote('http://127.0.0.1:4723', options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
