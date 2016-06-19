
/*¬ьюха, практически аналогична€ таблице станций. “упо прибиндили сюда развернутое им€ страны вместо кода*/
IF OBJECT_ID('Station_view', 'V') IS NOT NULL
    DROP VIEW [Station_view];
GO
CREATE VIEW [Station_view] AS
SELECT 
	[Weather_station].id_weather_station, 
	[Weather_station].usaf_wban, 
	[Weather_station].name,
	[Weather_station].country_code, 
	[Country_code].name as country, 
	[Weather_station].state_code, 
	[Weather_station].call_sign, 
	[Weather_station].lat, 
	[Weather_station].long, 
	[Weather_station].elevation 
	FROM [Weather_station]
	LEFT JOIN [Country_code] 
		ON [Weather_station].country_code = [Country_code].id_country_code
GO

/*¬ьюха, практически аналогична€ таблице данных. “упо прибиндили сюда развернутое sky_condition вместо кода*/
IF OBJECT_ID('Data_view', 'V') IS NOT NULL
    DROP VIEW [Data_view];
GO
CREATE VIEW [Data_view] AS
SELECT 
	[Raw_weather_data].id_station, 
	[Raw_weather_data].time, 
	[Raw_weather_data].temperature, 
	[Raw_weather_data].dewpoint, 
	[Raw_weather_data].pressure, 
	[Raw_weather_data].wind_direction, 
	[Raw_weather_data].wind_speed,
	[Raw_weather_data].sky_condition,
	[Sky_condition].name as full_sky_condition, 
	[Raw_weather_data].one_hour_precip, 
	[Raw_weather_data].six_hour_precip 
	FROM [Raw_weather_data]
	LEFT JOIN [Sky_condition] 
		ON [Raw_weather_data].sky_condition = [Sky_condition].id_sky_condition
GO

/*¬ьюха дл€ сценари€ номер 3. √руппирует средние данные по температуре и скорости ветра дл€ каждой станции по дн€м*/
IF OBJECT_ID('avg_temp_windSpeed_view', 'V') IS NOT NULL
    DROP VIEW [avg_temp_windSpeed_view];
GO
CREATE VIEW [avg_temp_windSpeed_view] AS
	SELECT	
		[Station_view].id_weather_station,
		[Station_view].usaf_wban,
		[Station_view].name, 
		[Station_view].country_code,
		[Station_view].country, 
		CONVERT(date, [Data_view].time) as 'Day', 
		AVG(temperature) as Temperature, 
		AVG(wind_speed) as Wind_speed
	FROM [Station_view]
	INNER JOIN [Data_view] 
		ON [Station_view].[id_weather_station] = [Data_view].[id_station]
	GROUP BY 
		[Station_view].id_weather_station,
		[Station_view].usaf_wban, 
		[Station_view].name, 
		[Station_view].country,
		[Station_view].country_code, 
		CONVERT(date, [Data_view].time)
	HAVING 
			AVG(temperature) is NOT NULL
		AND AVG(wind_speed) is NOT NULL
GO

/*—ценарий 1. ћинимальна€, средн€€ и максимальна€ температуры за год по данным заданной станции.*/
IF object_id(N'AggregateTemperatures', N'IF') IS NOT NULL
    DROP FUNCTION AggregateTemperatures
GO
CREATE FUNCTION AggregateTemperatures (@UsafWban varchar(12), @Year int)
RETURNS TABLE AS
RETURN 
	SELECT	
		[Station_view].id_weather_station,
		[Station_view].usaf_wban,
		[Station_view].name, 
		MAX(temperature) as 'Max temperature', 
		MIN(temperature) as 'Min temperature', 
		AVG(temperature) as 'Avg temperature'
FROM [Station_view]
INNER JOIN [Data_view] 
	ON [Station_view].[id_weather_station] = [Data_view].[id_station]
WHERE 
		year(time) = @Year
	AND [Station_view].usaf_wban = @UsafWban
GROUP BY 
	[Station_view].id_weather_station,
	[Station_view].usaf_wban, 
	[Station_view].name
GO

--Example
SELECT * From dbo.AggregateTemperatures('999999-00000', 2013)
GO

/*—ценарий 2 отобрать станции, наход€щиес€ в определенной стране, 
на которых зафиксирована средн€€ скорость ветра, превосход€ща€ среднюю скорость ветра 
замеренной на всех станци€х этой страны за определенный период. */
IF object_id(N'MostWindedForCountry', N'IF') IS NOT NULL
    DROP FUNCTION MostWindedForCountry
GO
CREATE FUNCTION MostWindedForCountry (@Country_code varchar(2), @TimeStart varchar(20), @TimeEnd varchar(20))
RETURNS TABLE AS
RETURN 
	SELECT * FROM (
		--—редние показатели ветра станции
		SELECT	
			[Station_view].[id_weather_station], 
			[Station_view].[usaf_wban], 
			[Station_view].name, 
			AVG(wind_speed) as Avg_wind
		FROM 
			[Station_view], 
			[Data_view]
        WHERE 
				[Station_view].[id_weather_station] = [Data_view].[id_station]
			AND time >= @TimeStart 
			AND time <= @TimeEnd
			AND [Station_view].country_code = @Country_code
		GROUP BY 
			[Station_view].[id_weather_station], 
			[Station_view].[usaf_wban],  
			[Station_view].name ) 
	AS Avg_wind_for_station
WHERE Avg_wind >= 
	--—редние показатели ветра по стране
	(SELECT AVG(wind_speed) as Avg_wind
	FROM [Station_view]
	INNER JOIN [Data_view] 
		ON	[Station_view].[id_weather_station] = [Data_view].[id_station]
	WHERE 
			time >= @TimeStart 
		AND time <= @TimeEnd
		AND [Station_view].country_code = @Country_code
	GROUP BY [Station_view].country)
GO

--Example
SELECT * From dbo.MostWindedForCountry('BY', '2000-1-1', '2013-1-1')




