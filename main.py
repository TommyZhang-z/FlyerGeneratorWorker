from io import BytesIO
import fitz
from models import Image, PDF, Text, Font

# from data import TEXT_DATA
import requests


pdf_document = fitz.open("./assets/empty.pdf")
digital_pdf = PDF(pdf_document)

# register fonts
digital_pdf.insert_font(Font.INTER_LIGHT)
digital_pdf.insert_font(Font.INTER_REGULAR)
digital_pdf.insert_font(Font.INTER_BOLD)
digital_pdf.insert_font(Font.INTER_SEMIBOLD)

from io import BytesIO
import os
from dotenv import load_dotenv
from celery import Celery
from data import TEXT_DATA
from models import PDF, Font, Image, Text
import dropbox
import datetime
from helper import convert_to_currency, convert_to_syd_time
import requests
import logging
import config as cfg
import fitz
from google_drive import upload_or_replace_file, TARGET_FOLDER_ID

BANNER_PATH = os.path.join(cfg.ASSETS_DIR, "banner.png")
EMPTY_DIGITAL_PATH = os.path.join(cfg.ASSETS_DIR, "ICONIC.pdf")

memo_data = {}
memo_facade_file = {}


# 111homes
TEXT_DATA = {
    "digital": {
        "lot_info": {
            "suburb": {
                "size": 27,
                "position": (58.88, 510.90),
                "font": Font.INTER_BOLD,
                "color": (36 / 255, 36 / 255, 36 / 255),
            },
            "address": {
                "size": 10,
                "position": (60.5, 534.3),
                "font": Font.INTER_REGULAR,
                "color": (36 / 255, 36 / 255, 36 / 255),
            },
            "lot_number": {
                "size": 9,
                "position": (300.5, 503),
                "font": Font.INTER_SEMIBOLD,
                "color": (36 / 255, 36 / 255, 36 / 255),
                "align": "center",
            },
            "date": {
                "size": 10,
                "position": (267, 544),
                "font": Font.INTER_LIGHT,
                "color": (36 / 255, 36 / 255, 36 / 255),
            },
            "land_size": {
                "size": 10,
                "position": (499, 500.3),
                "font": Font.INTER_BOLD,
                "color": (36 / 255, 36 / 255, 36 / 255),
            },
            "house_size": {
                "size": 10,
                "position": (510, 522.9),
                "font": Font.INTER_BOLD,
                "color": (36 / 255, 36 / 255, 36 / 255),
            },
            "lot_width": {
                "size": 10,
                "position": (502.4, 545.2),
                "font": Font.INTER_BOLD,
                "color": (36 / 255, 36 / 255, 36 / 255),
            },
            "land_price": {
                "size": 10,
                "position": (698, 500.0),
                "font": Font.INTER_BOLD,
                "color": (36 / 255, 36 / 255, 36 / 255),
            },
            "house_price": {
                "size": 10,
                "position": (704.3, 522.4),
                "font": Font.INTER_BOLD,
                "color": (36 / 255, 36 / 255, 36 / 255),
            },
            "package_price": {
                "size": 10,
                "position": (714.2, 545.0),
                "font": Font.INTER_BOLD,
                "color": (36 / 255, 36 / 255, 36 / 255),
            },
        },
        "banner": {
            "label": {
                "size": 17,
                "position": (700.69, 67.2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "price": {
                "size": 17,
                "position": (700.69, 88.0),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
        },
        "floorplan_info": {
            "floorplan_model": {
                "size": 15,
                "position": (589.5, 675.7),
                "font": Font.INTER_BOLD,
                "color": (0, 0, 0),
            },
            "bedrooms": {
                "size": 13,
                "position": (617.8, 719.4),
                "font": Font.INTER_REGULAR,
                "color": (0, 0, 0),
            },
            "bathrooms": {
                "size": 13,
                "position": (702.55, 719.4),
                "font": Font.INTER_REGULAR,
                "color": (0, 0, 0),
            },
            "garages": {
                "size": 13,
                "position": (786.9, 719.4),
                "font": Font.INTER_REGULAR,
                "color": (0, 0, 0),
            },
        },
    },
}


def generate_flyer(
    flyer_id,
    facade,
    floorplan_model,
    price,
    suburb,
    address,
    lot,
    land_price,
    house_price,
    land_size,
    house_size,
    lot_width,
    rego,
    bedroom,
    bathroom,
    parking_slot,
    facade_file_url,
    floorplan_file_url,
):
    logging.info(f"generating flyer [#{flyer_id}] ...")
    facade_name = facade
    digital_file_name = f"{flyer_id}.pdf"

    digital_path = os.path.join(cfg.DIGITAL_DIR, digital_file_name)

    try:
        with (
            requests.Session() as session,
            open(BANNER_PATH, "rb") as banner_file,
            open(EMPTY_DIGITAL_PATH, "rb") as empty_digital_file,
            # open(facade_file_url, "rb") as facade_file,
        ):
            if facade_file_url not in memo_facade_file:
                memo_facade_file[facade_file_url] = session.get(facade_file_url).content
            facade = Image(memo_facade_file[facade_file_url])
            if floorplan_file_url not in memo_data:
                memo_data[floorplan_file_url] = session.get(floorplan_file_url).content
            floorplan = PDF(fitz.open(stream=BytesIO(memo_data[floorplan_file_url])))
            banner = Image(banner_file.read())
            empty_digital = PDF(fitz.open(empty_digital_file))
            # empty_printable = PDF(fitz.open(empty_printable_file))
            # png_image = Image(png_file.read())
        empty_digital.insert_font(Font.INTER_LIGHT)
        empty_digital.insert_font(Font.INTER_REGULAR)
        empty_digital.insert_font(Font.INTER_BOLD)
        empty_digital.insert_font(Font.INTER_SEMIBOLD)

        empty_digital.add_image(facade, position=(0, 0), stretch=True)
        empty_digital.add_image(
            banner, position=(841.8900146484375 - 179.2, 44), image_size=(179.2, 56)
        )
        empty_digital.add_pdf(
            floorplan,
            position=(35, 632),
            size=(175 / 297 * 841.8900146484375, 125 / 420 * 1190.550048828125),
        )

        page_width = 841.8900146484375
        page_height = 1190.550048828125
        image_width = 23.52
        image_height = 6.34
        image_width_pt = image_width * 2.8346  # ≈ 66.67 points
        image_height_pt = image_height * 2.8346  # ≈ 17.98 points
        x_pos = page_width - image_width_pt - 10
        y_pos = 420

        # if os.path.exists(
        #     os.path.join(cfg.ASSETS_DIR, "fc_names", f"{facade_name}.png")
        # ):
        #     with open(
        #         os.path.join(cfg.ASSETS_DIR, "fc_names", f"{facade_name}.png"), "rb"
        #     ) as png_file:
        #         png_image = Image(png_file.read())
        #         empty_digital.add_image(
        #             png_image,
        #             position=(x_pos, y_pos),
        #             image_size=(image_width_pt, image_height_pt),
        #         )

        digital_texts = [
            # Lot info
            Text(
                text=suburb,
                **TEXT_DATA["digital"]["lot_info"]["suburb"],
            ),
            Text(text=address, **TEXT_DATA["digital"]["lot_info"]["address"]),
            Text(text=f"LOT {lot}", **TEXT_DATA["digital"]["lot_info"]["lot_number"]),
            Text(
                text=convert_to_syd_time(rego),
                **TEXT_DATA["digital"]["lot_info"]["date"],
            ),
            Text(
                text=f"{land_size}m²", **TEXT_DATA["digital"]["lot_info"]["land_size"]
            ),
            Text(
                text=f"{house_size}m²", **TEXT_DATA["digital"]["lot_info"]["house_size"]
            ),
            Text(text=f"{lot_width}m", **TEXT_DATA["digital"]["lot_info"]["lot_width"]),
            Text(
                text=convert_to_currency(land_price),
                **TEXT_DATA["digital"]["lot_info"]["land_price"],
            ),
            Text(
                text=convert_to_currency(house_price),
                **TEXT_DATA["digital"]["lot_info"]["house_price"],
            ),
            Text(
                text=convert_to_currency(price),
                **TEXT_DATA["digital"]["lot_info"]["package_price"],
            ),
            # Banner text
            Text(
                text="Package Price",
                **TEXT_DATA["digital"]["banner"]["label"],
            ),
            Text(
                text=convert_to_currency(price),
                **TEXT_DATA["digital"]["banner"]["price"],
            ),
            # Floorplan info
            Text(
                text=floorplan_model,
                **TEXT_DATA["digital"]["floorplan_info"]["floorplan_model"],
            ),
            Text(
                text=str(bedroom), **TEXT_DATA["digital"]["floorplan_info"]["bedrooms"]
            ),
            Text(
                text=str(bathroom),
                **TEXT_DATA["digital"]["floorplan_info"]["bathrooms"],
            ),
            Text(
                text=str(parking_slot),
                **TEXT_DATA["digital"]["floorplan_info"]["garages"],
            ),
        ]

        for text in digital_texts:
            empty_digital.add_text(text)

        empty_digital.pdf_file.save(digital_path)
        empty_digital.pdf_file.close()
        return {
            "digital_path": digital_path,
        }

    except Exception as e:
        logging.error(f"Error generating flyer: {str(e)}")
        raise

    finally:
        logging.warning("Cleaning up...")
        if os.path.exists(digital_path):
            # os.remove(digital_path)
            pass
        logging.warning("Cleaned up, task complete")


facade_dict = {
    "Orchid 1": "https://drive.google.com/uc?export=download&id=1YENgJXP0oSmy0hoXkwXqLzLDVCNH7kh9",
    "Orchid 2": "https://drive.google.com/uc?export=download&id=1qfa5X6BiMrcH4PO77hmuJa8vBn2RhAy7",
    "Olive I": "https://drive.google.com/uc?export=download&id=1rMpVBv1Dbh228GZwYRZ73nnmhkLuwliq",
    "Urban I": "https://drive.google.com/uc?id=1kG6dsbgO58PYtQySs3rt2mUCINQSZ0wt&export=download",
    "Urban IV": "https://drive.google.com/uc?export=download&id=1l5gBIm1Zq_5anuZerk5xNhnC71ST1-mM",
    "Urban 6": "https://drive.google.com/uc?export=download&id=1lgXcrY9fB7lpGZIB5kcjUoM00EvEEV59",
    "Urban VIII": "https://drive.google.com/uc?export=download&id=1tY7V7aCHWITPKF1BJuMWWMYiJ-ZSh4jw",
    "Olive II": "https://drive.google.com/uc?export=download&id=1IKFDDKHPrM6BCWcT-g75jHRm7aA7xp1-",
    "Jasmine": "https://drive.google.com/uc?export=download&id=1PJrhCjIqrwpDM5WNQUa7ODs5ZYhp8lQ_",
}

PALM_22 = {
    "url": "https://drive.google.com/uc?id=1vvZZ7b7EFUZ_JsEZxZO2An7cPykDekQV&export=download",
    "name": "PALM 22",
    "rooms": {
        "bedrooms": 5,
        "bathrooms": 3,
        "parkings": 1,
    },
    "dimensions": {"width": 9.1, "depth": 15, "minFrontage": 10},
    "area": 207.1,
    "price": 505000,
}

JASMINE_19_STUDIO = {
    "url": "https://drive.google.com/uc?export=download&id=1b9yxwM3YHT1QPrHf4lqPUP5v-et_d3oE",
    "name": "JASMINE 19 + Studio",
    "rooms": {
        "bedrooms": 5,
        "bathrooms": 4,
        "parkings": 1,
    },
    "dimensions": {"width": 7.01, "depth": 19.49, "minFrontage": 9},
    "area": 199.0,
    "price": 598000,
}

JASMINE_20 = {
    "url": "https://drive.google.com/uc?export=download&id=17ofTwBtjrNpnwY7WYJoO_cxttZmkxWOc",
    "name": "JASMINE 20",
    "rooms": {
        "bedrooms": 4,
        "bathrooms": 3,
        "parkings": 2,
    },
    "dimensions": {"width": 9.1, "depth": 16.5, "minFrontage": 10.9},
    "area": 188.4,
    "price": 506500,
}

JASMINE_20_STUDIO = {
    "url": "https://drive.google.com/uc?export=download&id=1jRAw1fszRVM82ceyYRANDh7eiEkUzeZJ",
    "name": "JASMINE 20 + Studio",
    "rooms": {
        "bedrooms": 5,
        "bathrooms": 3,
        "parkings": 2,
    },
    "dimensions": {"width": 9.1, "depth": 16.5, "minFrontage": 10.9},
    "area": 210.8,
    "price": 571500,
}

PINE_25 = {
    "url": "https://drive.google.com/uc?id=1f43MWHHbH_6jcqErI7rEWYOhGk5M1REl&export=download",
    "name": "PINE 25",
    "rooms": {
        "bedrooms": 5,
        "bathrooms": 4,
        "parkings": 2,
    },
    "dimensions": {"width": 9.1, "depth": 20.3, "minFrontage": 10},
    "area": 227.7,
    "price": 520000,
}

PINE_25_DUEL_KEY_SUNROOM = {
    "url": "https://drive.google.com/uc?export=download&id=1ODZpCdXiztF1gq6eDiU4rP7VNTMAc3Vo",
    "name": "PINE 25 Duel Key + Sunroom",
    "rooms": {
        "bedrooms": 5,
        "bathrooms": 4,
        "parkings": 2,
    },
    "dimensions": {"width": 9.1, "depth": 20.1, "minFrontage": 10.9},
    "area": 237.4,
    "price": 619_000.00,
}

CEDAR_22L = {
    "url": "https://drive.google.com/uc?export=download&id=1hmU7xfZ_lVoC_VBKESQ0PL5iRUqBfL2N",
    "name": "CEDAR 22L",
    "rooms": {
        "bedrooms": 5,
        "bathrooms": 4,
        "parkings": 1,
    },
    "dimensions": {"width": 7.425, "depth": 20.165, "minFrontage": 9.2},
    "area": 213.28,
    "price": 533000,
}

GEMINI_27 = {
    "url": "https://drive.google.com/uc?id=1Z6EOYjCEjqY-1kJPygEpszq5-naxZKw2&export=download",
    "name": "GEMINI 27",
    "rooms": {
        "bedrooms": 6,
        "bathrooms": 4,
        "parkings": 1,
    },
    "dimensions": {"width": 9.1, "depth": 18.61, "minFrontage": 10},
    "area": 248.7,
    "price": 621750,
}

GEMINI_27_STUDIO = {
    "url": "https://drive.google.com/uc?export=download&id=1jRAw1fszRVM82ceyYRANDh7eiEkUzeZJ",
    "name": "GEMINI 27 + Studio",
    "rooms": {
        "bedrooms": 7,
        "bathrooms": 5,
        "parkings": 1,
    },
    "dimensions": {"width": 9.1, "depth": 20.3, "minFrontage": 10},
    "area": 227.7,
    "price": 706750,
}


floorplan = {
    "PALM 22": PALM_22,
    "JASMINE 20": JASMINE_20,
    "JASMINE 20 + Studio": JASMINE_20_STUDIO,
    "PINE 25": PINE_25,
    "CEDAR 22L": CEDAR_22L,
    "GEMINI 27": GEMINI_27,
    "GEMINI 27 + Studio": GEMINI_27_STUDIO,
    "Pine 25 Dual Key + Sunroom": PINE_25_DUEL_KEY_SUNROOM,
    "JASMINE 19 + Studio": JASMINE_19_STUDIO,
}

preston_shared = {
    "suburb": "Preston",
    "project": "Preston Greens",
    "address": "Strathyre Dr",
    "rego": "Registered",
}

import csv

lots = []
with open("land_package_table.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        lots.append(
            (
                {
                    "lotNumber": row["lot_number"],
                    "landSize": row["area"],
                    "landPrice": row["land_cost"],
                    "lotWidth": row["width"],
                    "houseModel": row["house_model"],
                    "priceComparison": row["price_comparison"],
                    "buildingPackage": row["building_package"],
                },
                floorplan[row["house_model"]],
                {
                    "name": row["house_model"],
                    "url": facade_dict[
                        (
                            "Urban 6"
                            if row["house_model"] == "Pine 25 Dual Key + Sunroom"
                            else "Jasmine"
                        )
                    ],
                },
            )
        )


def get_lot_by_lot_number(lot_number, lots):
    for lot in lots:
        if lot["lotNumber"] == lot_number:
            return lot
    return None


def f(lot_number, floorplan_name, facade_name):
    lot = get_lot_by_lot_number(lot_number, lots)
    floorplan_ = floorplan[floorplan_name]
    facade_url = facade_dict[facade_name]
    return (
        lot,
        floorplan_,
        {
            "name": facade_name,
            "url": facade_url,
        },
    )


if __name__ == "__main__":

    shared = {
        "address": "80 Fourteenth Ave",
        "suburb": "Austral",
        "rego": "Registered",
    }

    # for lot in lots:
    #     print(lot)

    for lot, floorplan, facade in lots:
        generate_flyer(
            flyer_id=f"{shared['address']}_{lot['lotNumber']}_{floorplan['name']}_{facade['name']}_${lot['buildingPackage']}",
            facade=facade["name"],
            floorplan_model=floorplan["name"],
            price=lot["buildingPackage"],
            suburb=shared["suburb"],
            address=shared["address"],
            lot=lot["lotNumber"],
            land_price=lot["landPrice"],
            house_price=floorplan["price"],
            land_size=lot["landSize"],
            house_size=floorplan["area"],
            lot_width=lot["lotWidth"],
            rego=shared["rego"],
            bedroom=floorplan["rooms"]["bedrooms"],
            bathroom=floorplan["rooms"]["bathrooms"],
            parking_slot=floorplan["rooms"]["parkings"],
            facade_file_url=facade["url"],
            floorplan_file_url=floorplan["url"],
        )

    # for lot, floorplan, facade in package:
    #     generate_flyer(
    #         flyer_id=f"{shared['address']}_{lot['lotNumber']}_{floorplan['name']}_{facade['name']}_${floorplan["price"] + lot["landPrice"]}",
    #         facade=facade,
    #         floorplan_model=floorplan["name"],
    #         price=floorplan["price"] + lot["landPrice"],
    #         suburb=shared["suburb"],
    #         address=shared["address"],
    #         lot=lot["lotNumber"],
    #         land_price=lot["landPrice"],
    #         house_price=floorplan["price"],
    #         land_size=lot["landSize"],
    #         house_size=floorplan["area"],
    #         lot_width=lot["lotWidth"],
    #         rego=shared["rego"],
    #         bedroom=floorplan["rooms"]["bedrooms"],
    #         bathroom=floorplan["rooms"]["bathrooms"],
    #         parking_slot=floorplan["rooms"]["parkings"],
    #         facade_file_url=facade["url"],
    #         floorplan_file_url=floorplan["url"],
    #     )
