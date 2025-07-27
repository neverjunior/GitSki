# 🔍 GitSki - Secret Hunter

**Getting Rate Limited.. Sorry! what's that?**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██████╗ ██╗████████╗███████╗██╗  ██╗██╗    ╔═══════════════════════════╗    ║
║ ██╔════╝ ██║╚══██╔══╝██╔════╝██║ ██╔╝██║    ║   🔍 SECRET HUNTER 🔍    ║    ║
║ ██║  ███╗██║   ██║   ███████╗█████╔╝ ██║    ║   GitHub Secret Scanner   ║    ║
║ ██║   ██║██║   ██║   ╚════██║██╔═██╗ ██║    ║                           ║    ║
║ ╚██████╔╝██║   ██║   ███████║██║  ██╗██║    ║      - by Abhijeet        ║    ║
║  ╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝    ╚═══════════════════════════╝    ║
║                                                                              ║
║  🚀 Find Exposed API Keys • 🔐 Detect Secrets • 🎯 Target Specific Repos    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)](https://playwright.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/neverjunior/gitski?style=social)](https://github.com/neverjunior/gitski)

*A powerful secret hunting tool to scan GitHub repositories for exposed API keys, secrets, and credentials with advanced targeting capabilities*

---

## ✨ Features

### 🎯 **Advanced Targeting**
- **Repository-specific scanning** - Target specific repos, organizations, or users
- **String-based filtering** - Search for specific domains, companies, or keywords
- **Language filtering** - Focus on specific programming languages
- **Metadata filtering** - Filter by stars, forks, size, and dates

### 🔍 **Intelligent Detection**
- **40+ secret patterns** - Comprehensive regex patterns for various API keys
- **Real-time extraction** - Immediate key discovery and saving
- **Deduplication** - Smart duplicate detection and removal
- **File link following** - Deep scanning of individual files

### 🚀 **Performance & Reliability**
- **Rate limit handling** - Intelligent backoff and retry mechanisms
- **Batch processing** - Efficient file processing in batches
- **Headless mode** - Fast scanning without GUI
- **Cookie persistence** - Automated login with session management

### 🎨 **User Experience**
- **Verbose logging** - Detailed output for debugging
- **JSON output** - Structured results with metadata

### 🔧 **Flexibility**
- **Custom regex patterns** - Load patterns from JSON configuration
- **Multiple output formats** - Customizable output filenames
- **Configurable limits** - Adjustable page limits and batch sizes
- **Cross-platform** - Works on Windows, macOS, and Linux

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

## 🎬 Demo

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██████╗ ██╗████████╗███████╗██╗  ██╗██╗    ╔═══════════════════════════╗   ║
║ ██╔════╝ ██║╚══██╔══╝██╔════╝██║ ██╔╝██║    ║     🔍 SECRET HUNTER 🔍    ║   ║
║ ██║  ███╗██║   ██║   ███████╗█████╔╝ ██║    ║   GitHub Secret Scanner   ║   ║
║ ██║   ██║██║   ██║   ╚════██║██╔═██╗ ██║    ║                           ║   ║
║ ╚██████╔╝██║   ██║   ███████║██║  ██╗██║    ║      - by Abhijeet -       ║   ║
║  ╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝    ╚═══════════════════════════╝   ║
║                                                                              ║
║  🚀 Find Exposed API Keys • 🔐 Detect Secrets • 🎯 Target Specific Repos   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 Initializing GitSki Secret Scanner...
⚡ Loading advanced detection patterns...
🔍 Preparing GitHub search engine...
======================================================================
🚀 Ready to hunt for secrets! Let's go! 🚀
======================================================================
🎯 Loaded 40 regex patterns from regex_patterns.json
✅ Compiled pattern: OpenAI API Key
✅ Compiled pattern: AWS Access Key ID
✅ Compiled pattern: AWS Secret Access Key
...
🎯 Generated 520 search queries
🌐 Launching browser...
🔐 Attempting automated GitHub login...
✅ Login successful!
🚀 Starting secret hunt...
🔍 Query 1/520: (path:*.json) AND (api_key) AND (/sk-[a-zA-Z0-9]{48}/)
📄 Fetching page 1: https://github.com/search?q=...
🎯 Extracted 15 file URLs from search results
📦 Processing batch 1/1 (15 files)
🔍 File 1/15: https://github.com/...
🎯 Found 3 new keys in file
💾 Results saved to: keys.json
...
🎉 Scan complete! Found 127 total keys across 8 pattern types.
📊 Summary by pattern type:
  🔑 OpenAI API Key: 45 keys
  🔑 AWS Access Key ID: 23 keys
  🔑 GitHub Personal Access Token: 18 keys
  ...
💾 Results saved to: keys.json
🎯 Secret hunting session completed! 🎯
```

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.7 or higher
- Git
- GitHub account (for authentication)

### ⚡ Installation

1. **Clone the repository**
```bash
git clone https://github.com/neverjunior/gitski.git
cd gitski
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers**
```bash
playwright install chromium
```

4. **Configure GitHub credentials**
```bash
cp config_github.json.example config_github.json
# Edit config_github.json with your GitHub credentials
```

### 🎯 Basic Usage

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

### 🎯 Advanced Targeting

```bash
# Search in specific repository
python gitski.py --repo "microsoft/vscode"

# Search in specific organization
python gitski.py --org "microsoft"

# Search in specific user's repositories
python gitski.py --user "neverjunior"

# Search for specific string/domain
python gitski.py --string "example.com"

# Search in specific programming language
python gitski.py --language "python"

# Filter by repository size
python gitski.py --size ">1000"

# Filter by stars
python gitski.py --stars ">100"

# Filter by forks
python gitski.py --forks ">10"

# Filter by creation date
python gitski.py --created ">2023-01-01"

# Filter by last push date
python gitski.py --pushed ">2024-01-01"

# Combined filters
python gitski.py --repo "microsoft/vscode" --string "api_key" --verbose
python gitski.py --org "google" --language "javascript" --stars ">1000"
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

### Advanced Search Filters

```bash
# Search in specific repository
python gitski.py --repo "microsoft/vscode"

# Search in specific organization
python gitski.py --org "microsoft"

# Search in specific user's repositories
python gitski.py --user "neverjunior"

# Search for specific string/domain
python gitski.py --string "example.com"

# Search in specific programming language
python gitski.py --language "python"

# Filter by repository size
python gitski.py --size ">1000"

# Filter by stars
python gitski.py --stars ">100"

# Filter by forks
python gitski.py --forks ">10"

# Filter by creation date
python gitski.py --created ">2023-01-01"

# Filter by last push date
python gitski.py --pushed ">2024-01-01"

# Combined filters
python gitski.py --repo "microsoft/vscode" --string "api_key" --verbose
python gitski.py --org "google" --language "javascript" --stars ">1000"
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--headless` | Run browser in headless mode | `False` |
| `--verbose`, `-v` | Enable detailed output | `False` |
| `--output`, `-o` | Custom output filename | `keys.json` |
| `--max-pages` | Max pages per search query | `5` |
| `--repo` | Search in specific repository (owner/repo) | `None` |
| `--org` | Search in specific organization | `None` |
| `--user` | Search in specific user's repositories | `None` |
| `--string` | Search for specific string/domain | `None` |
| `--language` | Filter by programming language | `None` |
| `--size` | Filter by repository size (e.g., >1000) | `None` |
| `--stars` | Filter by stars (e.g., >100) | `None` |
| `--forks` | Filter by forks (e.g., >10) | `None` |
| `--created` | Filter by creation date (e.g., >2023-01-01) | `None` |
| `--pushed` | Filter by last push date (e.g., >2024-01-01) | `None` |

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

### GitHub Search Filters

GitSki supports all GitHub search filters for precise targeting:

#### **Repository & Organization Filters**
- `--repo "owner/repo"` - Search in specific repository
- `--org "organization"` - Search in organization repositories
- `--user "username"` - Search in user's repositories

#### **Content Filters**
- `--string "text"` - Search for specific text/domain/company
- `--language "python"` - Filter by programming language

#### **Repository Metadata Filters**
- `--size ">1000"` - Filter by repository size
- `--stars ">100"` - Filter by star count
- `--forks ">10"` - Filter by fork count
- `--created ">2023-01-01"` - Filter by creation date
- `--pushed ">2024-01-01"` - Filter by last push date

#### **Usage Examples**
```bash
# Target specific company repositories
python gitski.py --org "microsoft" --string "api_key"

# Search in popular repositories
python gitski.py --stars ">1000" --language "javascript"

# Focus on recent activity
python gitski.py --pushed ">2024-01-01" --string "password"

# Target specific domain
python gitski.py --string "example.com" --verbose
```

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

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### 🐛 **Report Issues**
- Use the [GitHub Issues](https://github.com/neverjunior/gitski/issues) page
- Provide detailed bug reports with steps to reproduce
- Include error messages and system information

### 💡 **Feature Requests**
- Suggest new features via GitHub Issues
- Discuss improvements in Discussions
- Submit pull requests for enhancements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=neverjunior/gitski&type=Date)](https://star-history.com/#neverjunior/gitski&Date)

---

<div align="center">

### 🔍 **GitSki - Secret Hunter**

**Made with ❤️ by [Abhijeet](https://x.com/neverjuniorr)**

[![Twitter](https://img.shields.io/badge/Twitter-@neverjuniorr-blue?style=flat&logo=twitter)](https://x.com/neverjuniorr)
[![GitHub](https://img.shields.io/badge/GitHub-neverjunior-black?style=flat&logo=github)](https://github.com/neverjunior)

*Happy secret hunting! 🎯*

</div> 
