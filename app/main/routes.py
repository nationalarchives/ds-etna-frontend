from urllib.parse import urlparse

from app.lib import cache, cache_key_prefix
from app.main import bp
from app.wagtail.api import all_pages, global_alerts
from flask import current_app, make_response, render_template, request


@bp.route("/browse/")
# @cache.cached(key_prefix=cache_key_prefix)
def browse():
    return render_template("main/browse.html", global_alerts=global_alerts())


@bp.route("/healthcheck/live/")
def healthcheck():
    return "ok"


@bp.route("/service-worker.min.js")
def service_worker():
    return current_app.send_static_file("service-worker.min.js")


@bp.route("/sitemap.xml")
@cache.cached(timeout=3600)
def sitemap():
    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc
    static_urls = list()
    for rule in current_app.url_map.iter_rules():
        if (
            not str(rule).startswith("/preview")
            and not str(rule).startswith("/healthcheck")
            and not str(rule).startswith("/sitemap.xml")
            and not str(rule).startswith("/service-worker.min.js")
        ):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                url = {"loc": f"{host_base}{str(rule)}"}
                static_urls.append(url)
    dynamic_urls = list()
    page_batch = 0
    wagtail_pages_count = 1
    wagtail_pages_added = 0
    while wagtail_pages_added < wagtail_pages_count:
        page_batch = page_batch + 1
        wagtail_pages = all_pages(batch=page_batch)
        wagtail_pages_count = wagtail_pages["meta"]["total_count"]
        for page in wagtail_pages["items"]:
            html_url = page["full_url"]
            if not any(
                static_url["loc"] == html_url for static_url in static_urls
            ):
                url = {
                    "loc": html_url,
                    # "lastmod": post.date_published.strftime("%Y-%m-%dT%H:%M:%SZ")
                }
                dynamic_urls.append(url)
        wagtail_pages_added = wagtail_pages_added + len(wagtail_pages["items"])
    xml_sitemap = render_template(
        "main/sitemap.xml",
        static_urls=static_urls,
        dynamic_urls=dynamic_urls,
        host_base=host_base,
    )
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"
    return response


@bp.route("/new-homepage/")
# @cache.cached(key_prefix=cache_key_prefix)
def new_homepage():
    return render_template("main/new_home.html")
