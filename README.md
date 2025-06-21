# Password Strength Analyzer & Custom Wordlist Generator

A cross-platform Python application with Tkinter GUI that evaluates password strength and generates attack-oriented wordlists from personal clues.

**Created by Sridhar S**
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)


## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
  - [Windows 10](#windows-10)
  - [Ubuntu 22.04](#ubuntu-2204)
  - [Manual Installation](#manual-installation)
- [Usage](#-usage)
  - [Password Analysis](#password-analysis)
  - [Wordlist Generation](#wordlist-generation)
- [Screenshots](#-screenshots)
- [License](#-license)

## 🚀 Features

### Password Analysis
- **zxcvbn Integration**: Uses the industry-standard zxcvbn library for accurate password strength assessment
- **Entropy Fallback**: Custom entropy calculation when zxcvbn is not available
- **Real-time Analysis**: Analyze passwords as you type
- **Color-coded Strength Meter**: Visual strength indicator (Very Weak → Very Strong)
- **Detailed Feedback**: Specific suggestions for password improvement
- **Crack Time Estimation**: Estimates time required to crack the password

### Wordlist Generation
- **Personal Information Input**: Name, birth date, pet name, favorite team, etc.
- **Custom Words**: Add your own words to the wordlist
- **Leetspeak Variations**: Common substitutions (a→@, e→3, i→1, o→0, s→$, t→7)
- **Case Variations**: lowercase, UPPERCASE, Title Case, AlTeRnAtInG
- **Year Appendages**: Current years, birth years, graduation years (4-digit and 2-digit)
- **Prefixes/Suffixes**: Common additions like "my", "123", "!", etc.
- **Export Ready**: Saves as UTF-8 text file for use with Hashcat, John the Ripper, etc.

### GUI Features
- **Cross-platform**: Works on Windows 10 and Ubuntu 22.04
- **Two-tab Interface**: Separate tabs for password analysis and wordlist generation
- **User-friendly**: Clean, intuitive interface with helpful tooltips
- **Real-time Preview**: See wordlist statistics and preview before saving
- **Progress Indicators**: Visual feedback during wordlist generation

## 📋 Requirements

- **Python 3.8+** (3.8, 3.9, 3.10, 3.11, 3.12 supported)
- **Operating System**: Windows 10 or Ubuntu 22.04 (other Linux distributions may work)
- **RAM**: Minimum 512 MB (1 GB recommended for large wordlists)
- **Storage**: 50 MB for installation, additional space for generated wordlists

### Python Dependencies
- `zxcvbn>=4.4.28` - Password strength estimation
- `nltk>=3.8.1` - Natural language processing utilities

## 💻 Installation

### Windows 10

1. **Download and Install Python**:
   - Download Python 3.8+ from [python.org](https://www.python.org/downloads/windows/)
   - During installation, **check "Add Python to PATH"**
   - Verify installation: Open Command Prompt and run `python --version`

2. **Download the Application**:
   - Download and extract the project files to a folder (e.g., `C:\PasswordTool`)

3. **Run the Installer**:
 Simply navigate to scripts folder and click installer_windows.bat
          Or
   ```cmd
   cd C:\PasswordTool
   scripts\installer_windows.bat
   ```

4. **Launch the Application**:
   - Navigate to project folder, click run_passwordtool.py
   - Or run: `.\venv\Scripts\python -m pass_tool.gui`

### Ubuntu 22.04

1. **Install Python and Dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv python3-tk
   ```

2. **Download the Application**:
   - Download and extract the project files to a folder (e.g., `~/PasswordTool`)

3. **Run the Installer**:
   ```bash
   cd ~/PasswordTool
   chmod +x scripts/installer_ubuntu.sh
   ./scripts/installer_ubuntu.sh
   ```

4. **Launch the Application**:
   - Use the desktop shortcut
   - Or from Applications menu → "Password Tool"
   - Or run: `./venv/bin/python -m pass_tool.gui`

### Manual Installation

If the automated installers don't work:

1. **Create Virtual Environment**:
   ```bash
   # Linux/Mac
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -e .
   ```

3. **Run the Application**:
   ```bash
   python -m pass_tool.gui
   ```

## 📖 Usage

### Password Analysis

1. **Open the Application** and navigate to the "Analyze Password" tab
2. **Enter a Password** in the input field
3. **View Results**:
   - Strength meter shows overall score (Very Weak to Very Strong)
   - Entropy shows password complexity in bits
   - Crack time estimates time required to break the password
   - Feedback provides specific improvement suggestions

**Tips**:
- Enable "Analyze as I type" for real-time feedback
- Use "Show Password" to verify what you've typed
- Aim for passwords with 60+ bits of entropy

### Wordlist Generation

1. **Navigate to "Generate Wordlist" tab**
2. **Enter Personal Information** (optional but recommended):
   - Full name, birth date, pet names, favorite teams, etc.
   - The more information you provide, the more targeted the wordlist

3. **Add Custom Words** (optional):
   - Add any additional words relevant to your target
   - One word per line

4. **Configure Options**:
   - **Leetspeak**: Include common character substitutions
   - **Case Variations**: Include different capitalization patterns
   - **Year Appendages**: Add relevant years (birth year, current year, etc.)
   - **Prefixes/Suffixes**: Add common prefixes and suffixes

5. **Set Word Limit**:
   - Default: 10,000 words
   - Increase for more comprehensive lists (may take longer to generate)

6. **Generate and Save**:
   - Click "Generate Wordlist" and wait for completion
   - Review the preview and statistics
   - Click "Save Wordlist" to export to a text file

**Example Use Cases**:
- **Social Engineering**: Generate passwords based on public information about a target
- **Penetration Testing**: Create custom wordlists for password attacks
- **Security Awareness**: Demonstrate how personal information can be used in attacks

## 📸 Screenshots

### Password Analysis Tab
*Analyze password strength with detailed feedback and visual indicators*
 ![tool](/assets/tool.png)

### Wordlist Generation Tab
*Generate custom wordlists from personal information with various transformations*
 ![wordlist](/assets/wordlist.png)


### Code Structure

- **`analyzer.py`**: Contains the `PasswordAnalyzer` class with zxcvbn integration and entropy fallback
- **`wordlist.py`**: Contains the `WordlistGenerator` class with all transformation logic
- **`gui.py`**: Contains the `PasswordToolGUI` class with the complete Tkinter interface


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛡️ Security Note

This tool is designed for legitimate security testing and educational purposes. Users are responsible for ensuring they have proper authorization before testing passwords or generating wordlists for systems they do not own.


**Created by Sridhar S - © 2025**
