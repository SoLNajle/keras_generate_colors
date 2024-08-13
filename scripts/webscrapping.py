import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.ppgpaints.com/color/color-families/browse-all-colors"
HTML_FILE = "data/colors.html"
CSV_FILE = "data/colors_pgp.csv"


def get_html(url):
    response = requests.get(url)
    return response.text


def read_html(html):
    with open(HTML_FILE, "w") as file:
        file.write(html)
    return HTML_FILE


def get_soup(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup


def find_colors(soup):
    colors = soup.find_all("a", class_="color-rect js-color-rect")
    return colors


def extract_color_info(color):
    name = color.find("h3").text
    code = color.find("span", class_="color-rect-code").text
    rgb_raw = color["style"]
    red = rgb_raw.split("rgb(")[-1].split(",")[0]
    green = rgb_raw.split("rgb(")[-1].split(",")[1]
    blue = rgb_raw.split("rgb(")[-1].split(",")[2][:-1]
    rgb = [red, green, blue]
    return name, rgb, code


def create_color_df(colors) -> pd.DataFrame:
    color_data = []
    color_df = pd.DataFrame(columns=["name", "red", "green", "blue", "code"])
    for color in colors:
        color_info = extract_color_info(color)
        color_rgb = color_info[1]
        color_info = {"name": color_info[0],
                      "red": color_rgb[0],
                      "green": color_rgb[1],
                      "blue": color_rgb[2],
                      "code": color_info[2]}
        color_data.append(color_info)
    color_df = pd.DataFrame(color_data)

    return color_df


def save_color_df(df):
    df.to_csv("data/colors_pgp.csv", index=False)


def main():
    html = get_html(URL)
    # html = read_html(HTML_FILE)
    soup = get_soup(html)
    colors = find_colors(soup)
    df = create_color_df(colors)
    save_color_df(df)
    print(df.head(4))


def test():
    a = 'style="background-color: rgb(213, 216, 215)'
    color = a.split("rgb(")[-1].split(",")[0]
    print(color)


if __name__ == "__main__":
    main()

