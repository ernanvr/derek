from openpyxl import Workbook
from requests import get
import os
from bs4 import BeautifulSoup, ResultSet, Tag


def main(base_url: str, page_notation: str, category: str):
    # Create a new workbook and select the active sheet
    workbook = Workbook()
    sheet = workbook.active

    if sheet is not None:
        sheet.append(["Descripción", "Precio"])  # Add headers

    # Construct the URL
    url = f"{base_url}{category}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    page = 1
    while True:
        # Fetch the webpage content
        response = get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        lis: ResultSet[Tag] = soup.find_all(
            "div", attrs={"class": "vtex-search-result-3-x-galleryItem"}
        )

        if not lis:  # Stop if no more products are found
            break

        # Extract and write product data to the Excel sheet
        for li in lis:
            nombre_tag = li.find(
                "div", attrs={"class": "vtex-product-summary-2-x-nameContainer"}
            )
            precio_tag = li.find("div", attrs={"class": "price-container"})

            if nombre_tag and precio_tag and sheet:
                nombre = nombre_tag.text.strip()
                precio = precio_tag.text.strip()
                sheet.append([nombre, precio])

        # Increment the page number and update the URL
        page += 1
        url = f"{base_url}{category}{page_notation}{page}"

    # Save the workbook to a file
    current_path = os.getcwd()
    file_path = os.path.join(current_path, "products_walmart.xlsx")
    workbook.save(file_path)
    print(f"Archivo creado exitosamente: {file_path}")
