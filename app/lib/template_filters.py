import re
from datetime import datetime


def tna_html(s):
    return s.replace("<ul>", '<ul class="tna-ul">').replace(
        "<ol>", '<ol class="tna-ol">'
    )


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def pretty_date(s):
    date = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    new_date = date.strftime("%d %B %Y")
    return new_date


def article_supertitle(s):
    if s == "articles.ArticlePage":
        return "The story of"
    if s == "articles.FocusedArticlePage":
        return "Focus on"
    if s == "articles.RecordArticlePage":
        return "Record revealed"
    return ""


def article_type(s):
    if s == "articles.ArticlePage" or s == "articles.FocusedArticlePage":
        return "Article"
    if s == "articles.RecordArticlePage":
        return "Records revealed"
    if s == "collections.HighlightGalleryPage":
        return "Gallery"
    if s == "collections.TimePeriodExplorerPage":
        return "Time period"
    if s == "collections.TopicExplorerPage":
        return "Topic"
    return ""


def brand_icon_from_url(s):
    if "facebook.com" in s:
        return "facebook"
    if "youtube.com" in s:
        return "youtube"
    return ""


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
