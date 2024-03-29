from app.wagtail.api import breadcrumbs, page_children, page_details
from flask import render_template


def categories_page(page_data):
    try:
        children_data = page_children(page_data["id"])
        all_children = [
            page_details(child["id"]) for child in children_data["items"]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    children = [
        {
            "id": child["id"],
            "title": child["title"],
            "url": child["meta"]["html_url"],
            "teaser": child["teaser_text"],
            "image": child["teaser_image_jpg"],
        }
        for child in all_children
    ]
    children_index_grid = [
        {
            "id": child["id"],
            "title": child["title"],
            "subtitle": str(len(child["page_highlights"])) + " images",
            "href": child["meta"]["html_url"],
            "teaser": child["teaser_text"],
            "src": child["teaser_image_jpg"]["full_url"],
            "alt": child["teaser_image_jpg"]["alt"],
            "width": child["teaser_image_jpg"]["width"],
            "height": child["teaser_image_jpg"]["height"],
        }
        for child in all_children
    ]
    return render_template(
        "explore/category.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        children=children,
        children_index_grid=children_index_grid,
    )
