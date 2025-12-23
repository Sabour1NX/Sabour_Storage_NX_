import random
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from pythonping import ping
import webbrowser
from requests.exceptions import RequestException, HTTPError
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import multiprocessing

def selectbaseURL():
    minDelay = 3000
    baseURL = None
    urls = [
        "18comic.vip",
        "18comic.ink",
        "jmcomic-zzz.one",
        "jmcomic-zzz.org",  
        "jm18c-qwq.club",
        "jm18c-qwq.org",
    ]

    for i in urls:
        try:
            result = ping(i, count=4, timeout=2)
            if result.success():
                urlDelay = result.rtt_avg_ms
                print(f"Domain: {i}, Delay: {urlDelay:.2f}ms")
                if urlDelay < minDelay:
                    minDelay = urlDelay
                    baseURL = i
            else:
                print(f"Domain: {i}, status: Unresponsive")
        except Exception as e:
            print(f"Domain: {i}, error: {str(e)}")
            continue
    
    if baseURL is None:
        print("All domain name tests failed. Randomly select one")
        baseURL = random.choice(urls)
    return baseURL

def random_JID (baseURL):
    randomID = random.randint(100000,999999)
    resultURL = "https://"+baseURL +"/album/"+ str(randomID)+"/"
    return resultURL

def BrowserAction(resultURL):
    k = 0
    while True:
        try:
            edge_options = Options()
            # 减少日志噪音
            edge_options.add_argument("--headless")
            edge_options.add_argument("--log-level=3")  # 只显示致命错误
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument("--disable-extensions")
            edge_options.add_argument("--disable-gpu")
            edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            #验证pid是否有效
            driver = webdriver.Edge(options=edge_options)
            driver.get(resultURL)
            current_url = driver.current_url
            print(f"current URL: {current_url}")
            if "error" in current_url:
                print("Invaild url , retrying...")
                driver.quit()
                break
            else:
                webbrowser.open(resultURL)#正式为用户打开
                isComplete = True
                return isComplete
        except RequestException as e:
            k += 1
            print(f"RequestException:{current_url} , retry{k}time(s)")
            if k>= 3:
                print("RequestExceptio:{current_url} , too many times!")
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
        except ConnectionError as e:
            print(f"ConnectionError: {e}")
            raise
        except HTTPError as e:
            print(f"HTTPError: {e}")
            print(f"status: {current_url.status_code}")
            raise
            
def randJMconic_work ():
    while True:
        isComplete = False
        try:
            baseURL = selectbaseURL ()
            resultURL = random_JID(baseURL)
            isComplete = BrowserAction(resultURL)
            if isComplete == True:
                break
            else:
                continue
        except Exception as e :
            print(e)
            break
        except KeyboardInterrupt:
            print("KeyboardInterrupt,exiting...")
            break

current_process = None#全局变量

def randJMconic_process_start ():
    global current_process
    current_process = multiprocessing.Process(target=randJMconic_work)
    current_process.start()
    print("进程已启动:randJMconic_work")

def Emergency_Stop ():
    global current_process
    if current_process and current_process.is_alive():
        current_process.terminate()  # 强制终止
        current_process.join(timeout=1.0)
        print("进程已立即终止:randJMconic_work")

def App_main ():
    root = tk.Tk()
    root.resizable(False, False)
    root.title("RandomJMcomic--自动翻牌器")
    root.geometry("450x350")
    label = tk.Label(root, text="功能：自动检测网络连接状态\n随机生成车牌号组成链接\n并自动前往目标网站", font=("微软雅黑", 8), fg="black")
    label.place(x=10, y=10, width=160, height=60)
    button_0 = tk.Button(root, text="随机JM本子", command=randJMconic_process_start)
    button_0.place(x=40,y=90,width=100,height=60)
    button_1 = tk.Button(root, text="急停",bg="red",activebackground="darkred", activeforeground="white",command=Emergency_Stop)
    button_1.place(x=40,y=180,width=100,height=60)
    
    try:
        image_JM_tan = Image.open("JmSmile.png")
        image_JM_tan = image_JM_tan.resize((250, 250), Image.LANCZOS)
        photo_jm_tan = ImageTk.PhotoImage(image_JM_tan)
        image_label = tk.Label(root, image=photo_jm_tan)
        image_label.place(x=170, y=10)
        image_label.image = photo_jm_tan
    except Exception as e:
        error_label = tk.Label(root, text=f"无法加载图片: {e}", fg="red")
        error_label.pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    App_main()