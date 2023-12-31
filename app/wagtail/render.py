import math

from app.lib import pagination_list
from app.wagtail.api import (
    breadcrumbs,
    page_children,
    page_children_paginated,
    page_details,
)
from flask import current_app, render_template, request


def render_content_page(page_data):
    page_type = page_data["meta"]["type"]
    if page_type == "home.HomePage":
        return home_page(page_data)
    if page_type == "collections.ExplorerIndexPage":
        return explore_index_page(page_data)
    if page_type == "articles.ArticleIndexPage":
        return article_index_page(page_data)
    if page_type == "articles.ArticlePage":
        return article_page(page_data)
    if (
        page_type == "collections.TopicExplorerIndexPage"
        or page_type == "collections.TimePeriodExplorerIndexPage"
    ):
        return category_index_page(page_data)
    if (
        page_type == "collections.TopicExplorerPage"
        or page_type == "collections.TimePeriodExplorerPage"
    ):
        return categories_page(page_data)
    if page_type == "articles.RecordArticlePage":
        return record_article_page(page_data)
    if page_type == "articles.FocusedArticlePage":
        return focused_article_page(page_data)
    if page_type == "collections.HighlightGalleryPage":
        return highlight_gallery_page(page_data)
    if page_type == "authors.AuthorIndexPage":
        return author_index_page(page_data)
    if page_type == "authors.AuthorPage":
        return author_page(page_data)
    current_app.logger.error(f"Template for {page_type} not handled")
    return render_template("errors/page-not-found.html"), 404


def home_page(page_data):
    return render_template(
        "main/home.html",
        page_data=page_data,
    )


def explore_index_page(page_data):
    try:
        large_cards_data = page_data["body"][0]["value"]
        large_card_1 = page_details(large_cards_data["page_1"])
        large_card_2 = page_details(large_cards_data["page_2"])
        featured_article = page_details(page_data["featured_article"]["id"])
        featured_pages = [
            page_details(featured_page_id)
            for featured_page_id in page_data["featured_articles"][0]["value"][
                "items"
            ]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    except Exception:
        return render_template("errors/page-not-found.html"), 404
    large_cards = [
        {
            "href": card["meta"]["html_url"],
            "src": card["teaser_image_jpg"]["full_url"],
            "alt": card["teaser_image_jpg"]["alt"],
            "width": card["teaser_image_jpg"]["width"],
            "height": card["teaser_image_jpg"]["height"],
            "title": card["title"],
        }
        for card in [large_card_1, large_card_2]
    ]
    return render_template(
        "explore/index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        large_cards=large_cards,
        featured_article=featured_article,
        featured_pages=featured_pages,
    )


def category_index_page(page_data):
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
    return render_template(
        "explore/category-index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        children=children,
    )


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


def article_index_page(page_data):
    children_per_page = 12
    page = int(request.args.get("page")) if "page" in request.args else 1
    try:
        children_data = page_children_paginated(
            page_data["id"], page, children_per_page
        )
    except ConnectionError:
        return render_template("errors/api.html"), 502
    pages = math.ceil(children_data["meta"]["total_count"] / children_per_page)
    if page > pages:
        return render_template("errors/page-not-found.html"), 404
    try:
        children = [
            page_details(child["id"]) for child in children_data["items"]
        ]
        featured_article = page_details(page_data["featured_article"]["id"])
        featured_pages = [
            page_details(featured_page_id)
            for featured_page_id in page_data["featured_pages"][0]["value"][
                "items"
            ]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    return render_template(
        "explore/stories.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        children=children,
        featured_article=featured_article,
        featured_pages=featured_pages,
        pagination_list=pagination_list(page, pages, 1, 1),
        page=page,
        pages=pages,
    )


def article_page(page_data):
    try:
        similar_items = [
            page_details(page["id"]) for page in page_data["similar_items"]
        ]
        latest_items = [
            page_details(page["id"]) for page in page_data["latest_items"]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    return render_template(
        "explore/article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        similar_items=similar_items,
        latest_items=latest_items,
    )


def record_article_page(page_data):
    return render_template(
        "explore/record-article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )


def focused_article_page(page_data):
    try:
        authors = (
            [page_details(author["author"]) for author in page_data["authors"]]
            if page_data["authors"]
            else []
        )
    except ConnectionError:
        return render_template("errors/api.html"), 502
    return render_template(
        "explore/focused-article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        authors=authors,
    )


def highlight_gallery_page(page_data):
    return render_template(
        "explore/highlight-gallery.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )


def author_index_page(page_data):
    try:
        children_data = page_children(page_data["id"])
        children = [
            page_details(child["id"]) for child in children_data["items"]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    return render_template(
        "authors/index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        children=children,
        page_data=page_data,
    )


def author_page(page_data):
    authored_focused_articles = []
    try:
        authored_focused_articles = [
            page_details(child["id"])
            for child in page_data["authored_focused_articles"]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    return render_template(
        "authors/details.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        authored_focused_articles=authored_focused_articles,
    )
