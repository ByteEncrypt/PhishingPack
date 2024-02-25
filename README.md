# PhishingPack

PhishingPack is a powerful phishing tool that provides phishing site templates for popular sites and it makes it easy to capture credentials from the victim. It provides a simple command-line interface (CLI) to manage and run your phishing campaigns.

<br/>

## Features

- User-friendly CLI
- Simple setup process
- Built-in templates
- Real-time data monitoring

<br/>

## Built-in templates

PhishingPack comes with the following built-in site templates:

- Amazon
- Facebook
- Instagram
- LinkedIn
- paypal

<br/>

## Requirements

`PhishingPack` is built with Python and its dependencies. So, you must have python 3.x installed on your operating system to run it.

<br/>

## Getting Started

To use PhishingPack, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/ByteEncrypt/PhishingPack.git
```

2. Change the current working directory

```bash
cd PhishingPack
```

3. Create a virtual environment and activate it:

```bash
python3 -m venv venv
```

4. Activate the virtual environment

```bash
venv\Scripts\activate # For Windows
source venv/bin/activate   # For Linux
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run the application:

```bash
python PhishingPack.py
```

<br/>

## Usage

Here are some basic commands to get you started:

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

## Building Your Own Template

It is not a big deal to build your own template. Just follow the following steps to create a new template:

- Create a new html file in the `templates` directory with the appropriate name.
- Place the corresponding css stylesheet in the `/static/styles` directory
- Place your template images and other assets in the `/static/images` directory
- Make sure to add the html form with the id `form` and the button with type `submit`
- Then must include `/static/scripts/formHandler.js` in the html file to automatically handle the form submission
- Finally, it is important to add the corresponding fields in `/config/sites.json` file to update main application configuration

That's all you need to do here.

<br/>

## Need help?

At the end, if you have any question or need any help, you can start a new discussion or issue for this repository.

<br/>

## Disclaimer

This tool should be used responsibly and ethically. Unauthorized phishing attempts may violate local laws and regulations. Always obtain proper authorization before conducting any security testing.
