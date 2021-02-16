#!/usr/bin/env python3
import subprocess
import optparse
import re


# Создание опций для программы
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest='interface', help='Интерфейс для изменения MAC адреcа.')
    parser.add_option("-m", "--mac", dest='new_mac', help='Новый MAC адреc.')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error('[-] Пожалуйста укажите интерфейс, используйте --help для информации.')
    elif not options.new_mac:
        parser.error('[-] Пожалуйста укажите новый MAC адресс, используйте --help для информации.')
    return options


# Создание вызовов необходимых команд в терминале
def change_mac(interface, new_mac):
    print('[+] Изменен MAC адресс ' + interface + ' на ' + new_mac)
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])


# Считываем МАС адресс нужного интерфейса
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface], universal_newlines=True)
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print('[-] Не возможно прочитать MAC адресс, проверьте интерфейс на наличие MAC!')


# Основной код программы
options = get_arguments()
current_mac = get_current_mac(options.interface)
print('Текущий MAC адресс = ' + str(current_mac))

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print('[+] MAC адресс был успешно изменен на ' + current_mac)
else:
    print('[-] MAC адресс не был изменен!')
