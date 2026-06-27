SELECT

    message_id,

    channel_name,

    CAST(message_date AS TIMESTAMP) AS message_date,

    TRIM(message_text) AS message_text,

    COALESCE(has_media, FALSE) AS has_media,

    image_path,

    COALESCE(views, 0) AS views,

    COALESCE(forwards, 0) AS forwards,

    LENGTH(COALESCE(message_text, '')) AS message_length,

    CASE
        WHEN image_path IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS has_image,

    ingested_at

FROM {{ source('raw', 'telegram_messages') }}

WHERE message_text IS NOT NULL
  AND TRIM(message_text) <> ''
