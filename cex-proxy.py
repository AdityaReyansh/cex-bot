import requests
import os
import sys
import time
import threading
import json
from urllib.parse import parse_qs, unquote
import colorama
from colorama import Fore, Style
import random

class CexAPI:
    def __init__(self):
        colorama.init()
        self.headers = {
            'accept': '*/*',
            'accept-language': 'vi-VN,vi;q=0.9,en-IN;q=0.8,en;q=0.7,fr-FR;q=0.6,fr;q=0.5,en-US;q=0.4',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://cexp17.cex.io',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://cexp17.cex.io/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36',
            'x-appl-version': '0.18.0',
            'x-request-userhash': 'none'
        }
        with open('proxy.txt', 'r', encoding='utf8') as f:
            self.proxies = [line.strip() for line in f if line.strip()]

    def create_session(self, proxy):
        session = requests.Session()
        session.headers.update(self.headers)
        session.proxies = {
            'http': proxy,
            'https': proxy
        }
        return session

    def log(self, msg, type='info'):
        timestamp = time.strftime("%H:%M:%S")
        if type == 'success':
            print(f"{Fore.GREEN}[*] {msg}{Style.RESET_ALL}")
        elif type == 'error':
            print(f"{Fore.RED}[!] {msg}{Style.RESET_ALL}")
        elif type == 'warning':
            print(f"{Fore.YELLOW}[*] {msg}{Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE}[*] {msg}{Style.RESET_ALL}")

    def wait_with_countdown(self, seconds):
        for i in range(seconds, -1, -1):
            sys.stdout.write(f"\r{Fore.YELLOW}[*] Waiting {i} seconds to continue...{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(1)
        print('')

    def get_user_info(self, auth_data, session):
        url = "https://cexp.cex.io/api/v2/getUserInfo"
        payload = {
            "devAuthData": auth_data["id"],
            "authData": auth_data["authString"],
            "platform": "android",
            "data": {}
        }
        try:
            response = session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Error in getUserInfo: {str(e)}")

    def claim_crypto(self, auth_data, session):
        url = "https://cexp.cex.io/api/v2/claimCrypto"
        payload = {
            "devAuthData": auth_data["id"],
            "authData": auth_data["authString"],
            "platform": "android",
            "data": {}
        }
        try:
            response = session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Error in claimCrypto: {str(e)}")

    def claim_multi_taps(self, auth_data, session):
        url = "https://cexp.cex.io/api/v2/claimMultiTaps"
        total_claimed = 0
        user_data = self.get_user_info(auth_data, session)
        remaining_energy = int(user_data['data']['multiTapsEnergy'])

        while remaining_energy > 100:
            tap = min(100, remaining_energy)
            payload = {
                "devAuthData": auth_data["id"],
                "authData": auth_data["authString"],
                "platform": "android",
                "data": {
                    "tapsEnergy": str(remaining_energy),
                    "tapsToClaim": str(tap),
                    "tapsTs": int(time.time() * 1000)
                }
            }
            try:
                response = session.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                if data['status'] != 'ok':
                    raise Exception(f"Claim failed: {json.dumps(data)}")

                total_claimed += tap
                if 'data' in data and 'multiTapsEnergy' in data['data']:
                    remaining_energy = int(data['data']['multiTapsEnergy'])
                else:
                    remaining_energy -= tap

                self.log(f"Tapped {tap} times. Remaining energy: {remaining_energy}", 'success')
                time.sleep(1)

            except Exception as e:
                raise Exception(f"Error during tapping: {str(e)}")

        return {"status": "ok", "message": f"Used up {total_claimed} energy!"}

    def get_game_config(self, auth_data, session):
        url = "https://cexp.cex.io/api/v2/getGameConfig"
        payload = {
            "devAuthData": auth_data["id"],
            "authData": auth_data["authString"],
            "platform": "android",
            "data": {}
        }
        try:
            response = session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Error in getGameConfig: {str(e)}")

    def get_user_cards(self, auth_data, session):
        url = "https://cexp.cex.io/api/v2/getUserCards"
        payload = {
            "devAuthData": auth_data["id"],
            "authData": auth_data["authString"],
            "platform": "android",
            "data": {}
        }
        try:
            response = session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Error in getUserCards: {str(e)}")

    def buy_upgrade(self, auth_data, upgrade_data, session):
        url = "https://cexp.cex.io/api/v2/buyUpgrade"
        payload = {
            "devAuthData": auth_data["id"],
            "authData": auth_data["authString"],
            "platform": "android",
            "data": upgrade_data
        }
        try:
            response = session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Error during upgrade: {str(e)}")

    def process_upgrades(self, auth_data, session, balance_usd):
        try:
            game_config = self.get_game_config(auth_data, session)
            user_cards = self.get_user_cards(auth_data, session)

            if not game_config['upgradeCardsConfig'] or not user_cards['cards']:
                raise Exception("Invalid data")

            for category in game_config['upgradeCardsConfig']:
                for upgrade in category['upgrades']:
                    user_card = user_cards['cards'].get(upgrade['upgradeId'], {})
                    current_level = user_card.get('lvl', 0)

                    if 'dependency' in upgrade and upgrade['dependency']:
                        dependency_card = user_cards['cards'].get(upgrade['dependency']['upgradeId'], {})
                        if dependency_card and dependency_card.get('lvl', 0) < upgrade['dependency']['level']:
                            self.log(f"Skipping card {upgrade['upgradeName']}: Upgrade conditions not met", 'warning')
                            continue

                    if current_level < len(upgrade['levels']):
                        next_level = current_level + 1
                        cost, ccy, effect, effect_ccy, ukn = upgrade['levels'][current_level]

                        if ccy == "USD" and balance_usd < cost:
                            self.log(f"Skipping card {upgrade['upgradeName']}: Not enough USD (requires {cost} USD, have {balance_usd} USD)", 'warning')
                            continue

                        upgrade_data = {
                            "categoryId": category['categoryId'],
                            "upgradeId": upgrade['upgradeId'],
                            "nextLevel": next_level,
                            "cost": cost,
                            "ccy": ccy,
                            "effect": effect,
                            "effectCcy": effect_ccy
                        }

                        try:
                            result = self.buy_upgrade(auth_data, upgrade_data, session)
                            if result['status'] == 'ok':
                                self.log(f"Successfully upgraded card {upgrade['upgradeName']} to level {next_level}", 'success')
                                balance_usd -= cost
                            else:
                                self.log(f"Failed to upgrade card {upgrade['upgradeName']}: {result.get('message', '')}", 'error')
                        except Exception as e:
                            pass
                        time.sleep(1)
        except Exception as e:
            self.log(f"Error processing upgrades: {str(e)}", 'error')

    def ask_question(self, query):
        return input(query)

    def check_proxy_ip(self, proxy):
        attempts = 0
        max_attempts = 1
        session = self.create_session(proxy)
        while attempts < max_attempts:
            try:
                response = session.get('https://api.ipify.org?format=json')
                if response.status_code == 200:
                    return response.json()['ip']
                else:
                    self.log(f"Cannot check proxy IP. Status code: {response.status_code}")
            except Exception as e:
                attempts += 1
                self.log(f"Error checking proxy IP (Attempt {attempts}/{max_attempts}): {str(e)}", 'red')
                if attempts < max_attempts:
                    time.sleep(2)
                else:
                    self.log(f"Error checking proxy IP after {max_attempts} attempts: {str(e)}")
                    break

    def sleep(self, ms):
        time.sleep(ms / 1000)

    def get_convert_data(self, auth_data, session):
        url = "https://cexp.cex.io/api/v2/getConvertData"
        payload = {
            "devAuthData": auth_data["id"],
            "authData": auth_data["authString"],
            "platform": "android",
            "data": {}
        }
        try:
            response = session.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'ok' and data['convertData']['lastPrices']:
                last_price = data['convertData']['lastPrices'][-1]
                return last_price
            else:
                raise Exception("Cannot retrieve last price")
        except Exception as e:
            raise Exception(f"Error in getConvertData: {str(e)}")

    def convert_crypto(self, auth_data, session, user_data, btc_to_convert=None):
        url = "https://cexp.cex.io/api/v2/convert"
        last_price = self.get_convert_data(auth_data, session)
        divisor = pow(10, int(user_data['precision_BTC']))
        if btc_to_convert is None:
            from_amount = round(float(user_data['balance_BTC']) / divisor, int(user_data['precision_BTC']))
        else:
            from_amount = btc_to_convert
        payload = {
            "devAuthData": auth_data["id"],
            "authData": auth_data["authString"],
            "platform": "android",
            "data": {
                "fromCcy": "BTC",
                "toCcy": "USD",
                "fromAmount": str(from_amount),
                "price": last_price
            }
        }
        try:
            response = session.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'ok':
                new_balance_usd = data['convert']['balance_USD']
                self.log(f"Successfully swapped Crypto to USD | New USD Balance: {new_balance_usd}", 'success')
                return new_balance_usd
            else:
                raise Exception("Conversion failed")
        except Exception as e:
            raise Exception(f"Error in convertCrypto: {str(e)}")

    def ask_swap_percentage(self):
        while True:
            percentage = self.ask_question('How much % of balance_BTC do you want to swap to USD? (0-100): ')
            try:
                parsed_percentage = float(percentage)
                if 0 <= parsed_percentage <= 100:
                    return parsed_percentage
                else:
                    self.log('Invalid value. Please enter a number from 0 to 100.', 'error')
            except ValueError:
                self.log('Invalid value. Please enter a number from 0 to 100.', 'error')

    def main(self):
        data_file = 'data.txt'
        data = []
        with open(data_file, 'r', encoding='utf8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parsed = parse_qs(line)
                    user_json = json.loads(unquote(parsed.get('user', [''])[0]))
                    data.append({
                        'id': user_json['id'],
                        'authString': line,
                        'hash': parsed.get('hash', [''])[0]
                    })

        self.log('Tool shared on Airdrop Automation Telegram channel (@airdrop_auto_free)', 'success')

        buy_cards = self.ask_question('Do you want to buy and upgrade cards? (y/n): ')
        buy_cards_decision = buy_cards.lower() == 'y'

        swap = self.ask_question('Do you want to swap Crypto to USD? (y/n): ')
        do_swap = swap.lower() == 'y'
        swap_percentage = 0
        if do_swap:
            swap_percentage = self.ask_swap_percentage()

        while True:
            for i, account_data in enumerate(data):
                try:
                    proxy = self.proxies[i % len(self.proxies)]
                    session = self.create_session(proxy)
                    session.headers.update({
                        'x-request-userhash': account_data.get('hash')
                    })
                    proxy_ip = 'Unknown'
                    try:
                        proxy_ip = self.check_proxy_ip(proxy)
                    except Exception as e:
                        self.log(f"Cannot check proxy IP: {str(e)}", 'red')

                    result = self.get_user_info(account_data, session)
                    if result['status'] == 'ok':
                        user_data = result['data']
                        print(f"========== Account {i + 1} | {Fore.GREEN}{user_data['first_name']}{Style.RESET_ALL} | IP: {proxy_ip} ==========")
                        claim_crypto_result = self.claim_crypto(account_data, session)
                        if claim_crypto_result['status'] == 'ok':
                            self.log("Successfully claimed Crypto!", 'success')
                        else:
                            self.log("Failed to claim Crypto!", 'error')

                        divisor = pow(10, int(user_data['precision_BTC']))
                        self.log(f"Balance BTC: {float(user_data['balance_BTC']) / divisor}", 'success')
                        self.log(f"Balance USD: {user_data['balance_USD']}", 'success')
                        self.log(f"Balance CEXP: {user_data['balance_CEXP']}", 'success')
                        self.log(f"Energy: {user_data['multiTapsEnergy']} / {user_data['multiTapsEnergyLimit']}", 'info')

                        if do_swap:
                            if float(user_data['balance_BTC']) > 0.0 and swap_percentage > 0:
                                try:
                                    btc_to_convert = round((float(user_data['balance_BTC']) / divisor) * (swap_percentage / 100), int(user_data['precision_BTC']))
                                    user_data['balance_BTC'] = btc_to_convert * divisor
                                    new_balance_usd = self.convert_crypto(account_data, session, user_data, btc_to_convert)
                                    user_data['balance_USD'] = new_balance_usd
                                    self.log(f"New USD Balance after swap: {new_balance_usd}", 'success')
                                except Exception as e:
                                    self.log(f"Cannot convert crypto: {str(e)}", 'error')
                            else:
                                self.log("Not enough BTC to swap or invalid percentage.", 'warning')

                        if user_data['multiTapsEnergy'] > 100:
                            try:
                                claim_multi_taps_result = self.claim_multi_taps(account_data, session)
                                self.log(claim_multi_taps_result['message'], 'success')

                                final_user_info = self.get_user_info(account_data, session)
                                self.log(f"Balance USD: {final_user_info['data']['balance_USD']}", 'success')
                            except Exception as e:
                                pass
                        else:
                            self.log("Not enough energy, need over 100 to tap", 'warning')

                        if buy_cards_decision:
                            self.process_upgrades(account_data, session, float(user_data['balance_USD']))

                    else:
                        self.log(f"Error reading account {i + 1}: {json.dumps(result)}", 'error')

                except Exception as e:
                    self.log(f"Error processing account {i + 1}: {str(e)}", 'error')

            self.wait_with_countdown(1800)

if __name__ == '__main__':
    api = CexAPI()
    try:
        api.main()
    except Exception as e:
        print(e)
        sys.exit(1)
