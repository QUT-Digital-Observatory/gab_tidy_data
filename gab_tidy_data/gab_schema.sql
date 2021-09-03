-----------------------------------
-- Gab Tidy Data metadata tables --
-----------------------------------

-- Metadata table for gab_tidy_data tool
create table _gab_tidy_data (
    metadata_key text primary key on conflict fail,
    metadata_value text
);

-- Update this whenever the schema is changed!!!
insert into _gab_tidy_data values ("schema_version", "2021-08-30");

-- Metadata table to track which files have been inserted into this database
create table _inserted_files (
    id integer primary key,
    filename string not null,
    num_gabs_inserted integer,  -- null may indicate unsuccessful insert
    num_parsing_failures integer,  -- counts lines of input file, not gabs
    inserted_at real,  -- time in UTC (julianday format, see sqlite docs)
    inserted_by_version text  -- stores the gab_tidy_data tool version
);

---------------------
-- Gab data tables --
---------------------

-- While technically these can change over time, for simplicity we treat them as static
create table emoji (
    shortcode text primary key,
    url text,
    static_url text
);
-- fields omitted:
-- - visible_in_picker

-- One row for every account per file - If multiple files are loaded, accounts may have
-- multiple rows.
create table account (
    id text, -- Gab-provided user id
    username text not null,
    acct text,
    display_name text,
    locked integer, -- boolean
    bot integer, -- boolean
    created_at text, -- Unparsed ISO datetime
    created_at_parsed real generated always as (julianday(created_at)) stored, -- created_at in julianday format
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
    _file_id integer references _inserted_files (id),
    primary key (id, _file_id)
);

create table account_fields (
    account_id text references account (id),
    _file_id integer references _inserted_files (id),
    ordering integer,  -- Which order the fields appear in, starting at 1
    name text,
    value text,
    verified_at text,
    primary key (account_id, _file_id, ordering)
);

create table account_emoji (
    account_id text references account (id),
    _file_id integer references _inserted_files (id),
    emoji_shortcode text references emoji (shortcode),
    primary key (account_id, _file_id, emoji_shortcode)
);

create table group_category (
    id integer,
    created_at text,
    updated_at text,
    text text,
    primary key (id)
);

create table gab_group ( -- note: sqlite does not allow naming a table "group"
    id text,
    title text,
    description text,
    description_html text,
    cover_image_url text,
    is_archived integer, -- boolean
    member_count integer,
    created_at text,
    created_at_parsed real generated always as (julianday(created_at)) stored, -- created_at in julianday format
    is_private integer, -- boolean
    is_visible integer, -- boolean
    slug text,
    url text,
    group_category integer references group_category (id),
    has_password integer, -- boolean
    _file_id integer references _inserted_files (id),
    primary key (id, _file_id)
);
-- Fields omitted:
-- - password

-- Groups have their own tag structure, separate from post tags
create table group_tag (
    group_id text references gab_group (id),
    _file_id integer references _inserted_files (id),
    tag text,
    primary key (group_id, _file_id, tag)
);

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
);
-- Fields omitted:
-- - meta object containing media dimensions etc

-- Does this change over time?
create table card (
    id text primary key,
    url text,
    title text,
    description text,
    type text,
    provider_name text,
    provider_url text,
    html text,
    image_url text,
    embed_url text,
    updated_at text
);
-- fields omitted:
-- - display fields: width and height

create table gab (
    id text, -- Gab-provided id
    created_at text not null, -- Unparsed text - appears to be in ISO format
    created_at_parsed real generated always as (julianday(created_at)) stored, -- created_at in julianday format
    revised_at text, -- Unparsed text
    revised_at_parsed real generated always as (julianday(revised_at)) stored, -- revised_at in julianday format
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
    reblog text, -- Always null. Should be json if not null in theory. Does the Gab hashtag API only give original posts and no reblogs?
    account_id text references account (id),
    group_id text references gab_group (id),
    card_id text references card (id),
    _embedded_gab integer, -- boolean - True means this gab was embedded in a gab that was in the search results, rather than being directly in the search results itself
    _file_id integer references _inserted_files (id), -- which result file this record was loaded from
    primary key (id, _file_id)
);
-- fields omitted:
-- - User-specific: favourited, reblogged, bookmark_collection_id
-- - quote: use quote_of_id to identify the quoted tweet
-- fields added:
-- - created_at_parsed, revised_at_parsed
-- - mention_user_ids, mention_usernames, tags - convenience columns duplicating
--   information available in the gab_mention and gab_tag tables respectively

-- This shouldn't change over time
create table gab_tag (
    gab_id text references gab (id),
    name text, -- tag name
    url text, -- Gab url for tag
    primary key (gab_id, name)
);

-- This shouldn't change over time
create table gab_mention (
    gab_id text references gab (id),
    account_id text not null, -- User may or may not be contained in Account table
    url text, -- Corresponds to account.url
    acct text, -- Corresponds to account.acct
    primary key (gab_id, account_id)
);

create table gab_media_attachment (
    gab_id text references gab (id),
    media_attachment_id text references media_attachment (id)
);

-- Assumes emoji are only in the content, and that the content doesn't change over time
create table gab_emoji (
    gab_id text references gab (id),
    emoji_shortcode text references emoji (shortcode)
);


---------------------
--      Views      --
---------------------

-- These views remove the time element from the tables, so there is only one row per
-- post, account, etc. Where the full table does have multiple rows per post (for
-- example), it is arbitrary which row for each post is displayed in the view, but in
-- practice it usually seems to be the first row in the table per post.
-- See https://www.sqlite.org/quirks.html#aggregate_queries_can_contain_non_aggregate_result_columns_that_are_not_in_the_group_by_clause

create view gab_unique as select * from gab group by id;

create view account_unique as select * from account group by id;

create view gab_group_unique as select * from gab_group group by id;
