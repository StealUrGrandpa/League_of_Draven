import requests



def choice():
    gg = input('What to do? (1. add/2. delete)\n')
    return gg
def add_champion(champ, runes):
    url = "https://StealUrGrandpa.pythonanywhere.com/database/add"

    new_champion = {
        champ : runes
    }

    response = requests.post(url, json=new_champion)


def delete_champion():
    url = "https://StealUrGrandpa.pythonanywhere.com/database/delete"  # Replace with your URL
    data_to_delete = {
        "keys": ["Yasuo"]
    }

    response = requests.delete(url, json=data_to_delete)

    print(response.json())


