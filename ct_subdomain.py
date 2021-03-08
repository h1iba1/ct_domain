import requests
import re
import time
import sys


def get_result(target):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }

    req = requests.get(url='https://crt.sh/?CN=%25.' + target.strip('\n'), headers=headers, verify=True)
    results = re.findall(r"<TD>(.+\w)</TD>", req.text)
    # 去除开始爆破的域名防止多次搜索

    # 去除获取列表中的重复元素
    # results = {}.fromkeys(results).keys()
    results = list(set(results))

    # read_domain_file = open('domain.txt', 'r')
    read_tar_file = open('target.txt', 'r')
    target = target.strip('\n')
    if target in results:
        results.remove(target)

    if '*.' + target in results:
        results.remove('*.' + target)

    read_tar_file.close()
    return results


def file_exec(results):
    subdomain = 0
    domain = 0

    tar_file = open('target.txt', 'a')
    domain_file = open('domain.txt', 'a')

    for result in results:
        read_domain_file = open('domain.txt', 'r')
        read_tar_file = open('target.txt', 'r')
        # if '*' in result and (result not in read_tar_file.readlines()):
        if '*' in result:
            test = read_tar_file.readlines()

            result = result.replace('*.', '')
            tar_file.write(result + '\n')
            domain += 1
            read_tar_file.close()
        elif result not in read_domain_file.readlines():
            # else:
            test = read_domain_file.readlines()
            domain_file.write(result + '\n')
            subdomain += 1
            read_domain_file.close()

    tar_file.close()
    domain_file.close()
    print('获取域名：' + str(domain) + '个')
    print('获取子域名：' + str(subdomain) + '个' + '\n')


def get_target_file():
    # tar_file = open('target.txt', 'r')
    with open('target.txt', 'r') as tar_file:
        for target in tar_file.readlines():
            print("开始进行" + target.strip('\n') + "爆破:")
            file_exec(get_result(target))
            time.sleep(0.1)
    tar_file.close()


def display():
    count = len(open('domain.txt', 'r').readlines())
    print("总共发现子域名" + str(count) + '个' + '\n')


if __name__ == '__main__':
    target = sys.argv[1]
    print("开始进行" + target.strip('\n') + "爆破:")
    file_exec(get_result(target))
    print('开始进行多级域名爆破' + '\n')
    get_target_file()
    display()

