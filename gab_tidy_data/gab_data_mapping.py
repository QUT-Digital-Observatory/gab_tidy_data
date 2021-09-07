"""
Gab data mapping

This file contains the mappings from the Gab JSON to the relational data structure
used in this tool. It should be viewed and edited alongside gab_schema.sql, which
contains the SQL statements to create the tables.

There is a function to map each Gab data entity from the relevant JSON object to the
relevant table(s). These functions provide appropriate SQL insert statements and mapped
data to use with those insert statements, but do not execute those statements - this
should be done by the calling function.

Within each function, there is a data mapping dictionary for each table which that
function maps to. The keys (left-hand-side) of the dictionary are the column names
(this must correspond to the named parameters in the relevant SQL insert statement),
and the values (right-hand-side) are how that field can be found, parsed, calculated etc
from the JSON.

This file and the mapping functions are structured this way in order to make it as easy
as possible to create and modify the json->relational mapping and minimise human error
in doing so.

The SQL queries should specify what should happen on primary key conflict.
"""

from logging import getLogger
from typing import Dict, List, Any

logger = getLogger(__name__)


# Database schema version - must be consistent with gab_schema.sql
schema_version = "2021-08-30"


# Tables are ordered by how data should be inserted if foreign key integrity were to be
# enforced
data_table_names = [
    "emoji",
    "account",
    "account_fields",
    "account_emoji",
    "group_category",
    "gab_group",
    "group_tag",
    "media_attachment",
    "card",
    "gab",
    "gab_mention",
    "gab_media_attachment",
    "gab_tag",
    "gab_emoji",
]
insert_sql = dict()


# -------------------
# ---    Emoji    ---
# -------------------
insert_sql[
    "emoji"
] = """
    insert or ignore into emoji (
        shortcode,
        url, static_url
    ) values (
        :shortcode,
        :url, :static_url
    )
"""


def map_emoji_list_for_insert(emoji_json) -> Dict[str, List[Dict]]:
    mapped = [
        {
            "shortcode": emoji["shortcode"],
            "url": emoji["url"],
            "static_url": emoji["static_url"],
        }
        for emoji in emoji_json
    ]
    return {"emoji": mapped}


# -------------------
# ---   Account   ---
# -------------------

insert_sql[
    "account"
] = """
    insert or replace into account (
        id, username, acct, display_name,
        locked, bot,
        created_at,
        note, url, avatar, avatar_static, header, header_static,
        is_spam,
        followers_count, following_count, statuses_count,
        is_pro, is_verified, is_donor, is_investor,
        _file_id
    )
    values (
        :id, :username, :acct, :display_name,
        :locked, :bot,
        :created_at,
        :note, :url, :avatar, :avatar_static, :header, :header_static,
        :is_spam,
        :followers_count, :following_count, :statuses_count,
        :is_pro, :is_verified, :is_donor, :is_investor,
        :_file_id
    )
"""
insert_sql[
    "account_emoji"
] = """
    insert or ignore into account_emoji (
        account_id, _file_id,
        emoji_shortcode
    ) values (
        :account_id, :_file_id,
        :emoji_shortcode
    )
"""
insert_sql[
    "account_fields"
] = """
    insert or ignore into account_fields (
        account_id, _file_id,
        ordering,
        name, value,
        verified_at
    ) values (
        :account_id, :_file_id,
        :ordering,
        :name, :value,
        :verified_at
    )
"""


