from typing import cast, Callable
from scrapers import superselectos, walmart, pricesmart, chilax, mimascota
from utils.get_number_between_options import get_number


ScrappingFunction = Callable[[str, str, str], None]


def scrape_products_prompt() -> None:
    """
    Scrapes product data from a website and saves it to an Excel file.
    Parameters are entered interactively via prompts.

    Returns:
        None: The results are saved to an Excel file.
    """
    # Prompt user for parameters
    scrapping_sources: dict[int, dict[str, str | ScrappingFunction]] = {
        1: {
            "key": "superselectos",
            "base_url": "https://www.superselectos.com/products?category=",
            "page_notation": "?page=",
            "function": superselectos.main,
        },
        2: {
            "key": "walmart",
            "base_url": "https://www.walmart.com.sv/",
            "page_notation": "?page=",
            "function": walmart.main,
        },
        3: {
            "key": "pricesmart",
            "base_url": "https://www.pricesmart.com/es-sv/categoria/",
            "page_notation": "?page=",
            "function": pricesmart.main,
        },
        4: {
            "key": "mimascota",
            "base_url": "https://sv.miscota.com/",
            "page_notation": "?pag=",
            "function": mimascota.main,
        },
        5: {
            "key": "chilax",
            "base_url": "https://chilax.es/product-category/",
            "page_notation": "/page/",
            "function": chilax.main,
        },
    }

    prompt_message = "Select website from following available: \n"
    for i, source in enumerate(scrapping_sources.values(), 1):
        prompt_message += f"{i}. {source["key"]} \n"

    scrapping_source_option_number = get_number(prompt_message, len(scrapping_sources))

    category: str = input("Enter the category code or name: ").strip()
    source = scrapping_sources[scrapping_source_option_number]

    try:
        base_url = cast(str, source["base_url"])
        page_notation = cast(str, source["page_notation"])
        source_scrapping_routine = cast(ScrappingFunction, source["function"])

        source_scrapping_routine(base_url, page_notation, category)
    except Exception as e:
        return print(f"Error: {e}")


scrape_products_prompt()
