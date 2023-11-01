# ARM Converter
A local ARM converter for iOS Reverse Engineering similar to armconverter.com. It has support for ARM32 & ARM64 with both little & big endian. You can extend it by downloading different toolchains. Currently, `as` and `objdump` are required for the script to work. Download the ARM toolchains [here](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads). 

## Building
- Run `python -m build` to build the package
- Install with `pip install --force-reinstall arm_converter --find-links=dist`

## Publishing
- Check with `twine check dist/*`
- Upload to TestPyPI before publishing it `twine upload -r testpypi dist/*`
  - Install with `pip install arm_converter -i https://testpypi.python.org/pypi`
- Publish it with `twine upload dist/*`
