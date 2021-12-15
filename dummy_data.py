import string
import random
import names


def generate_user():
    name = names.get_first_name()
    username = name + \
        random.choice(string.punctuation) + \
        "".join(random.sample(string.digits, 5))

    email = name + "".join(random.sample(string.digits, 5)) + "@" + \
        "".join(random.choices(string.ascii_lowercase, k=3)) + ".com"
        
    return {
        "username": username,
        "email": email,
    }


def generate_bank():
    iban = generate_iban()
    firstname = names.get_first_name()
    lastname = names.get_last_name()
    return {
        "iban": iban,
        "firstname": firstname,
        "lastname": lastname
    }


def generate_iban():
    country_code = random.choices(string.ascii_uppercase, k=2)
    iban = country_code + random.choices(string.digits, k=20)
    return "".join(iban)

def generate_playlist(username: str):
    return username + "'s playlist"