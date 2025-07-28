import re
import time
import os
import argparse
from playwright.sync_api import sync_playwright
import requests
import json

CONFIG_FILE = 'config_github.json'
REGEX_CONFIG_FILE = 'regex_patterns.json'
COOKIE_FILE = 'cookie.txt'
KEYS_FILE = 'keys.json'
MAX_PAGES = 5 

BANNER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██████╗ ██╗████████╗███████╗██╗  ██╗██╗    ╔═══════════════════════════╗    ║
║ ██╔════╝ ██║╚══██╔══╝██╔════╝██║ ██╔╝██║    ║   🔍 SECRET HUNTER 🔍    ║    ║
║ ██║  ███╗██║   ██║   ███████╗█████╔╝ ██║    ║   GitHub Secret Scanner   ║    ║
║ ██║   ██║██║   ██║   ╚════██║██╔═██╗ ██║    ║                           ║    ║
║ ╚██████╔╝██║   ██║   ███████║██║  ██╗██║    ║      - by Abhijeet        ║    ║
║  ╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝    ╚═══════════════════════════╝    ║
║                                                                              ║
║  🚀 Find Exposed API Keys • 🔐 Detect Secrets • 🎯 Target Specific Repos   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

def print_banner():
    print(BANNER)
    print("🎯 Initializing GitSki Secret Scanner...")
    print("⚡ Loading advanced detection patterns...")
    print("🔍 Preparing GitHub search engine...")
    print("=" * 70)
    print("🚀 Ready to hunt for secrets! Let's go! 🚀")
    print("=" * 70)

def print_status(message, status_type="INFO"):
    colors = {
        "INFO": "🔵",
        "SUCCESS": "✅", 
        "WARNING": "⚠️",
        "ERROR": "❌",
        "KEY": "🔑",
        "FOUND": "🎯",
        "SCANNING": "🔍",
        "WAITING": "⏳",
        "LOGIN": "🔐",
        "BROWSER": "🌐"
    }
    icon = colors.get(status_type, "ℹ️")
    print(f"{icon} {message}")

def print_progress(current, total, prefix="Progress"):
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    percentage = current / total * 100
    print(f"\r{prefix}: |{bar}| {percentage:.1f}% ({current}/{total})", end='', flush=True)
    if current == total:
        print()  # Final newline when complete

def print_page_file_progress(page_num, max_pages, file_num, total_files, query_num, total_queries):
    page_percentage = (page_num / max_pages) * 100
    file_percentage = (file_num / total_files) * 100 if total_files > 0 else 0
    
    # Clear the line and print progress using ANSI escape codes
    print(f"\r\033[K", end='', flush=True)  # Clear line from cursor to end
    print(f"Query {query_num}/{total_queries} | Page {page_num}/{max_pages} ({page_percentage:.1f}%) | File {file_num}/{total_files} ({file_percentage:.1f}%)", end='', flush=True)

EXTENSIONS = [
    'json', 'xml', 'properties', 'sql', 'txt', 'log', 'tmp', 'backup', 'bak', 'enc',
    'yml', 'yaml', 'toml', 'ini', 'config', 'conf', 'cfg', 'env', 'envrc', 'prod',
    'secret', 'private', 'key'
]
KEYWORDS = [
    'access_key', 'secret_key', 'access_token', 'api_key', 'apikey', 'api_secret',
    'apiSecret', 'app_secret', 'application_key', 'app_key', 'appkey', 'auth_token', 'authsecret'
]

DEFAULT_REGEX_PATTERNS = [
    {
        "name": "OpenAI API Key",
        "pattern": r'sk-[a-zA-Z0-9]{48}',
        "description": "OpenAI API keys starting with sk-"
    }
]

