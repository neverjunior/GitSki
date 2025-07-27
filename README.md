# 🔍 GitSki - GitHub Secret Scanner

<div align="center">

```
 ██████╗ ██╗████████╗███████╗██╗  ██╗██╗
██╔════╝ ██║╚══██╔══╝██╔════╝██║ ██╔╝██║
██║  ███╗██║   ██║   ███████╗█████╔╝ ██║
██║   ██║██║   ██║   ╚════██║██╔═██╗ ██║
╚██████╔╝██║   ██║   ███████║██║  ██╗██║
 ╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝

╔══════════════════════════════════════════════════════════════╗
║                    GitHub Secret Scanner                     ║
║                    Find Exposed API Keys                     ║
║                                                              ║
║                    - by Abhijeet                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Getting Rate Limited.. Sorry what's that?**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)](https://playwright.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/yourusername/gitski?style=social)](https://github.com/yourusername/gitski)

*A powerful tool to scan GitHub repositories for exposed API keys, secrets, and credentials*

</div>

---

## 🚀 Features

### 🔐 **Comprehensive Secret Detection**
- **40+ regex patterns** for detecting various types of secrets
- **Cloud Services**: AWS, Google Cloud, Azure, Firebase
- **Payment APIs**: Stripe, PayPal, Square, Braintree
- **Social Media**: Facebook, Twitter, LinkedIn, GitHub
- **DevOps Tools**: Slack, Heroku, SendGrid, Twilio
- **Security**: Private keys, SSH credentials, OAuth tokens

### 🎯 **Advanced Scanning Capabilities**
- **File-level scanning** - Visits individual files to find hidden secrets
- **Batch processing** - Efficient handling of large repositories
- **Rate limiting** - Respects GitHub's API limits with exponential backoff
- **Deduplication** - Prevents duplicate entries from same files
- **Real-time results** - Saves findings as they're discovered

### ⚙️ **Flexible Configuration**
- **Custom regex patterns** - Add your own detection rules
- **Browser control** - Headless or visible mode
- **Verbose output** - Detailed or minimal logging
- **Custom output** - JSON format with structured data
- **Configurable limits** - Adjust search depth and batch sizes

### 📊 **Rich Output Format**
```json
{
  "OpenAI API Key": [
    {
      "matched_string": "sk-1234567890abcdef...",
      "file_url": "https://github.com/user/repo/blob/main/config.json",
      "description": "OpenAI API keys starting with sk-"
    }
  ],
  "AWS Secret Access Key": [
    {
      "matched_string": "AKIA...",
      "file_url": "https://github.com/user/repo/blob/main/.env",
      "description": "AWS Secret Access Key with variable names"
    }
  ]
}
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Git
- GitHub account (for authentication)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/gitski.git
cd gitski
```

2. **Install dependencies**
```bash
pip install playwright
playwright install
```

3. **Configure credentials**
```bash
# Create config file with your GitHub credentials
cp config_github.json.example config_github.json
# Edit config_github.json with your GitHub username and password
```

4. **Run GitSki**
```bash
python gitski.py
```

---

## 📖 Usage

### Basic Commands

```bash
# Basic scan (visible browser, minimal output)
python gitski.py

# Headless mode (no GUI, faster)
python gitski.py --headless

# Verbose output (detailed logging)
python gitski.py --verbose

# Custom output file
python gitski.py --output my_results.json

# Custom number of pages per query
python gitski.py --max-pages 10

# Combined options
python gitski.py --headless --verbose --output results.json
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--headless` | Run browser in headless mode | `False` |
| `--verbose`, `-v` | Enable detailed output | `False` |
| `--output`, `-o` | Custom output filename | `keys.json` |
| `--max-pages` | Max pages per search query | `5` |

### Configuration Files

#### `config_github.json`
```json
{
  "username": "your_github_username",
  "password": "your_github_password"
}
```

#### `regex_patterns.json` (Optional)
```json
[
  {
    "name": "Custom Pattern",
    "pattern": "your_regex_pattern",
    "description": "Description of what this pattern detects"
  }
]
```

---

## 🔧 Configuration

### Custom Regex Patterns

GitSki comes with 40+ pre-configured patterns, but you can add your own:

1. **Edit `regex_patterns.json`**
2. **Add your pattern**:
```json
{
  "name": "My Custom Secret",
  "pattern": "my_secret_[a-zA-Z0-9]{32}",
  "description": "Detects my custom secret format"
}
```

### Search Queries

GitSki automatically generates search queries based on:
- **File extensions**: `.json`, `.env`, `.config`, `.yml`, etc.
- **Keywords**: `api_key`, `secret`, `token`, `password`, etc.
- **Pattern matching**: Specific regex patterns for each secret type

---

## 📊 Output Format

### JSON Structure
```json
{
  "Pattern Name": [
    {
      "matched_string": "actual_secret_value",
      "file_url": "https://github.com/user/repo/blob/main/file.ext",
      "description": "Pattern description"
    }
  ]
}
```

### Sample Output
```json
{
  "OpenAI API Key": [
    {
      "matched_string": "sk-1234567890abcdef1234567890abcdef1234567890abcdef",
      "file_url": "https://github.com/example/repo/blob/main/config.json",
      "description": "OpenAI API keys starting with sk-"
    }
  ],
  "AWS Secret Access Key": [
    {
      "matched_string": "AKIAIOSFODNN7EXAMPLE",
      "file_url": "https://github.com/example/repo/blob/main/.env",
      "description": "AWS Secret Access Key with variable names"
    }
  ]
}
```

---

## 🛡️ Security & Ethics

### ⚠️ **Important Disclaimer**

GitSki is designed for **ethical security research** and **responsible disclosure**. Please:

- **Only scan repositories you own or have permission to scan**
- **Respect GitHub's Terms of Service**
- **Use responsibly and ethically**
- **Report findings to repository owners privately**
- **Do not use for malicious purposes**

### 🔒 **Best Practices**

1. **Get permission** before scanning repositories
2. **Use rate limiting** to avoid overwhelming GitHub's servers
3. **Report vulnerabilities** through proper channels
4. **Respect privacy** and confidentiality
5. **Follow responsible disclosure** guidelines

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 **Report Issues**
- Use the [GitHub Issues](https://github.com/yourusername/gitski/issues) page
- Provide detailed bug reports with steps to reproduce
- Include error messages and system information

### 💡 **Feature Requests**
- Suggest new regex patterns
- Propose UI/UX improvements
- Request new detection capabilities

### 🔧 **Code Contributions**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📝 **Adding New Patterns**
1. Add your regex pattern to `regex_patterns.json`
2. Test thoroughly with sample data
3. Update documentation if needed
4. Submit a pull request

---


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **GitHub** for providing the platform
- **Playwright** for browser automation
- **Open source community** for regex patterns
- **Security researchers** for responsible disclosure practices

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/gitski&type=Date)](https://star-history.com/#yourusername/gitski&Date)

---

<div align="center">

**Made by Abhijeet with ❤️ for the security community**

[![Twitter](https://img.shields.io/badge/Twitter-Follow-blue?style=social&logo=twitter)](https://x.com/neverjuniorr)

</div> 
