SELECT * FROM YTData..YTStats

--Take the most useful columns and order it by the most popular by views
SELECT title, publishedAt, viewCount, likeCount, commentCount, durationSecs FROM YTData..YTStats
ORDER BY viewCount DESC 

--Take the most useful columns and look at just the character teaser videos
SELECT title, publishedAt, viewCount, likeCount, commentCount, durationSecs FROM YTData..YTStats
WHERE title LIKE '%Character Teaser%';

--See the total viewership by year and compare to previous year
SELECT  YEAR(publishedAt) as year_published,SUM(viewCount) as views_this_year,
		LAG(SUM(viewCount)) OVER (ORDER BY(YEAR(publishedAt))) AS views_last_year
		FROM YTData..YTStats
		GROUP BY YEAR(publishedAt)


--See the average viewership by year and compare to previous year
SELECT  YEAR(publishedAt) as year_published,AVG(viewCount) as avg_views_by_year,
		LAG(AVG(viewCount)) OVER (ORDER BY (YEAR(publishedAt))) as avg_views_last_year
		FROM YTData..YTStats 
		GROUP BY YEAR(publishedAt);

--Whats the total avg of the viewership?
SELECT AVG(viewCount) as avg_views
		FROM YTData..YTStats;

