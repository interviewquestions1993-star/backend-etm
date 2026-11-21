import urllib.request
import json
import urllib.parse
import re

def _sanitize_json_text(s: str) -> str:
    # First, strip trailing commas from arrays and objects
    s = re.sub(r',\s*}', '}', s)
    s = re.sub(r',\s*]', ']', s)
    
    out_chars = []
    in_str = False
    esc = False
    for ch in s:
        if ch == '"' and not esc:
            in_str = not in_str
            out_chars.append(ch)
            esc = False
            continue
        if ch == '\\' and not esc:
            esc = True
            out_chars.append(ch)
            continue
        if esc:
            out_chars.append(ch)
            esc = False
            continue
        if in_str and ch == '\n':
            out_chars.append('\\n')
            continue
        if in_str and ch == '\r':
            out_chars.append('\\r')
            continue
        if in_str and ch == '\t':
            out_chars.append('\\t')
            continue
        out_chars.append(ch)
    return ''.join(out_chars)

url = "https://raw.githubusercontent.com/learnenglishandgrow93-web/cbse-mcq-bank/refs/heads/main/Advanced%20Features%20of%20Excel%202019-MCQ-v1"
print(f"Fetching {url}...")
try:
    with urllib.request.urlopen(url, timeout=15) as response:
        content = response.read().decode("utf-8")
        print(f"Content length: {len(content)}")
        
        first_bracket = content.find('[')
        last_bracket = content.rfind(']')
        if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
            content = content[first_bracket:last_bracket+1]
            print("Extracted JSON array.")
        else:
            print("Could not find [ and ].")
        
        sanitized = _sanitize_json_text(content)
        data = json.loads(sanitized)
        print(f"Successfully parsed {len(data)} items.")
except Exception as exc:
    print(f"Error: {exc}")
