from sqlalchemy import text


def top_products(db, limit):

    return db.execute(
        text("""
            SELECT
                detected_class,
                COUNT(*) AS mentions
            FROM fct_image_detections
            GROUP BY detected_class
            ORDER BY mentions DESC
            LIMIT :limit
        """),
        {"limit": limit},
    ).mappings().all()


def search_messages(db, query, limit):

    return db.execute(
        text("""
            SELECT
                m.message_id,
                c.channel_name AS channel,
                m.message_text,
                m.views
            FROM fct_messages m
            JOIN dim_channels c
                ON m.channel_key = c.channel_key
            WHERE LOWER(m.message_text)
                LIKE LOWER(:query)
            LIMIT :limit
        """),
        {
            "query": f"%{query}%",
            "limit": limit,
        },
    ).mappings().all()


def channel_activity(db, channel):

    return db.execute(
        text("""
            SELECT
                c.channel_name,
                COUNT(*) AS total_messages,
                SUM(m.views) AS total_views,
                AVG(m.views) AS average_views
            FROM fct_messages m
            JOIN dim_channels c
                ON m.channel_key = c.channel_key
            WHERE LOWER(c.channel_name)=LOWER(:channel)
            GROUP BY c.channel_name
        """),
        {"channel": channel},
    ).mappings().first()


def visual_content(db):

    return db.execute(
        text("""
            SELECT
                c.channel_name,
                COUNT(DISTINCT f.message_id)
                    AS total_images
            FROM fct_image_detections f
            JOIN dim_channels c
                ON f.channel_key=c.channel_key
            GROUP BY c.channel_name
            ORDER BY total_images DESC
        """)
    ).mappings().all()
