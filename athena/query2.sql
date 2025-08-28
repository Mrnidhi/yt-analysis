CREATE EXTERNAL TABLE IF NOT EXISTS yt_base.analytics_youtube_trending (
  video_id STRING,
  title STRING,
  publish_time STRING,
  views BIGINT,
  likes BIGINT
)
PARTITIONED BY (
  region STRING,
  trending_date DATE
)
STORED AS PARQUET
LOCATION 's3://youtube-trend-nidhi/youtube-trending-datalake/analytics/';
