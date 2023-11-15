from argparse import ArgumentParser
from os import getenv
from pathlib import Path
from sys import stdout
from textwrap import dedent
from time import sleep

from classes import BardAPI, BardCookies, Colors, Utils

from dotenv import load_dotenv; load_dotenv()


class StartBard:
    def __init__(self, delay: float = 0.003, proxy: str = None):
        self.delay = delay
        self.proxy = proxy
        self._result()

    def _instruction(self):
        self._delay_print(dedent("""
            CLI tool for interacting with Google's Bard chatbot (https://bard.google.com)
               [!] PLEASE DOUBLE 'enter' TO SEND A MESSAGE.
                  - Type !clear to clear the console.
                  - Type !reset to reset the conversation.
                  - Type !exit to exit the program.
        """))

    def _delay_print(self, words: str):
        for word in words:
            stdout.write(word)
            stdout.flush()
            sleep(self.delay)
        stdout.write('\n')

    def _get_query(self, prompt: str) -> str:
        print(prompt, end='')
        return '\n'.join(iter(input, ''))

    def _handle_user_prompt(self, user_prompt: str, bard: BardAPI) -> bool:
        if user_prompt == '!exit':
            return False
        elif user_prompt == '!clear':
            Utils.clear_console()
            self._instruction()
        elif user_prompt == '!reset':
            self._reset_bard(bard)
            Utils.clear_console()
            self._instruction()
        else:
            self._ask_bard(user_prompt, bard)
        return True

    def _reset_bard(self, bard: BardAPI):
        bard.conversation_id = ''
        bard.response_id = ''
        bard.choice_id = ''

    def _ask_bard(self, user_prompt: str, bard: BardAPI):
        response = bard.question(user_prompt)
        self._delay_print(f'{Colors.DARKB}Bard{Colors.END} : {response}')

    def _get_bard_instance(self, args_1psid: str, args_1psidts: str) -> BardAPI:
        cookies = BardCookies.get_configuration(args_1psid, args_1psidts)
        if cookies.get('Secure-1PSID') and cookies.get('Secure-1PSIDTS'):
            return BardAPI(cookies=cookies, proxy=self.proxy)
        return None

    def _parse_arguments(self) -> tuple:
        parser = ArgumentParser()
        parser.add_argument('-s', '--session', type=str, help='__Secure-1PSID cookie')
        parser.add_argument('-st', '--session_ts', type=str, help='__Secure-1PSIDTS cookie')
        args = parser.parse_args()
        return args.session, args.session_ts

    def _start_chat(self, bard: BardAPI):
        while True:
            user_prompt = self._get_query(f'\n{Colors.GREEN}You{Colors.END} : ')
            if not self._handle_user_prompt(user_prompt, bard):
                break

    def _result(self):
        Utils.clear_console()
        self._instruction()
        config_file_path = Path(BardCookies.CONFIG_FILE)

        if config_file_path.exists():
            self._delay_print('✅ Configuration file found!\n')

        args_1psid, args_1psidts = self._parse_arguments()
        bard = self._get_bard_instance(args_1psid, args_1psidts)
        self._start_chat(bard)


if __name__ == '__main__':
    """
    If you want to use a proxy,
    Please update your PROXY in the environment variable or in the .env file.
    Otherwise, leave it as it is; it will be set to None.
    """
    StartBard(delay=0.002, proxy=getenv('PROXY'))
