import os

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created successfully!")
    else:
        print(f"Folder '{folder_name}' already exists.")

def create_file(file_path, content=""):
    with open(file_path, 'w') as file:
        file.write(content)
        print(f"File '{file_path}' created and content written successfully!")

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"File '{file_path}' content:")
            print(content)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

def search_file(file_name, search_directory):
    for root, dirs, files in os.walk(search_directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def main():
    folder_name = input("Enter the name of the folder you want to create: ")
    create_folder(folder_name)

    file_name = input("Enter the name of the file you want to create (with extension): ")
    file_path = os.path.join(folder_name, file_name)


if __name__ == "__main__":
    main()
