<div align='center'>

# Bard-CLI <img src='https://www.gstatic.com/lamda/images/favicon_v1_150160cddff7f294ce30.svg' width='35px'>

**Bard** CLI tool for interacting with Google's Bard chatbot.

<img src='https://github.com/x404xx/Bard-CLI/assets/114883816/952090f3-d5af-41d0-b9cc-90e4341f6273' width='auto' height='auto'>

</div>

## Authentication

Go to https://bard.google.com/

-   F12 for console
-   Copy the values

    -   Firefox Session: Go to Application → Cookies → `__Secure-1PSID` and `__Secure-1PSIDTS`. Copy the value of that cookie.

> **Note**
> After obtaining a `__Secure-1PSID` and `__Secure-1PSIDTS` you can save them somewhere and then run the program. By default, the program will ask you for a `__Secure-1PSID` and `__Secure-1PSIDTS` and make the JSON file automatically for you. Alternatively, you can create the **.env** or JSON file (_**bard_cookies.json**_) manually.

## Usage

To use _**Bard-CLI**_, open your terminal and navigate to the folder that contains _**Bard-CLI**_ content ::

```
pip install -r requirements.txt
```

Authenticate _**Bard-CLI**_ with command-line ::

```python
python main.py -s YOUR__Secure-1PSID -st YOUR__Secure-1PSIDTS
```

Alternatively, you can run _**Bard-CLI**_ without command-line. It will prompt you for the input `__Secure-1PSID` and `__Secure-1PSIDTS` ::

```python
python main.py
```

## Legal Disclaimer

> **Note**
> This was made for educational purposes only, nobody which directly involved in this project is responsible for any damages caused. **_You are responsible for your actions._**
