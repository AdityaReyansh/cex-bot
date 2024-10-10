## Table of Contents

*   [Recommendation Before Use](#recommendation-before-use)
*   [Features](#features)
*   [Settings](#settings)
*   [Quick Start](#quick-start)
*   [Prerequisites](#prerequisites)
*   [Installation](#installation)
*   [Support](#support-this-project)
*   [Contacts](#contacts)

# CexAPI Tool

## Recommendation Before Use

Before using this tool, please ensure that automating interactions with the cex.io platform does not violate their terms of service or any applicable laws in your jurisdiction. Use this tool responsibly and at your own risk.

## Features

| Feature | Supported |
| --- | --- |
| Automatic Crypto Claiming | ✅   |
| Automatic Energy Tapping | ✅   |
| Automatic Card Purchasing and Upgrading | ✅   |
| Crypto to USD Conversion | ✅   |
| Multiple Account Management with Proxies | ✅   |
| User-Friendly Command-Line Interface | ✅   |
| Proxy Binding to Sessions | ✅   |
| Customizable Settings | ✅   |
| Sleep Mode Between Rounds | ✅   |
| Multithreading Support | ✅   |

## Settings

| Setting | Description |
| --- | --- |
| **buy\_cards\_decision** | Decide whether to automatically buy and upgrade cards (default: Prompted at runtime) |
| **do\_swap** | Decide whether to swap Crypto to USD (default: Prompted at runtime) |
| **swap\_percentage** | Percentage of Crypto balance to swap to USD (default: User input) |
| **proxies** | List of proxies from `proxy.txt` to manage multiple accounts |
| **data** | Account data from `data.txt` |
| **headers** | Custom headers for HTTP requests (including User-Agent) |
| **sleep\_time** | Time in seconds to sleep between rounds (default: 1800 seconds) |
| **max\_attempts** | Maximum attempts for checking proxy IP (default: 1) |
| **User-Agent** | Custom User-Agent string for HTTP requests |
| **Logging Levels** | Customize log levels for different types of messages |

## Quick Start

To install libraries and run the tool, follow the instructions for your operating system below.

## Prerequisites

Before you begin, make sure you have the following installed:

*   [Python](https://www.python.org/downloads/) **IMPORTANT**: Use **Python 3.6 or later**.
*   Basic understanding of command-line operations.
*   Account data prepared in `data.txt`.
*   Proxy list prepared in `proxy.txt`.

## Installation

### Linux Manual Installation

1.  **Install Python 3 and pip:**
    
    `sudo apt update sudo apt install python3 python3-pip -y`
    
2.  **Install Required Libraries:**
    
    `pip3 install requests colorama`
    
3.  **Download the Script:**
    
    `git clone https://github.com/AdityaReyansh/cex-bot.git cd cex-bot`
    
4.  **Prepare `data.txt` and `proxy.txt`:**
    
    *   Create `data.txt` containing your account data in the "query_id=AAElJXXXX" format.
        
    *   Create `proxy.txt` containing your proxies, one per line, in the format:
        
        `http://username:password@proxy_ip:proxy_port`
        
        or
        
        `https://proxy_ip:proxy_port`
        
5.  **Run the Script:**
    
    `python3 cexapi.py`
    

### Windows Manual Installation

1.  **Install Python 3:**
    
    *   Download and install Python 3 from the [official website](https://www.python.org/downloads/windows/).
    *   During installation, ensure you check "Add Python to PATH".
2.  **Open Command Prompt:**
    
    Press `Win + R`, type `cmd`, and press Enter.
    
3.  **Install Required Libraries:**
    
    
    `pip install requests colorama`
    
4.  **Download the Script:**
    
    `git clone https://github.com/yourusername/cexapi-tool.git cd cexapi-tool`
    
5.  **Prepare `data.txt` and `proxy.txt`:**
    
    *   Create `data.txt` with your account data.
    *   Create `proxy.txt` with your proxies in the required format.
6.  **Run the Script:**
    
    
    `python cexapi.py`
    

### Termux Manual Installation

1.  **Install Termux:**
    
    *   Download Termux from the F\-Droid repository or [GitHub](https://github.com/termux/termux-app#installation).
2.  **Update and Upgrade Packages:**
    
    
    `pkg update && pkg upgrade -y`
    
3.  **Install Python and Git:**

    
    `pkg install python git -y`
    
4.  **Install Required Libraries:**

    `pip install requests colorama`
    
5.  **Download the Script:**

    `git clone https://github.com/yourusername/cexapi-tool.git cd cexapi-tool`
    
6.  **Prepare `data.txt` and `proxy.txt`:**
    
    *   Use `nano` or any text editor to create `data.txt` and `proxy.txt` with the required content.
7.  **Run the Script:**
    
    `python cexapi.py`
    

## Support This Project

If you'd like to support the development of this project, please consider making a donation. Every contribution helps!

Your support allows us to keep improving the project and bring more features!

Thank you for your generosity! 🙌

## Contacts

For support or questions, you can contact me [![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/airdrop_auto_free)
