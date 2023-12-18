from cryptography.fernet import Fernet
import os
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

def generate_key():
    key = Fernet.generate_key()
    print(f"{Fore.GREEN}Generated Key:{Style.RESET_ALL} {key.decode('utf-8')}")
    return key

def write_key(key, key_filename="secret.key"):
    with open(key_filename, "wb") as key_file:
        key_file.write(key)

def load_key(key_filename="secret.key"):
    return open(key_filename, "rb").read()

def encrypt_folder_to_file(folder_path, key, output_filename="encrypted_data.dat"):
    cipher = Fernet(key)
    encrypted_data_list = []

    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            with open(file_path, "rb") as file:
                plaintext = file.read()
                encrypted_data = cipher.encrypt(plaintext)
                encrypted_data_list.append((file_path, encrypted_data))

    desktop_path = Path.home() / "Desktop"
    output_filepath = desktop_path / output_filename

    with open(output_filepath, "wb") as output_file:
        for file_path, encrypted_data in encrypted_data_list:
            output_file.write(file_path.encode('utf-8') + b'\n')
            output_file.write(encrypted_data + b'\n')

def decrypt_file_to_folder(input_filename, key, output_folder_path):
    cipher = Fernet(key)

    with open(input_filename, "rb") as input_file:
        lines = input_file.readlines()

    try:
        for i in range(0, len(lines), 2):
            file_path = lines[i].decode('utf-8').strip()
            encrypted_data = lines[i + 1].strip()
            decrypted_data = cipher.decrypt(encrypted_data)

            output_file_path = os.path.join(output_folder_path, Path(file_path).name)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            with open(output_file_path, "wb") as file:
                file.write(decrypted_data)
    except Exception as e:
        print(f"{Fore.RED}Error during decryption:{Style.RESET_ALL} {e}")

def print_banner():
    banner = f"""{Fore.CYAN}
   ____ _                 _     ____                  _           
  / ___| | ___  _   _  __| |   |  _ \ ___  ___ _ __ | | ___  _ __ 
 | |   | |/ _ \| | | |/ _` |   | |_) / _ \/ _ \ '_ \| |/ _ \| '__|
 | |___| | (_) | |_| | (_| |   |  __/  __/  __/ | | | | (_) | |   
  \____|_|\___/ \__,_|\__,_|   |_|   \___|\___|_| |_|_|\___/|_|   
  
{Fore.YELLOW}Made by AsyNoName{Style.RESET_ALL}"""
    print(banner)

def main():
    print_banner()
    action = input(f"{Fore.YELLOW}Enter 'e for encrypt' or 'd for decrypt':{Style.RESET_ALL} ").lower()
    key_filename = "secret.key"

    if os.path.exists(key_filename):
        key = load_key(key_filename)
    else:
        key = generate_key()
        write_key(key, key_filename)

    if action == 'e':
        folder_path = input(f"{Fore.YELLOW}Enter the folder path to encrypt:{Style.RESET_ALL} ")
        encrypt_folder_to_file(folder_path, key)
    elif action == 'd':
        input_filename = input(f"{Fore.YELLOW}Enter the encrypted file path to decrypt:{Style.RESET_ALL} ")
        output_folder_path = input(f"{Fore.YELLOW}Enter the folder path to store decrypted files:{Style.RESET_ALL} ")
        decrypt_file_to_folder(input_filename, key, output_folder_path)
    else:
        print(f"{Fore.RED}Invalid action. Please enter 'encrypt' or 'decrypt'.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