def load_regex_patterns():
    if os.path.exists(REGEX_CONFIG_FILE):
        try:
            with open(REGEX_CONFIG_FILE, 'r') as f:
                patterns = json.load(f)
            print_status(f"Loaded {len(patterns)} regex patterns from {REGEX_CONFIG_FILE}", "FOUND")
            return patterns
        except Exception as e:
            print_status(f"Error loading regex patterns: {e}. Using defaults.", "WARNING")
            return DEFAULT_REGEX_PATTERNS
    else:
        print_status(f"Regex config file {REGEX_CONFIG_FILE} not found. Using defaults.", "INFO")
        return DEFAULT_REGEX_PATTERNS

def compile_regex_patterns(patterns):
    compiled_patterns = []
    for pattern_data in patterns:
        try:
            compiled_pattern = re.compile(pattern_data["pattern"])
            compiled_patterns.append({
                "name": pattern_data["name"],
                "pattern": compiled_pattern,
                "description": pattern_data.get("description", "")
            })
            print_status(f"Compiled pattern: {pattern_data['name']}", "SUCCESS")
        except Exception as e:
            print_status(f"Error compiling pattern '{pattern_data['name']}': {e}", "ERROR")
    return compiled_patterns

def generate_queries(args, compiled_patterns):
    queries = []
    
    base_filters = []
    
    if args.repo:
        base_filters.append(f"repo:{args.repo}")
    if args.org:
        base_filters.append(f"org:{args.org}")
    if args.user:
        base_filters.append(f"user:{args.user}")
    if args.string:
        base_filters.append(f'"{args.string}"')
    
    base_filter_string = " ".join(base_filters) if base_filters else ""
    
    for ext in EXTENSIONS:
        for kw in KEYWORDS:
            for pattern_info in compiled_patterns:
                pattern_name = pattern_info["name"]
                pattern_regex = pattern_info["pattern"].pattern
                
                if base_filter_string:
                    q = f'{base_filter_string} (path:*.{ext}) AND ({kw}) AND (/{pattern_regex}/)'
                else:
                    q = f'(path:*.{ext}) AND ({kw}) AND (/{pattern_regex}/)'
                queries.append(q)
    
    return queries

def load_cookies(context):
    if not os.path.exists(COOKIE_FILE):
        print_status(f"Cookie file '{COOKIE_FILE}' not found", "INFO")
        return False
    
    try:
        with open(COOKIE_FILE, 'r') as f:
            cookie_str = f.read().strip()
        
        if not cookie_str:
            print_status(f"Cookie file '{COOKIE_FILE}' is empty", "WARNING")
            return False
        
        cookies = []
        for pair in cookie_str.split(';'):
            if '=' in pair:
                name, value = pair.strip().split('=', 1)
                cookies.append({
                    'name': name,
                    'value': value,
                    'domain': '.github.com',
                    'path': '/',
                    'httpOnly': False,
                    'secure': True,
                    'sameSite': 'Lax',
                })
        
        if not cookies:
            print_status(f"No valid cookies found in '{COOKIE_FILE}'", "WARNING")
            return False
        
        context.add_cookies(cookies)
        print_status(f"Loaded {len(cookies)} cookies from '{COOKIE_FILE}'", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Could not load cookies: {e}", "ERROR")
        return False

def check_and_handle_unicorn(page, verbose=False, context="page"):
    """Check for Unicorn error page and handle it"""
    try:
        page_title = page.title()
        if "Unicorn" in page_title:
            if verbose:
                print_status(f"Detected Unicorn error page during {context}, refreshing...", "WARNING")
            page.reload()
            time.sleep(5)  # Wait for page to reload
            return True
    except Exception:
        pass
    return False

def save_cookies(context):
    cookies = context.cookies()
    cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies if c['domain'].endswith('github.com')])
    with open(COOKIE_FILE, 'w') as f:
        f.write(cookie_str)
    # Removed print statement to avoid interfering with progress display

def get_github_credentials():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file '{CONFIG_FILE}' not found.")
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    username = config.get('username')
    password = config.get('password')
    if not username or not password:
        raise ValueError("Username or password missing in config file.")
    return username, password

