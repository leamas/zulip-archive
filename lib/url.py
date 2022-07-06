"""
Sometimes it feels like 80% of the battle with creating a
static website is getting all the URLs correct.

These are some helpers.

Here are some naming conventions for URL pieces:

    zulip_url: https://example.zulip.com
    site_url: https://example.zulip-archive.com
    html_root: archive

And then URLs use Zulip stream/topics, which are sometimes
"sanitized" to guarantee uniqueness and not have special characters:

    stream_id: 599
    stream_name: general
    topic_name: lunch

    sanitized_stream_name : 599-general
    sanitized_topic_name: lunch
"""

import urllib.parse


def zulip_post_url(zulip_url, stream_id, stream_name, topic_name, post_id):
    """
    https://example.zulipchat.com/#narrow/stream/213222-general/topic/hello/near/179892604
    """
    sanitized = urllib.parse.quote(
        "{0}-{1}/topic/{2}/near/{3}".format(stream_id, stream_name, topic_name, post_id)
    )
    return zulip_url + "#narrow/stream/" + sanitized


def archive_stream_url(site_url, html_root, sanitized_stream_name):
    """
    http://127.0.0.1:4000/archive/stream/213222-general/index.html
    """
    base_url = urllib.parse.urljoin(site_url, html_root)
    return f"{base_url}/stream/{sanitized_stream_name}/index.html"


def archive_topic_url(site_url, html_root, sanitized_stream_name, sanitized_topic_name):
    """
    http://127.0.0.1:4000/archive/stream/213222-general/topic/newstreams.html
    """
    base_url = urllib.parse.urljoin(site_url, html_root)
    return (
        f"{base_url}/stream/{sanitized_stream_name}/topic/{sanitized_topic_name}.html"
    )


def archive_message_url(
    site_url, html_root, sanitized_stream_name, sanitized_topic_name, msg_id
):
    """
    http://127.0.0.1:4000/archive/stream/213222-general/topic/newstreams.html#1234567
    """
    topic_url = archive_topic_url(
        site_url, html_root, sanitized_stream_name, sanitized_topic_name
    )
    return f"{topic_url}#{msg_id}"


## String cleaning functions


def sanitize(s):
    """
    Sanitize the string to a safe string that can be used in URLs

    This is copied from Zulip's core code:
    https://github.com/zulip/zulip/blob/de31114d700561f32139a63a0e5f33d5c30039b3/zerver/lib/url_encoding.py#L8
    """
    return urllib.parse.quote(s, safe=b"").replace(".", "%2E").replace("%", ".")


# create a unique sanitized identifier for a stream
def sanitize_stream(stream_name, stream_id):
    """
    Encode streams for urls as something like 99-Foo-bar.

    This is copied from Zulip's core code:
    https://github.com/zulip/zulip/blob/de31114d700561f32139a63a0e5f33d5c30039b3/zerver/lib/url_encoding.py#L15
    """

    stream_name = stream_name.replace(" ", "-")
    return str(stream_id) + "-" + sanitize(stream_name)
