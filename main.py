# ANSI escapes for colors and attributes
def colored(text, color=None, attrs=None):
    colors = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
    }

    attributes = {
        "bold": 1,
        "underline": 4,
        "reversed": 7,
    }

    codes = []
    if color and color in colors:
        codes.append(str(colors[color]))

    if attrs:
        for attr in attrs:
            if attr in attributes:
                codes.append(str(attributes[attr]))

    if codes:
        codes = ";".join(codes)
        return f"\033[{codes}m{text}\033[0m"
    return text

def to_hex(byte):
    return f"{byte:02x}"

def to_ascii(byte):
    return colored(chr(byte), "blue") if 32 <= byte <= 126 else '.'

def hexdump(file_path, width=16):
    with open(file_path, "rb") as f:
        offset = 0
        while True:
            chunk = f.read(width)
            if not chunk:
                break

            hex_values = ' '.join(to_hex(byte) for byte in chunk)
            ascii_values = ''.join(to_ascii(byte) for byte in chunk)
            # len(last chunk) could be < width
            padding = '   ' * (width - len(chunk))
            line = colored(f"{offset:08x}  ", "magenta", attrs=["bold"])
            line += colored(hex_values, "green") + padding
            line += f"  |{ascii_values}|"
            print(line, end=" ")
            command_key = input("$ ")
            if len(command_key) == 1:
              offset = int(input("seek "))

            offset += len(chunk)

if __name__ == "__main__":
    file_path = input("file path " + colored("$ ", "green"))
    hexdump(file_path)
