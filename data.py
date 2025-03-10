from models import Font

TEXT_DATA = {
    "digital": {
        "lot_info": {
            "suburb": {
                "size": 27,
                "position": (58.88, 513.90),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "address": {
                "size": 14,
                "position": (60.5, 541.3),
                "font": Font.INTER_REGULAR,
                "color": (1, 1, 1),
            },
            "lot_number": {
                "size": 9,
                "position": (300.5, 503),
                "font": Font.INTER_SEMIBOLD,
                "color": (1, 1, 1),
                "align": "center",
            },
            "date": {
                "size": 10,
                "position": (267, 544),
                "font": Font.INTER_LIGHT,
                "color": (1, 1, 1),
            },
            "land_size": {
                "size": 10,
                "position": (499, 500.3),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "house_size": {
                "size": 10,
                "position": (510, 522.9),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "lot_width": {
                "size": 10,
                "position": (502.4, 545.2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "land_price": {
                "size": 10,
                "position": (698, 500.0),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "house_price": {
                "size": 10,
                "position": (704.3, 522.4),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "package_price": {
                "size": 10,
                "position": (714.2, 545.0),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
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
    "print": {
        "lot_info": {
            "suburb": {
                "size": 27,
                "position": (37.14, 513.90 - 2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "address": {
                "size": 14,
                "position": (38.16, 541.3 - 2),
                "font": Font.INTER_REGULAR,
                "color": (1, 1, 1),
            },
            "lot_number": {
                "size": 9,
                "position": (300.5 - 38, 503 - 2),
                "font": Font.INTER_SEMIBOLD,
                "color": (1, 1, 1),
                "align": "center",
            },
            "date": {
                "size": 10,
                "position": (267 - 38, 544 - 2),
                "font": Font.INTER_LIGHT,
                "color": (1, 1, 1),
            },
            "land_size": {
                "size": 10,
                "position": (499 - 63.80, 500.3 - 2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "house_size": {
                "size": 10,
                "position": (510 - 63.80, 522.9 - 2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "lot_width": {
                "size": 10,
                "position": (502.4 - 63.80, 545.2 - 2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "land_price": {
                "size": 10,
                "position": (698 - 115.8, 500.0 - 2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "house_price": {
                "size": 10,
                "position": (704.3 - 115.8, 522.4 - 2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "package_price": {
                "size": 10,
                "position": (714.2 - 115.8, 545.0 - 2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "bedrooms": {
                "size": 10,
                "position": (780.2 - 2, 500.0 - 2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "bathrooms": {
                "size": 10,
                "position": (780.2, 523.4 - 2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "garages": {
                "size": 10,
                "position": (780.2 - 9, 545.5 - 2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
        },
        "banner": {
            "label": {
                "size": 17,
                "position": (841.8900146484375 - 179.2 + 38, 67.2),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
            "price": {
                "size": 17,
                "position": (841.8900146484375 - 179.2 + 38, 88.0),
                "font": Font.INTER_BOLD,
                "color": (1, 1, 1),
            },
        },
        "floorplan_info": {
            "floorplan_model": {
                "size": 15,
                "position": (589.5, 80.7),
                "font": Font.INTER_BOLD,
                "color": (0, 0, 0),
            },
            "bedrooms": {
                "size": 13,
                "position": (617.8, 125),
                "font": Font.INTER_REGULAR,
                "color": (0, 0, 0),
            },
            "bathrooms": {
                "size": 13,
                "position": (702.55, 125),
                "font": Font.INTER_REGULAR,
                "color": (0, 0, 0),
            },
            "garages": {
                "size": 13,
                "position": (786.9, 125),
                "font": Font.INTER_REGULAR,
                "color": (0, 0, 0),
            },
        },
    },
}
