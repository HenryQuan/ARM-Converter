import sys
from arm_converter import convert_arm32, convert_arm64

print("Enter instructions: (end with Ctrl+Z)")
input = sys.stdin.read()
print("ARM32:")
print(convert_arm32(input))

print("\nARM64:")
print(convert_arm64(input))
