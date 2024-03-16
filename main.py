# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import requests
from bs4 import BeautifulSoup
import openai
import json
import asyncio

async def get_website_links_async(url, depth, collected_urls=None):
    collected_urls = collected_urls or set()
    if depth == 0:
        return collected_urls

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            print(soup)
            links = soup.find_all('a', href=True)
            for link in links:
                href_value = link['href']
                full_url = href_value if href_value.startswith('http') else url + href_value

                if full_url not in collected_urls:
                    collected_urls.add(full_url)
                    await get_website_links_async(full_url, depth - 1, collected_urls)
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")

    return collected_urls

async def get_car_data_async(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.text

            openai.api_key = 'your-openai-api-key'
            prompt = "You are an analyst compiling data from car websites. Here is the text from a website with car information, I need to extract information as json data for the following fields, " + \
                "StockNumber, Vin, SellingPrice, PreviousPrice, Description, Condition(New or Used), Make, Model, YearModel, TrimModel, BodyType, " + \
                "ExteriorColor, Mileage, FuelType, Engine, Transmission. If you can't find data just set the value to null. " + \
                "Also add the vehicle technical data as an array called TechnicalOptions, and the vehicle Options as VehicleOptions as an array," + \
                " also set to null if not found. If the text doesn't have any VIN, then just return an empty json since is not a valid car site.\n"

            result = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "assistant", "content": prompt + data}
                ]
            )

            return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return None

async def main():
    #target_url = "https://www.boyergmbancroft.com/en"
    target_url = "https://networkofnature.org/"
    #target_url = "https://networkofnature.org/species/forbs/"
    max_depth = 1
    filter_word = ["forbs","graminoids"]

    found_urls = await get_website_links_async(target_url, max_depth)
    #for url in found_urls:
        #print(url)
        # if any(word in url for word in filter_word):
        #     found_urls2 = await get_website_links_async(url, max_depth)
        #     for url2 in found_urls2:
        #         print("filtered: " + url2)

    # for url in found_urls:
    #     print(url)
    #     if filter_word in url:
    #         car_data = await get_car_data_async(url)
    #         if car_data:
    #             with open("C:\\Users\\laalm\\Desktop\\Crawler.txt", "a") as f:
    #                 f.write(car_data + '\n')

asyncio.run(main())



# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#     #target_url = "https://www.boyergmbancroft.com/en/"
#     target_url = "https://networkofnature.org/species/graminoids/"
#     max_depth = 5
#     filter_word = "used-inventory"
#
#     found_urls = await get_website_links_async(target_url, max_depth)
#     print(found_urls)
#     # for url in found_urls:
#     #     print(url)
#     #     if filter_word in url:
#     #         car_data = await get_car_data_async(url)
#     #         if car_data:
#     #             with open("C:\\Users\\laalm\\Desktop\\Crawler.txt", "a") as f:
#     #                 f.write(car_data + '\n')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
