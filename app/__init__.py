import re

from app.lib import cache, image_details, media_details, page_details
from config import Config, config
from flask import Flask
from jinja2 import ChoiceLoader, PackageLoader


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)

    cache.init_app(app)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PackageLoader("tna_frontend_jinja"),
        ]
    )

    @app.template_filter("tna_html")
    def tna_html_filter(s):
        return s.replace("<ul>", '<ul class="tna-ul">').replace(
            "<ol>", '<ol class="tna-ol">'
        )

    @app.template_filter("slugify")
    def slugify(s):
        s = s.lower().strip()
        s = re.sub(r"[^\w\s-]", "", s)
        s = re.sub(r"[\s_-]+", "-", s)
        s = re.sub(r"^-+|-+$", "", s)
        return s

    @app.template_filter("article_supertitle")
    def article_supertitle(s):
        if s == "articles.ArticlePage":
            return "The story of"
        if s == "articles.FocusedArticlePage":
            return "Focus on"
        if s == "articles.RecordArticlePage":
            return "Record revealed"
        return ""

    @app.template_filter("brand_icon_from_url")
    def brand_icon_from_url(s):
        if "facebook.com" in s:
            return "facebook"
        if "youtube.com" in s:
            return "youtube"
        return ""

    @app.template_filter("headings_list")
    def headings_list(s):
        headings_raw = re.findall(
            r'<h([1-6])[^>]*id="([\w\-]+)"[^>]*>\s*([\w\s\.]+)\s*<', s
        )
        headings = [
            {
                "title": heading[2],
                "id": heading[1],
                "level": heading[0],
                "children": [],
            }
            for heading in headings_raw
        ]
        return headings

    @app.context_processor
    def cms_processor():
        def get_wagtail_image(image_id):
            image_data = image_details(image_id)
            return image_data

        def get_wagtail_page(page_id):
            page_data = page_details(page_id)
            return page_data

        def get_wagtail_media(media_id):
            media_data = media_details(media_id)
            return media_data

        return dict(
            get_wagtail_image=get_wagtail_image,
            get_wagtail_page=get_wagtail_page,
            get_wagtail_media=get_wagtail_media,
            WAGTAIL_MEDIA_URL=config["WAGTAIL_MEDIA_URL"],
        )

    from .explore import bp as explore_bp
    from .main import bp as site_bp
    from .wagtail import bp as wagtail_bp

    app.register_blueprint(site_bp)
    app.register_blueprint(explore_bp, url_prefix="/explore-the-collection")
    app.register_blueprint(wagtail_bp)

    return app
