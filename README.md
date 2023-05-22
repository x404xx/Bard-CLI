<div align="center">

# Bard-CLI <img src="https://www.gstatic.com/lamda/images/favicon_v1_150160cddff7f294ce30.svg" width="35px" />

**Bard** CLI tool for interacting with Google's Bard chatbot.

<img src="https://github.com/x404xx/Bard-CLI/assets/114883816/952090f3-d5af-41d0-b9cc-90e4341f6273" width="auto" height="auto">

</div>

## **Authentication**

Go to https://bard.google.com/

-   F12 for console
-   Copy the values
    -   Session: Go to Application → Cookies → `__Secure-1PSID`. Copy the value of that cookie.

    <img src="https://github.com/x404xx/Bard-CLI/assets/114883816/6c221352-5c60-41f3-82cf-0bf773a58071" width="auto" height="auto">

> **Note**
> After obtaining a `__Secure-1PSID`, you can save them somewhere and then run the program. By default, the program will ask you for a `__Secure-1PSID` and make the JSON file automatically for you. Alternatively, you can create the **.env** or JSON file (**_bard_cookies.json_**) manually.

## **Usage**

To use _Bard-CLI_, open your terminal and navigate to the folder that contains _Bard-CLI_ content ::

```sh
pip install -r requirements.txt
```

Authenticate _Bard-CLI_ with command-line ::

```sh
python main.py --session YOUR__Secure-1PSID
```

Alternatively, you can run _Bard-CLI_ without command-line. It will prompt you for the input `__Secure-1PSID` ::

```sh
python main.py
```

## **Legal Disclaimer**

> **Note**
> This was made for educational purposes only, nobody which directly involved in this project is responsible for any damages caused. **_You are responsible for your actions._**
