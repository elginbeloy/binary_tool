from shutil import get_terminal_size

TERMINAL_HEIGHT_LINES = get_terminal_size().lines

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


def update_file(original_file_path, byte_changes):
    new_file_path = input("File save path " + colored("$ ", "green"))
    with open(original_file_path, "rb") as original_file, open(new_file_path, "wb") as new_file:
        offset = 0
        data = original_file.read()
        for i, byte in enumerate(data):
            if f"{i:08x}" in byte_changes:
                new_byte = byte_changes[f"{i:08x}"]
                new_file.write(bytes([new_byte]))
            else:
                new_file.write(bytes([byte]))
    print(colored(f"Saved to {new_file_path}!", "green"))

def hexdump(file_path, width=16):
    byte_changes = {}
    with open(file_path, "rb") as f:
        offset = 0
        skip_offset = width * (TERMINAL_HEIGHT_LINES - 4)
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
            print(line, end=("\n" if skip_offset > 0 else " "))
            if skip_offset > 0:
              skip_offset -= len(chunk)
              offset += len(chunk)
              continue

            command_key = input(" ")
            if len(command_key) == 1:
                if command_key == "q":
                    exit()
                elif command_key == "d":
                    skip_offset = width * TERMINAL_HEIGHT_LINES
                elif command_key == "s":
                    offset = int(input("seek to byte (offset hex): "), 16)
                    f.seek(offset)
                elif command_key == "e":
                    to_edit_offset = input("byte to edit (hex offset): ")
                    byte_changes[to_edit_offset] = int(input("new value (hex): "), 16)
                    if input("save updates? [y/N] ") == "y":
                        update_file(file_path, byte_changes)
            else:
              offset += len(chunk)

if __name__ == "__main__":
    file_path = input("file path " + colored("$ ", "green"))
    print(colored(
      "d = page down, s = seek, e = edit, q = quit", "blue",
      attrs=["bold"]
    ))
    print()
    hexdump(file_path)
