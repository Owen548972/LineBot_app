import random
import requests
from bs4 import BeautifulSoup


def get_lottory():
    numbers = random.sample(list(range(1, 50)), 6)
    spec_number = random.randint(1, 50)
    numbers = ",".join(map(str, numbers)) + f"特別號: {spec_number}"
    print(numbers)
    return numbers


def get_true_lottory():
    url = "https://www.taiwanlottery.com.tw/lotto/superlotto638/history.aspx"
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        trs = soup.find("table", class_="table_org td_hm").find_all("tr")
        numbers = trs[5].text.strip().split()[1:]
        big_lottory = ",".join(numbers[:-1]) + f" 特別號:{numbers[-1]}"
        date = ",".join(trs[1].text.strip().split()[:2])
        result = f"期數/日期 {date}\n號碼:{big_lottory}"
        return result
    except Exception as e:
        print(e)

    return "查詢失敗,請稍後查詢..."


if __name__ == "__main__":
    get_lottory()
    get_true_lottory()
