SELECT
  title,
  region,
  trending_date,
  MAX(views) AS top_views
FROM
  yt_base.analytics_youtube_trending
GROUP BY
  title, region, trending_date
ORDER BY
  top_views DESC
LIMIT 10;
