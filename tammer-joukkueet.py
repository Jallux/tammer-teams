import argparse
import requests
from bs4 import BeautifulSoup

url = 'https://kyykka.pro/ranking/tammer-kyykk%C3%A4/2024'
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    miehet_section = soup.find('h3', string='Miehet')
    
    if miehet_section:
        miehet_table = miehet_section.find_next('table')
        
        if miehet_table:
            ranking = []
            
            rows = miehet_table.find_all('tr')
            
            for row in rows:
                columns = row.find_all('td')
                if columns:
                    first_column = columns[0].text.strip().lower().split()
                    ranking.append(f"{first_column[1]} {first_column[0]}")
        else:
            print("Miehet table not found.")
    else:
        print("Miehet section not found.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

parser = argparse.ArgumentParser(description="Tammer-kyykän joukkueengeneroimistyökalu.")
parser.add_argument("mode", choices=['mj', 'mp'], help="mj tai mp.")

parser.add_argument("--ilmo", help="Tiedosto, jossa listattuna kaikki ilmoittautuneet omille riveilleen (sukunimi etunumi)", default="ilmo.txt")
parser.add_argument("--ranking", help="Tiedosto, jossa listattuna kaikki pelaajat ranking järjestyksessä omille riveilleen. Muotoilu sama kuin https://kyykka.pro/ranking/", default=ranking)

args = parser.parse_args()

with open(args.ilmo, 'r', encoding='utf-8') as file:
    ilmoittautuneet = [line.strip().lower() for line in file]

if args.ranking != ranking:
    with open(args.ranking, 'r', encoding='utf-8') as file:
        rankingnames = [line.strip().lower() for line in file]
        ranking = [f"{surname.lower()} {firstname.lower()}" for firstname, surname in (name.split() for name in rankingnames)]

order_index = {name: index for index, name in enumerate(ranking)}
large_index = len(ranking) + 1

teams = sorted(ilmoittautuneet, key=lambda name: order_index.get(name, large_index))

i, j = 1, 1
for member in teams:
    print(f"{i}. {member} (Tammer {j})")
    if args.mode == "mj" and i % 4 == 0:
        j+=1
    elif args.mode == "mp" and i % 2 == 0:
        j+=1
    i+=1