def extract_file_urls_from_page(page):
    file_urls = []
    try:
        if check_and_handle_unicorn(page, verbose=False, context="URL extraction"):
            return []
        
        file_links = page.query_selector_all('a[data-testid="link-to-search-result"]')
        for link in file_links:
            href = link.get_attribute('href')
            if href and '/blob/' in href:
                if href.startswith('/'):
                    href = 'https://github.com' + href
                file_urls.append(href)
    except Exception as e:
        # Only print in verbose mode to avoid interfering with progress display
        pass
    return file_urls

def visit_file_and_extract_keys(page, file_url, all_keys, compiled_patterns, verbose=False, max_retries=3):
    for attempt in range(max_retries):
        try:
            if verbose:
                print_status(f"Visiting file: {file_url}", "SCANNING")
            response = page.goto(file_url, timeout=30000)
            
            # Check for Unicorn error page
            if check_and_handle_unicorn(page, verbose=verbose, context="file visit"):
                continue
            
            if response.status == 429:
                wait_time = 30 if attempt == 0 else 60 if attempt == 1 else 180
                if verbose:
                    print_status(f"Rate limited (429), waiting {wait_time} seconds...", "WAITING")
                time.sleep(wait_time)
                continue
            
            if response.status != 200:
                if verbose:
                    print_status(f"Unexpected status code: {response.status}", "ERROR")
                if attempt < max_retries - 1:
                    wait_time = 30 if attempt == 0 else 60
                    if verbose:
                        print_status(f"Retrying in {wait_time} seconds...", "WAITING")
                    time.sleep(wait_time)
                    continue
                else:
                    if verbose:
                        print_status(f"Failed after {max_retries} attempts", "ERROR")
                    with open('skipped.txt', 'a') as f:
                        f.write(f"FILE: {file_url}\n")
                    print_status(f"Added file to skipped.txt", "WARNING")
                    return False
            
            file_content = page.content()
            keys = extract_keys_from_code(file_content, compiled_patterns, file_url, verbose)
            
            new_keys_count = 0
            new_keys_summary = []
            
            for pattern_name, key_list in keys.items():
                if pattern_name not in all_keys:
                    all_keys[pattern_name] = []
                
                pattern_new_count = 0
                for key_data in key_list:
                    is_duplicate = False
                    for existing_key in all_keys[pattern_name]:
                        if (existing_key["matched_string"] == key_data["matched_string"] and 
                            existing_key["file_url"] == key_data["file_url"]):
                            is_duplicate = True
                            break
                    
                    if not is_duplicate:
                        all_keys[pattern_name].append(key_data)
                        new_keys_count += 1
                        pattern_new_count += 1
                
                if pattern_new_count > 0:
                    new_keys_summary.append(f"{pattern_new_count} {pattern_name}")
            
            if new_keys_count > 0:
                summary_text = ", ".join(new_keys_summary)
                if verbose:
                    print_status(f"Found {new_keys_count} new keys in file: {summary_text}", "FOUND")
                save_results_to_json(all_keys, KEYS_FILE)
            else:
                if verbose:
                    print_status(f"No new keys found in file", "WARNING")
            
            return True
            
        except Exception as e:
            if verbose:
                print_status(f"Error on attempt {attempt + 1}: {e}", "ERROR")
            if attempt < max_retries - 1:
                wait_time = 30 if attempt == 0 else 60
                if verbose:
                    print_status(f"Retrying in {wait_time} seconds...", "WAITING")
                time.sleep(wait_time)
    
    if verbose:
        print_status(f"Failed to visit file after {max_retries} attempts", "ERROR")
    with open('skipped.txt', 'a') as f:
        f.write(f"FILE: {file_url}\n")
    if verbose:
        print_status(f"Added file to skipped.txt", "WARNING")
    return False

