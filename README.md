# PhishingPack

PhishingPack is a powerful phishing tool that makes it easy to perform phishing attacks. It provides a simple command-line interface (CLI) to manage and run your phishing campaigns. With its modular design, you can easily add more templates and customize existing ones to fit your needs.

## Features

- User-friendly CLI
- Simple setup process
- Built-in template selector
- Real-time data monitoring
- Data collection and storage
- Multi-platform support

## Requirements

- Python 3.x
- `Flask`: A lightweight web framework for creating APIs
- `rich`: For colorful terminal output
- `pyfiglet`: To create eye-catching headers

## Getting Started

To use PhishingPack, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/ByteEncrypt/PhishingPack.git
cd PhishingPack
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate   # On Windows, use `env\Scripts\activate` instead.
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

## Usage

After starting the application, you will see the prompt `PhishingPack >`. Here are some basic commands to get you started:

| Command            | Description                         |
| ------------------ | ----------------------------------- |
| **help**           | Show available commands             |
| **clear**          | Clear the console screen            |
| **exit**           | Exit the application                |
| **server start**   | Start the phishing website          |
| **server stop**    | Stop the running phishing website   |
| **server status**  | Check whether the server is running |
| **server monitor** | Watch real-time attack results      |
| **data display**   | View captured credentials           |
| **data clear**     | Remove all stored credentials       |

For detailed information about each command, enter `help <command>`, e.g., `help server`.

## Building Your Own Template

Creating a new template involves editing HTML files located inside the `templates` directory. Make sure to include form fields with names matching those expected by PhishingPack:

- `username`
- `password`
- `user_agent`
- `time`

Once created, select the new template when launching the server.

## Disclaimer

This tool should be used responsibly and ethically. Unauthorized phishing attempts may violate local laws and regulations. Always obtain proper authorization before conducting any security testing.
