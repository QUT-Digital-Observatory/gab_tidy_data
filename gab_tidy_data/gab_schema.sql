create table account (
    id text primary key, -- Gab-provided user id
    username text not null,
    acct text,
    display_name text,
    locked integer, -- boolean
    bot integer, -- boolean
    created_at text, -- Unparsed ISO datetime
    created_at_parsed real, -- created_at in julianday format
    note text,
    url text,
    avatar text,
    avatar_static text,
    header text,
    header_static text,
    is_spam integer, -- boolean
    followers_count integer,
    following_count integer,
    statuses_count integer,
    is_pro integer, -- boolean
    is_verified integer, -- boolean
    is_donor integer, -- boolean
    is_investor integer, --boolean,

)
-- fields TODO:
-- - emojis
-- - fields


create table group (
) -- TODO


create table media_attachment (
    id text primary key,
    type text not null,
    url text not null,
    preview_url text,
    source_mp4 text,
    remote_url text,
    text_url text,
    description text,
    blurhash text,
    file_content_type text
)
-- Fields omitted:
-- - meta object containing media dimensions etc


create table gab (
    id text primary key, -- Gab-provided id
    created_at text not null, -- Unparsed text - appears to be in ISO format
    created_at_parsed real, -- created_at in julianday format
    revised_at text, -- Unparsed text
    revised_at_parsed real, -- revised_at in julianday format
    in_reply_to_id text,
    in_reply_to_account_id text,
    sensitive integer, -- boolean
    spoiler_text text,
    visibility text,
    language text,
    uri text,
    url text,
    replies_count integer,
    reblogs_count integer,
    pinnable integer, -- boolean
    pinnable_by_group integer, -- boolean
    favourites_count integer,
    quote_of_id text,
    expires_at ???,
    has_quote ???,
    content text, -- HTML text of gab
    rich_content text, -- Not sure how different from content?
    plain_markdown text,
    -- reblog
    account_id text references account (id),
    group_id text references group (id),
    -- mentions
    -- tags
)
-- fields omitted:
-- - User-specific: favourited, reblogged, bookmark_collection_id
-- - quote: use quote_of_id to identify the quoted tweet
-- fields added:
-- - created_at_parsed, revised_at_parsed
-- fields TODO:
-- - reblog
-- - mentions
-- - tags

create table gab_media_attachment (
    gab_id text references gab (id),
    media_attachment_id text references media_attachment (id)
)

-- Metadata table to track which files have been inserted into this database
create table _inserted_files (
    filename string not null,
    num_records_inserted integer,
    inserted_at real default (julianday('now', 'utc'))
)