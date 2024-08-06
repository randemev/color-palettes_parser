import requests
import bs4
import random
'''
 TODO: bs4: 
  1) для рандомных страниц DONE 
  2) для заданных пользователем страниц NOT DONE

  + все то же, 
  но с возможностью выбора категории (warm, cold...) для поиска DONE 50%
'''


link = "https://colorpalettes.net/"

def correction_category(category):
    if category != None:
        return link + f"category/{category}"
    return link

def get_num_of_pages(category = None):
    '''
    Пересчитывает страницы на https://colorpalettes.net/
    '''
    _link = correction_category(category)
    response = requests.get(_link).text
    soup = bs4.BeautifulSoup(response, "html.parser")

    num_of_pages = int(soup.find("article", class_ = "tipe outer")\
                        .find("div", class_ = "internal bigp")\
                        .find("div", class_ = "navigation")\
                        .find_all("a")[-2].text)

    return num_of_pages

def get_random(category = None):
    '''
    Выдает рандомную цветовую палитру (.jpg)
    '''
    num_of_pages = get_num_of_pages(category)

    i = random.randint(1, num_of_pages)
    _link = correction_category(category)
    response = requests.get(f"{_link}/page/{i}").text
    soup = bs4.BeautifulSoup(response, "html.parser")

    boxes = soup.find("article", class_ = "tipe outer")\
                .find("div", class_ = "nointernal")\
                .find_all("div", class_ = "w6")

    #исключает первую картинку первой странички (там не то)
    j = random.randint(int(i == 0), len(boxes) - 1)
    box = boxes[j]

    palette_name = box.find_all("a")[1].find("h3").getText()
    list_tags = box.find("p")\
                    .find_all("a")
    msg = f"{palette_name}\nТэги:\n{list_tags[0].getText()}"
    for tag in list_tags[1::]:
        msg += f", {tag.getText()}"
    
    image_link = box.find("img").get("src")
    image_bytes = requests.get(image_link).content

    # FIXME: для каждого пользователя должно быть свое имя файла!!! (желательно по @тегу)
    # но делал прогу буквально за день, так что исправлю позже
    with open("tmp.jpg", "wb") as file:
        file.write(image_bytes)

    return msg

if __name__ == "__main__":
    get_random()