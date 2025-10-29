import ctypes
import os
import pefile

# Load the NVTT DLL
# dll_path = r"C:\Program Files\NVIDIA Corporation\NVIDIA Texture Tools\nvtt30205.dll"
dll_path = r"C:\Users\denys.oligov\source\repos\SymbolsIntrospection\x64\Debug\SymbolExtractorDLL.dll"


try:
    pe = pefile.PE(dll_path)
    print(f"Exported functions in {dll_path}:\n")

    # Iterate through the Export Directory Table
    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            if exp.name:
                print(f"- {exp.name.decode('utf-8')} (Ordinal: {exp.ordinal})")
    else:
        print("No export table found. This DLL might not expose functions directly.")

except FileNotFoundError:
    print(f"Error: Cannot find {dll_path}.")
except Exception as e:
    print(f"Error loading DLL: {e}")


# try:
#     pe = pefile.PE(dll_path)
#     print(f"Exported NVTT functions in {dll_path}:\n")

#     # Iterate through the Export Directory Table and filter for 'nvtt'
#     if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
#         for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
#             if exp.name and exp.name.decode().startswith("nvtt"):
#                 print(f"- {exp.name.decode()} (Ordinal: {exp.ordinal})")
#     else:
#         print("No export table found. This DLL might not expose functions directly.")

# except FileNotFoundError:
#     print(f"Error: Cannot find {dll_path}.")
# except Exception as e:
#     print(f"Error loading DLL: {e}")