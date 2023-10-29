import subprocess

def convert(instructions: str, as_path: str, objdump_path: str) -> str:
    """
    Run `as` to compile instructions to assembly.
    Then, run `objdump` to disassemble the object file.
    """
    with open("temp/temp.asm", "w") as f:
        f.write(instructions + "\n")

    proc = subprocess.run(
        [as_path, "temp/temp.asm"],
        stdout=subprocess.PIPE,
    )

    # make sure there are no errors
    if proc.returncode != 0:
        return "Invalid instructions"

    proc = subprocess.run(
        [objdump_path, "-d", "a.out"],
        stdout=subprocess.PIPE,
    )

    output = proc.stdout.decode("utf-8")
    if output == "":
        return "Invalid instructions"
    temp = output.split("<.text>:")[1].strip()
    temp = temp.split("\n")
    instructions = []
    for line in temp:
        instructions.append(line.split(":")[1].strip().upper())
    return "\n".join(instructions)

def convert_arm32(instructions: str) -> str:
    return convert(instructions, "tools/arm-none-eabi-as.exe", "tools/arm-none-eabi-objdump.exe")

def convert_arm64(instructions: str) -> str:
    return convert(instructions, "tools/aarch64-none-elf-as.exe", "tools/aarch64-none-elf-objdump.exe")


if __name__ == "__main__":
    print(convert_arm64("mov x0, x1\ncmp x8, x9\nadds x0, x3, x4"))
