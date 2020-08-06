import pandas as pd
import os


def get_provincies_link():
    return (pd.read_csv(filepath_or_buffer="/home/carlos/Documents/Scrapping/CrawlIdealista/CrawlIdealista/provincies.csv")['provincies'])

def get_provincies(tipos):
    result = []
    provincies = get_provincies_link()
    for tipo in tipos:
        for province in provincies:
            result.append(province.replace('<redef>', tipo))
    return result