def map_account_for_insert(file_id, gab_id, account_json) -> Dict[str, List[Dict]]:
    """
    Takes JSON object for the gab user account, and the Gab ID of the Gab this user
    account information was fetched with, and returns an SQL insert statement, ready
    to be executed.

    If any field names need to be changed or special field parsing needs to be done
    to map the account information from the Gab JSON to the database table, this is
    where to do it.
    """
    account = {  # comments indicate SQLite column type
        "id": account_json["id"],  # text
        "username": account_json["username"],  # text
        "acct": account_json["acct"],  # text
        "display_name": account_json["display_name"],  # text
        "locked": account_json["locked"],  # integer (boolean)
        "bot": account_json["bot"],  # integer (boolean)
        "created_at": account_json["created_at"],  # text (ISO datetime)
        "note": account_json["note"],  # text
        "url": account_json["url"],  # text
        "avatar": account_json["avatar"],  # text
        "avatar_static": account_json["avatar_static"],  # text
        "header": account_json["header"],  # text
        "header_static": account_json["header_static"],  # text
        "is_spam": account_json["is_spam"],  # integer (boolean)
        "followers_count": account_json["followers_count"],  # integer
        "following_count": account_json["following_count"],  # integer
        "statuses_count": account_json["statuses_count"],  # integer
        "is_pro": account_json["is_pro"],  # integer (boolean)
        "is_verified": account_json["is_verified"],  # integer (boolean)
        "is_donor": account_json["is_donor"],  # integer (boolean)
        "is_investor": account_json["is_investor"],  # integer (boolean)
        "_file_id": file_id,
    }

    account_fields = []
    for i, field in enumerate(account_json["fields"], start=1):
        account_fields.append(
            {
                "account_id": account["id"],
                "_file_id": file_id,
                "ordering": i,
                "name": field["name"],
                "value": field["value"],
                "verified_at": field["verified_at"],
            }
        )

    emoji = map_emoji_list_for_insert(account_json["emojis"])["emoji"]
    account_emoji = []
    for e in emoji:
        account_emoji.append(
            {
                "account_id": account["id"],
                "_file_id": file_id,
                "emoji_shortcode": e["shortcode"],
            }
        )

    return {
        "account": [account],
        "emoji": emoji,
        "account_emoji": account_emoji,
        "account_fields": account_fields,
    }


# -------------------
# ---    Group    ---
# -------------------

insert_sql[
    "gab_group"
] = """
    insert or replace into gab_group (
        id, title, slug, url,
        description, description_html, cover_image_url,
        group_category,
        is_archived, is_private, is_visible,
        member_count,
        created_at,
        has_password,
        _file_id
    ) values (
        :id, :title, :slug, :url,
        :description, :description_html, :cover_image_url,
        :group_category,
        :is_archived, :is_private, :is_visible,
        :member_count,
        :created_at,
        :has_password,
        :_file_id
    )
"""
insert_sql[
    "group_tag"
] = """
    insert or ignore into group_tag (
        group_id, _file_id,
        tag
    ) values (
        :group_id, :_file_id,
        :tag
    )
"""
insert_sql[
    "group_category"
] = """
    insert or ignore into group_category (
        id,
        created_at, updated_at,
        text
    ) values (
        :id,
        :created_at, :updated_at,
        :text
    )
"""


def map_group_category_for_insert(category_json) -> Dict[str, List[Dict]]:
    category = {
        "id": category_json["id"],  # integer
        "created_at": category_json["created_at"],  # text
        "updated_at": category_json["updated_at"],  # text
        "text": category_json["text"],  # text
    }
    return {"group_category": [category]}


def map_group_for_insert(file_id, group_json) -> Dict[str, List[Dict]]:
    group = {
        "id": group_json["id"],  # text
        "title": group_json["title"],  # text
        "description": group_json["description"],  # text
        "description_html": group_json["description_html"],  # text
        "cover_image_url": group_json["cover_image_url"],  # text
        "is_archived": group_json["is_archived"],  # integer (boolean)
        "member_count": group_json["member_count"],  # integer
        "created_at": group_json["created_at"],  # text
        "is_private": group_json["is_private"],  # integer (boolean)
        "is_visible": group_json["is_visible"],  # integer (boolean)
        "slug": group_json["slug"],  # text
        "url": group_json["url"],  # text
        "has_password": group_json["has_password"],  # integer (boolean)
        "group_category": None,  # integer - filled out below
        "_file_id": file_id,  # text
    }

    if group_json["tags"] is not None:
        tags = [
            {"group_id": group["id"], "_file_id": file_id, "tag": tag}
            for tag in group_json["tags"]
        ]
    else:
        tags = []

    category_json = group_json["group_category"]

    if category_json is not None:
        category = map_group_category_for_insert(category_json)["group_category"]
        group["group_category"] = category[0]["id"]
    else:
        category = []

    return {"group_category": category, "gab_group": [group], "group_tag": tags}


# ------------------------
# --- Media Attachment ---
# ------------------------

insert_sql[
    "media_attachment"
] = """
    insert or replace into media_attachment (
        id,
        type, file_content_type,
        url, preview_url, source_mp4, remote_url, text_url,
        description,
        blurhash
    ) values (
        :id,
        :type, :file_content_type,
        :url, :preview_url, :source_mp4, :remote_url, :text_url,
        :description,
        :blurhash
    )
"""
insert_sql[
    "gab_media_attachment"
] = """
    insert or ignore into gab_media_attachment (
        gab_id,
        media_attachment_id
    ) values (
        :gab_id,
        :media_attachment_id
    )
"""


