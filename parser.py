import time
import requests
from bs4 import BeautifulSoup


def parse_medicine_info(medicine_name):
    url = f"https://www.vidal.ru/search?q={medicine_name}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Находим все ссылки на препараты
        links = soup.select('td.products-table-name a')

        # Если есть найденные препараты, парсим информацию о них
        if links:
            results = []
            for link in links:
                medicine_url = link['href']
                medicine_info = parse_single_medicine_info(medicine_url)
                if medicine_info:
                    results.append(medicine_info)
                    time.sleep(1)
            return results
    return None


def parse_single_medicine_info(medicine_url):
    full_url = f"https://www.vidal.ru{medicine_url}"
    response = requests.get(full_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        info_block = soup.find('div', class_='more-info')

        if info_block:
            dosages = info_block.find('div', {'id': 'dosage'}).find('div', {'class': 'block-content'}).get_text(strip=True)
            indications = info_block.find('div', {'id': 'indication'}).find('div', {'class': 'block-content'}).get_text(strip=True)
            contraindications = info_block.find('div', {'id': 'contra'}).find('div', {'class': 'block-content'}).get_text(strip=True)

            return {
                'url': full_url,
                'dosages': dosages,
                'indications': indications,
                'contraindications': contraindications
            }
    return None