def process_files_in_batches(page, file_urls, all_keys, compiled_patterns, verbose=False, batch_size=20, query_num=1, total_queries=1, page_num=1, max_pages=5):
    total_files = len(file_urls)
    if verbose:
        print_status(f"Found {total_files} files to process", "FOUND")
    
    for i in range(0, total_files, batch_size):
        batch = file_urls[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_files + batch_size - 1) // batch_size
        
        if verbose:
            print_status(f"Processing batch {batch_num}/{total_batches} ({len(batch)} files)", "SCANNING")
        
        for j, file_url in enumerate(batch):
            if verbose:
                print_status(f"File {i + j + 1}/{total_files}", "SCANNING")
            else:
                # Update file progress on the same line without creating new line
                file_percentage = ((i + j + 1) / total_files) * 100
                print(f"\r\033[K", end='', flush=True)  # Clear line from cursor to end
                print(f"Query {query_num}/{total_queries} | Page {page_num}/{max_pages} ({(page_num/max_pages)*100:.1f}%) | File {i + j + 1}/{total_files} ({file_percentage:.1f}%)", end='', flush=True)
            visit_file_and_extract_keys(page, file_url, all_keys, compiled_patterns, verbose)
            
            if j < len(batch) - 1:
                delay = 2 + (j % 2)
                time.sleep(delay)
        
        if i + batch_size < total_files:
            if verbose:
                print_status(f"Batch {batch_num} complete. Taking a 10-second break...", "WAITING")
            time.sleep(10)
    
    # No newline after file processing to keep progress on same line

def extract_keys_from_code(code, compiled_patterns, file_url="", verbose=False):
    all_keys = {}
    for pattern_info in compiled_patterns:
        keys = pattern_info["pattern"].findall(code)
        if keys:
            pattern_name = pattern_info["name"]
            if pattern_name not in all_keys:
                all_keys[pattern_name] = []
            
            for key in keys:
                key_data = {
                    "matched_string": key,
                    "file_url": file_url,
                    "description": pattern_info.get("description", "")
                }
                all_keys[pattern_name].append(key_data)
                
            if verbose:
                print_status(f"Found {len(keys)} {pattern_name}: {keys[:3]}{'...' if len(keys) > 3 else ''}", "KEY")
    return all_keys

def extract_keys_from_json(json_str, compiled_patterns, file_url="", verbose=False):
    keys = {}
    try:
        data = json.loads(json_str)
        keys.update(extract_keys_from_object(data, compiled_patterns, file_url, verbose))
    except json.JSONDecodeError:
        for pattern_info in compiled_patterns:
            found_keys = pattern_info["pattern"].findall(json_str)
            if found_keys:
                pattern_name = pattern_info["name"]
                if pattern_name not in keys:
                    keys[pattern_name] = []
                
                for key in found_keys:
                    key_data = {
                        "matched_string": key,
                        "file_url": file_url,
                        "description": pattern_info.get("description", "")
                    }
                    keys[pattern_name].append(key_data)
                
                if verbose:
                    print_status(f"Found {len(found_keys)} {pattern_name} in JSON string: {found_keys[:3]}{'...' if len(found_keys) > 3 else ''}", "KEY")
    return keys

def extract_keys_from_object(obj, compiled_patterns, file_url="", verbose=False):
    keys = {}
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(key, str):
                for pattern_info in compiled_patterns:
                    found_keys = pattern_info["pattern"].findall(key)
                    if found_keys:
                        pattern_name = pattern_info["name"]
                        if pattern_name not in keys:
                            keys[pattern_name] = []
                        
                        for found_key in found_keys:
                            key_data = {
                                "matched_string": found_key,
                                "file_url": file_url,
                                "description": pattern_info.get("description", "")
                            }
                            keys[pattern_name].append(key_data)
                        
                        if verbose:
                            print_status(f"Found {len(found_keys)} {pattern_name} in key: {found_keys[:3]}{'...' if len(found_keys) > 3 else ''}", "KEY")
            nested_keys = extract_keys_from_object(value, compiled_patterns, file_url, verbose)
            for pattern_name, key_list in nested_keys.items():
                if pattern_name not in keys:
                    keys[pattern_name] = []
                keys[pattern_name].extend(key_list)
    elif isinstance(obj, list):
        for item in obj:
            nested_keys = extract_keys_from_object(item, compiled_patterns, file_url, verbose)
            for pattern_name, key_list in nested_keys.items():
                if pattern_name not in keys:
                    keys[pattern_name] = []
                keys[pattern_name].extend(key_list)
    elif isinstance(obj, str):
        for pattern_info in compiled_patterns:
            found_keys = pattern_info["pattern"].findall(obj)
            if found_keys:
                pattern_name = pattern_info["name"]
                if pattern_name not in keys:
                    keys[pattern_name] = []
                
                for found_key in found_keys:
                    key_data = {
                        "matched_string": found_key,
                        "file_url": file_url,
                        "description": pattern_info.get("description", "")
                    }
                    keys[pattern_name].append(key_data)
                
                if verbose:
                    print_status(f"Found {len(found_keys)} {pattern_name} in string: {found_keys[:3]}{'...' if len(found_keys) > 3 else ''}", "KEY")
    
    return keys

