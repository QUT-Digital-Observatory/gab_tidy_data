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
-- TODO: incorporate time (gab_id, gab_created_at, change primary key, change table name to gab_account?)


create table group (
    id text primary key,
    title text,
    description text,
    description_html text,
    cover_image_url text,
    is_archived integer, -- boolean
    member_count integer,
    created_at text,
    created_at_parsed float, -- created_at in julianday format
    is_private integer, -- boolean
    is_visible integer, -- boolean
    slug text,
    url text,
    -- tags
    -- group_category
    has_password integer -- boolean
) -- TODO: incorporate time
-- Fields omitted:
-- - password

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
    expires_at text, -- Presumably a date? Not contained in sample data
    has_quote integer, -- boolean
    content text, -- HTML text of gab
    rich_content text, -- Not sure how different from content?
    plain_markdown text,
    -- reblog
    account_id text references account (id),
    group_id text references group (id),
    mention_user_ids text, -- List (comma-separated) of account IDs of mentioned users
    mention_usernames text -- List (comma-separated) of usernames of mentioned users
    tags text -- List (comma-separated) of tag names
)
-- fields omitted:
-- - User-specific: favourited, reblogged, bookmark_collection_id
-- - quote: use quote_of_id to identify the quoted tweet
-- fields added:
-- - created_at_parsed, revised_at_parsed
-- - mention_user_ids, mention_usernames, tags - convenience columns duplicating
--   information available in the gab_mention and gab_tag tables respectively
-- fields TODO:
-- - reblog -- is this field unused or just no values present in this sample data?

create table gab_mention (
    gab_id text references gab (id),
    account_id text not null, -- User may or may not be contained in Account table
    url text, -- Corresponds to account.url
    acct text -- Corresponds to account.acct
)

create table gab_media_attachment (
    gab_id text references gab (id),
    media_attachment_id text references media_attachment (id)
)

create table gab_tag (
    gab_id text references gab (id),
    name text not null, -- tag name
    url text not null -- Gab url for tag
)

-- Metadata table to track which files have been inserted into this database
create table _inserted_files (
    filename string not null,
    num_records_inserted integer,
    inserted_at real default (julianday('now', 'utc'))
)