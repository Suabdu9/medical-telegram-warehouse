{{ config(materialized='table') }}

SELECT

    d.message_id,

    m.channel_key,

    m.date_key,

    d.image,

    d.channel,

    d.class_name AS detected_class,

    d.confidence AS confidence_score,

    d.image_category

FROM public.image_detections d

JOIN {{ ref('fct_messages') }} m
    ON d.message_id = m.message_id