def save_results_to_json(all_keys, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(all_keys, f, indent=2)
    except Exception as e:
        print_status(f"Error saving results: {e}", "ERROR")

def main():
    parser = argparse.ArgumentParser(description='GitSki - GitHub Secret Scanner')
    parser.add_argument('--headless', action='store_true', 
                       help='Run browser in headless mode (no GUI)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--max-pages', type=int, default=5,
                       help='Maximum number of pages to search per query (default: 5)')
    parser.add_argument('--output', '-o', type=str, default='keys.json',
                       help='Output file name for results (default: keys.json)')
    parser.add_argument('--repo', type=str, default=None,
                       help='Search only in specific repository (format: owner/repo)')
    parser.add_argument('--org', type=str, default=None,
                       help='Search only in specific organization')
    parser.add_argument('--user', type=str, default=None,
                       help='Search only in specific user\'s repositories')
    parser.add_argument('--string', type=str, default=None,
                       help='Search for specific string (domain, company, etc.)')
    args = parser.parse_args()
    
    global MAX_PAGES, KEYS_FILE
    MAX_PAGES = args.max_pages
    KEYS_FILE = args.output
    
    print_banner()
    print_status(f"Writing results to: {os.path.abspath(KEYS_FILE)}", "INFO")
    print_status(f"Browser mode: {'Headless' if args.headless else 'Visible'}", "BROWSER")
    print_status(f"Verbose mode: {'Enabled' if args.verbose else 'Disabled'}", "INFO")
    print_status(f"Max pages per query: {MAX_PAGES}", "INFO")
    
    if args.repo:
        print_status(f"Repository target: {args.repo}", "FOUND")
    if args.org:
        print_status(f"Organization target: {args.org}", "FOUND")
    if args.user:
        print_status(f"User target: {args.user}", "FOUND")
    if args.string:
        print_status(f"String target: {args.string}", "SCANNING")
    
    patterns = load_regex_patterns()
    compiled_patterns = compile_regex_patterns(patterns)
    
    all_keys = {}
    queries = generate_queries(args, compiled_patterns)
    total_queries = len(queries)
    print_status(f"Generated {total_queries} search queries", "INFO")
    
    with sync_playwright() as p:
        print_status("Launching browser...", "BROWSER")
        browser = p.chromium.launch(headless=args.headless)
        context = browser.new_context()
        cookies_loaded = load_cookies(context)
        page = context.new_page()
        
        if not cookies_loaded:
            print_status("No valid cookies found. Attempting automated GitHub login...", "LOGIN")
            try:
                username, password = get_github_credentials()
                print_status("Credentials loaded successfully", "SUCCESS")
                
                page.goto('https://github.com/login', timeout=30000)
                
                # Check for Unicorn error page during login
                if check_and_handle_unicorn(page, verbose=True, context="login"):
                    page.goto('https://github.com/login', timeout=30000)
                
                print_status("Navigated to GitHub login page", "LOGIN")
                
                page.fill('input[name="login"]', username)
                page.fill('input[name="password"]', password)
                page.click('input[type="submit"]')
                print_status("Login form submitted", "LOGIN")
                
                try:
                    page.wait_for_url('https://github.com/', timeout=15000)
                    print_status("Login successful!", "SUCCESS")
                    save_cookies(context)
                except Exception as e:
                    print_status(f"Login timeout or 2FA required: {e}", "WARNING")
                    print_status("Please complete login manually in the browser window", "WARNING")
                    input("Press Enter after completing login...")
                    save_cookies(context)
            except Exception as e:
                print_status(f"Login failed: {e}", "ERROR")
                print_status("Please check your config_github.json file", "ERROR")
                return
        else:
            print_status("Using saved session cookies", "SUCCESS")
        
        print_status("Starting secret hunt...", "SCANNING")
        for i, query in enumerate(queries, 1):
            if args.verbose:
                print_status(f"Query {i}/{total_queries}: {query}", "SCANNING")
            
            for page_num in range(1, MAX_PAGES + 1):
                url = f"https://github.com/search?q={requests.utils.quote(query)}&type=code&sort=updated&order=desc&p={page_num}"
                if args.verbose:
                    print_status(f"Fetching page {page_num}: {url}", "SCANNING")
                
                search_success = False
                no_results_found = False
                for search_attempt in range(3):
                    try:
                        response = page.goto(url, timeout=30000)
                        
                        # Check for Unicorn error page
                        if check_and_handle_unicorn(page, verbose=args.verbose, context="search"):
                            continue
                        
                        if response.status == 429:
                            wait_time = 30 if search_attempt == 0 else 60 if search_attempt == 1 else 180
                            print_status(f"Search rate limited (429), waiting {wait_time} seconds...", "WAITING")
                            time.sleep(wait_time)
                            continue
                        
                        if response.status != 200:
                            print_status(f"Unexpected status code: {response.status}", "ERROR")
                            if search_attempt < 2:
                                wait_time = 30 if search_attempt == 0 else 60
                                print_status(f"Retrying in {wait_time} seconds...", "WAITING")
                                time.sleep(wait_time)
                                continue
                            else:
                                print_status(f"Failed after 3 attempts with status {response.status}, skipping page {page_num}", "ERROR")
                                break
                        
                        file_urls = extract_file_urls_from_page(page)
                        if file_urls:
                            if args.verbose:
                                print_status(f"Extracted {len(file_urls)} file URLs from search results", "FOUND")
                            else:
                                if page_num == 1:  # Only show progress line once per query
                                    print_page_file_progress(page_num, MAX_PAGES, 0, len(file_urls), i, total_queries)
                            process_files_in_batches(page, file_urls, all_keys, compiled_patterns, args.verbose, 20, i, total_queries, page_num, MAX_PAGES)
                            search_success = True
                            break
                        else:
                            if args.verbose:
                                print_status(f"No file URLs found on page {page_num}", "WARNING")
                            no_results_found = True
                            break

                    except Exception as e:
                        print_status(f"Error on attempt {search_attempt + 1}: {e}", "ERROR")
                        if search_attempt < 2:
                            wait_time = 30 if search_attempt == 0 else 60
                            print_status(f"Retrying in {wait_time} seconds...", "WAITING")
                            time.sleep(wait_time)
                        else:
                            print_status(f"Failed after 3 attempts due to error: {e}", "ERROR")
                            break
                
                if not search_success and not no_results_found:
                    print_status(f"Search page failed after all retries", "ERROR")
                
                if no_results_found:
                    break
            time.sleep(2)
    
    total_keys = sum(len(key_list) for key_list in all_keys.values())
    print_status(f"Scan complete! Found {total_keys} total keys across {len(all_keys)} pattern types.", "SUCCESS")
    
    if all_keys:
        print_status("Summary by pattern type:", "INFO")
        for pattern_name, key_list in all_keys.items():
            print_status(f"{pattern_name}: {len(key_list)} keys", "KEY")
    
    save_results_to_json(all_keys, KEYS_FILE)
    print_status(f"Results saved to: {os.path.abspath(KEYS_FILE)}", "SUCCESS")
    print_status("Secret hunting session completed!", "SUCCESS")
    browser.close()

if __name__ == '__main__':
    main()
