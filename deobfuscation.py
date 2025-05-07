import jsbeautifier
import re
import os

def decode_from_charcode(js_code):
    # Example: String.fromCharCode(104, 105) → "hi"
    pattern = r'String\.fromCharCode\(([\d,\s]+)\)'

    def decode_match(match):
        chars = match.group(1).split(',')
        decoded = ''.join([chr(int(c.strip())) for c in chars])
        return f'"{decoded}"'

    return re.sub(pattern, decode_match, js_code)

def decode_hex(js_code):
    # Example: \x68\x69 → hi
    return re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), js_code)

def deobfuscate_js_file(input_path, output_path):
    if os.path.abspath(input_path) == os.path.abspath(output_path):
        print("⚠️  Output file cannot be the same as the input file. Please choose a different name.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        js_code = f.read()

    print("[*] Beautifying JavaScript...")
    beautified = jsbeautifier.beautify(js_code)

    print("[*] Decoding fromCharCode...")
    beautified = decode_from_charcode(beautified)

    print("[*] Decoding hex values...")
    beautified = decode_hex(beautified)

    print("[*] Removing obfuscated eval blocks...")
    beautified = re.sub(
        r'eval\(function\s*\(p,a,c,k,e,d.*?\)\)',
        r'/* [Obfuscated eval removed] */',
        beautified,
        flags=re.DOTALL
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(beautified)

    print(f"[+] Deobfuscated code saved to: {output_path}")

# --- Main execution ---
if __name__ == "__main__":
    print("🔍 Enter the path to the obfuscated JavaScript file:")
    input_file = input("📄 Input file: ").strip()
    output_file = input("💾 Output file (must be different): ").strip()
    deobfuscate_js_file(input_file, output_file)
