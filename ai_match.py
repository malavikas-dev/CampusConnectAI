from models import (
    get_all_lost_items,
    add_notification
)

def check_matches(lost_item, found_items):

    matches = []

    for item in found_items:

        score = 0


        # Category matching
        if lost_item["category"].lower() == item["category"].lower():
            score += 40


        # Location matching
        if lost_item["location"].lower() == item["location"].lower():
            score += 20


        # Item name matching
        lost_name = lost_item["item_name"].lower()
        found_name = item["item_name"].lower()

        if lost_name in found_name or found_name in lost_name:
            score += 30


        # Date matching
        if lost_item["date"] == item["date"]:
            score += 10



        if score >= 40:

            matches.append({
                "item": item,
                "score": score
            })


    matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return matches