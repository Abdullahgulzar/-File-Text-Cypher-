import os

# Caesar cipher encryption function
def encrypt_text_caesar(plain_text, shift=3):
    encrypted = ""
    for char in plain_text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            encrypted += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted += char
    return encrypted

# Caesar cipher decryption function
def decrypt_text_caesar(encrypted_text, shift=3):
    return encrypt_text_caesar(encrypted_text, -shift)

# Playfair cipher encryption function
def encrypt_text_playfair(plain_text, key="KEYWORD"):
    key = ''.join(sorted(set(key), key=key.index))
    table = create_playfair_table(key)

    # Prepare text by removing spaces and handling double letters
    text = ''.join(plain_text.split()).upper().replace("J", "I")  # Standard Playfair replaces 'J' with 'I'
    
    # Ensuring text is split into digraphs correctly
    prepared_text = ""
    i = 0
    while i < len(text):
        if i < len(text) - 1 and text[i] == text[i + 1]:  
            prepared_text += text[i] + "X"  # Insert 'X' between double letters
            i += 1
        else:
            prepared_text += text[i]
        i += 1

    if len(prepared_text) % 2 != 0:
        prepared_text += 'X'  # Padding with 'X' if text has odd length

    encrypted = ""
    for i in range(0, len(prepared_text), 2):
        pair = prepared_text[i:i+2]
        row1, col1 = find_position(pair[0], table)
        row2, col2 = find_position(pair[1], table)
        
        if row1 == row2:  # Same row
            encrypted += table[row1][(col1 + 1) % 5]
            encrypted += table[row2][(col2 + 1) % 5]
        elif col1 == col2:  # Same column
            encrypted += table[(row1 + 1) % 5][col1]
            encrypted += table[(row2 + 1) % 5][col2]
        else:  # Rectangle swap
            encrypted += table[row1][col2]
            encrypted += table[row2][col1]
    
    return encrypted

# Playfair cipher decryption function
def decrypt_text_playfair(encrypted_text, key="KEYWORD"):
    key = ''.join(sorted(set(key), key=key.index))
    table = create_playfair_table(key)

    text = encrypted_text.upper()
    decrypted = ""
    for i in range(0, len(text), 2):
        pair = text[i:i+2]
        row1, col1 = find_position(pair[0], table)
        row2, col2 = find_position(pair[1], table)
        
        if row1 == row2:  # Same row
            decrypted += table[row1][(col1 - 1) % 5]
            decrypted += table[row2][(col2 - 1) % 5]
        elif col1 == col2:  # Same column
            decrypted += table[(row1 - 1) % 5][col1]
            decrypted += table[(row2 - 1) % 5][col2]
        else:  # Rectangle swap
            decrypted += table[row1][col2]
            decrypted += table[row2][col1]
    
    return decrypted

# Create Playfair cipher table based on the key
def create_playfair_table(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # 'J' is omitted
    table = []
    for char in key:
        if char not in table and char != 'J':
            table.append(char)
    
    for char in alphabet:
        if char not in table:
            table.append(char)
    
    table = [table[i:i+5] for i in range(0, 25, 5)]
    return table

# Find position of a character in the Playfair table
def find_position(char, table):
    for i, row in enumerate(table):
        if char in row:
            return i, row.index(char)
    return None, None

# Function to write encrypted text to a file
def write_to_file(filename, encrypted_text):
    with open(filename, 'w') as file:
        file.write(encrypted_text)
    print(f"Encrypted text saved to {filename}")

# Function to read encrypted text from a file
def read_from_file(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} does not exist.")
        return None
    with open(filename, 'r') as file:
        return file.read()

# Main function to interact with the user
def main():
    print("Welcome to the File Text Cipher Program!")
    
    while True:
        print("\nChoose an option:")
        print("1. Create or edit a file with encrypted text")
        print("2. Decrypt and read text from an existing file")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == "1":
            filename = input("Enter the filename (with .txt extension): ").strip()
            cipher_choice = input("Choose a cipher (1. Caesar, 2. Playfair): ").strip()
            plain_text = input("Enter the text to encrypt: ")

            if cipher_choice == "1":
                encrypted_text = encrypt_text_caesar(plain_text)
            elif cipher_choice == "2":
                encrypted_text = encrypt_text_playfair(plain_text)
            else:
                print("Invalid cipher choice.")
                continue
            
            write_to_file(filename, encrypted_text)
        
        elif choice == "2":
            filename = input("Enter the filename to decrypt: ").strip()
            cipher_choice = input("Choose a cipher (1. Caesar, 2. Playfair): ").strip()
            
            encrypted_text = read_from_file(filename)
            if encrypted_text is not None:
                if cipher_choice == "1":
                    decrypted_text = decrypt_text_caesar(encrypted_text)
                elif cipher_choice == "2":
                    decrypted_text = decrypt_text_playfair(encrypted_text)
                else:
                    print("Invalid cipher choice.")
                    continue
                
                print("\nEncrypted text from file:")
                print(encrypted_text)
                print("\nDecrypted text:")
                print(decrypted_text)
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