def map_media_for_insert(gab_id, media_json) -> Dict[str, List[Dict]]:
    media_field_mapping = {
        "id": media_json["id"],  # text
        "type": media_json["type"],  # text
        "url": media_json["url"],  # text
        "preview_url": media_json["preview_url"],  # text
        "source_mp4": media_json["source_mp4"],  # text
        "remote_url": media_json["remote_url"],  # text
        "text_url": media_json["text_url"],  # text
        "description": media_json["description"],  # text
        "blurhash": media_json["blurhash"],  # text
        "file_content_type": media_json["file_content_type"],  # text
    }
    gab_media_relationship_mapping = {
        "gab_id": gab_id,  # text
        "media_attachment_id": media_json["id"],  # text
    }
    return {
        "media_attachment": [media_field_mapping],
        "gab_media_attachment": [gab_media_relationship_mapping],
    }


# -------------------
# ---     Tag     ---
# -------------------
insert_sql[
    "gab_tag"
] = """
insert or ignore into gab_tag (
    gab_id,
    name, url
) values (
    :gab_id,
    :name, :url
)
"""


def map_gab_tags_for_insert(gab_id, tags_json) -> Dict[str, List[Dict]]:
    tags = []
    for t in tags_json:
        tags.append(
            {
                "gab_id": gab_id,  # text
                "name": t["name"],  # text
                "url": t["url"],  # text
            }
        )

    return {"gab_tag": tags}


# -------------------
# ---    Card     ---
# -------------------
insert_sql[
    "card"
] = """
insert or ignore into card (
    id, url, title,
    description,
    type,
    provider_name, provider_url,
    html,
    image_url, embed_url,
    updated_at
) values (
    :id, :url, :title,
    :description,
    :type,
    :provider_name, :provider_url,
    :html,
    :image_url, :embed_url,
    :updated_at
)
"""


def map_card_for_insert(card_json) -> Dict[str, List[Dict]]:
    card = {
        "id": card_json["id"],  # text
        "url": card_json["url"],  # text
        "title": card_json["title"],  # text
        "description": card_json["description"],  # text
        "type": card_json["type"],  # text
        "provider_name": card_json["provider_name"],  # text
        "provider_url": card_json["provider_url"],  # text
        "html": card_json["html"],  # text
        "image_url": card_json["image"],  # text
        "embed_url": card_json["embed_url"],  # text
        "updated_at": card_json["updated_at"],  # text
    }

    return {"card": [card]}


# -------------------
# ---     Gab     ---
# -------------------

# missing reblog, mention_user_ids, mention_usernames
insert_sql[
    "gab"
] = """
insert or replace into gab (
    id,
    created_at, revised_at, expires_at,
    in_reply_to_id, in_reply_to_account_id,
    sensitive, spoiler_text, visibility,
    language,
    uri, url,
    replies_count, reblogs_count, favourites_count,
    pinnable, pinnable_by_group,
    quote_of_id, has_quote,
    reblog,
    content, rich_content, plain_markdown,
    account_id, group_id, card_id,
    _embedded_gab,
    _file_id
) values (
    :id,
    :created_at, :revised_at, :expires_at,
    :in_reply_to_id, :in_reply_to_account_id,
    :sensitive, :spoiler_text, :visibility,
    :language,
    :uri, :url,
    :replies_count, :reblogs_count, :favourites_count,
    :pinnable, :pinnable_by_group,
    :quote_of_id, :has_quote,
    :reblog,
    :content, :rich_content, :plain_markdown,
    :account_id, :group_id, :card_id,
    :_embedded_gab,
    :_file_id
)
"""
insert_sql[
    "gab_mention"
] = """
insert or ignore into gab_mention (
    gab_id, account_id,
    url, acct
) values (
    :gab_id, :account_id,
    :url, :acct
)
"""
insert_sql[
    "gab_emoji"
] = """
insert or ignore into gab_emoji (
    gab_id, emoji_shortcode
) values (
    :gab_id, :emoji_shortcode
)
"""


def add_mappings(to_extend: Dict[Any, List], addition: Dict[Any, List]):
    """
    Appends all the mappings for each table from `addition` into `to_extend`.
    Expects all keys in `addition` to already exist in `to_extend`.
    """
    for table in addition.keys():
        to_extend[table].extend(addition[table])


