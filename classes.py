import json
import os
import sys
from random import randint
from re import search, sub
from textwrap import dedent
from time import sleep
from typing import Dict

from dotenv import load_dotenv
from halo import Halo
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer
from requests import Session
from spinners import Spinners


class Colors:
    GREEN = '\033[38;5;121m'
    DARKB = '\033[38;5;20m'
    LPURPLE = '\033[38;5;141m'
    END = '\033[0m'


class Utils:
    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def exit_program():
        sys.exit()


class Formatter:
    CODE_INDENTIFIER = '```'
    CODE_INDENT = '        '
    DASH = r'`(.*?)`'

    @classmethod
    def _code_block(cls, text: str) -> str:
        return sub(cls.DASH, r'\g<1>', text)

    @classmethod
    def _highlight_code(cls, text: str) -> str:
        code = highlight(text, PythonLexer(), Terminal256Formatter(style='fruity')).strip()
        highlighted_lines = [cls.CODE_INDENT + line.replace('python', '') for line in code.splitlines()]
        return '\n'.join(highlighted_lines)

    @classmethod
    def final_text(cls, response: str) -> str:
        sections = response.split(cls.CODE_INDENTIFIER)
        formatted_text = ''
        for idx, text in enumerate(sections):
            if idx % 2 == 0:
                formatted_text += cls._code_block(f'{Colors.LPURPLE}{text}{Colors.END}')
            else:
                formatted_text += cls._highlight_code(text)
        return formatted_text


class BardAPI:
    BASE_URL = 'https://bard.google.com'

    def __init__(self, cookies: dict, proxy: str = None):
        self.spinner = Halo(text_color='blue', spinner=Spinners['point'].value, color='magenta')
        self.reqid = randint(1000000, 8999999)
        self.conversation_id = ''
        self.response_id = ''
        self.choice_id = ''
        self.session = Session()
        self.session.proxies.update({'http': proxy, 'https': proxy})
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'})
        self.session.cookies.set('__Secure-1PSID', cookies['Secure-1PSID'])
        self.session.cookies.set('__Secure-1PSIDTS', cookies['Secure-1PSIDTS'])
        self.snlm0e = self._get_snlm0e()

    def __del__(self):
        self.session.close()
        print('Session Closed!')

    def _get_snlm0e(self) -> str:
        with self.spinner as status:
            status.start('Loading..')
            sleep(1)
            try:
                response = self.session.get(self.BASE_URL, timeout=10)
            except Exception as exc:
                status.fail(f'Requests encountered an error: {str(exc)}')
                Utils.exit_program()
            else:
                snlm0e = search(r'SNlM0e":"(.*?)"', response.text)
                if snlm0e is None:
                    status.fail('Fail to get BardAI!')
                    Utils.exit_program()
                else:
                    snlm0e = snlm0e[1]
                    status.succeed(f'Welcome to BardAI!')
                    return snlm0e

    def question(self, message: str) -> str:
        params = {
            'bl': 'boq_assistant-bard-web-server_20231031.09_p7',
            '_reqid': str(self.reqid),
            'rt': 'c',
        }

        message_body = [
            [message],
            None,
            [self.conversation_id, self.response_id, self.choice_id],
        ]

        data = {
            'f.req': json.dumps([None, json.dumps(message_body)]),
            'at': self.snlm0e,
        }

        with self.spinner as status:
            status.start('Please wait! Bard is thinking ..')
            try:
                response = self.session.post(
                    f'{self.BASE_URL}/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate',
                    params=params,
                    data=data,
                    timeout=60,
                )
            except Exception as exc:
                status.fail(f'Requests encountered an error: {str(exc)}')
                Utils.exit_program()
            else:
                chat_data = json.loads(response.content.splitlines()[3])[0][2]
                if not chat_data:
                    status.warn(f'Chat data encountered an error: {response.content}.')
                    Utils.exit_program()

                json_chat_data = json.loads(chat_data)
                results = {
                    'content': json_chat_data[4][0][1][0],
                    'conversation_id': json_chat_data[1][0],
                    'response_id': json_chat_data[1][1],
                    'factualityQueries': json_chat_data[3],
                    'textQuery': json_chat_data[2][0] if json_chat_data[2] is not None else '',
                    'choices': [{'id': i[0], 'content': i[1]} for i in json_chat_data[4]]
                }
                self.conversation_id = results['conversation_id']
                self.response_id = results['response_id']
                self.choice_id = results['choices'][0]['id']
                self.reqid += 1000000
                status.succeed('Solution Found!')
                return Formatter.final_text(results['content'])


class BardCookies:
    CONFIG_FILE = 'bard_cookies.json'
    MISSING_CONFIG = '''
    ⚠️  Could not find (Secure-1PSID, Secure-1PSIDTS) in environment variables or configuration.
    ⚠️  Please choose one of the following options:
        [1] Manually enter (Secure-1PSID, Secure-1PSIDTS)
        [2] Exit
    '''

    @staticmethod
    def _user_choice() -> Dict[str, str]:
        while True:
            user_choice = input('Enter your choice: ')
            if user_choice == '2':
                Utils.exit_program()
            elif user_choice == '1':
                return {
                    'Secure-1PSID': input('Enter __Secure-1PSID cookie: '),
                    'Secure-1PSIDTS': input('Enter __Secure-1PSIDTS cookie: '),
                }
            else:
                print('📛 Wrong input! Please check your value!')

    @classmethod
    def _save_config(cls, config: Dict[str, str]):
        with open(cls.CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)
        print(f'\n"{cls.CONFIG_FILE}" file has been created successfully.\n')

    @classmethod
    def _load_config(cls) -> Dict[str, str]:
        try:
            with open(cls.CONFIG_FILE, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @classmethod
    def _prompt_user_choice(cls) -> Dict[str, str]:
        print(dedent(cls.MISSING_CONFIG))
        return cls._user_choice()

    @classmethod
    def _set_bard_cookies(cls, secure_1PSID: str, secure_1PSIDTS: str):
        cls.save_config(config={'Secure-1PSID': secure_1PSID, 'Secure-1PSIDTS': secure_1PSIDTS})

    @classmethod
    def _get_bard_cookies(cls, args_1psid: str, args_1psidts: str):
        load_dotenv()
        secure_1PSID = os.getenv('Secure-1PSID')
        secure_1PSIDTS = os.getenv('Secure-1PSIDTS')

        if not secure_1PSID and not secure_1PSIDTS:
            if args_1psid and args_1psidts:
                secure_1PSID = args_1psid
                secure_1PSIDTS = args_1psidts
            else:
                config = cls._prompt_user_choice()
                secure_1PSID = config['Secure-1PSID']
                secure_1PSIDTS = config['Secure-1PSIDTS']
            cls._set_bard_cookies(secure_1PSID, secure_1PSIDTS)

        return secure_1PSID, secure_1PSIDTS

    @classmethod
    def get_configuration(cls, args_1psid: str, args_1psidts: str):
        config = cls._load_config()
        secure_1PSID = config.get('Secure-1PSID')
        secure_1PSIDTS = config.get('Secure-1PSIDTS')

        if not secure_1PSID and not secure_1PSIDTS:
            secure_1PSID, secure_1PSIDTS = cls._get_bard_cookies(
                args_1psid, args_1psidts
            )

        config['Secure-1PSID'] = secure_1PSID
        config['Secure-1PSIDTS'] = secure_1PSIDTS
        return config
