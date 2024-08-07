from app.wagtail.api import breadcrumbs, page_children
from flask import current_app, render_template


def people_index_page(page_data):
    try:
        children = page_children(
            page_data["id"],
            {
                "type": "people.PersonPage",
                "fields": "_,title,teaser_image,role,html_url",
                "order": "title",
            },
        )
    except ConnectionError:
        current_app.logger.error(
            f"API error getting children for page {page_data['id']}"
        )
        return render_template("errors/api.html"), 502
    except Exception:
        current_app.logger.error(
            f"Exception getting children for page {page_data['id']}"
        )
        return render_template("errors/server.html"), 500
    return render_template(
        "people/index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        children=children["items"],
        page_data=page_data,
    )