def map_mentions_for_insert(gab_id, mentions_json) -> Dict[str, list]:
    mentions = []
    for mention in mentions_json or []:
        mentions.append(
            {
                "gab_id": gab_id,
                "account_id": mention["id"],  # text
                "url": mention["url"],  # text
                "acct": mention["acct"],  # text
            }
        )
    return {"gab_mention": mentions}


def map_gab_for_insert(file_id, gab_json, embedded_gab=False) -> Dict[str, list]:
    """
    As the top-level json, object, this function will call all other mapping functions.
    This may include map_gab_for_insert itself where gabs are embedded (e.g. quotes)
    """
    gab_id = gab_json["id"]

    # Dict *ought* to retain key order - needed for foreign key integrity (if used)
    mappings = {t: [] for t in data_table_names}

    # Account
    account_mappings = map_account_for_insert(file_id, gab_id, gab_json["account"])
    account_id = account_mappings["account"][0]["id"]
    add_mappings(mappings, account_mappings)

    # Group
    if gab_json["group"] is not None:
        group_mappings = map_group_for_insert(file_id, gab_json["group"])
        group_id = group_mappings["gab_group"][0]["id"]
        add_mappings(mappings, group_mappings)
    else:
        group_id = None

    # Media attachments
    for media_json in gab_json["media_attachments"]:
        media_mappings = map_media_for_insert(gab_id, media_json)
        for table, mapping_list in media_mappings.items():
            mappings[table].extend(mapping_list)

    # Tags
    add_mappings(mappings, map_gab_tags_for_insert(gab_id, gab_json["tags"]))

    # Mentions
    add_mappings(mappings, map_mentions_for_insert(gab_id, gab_json["mentions"]))

    # Emoji
    emoji = map_emoji_list_for_insert(gab_json["emojis"])
    gab_emoji = []
    for e in emoji["emoji"]:
        gab_emoji.append({"gab_id": gab_id, "emoji_shortcode": e["shortcode"]})
    add_mappings(mappings, emoji)
    add_mappings(mappings, {"gab_emoji": gab_emoji})

    # Card
    if gab_json["card"] is not None:
        card = map_card_for_insert(gab_json["card"])
        add_mappings(mappings, card)
        card_id = card["card"][0]["id"]
    else:
        card_id = None

    # Gab attributes
    mappings["gab"].append(
        {
            "id": gab_id,  # text
            "created_at": gab_json["created_at"],  # text
            "revised_at": gab_json["revised_at"],  # text
            "in_reply_to_id": gab_json["in_reply_to_id"],  # text
            "in_reply_to_account_id": gab_json["in_reply_to_account_id"],  # text
            "sensitive": gab_json["sensitive"],  # integer (boolean)
            "spoiler_text": gab_json["spoiler_text"],  # text
            "visibility": gab_json["visibility"],  # text
            "language": gab_json["language"],  # text
            "uri": gab_json["uri"],  # text
            "url": gab_json["url"],  # text
            "replies_count": gab_json["replies_count"],  # integer
            "reblogs_count": gab_json["reblogs_count"],  # integer
            "pinnable": gab_json["pinnable"],  # integer (boolean)
            "pinnable_by_group": gab_json["pinnable_by_group"],  # integer (boolean)
            "favourites_count": gab_json["favourites_count"],  # integer
            "quote_of_id": gab_json["quote_of_id"],  # text
            "expires_at": gab_json["expires_at"],  # text
            "has_quote": gab_json["has_quote"],  # integer (boolean)
            "content": gab_json["content"],  # text
            "rich_content": gab_json["rich_content"],  # text
            "plain_markdown": gab_json["plain_markdown"],  # text
            "reblog": gab_json[
                "reblog"
            ],  # text - may need to be parsed as embedded gab
            "account_id": account_id,  # text
            "group_id": group_id,  # text
            "card_id": card_id,  # text
            "_embedded_gab": embedded_gab,  # integer (boolean)
            "_file_id": file_id,  # integer
        }
    )

    embedded_gabs = []

    # process quotes
    if gab_json["quote"] is not None:
        embedded_gabs.append(
            map_gab_for_insert(file_id, gab_json["quote"], embedded_gab=True)
        )

    # Merge embedded gabs in with this gab!
    merged_mappings = {t: [] for t in data_table_names}

    # This gab goes last after any embedded gabs
    for mapped_gab in embedded_gabs + [mappings]:
        add_mappings(merged_mappings, mapped_gab)

    return merged_mappings
