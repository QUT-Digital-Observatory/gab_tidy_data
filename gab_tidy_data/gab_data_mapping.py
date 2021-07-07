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
from typing import Tuple, Dict, List

logger = getLogger(__name__)

data_table_names = [
    'gab',
    'account',
    'group',
    'media_attachment',
    'gab_mention',
    'gab_media_attachment',
    'gab_tag'
]


def map_account_for_insert(gab_id, account_json) -> List[Tuple[str, Dict]]:
    """
    Takes JSON object for the gab user account, and the Gab ID of the Gab this user
    account information was fetched with, and returns an SQL insert statement, ready
    to be executed.

    If any field names need to be changed or special field parsing needs to be done
    to map the account information from the Gab JSON to the database table, this is
    where to do it.
    """
    field_mapping = {  # comments indicate SQLite column type
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
        "posted_gab_id": gab_id,  # text
    }

    return [("""
        insert or replace into account (
            id, username, acct, display_name,
            locked, bot,
            created_at,
            note, url, avatar, avatar_static, header, header_static,
            is_spam,
            followers_count, following_count, statuses_count,
            is_pro, is_verified, is_donor, is_investor,
            posted_gab_id
        )
        values (
            :id, :username, :acct, :display_name,
            :locked, :bot,
            :created_at,
            :note, :url, :avatar, :avatar_static, :header, :header_static,
            :is_spam,
            :followers_count, :following_count, :statuses_count,
            :is_pro, :is_verified, :is_donor, :is_investor,
            :posted_gab_id
        )
    """, field_mapping)]


def map_group_for_insert(gab_id, group_json) -> List[Tuple[str, Dict]]:
    field_mapping = {
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
        "posted_gab_id": gab_id,  # text
    }

    return [("""
        insert or replace into gab_group (
            id, title, slug, url
            description, description_html, cover_image_url,
            is_archived, is_private, is_visible
            member_count,
            created_at,
            has_password,
            posted_gab_id
        ) values (
            :id, :title, :slug, :url
            :description, :description_html, :cover_image_url,
            :is_archived, :is_private, :is_visible
            :member_count,
            :created_at,
            :has_password,
            :posted_gab_id
        )
    """, field_mapping)]


def map_media_for_insert(gab_id, media_json) -> List[Tuple[str, Dict]]:
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
        "gab_media_attachment_id": media_json["id"]  # text
    }
    return [("""
        insert or replace into media_attachment (
            id,
            type, file_content_type
            url, preview_url, source_mp4, remote_url, text_url,
            description,
            blurhash
        ) values (
            :id,
            :type, :file_content_type
            :url, :preview_url, :source_mp4, :remote_url, :text_url,
            :description,
            :blurhash
        )
    """, media_field_mapping),
            ("""
        insert or ignore into gab_media_attachment (
            gab_id,
            media_attachment_id
        ) values (
            :gab_id,
            :media_attachment_id
        )
    """, gab_media_relationship_mapping)]


def map_gab_tag_for_insert(gab_id, tag_json):
    pass


def map_gab_for_insert(gab_id, gab_json) -> List[Tuple[str, Dict]]:
    """
    As the top-level json, object, this function will call all other mapping functions.
    """
    field_mapping = {

    }