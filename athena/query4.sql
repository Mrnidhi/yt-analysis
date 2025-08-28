SELECT region, trending_date, title, views
FROM yt_base.analytics_youtube_trending
ORDER BY views DESC
LIMIT 10;
