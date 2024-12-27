from openpyxl import Workbook
import os
from bs4 import BeautifulSoup, ResultSet, Tag
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait


def main(base_url: str, page_notation: str, category: str):
    service = Service(ChromeDriverManager().install())
    option = ChromeOptions()
    option.add_argument("--headless")
    driver = Chrome(service=service, options=option)

    workbook = Workbook()
    sheet = workbook.active

    try:
        url = f"{base_url}{category}"

        if sheet is not None:
            sheet.append(["Descripción", "Precio"])  # Add headers

        page = 1
        while True:
            driver.get(url)
            _ = WebDriverWait(driver, 10)  # 10 seconds timeout

            html = driver.page_source
            # Fetch the webpage content
            soup = BeautifulSoup(html, "html.parser")

            result_list: ResultSet[Tag] = soup.find_all(
                "div", attrs={"class": "product-card-vertical"}
            )

            if not result_list:  # Stop if no more products are found
                break

            # Extract and write product data to the Excel sheet
            for li in result_list:
                nombre_tag = li.find("span", attrs={"class": "product-card__title"})
                precio_tag = li.find("span", attrs={"class": "sf-price__regular"})

                if nombre_tag and precio_tag and sheet:
                    nombre = nombre_tag.text.strip()
                    precio = precio_tag.text.strip()
                    sheet.append([nombre, precio])

            # Increment the page number and update the URL
            page += 1
            url = f"{base_url}{category}{page_notation}{page}"

        current_path = os.getcwd()
        file_path = os.path.join(current_path, "products_pricemart.xlsx")
        workbook.save(file_path)
        print(f"Archivo creado exitosamente: {file_path}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    # Save the workbook to a file
