CREATE DATABASE IF NOT EXISTS statistics;

CREATE TABLE IF NOT EXISTS statistics.likes (
    author_id String,
    source_id String,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY (post_id);

CREATE TABLE IF NOT EXISTS statistics.comments (
    comment_id String,
    author_id String,
    source_id String,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY (post_id);
