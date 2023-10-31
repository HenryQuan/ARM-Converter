import subprocess
import platform
import os

from enum import Enum


class Encoding(Enum):
    LITTLE_ENDIAN = 0
    BIG_ENDIAN = 1

def _system_check():
    curr_system = platform.system()
    if curr_system != "Windows":
        print(f"Unsupported system: {curr_system}")
        exit(-1)

def convert(
    instructions: str,
    as_path: str,
    objdump_path: str,
    encoding: Encoding = Encoding.LITTLE_ENDIAN,
) -> str:
    """
    Run `as` to compile instructions to assembly.
    Then, run `objdump` to disassemble the object file.
    """

    current_directory = os.path.dirname(os.path.realpath(__file__))
    temp_path = os.path.join(current_directory, "temp.asm")
    with open(temp_path, "w") as f:
        f.write(instructions + "\n")

    as_path = os.path.join(current_directory, as_path)
    objdump_path = os.path.join(current_directory, objdump_path)

    proc = subprocess.run(
        [as_path, temp_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )

    # make sure there are no errors
    if proc.returncode != 0:
        return "Invalid instructions"

    proc = subprocess.run(
        [objdump_path, "-d", "a.out"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )

    output = proc.stdout.decode("utf-8")
    if output == "":
        return "Invalid instructions"
    temp = output.split("<.text>:")[1].strip()
    temp = temp.split("\n")
    instructions = []
    for line in temp:
        raw = line.split(":")[1].strip().upper().split("\t")
        # the machine code starts first
        code = raw[0].strip()
        if encoding == Encoding.LITTLE_ENDIAN:
            # reverse per two characters
            code = "".join(reversed([code[i : i + 2] for i in range(0, len(code), 2)]))
        code = f"{code}:\t" + "\t".join(raw[1:])
        instructions.append(code)
    return "\n".join(instructions)


def convert_arm32(
    instructions: str,
    encoding: Encoding = Encoding.LITTLE_ENDIAN,
) -> str:
    _system_check()
    return convert(
        instructions,
        "tools/arm-none-eabi-as.exe",
        "tools/arm-none-eabi-objdump.exe",
        encoding,
    )


def convert_arm64(
    instructions: str,
    encoding: Encoding = Encoding.LITTLE_ENDIAN,
) -> str:
    _system_check()
    return convert(
        instructions,
        "tools/aarch64-none-elf-as.exe",
        "tools/aarch64-none-elf-objdump.exe",
        encoding,
    )
