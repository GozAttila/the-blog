import os

BLACKLIST_DIR = os.path.join(os.path.dirname(__file__), 'blacklists')

def load_blacklist():
    blacklist = set()
    for filename in os.listdir(BLACKLIST_DIR):
        if filename not in {'LICENSE', 'whitelist.txt'} and not filename.endswith('.md'):
            with open(os.path.join(BLACKLIST_DIR, filename), 'r', encoding='utf-8') as file:
                blacklist.update(line.strip().lower() for line in file)
    return blacklist

def load_whitelist():
    whitelist = set()
    whitelist_path = os.path.join(BLACKLIST_DIR, 'whitelist.txt')
    if os.path.exists(whitelist_path):
        with open(whitelist_path, 'r', encoding='utf-8') as file:
            whitelist.update(line.strip().lower() for line in file)
    return whitelist

def is_valid_username(username):
    whitelist = load_whitelist()
    if username.lower() in whitelist:
        return True

    blacklist = load_blacklist()
    if username.lower() in blacklist:
        return False
    return True

def check_text_validity(text):
    whitelist = load_whitelist()
    blacklist = load_blacklist()
    words = text.strip().lower().split()

    invalid_words = [word for word in words if word not in whitelist and word in blacklist]

    return len(invalid_words) == 0, invalid_words

def add_to_file(list_type, word):
    list_path = os.path.join(BLACKLIST_DIR, f'{list_type}.txt')
    with open(list_path, 'r', encoding='utf-8') as file:
        lines = file.read()
        last_char = lines[-1] if lines else '\n'

    with open(list_path, 'a', encoding='utf-8') as file:
        if last_char != '\n':
            file.write('\n')
        file.write(word + '\n')

def remove_from_file(list_type, word):
    list_path = os.path.join(BLACKLIST_DIR, f'{list_type}.txt')
    with open(list_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(list_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip().lower() != word.lower():
                file.write(line)

