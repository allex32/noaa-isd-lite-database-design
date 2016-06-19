USE [NOAA-Big]
GO

/****** Object:  UserDefinedFunction [dbo].[AggregateTemperatures]    Script Date: 19.06.2016 19:12:42 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER FUNCTION [dbo].[AggregateTemperatures] (@UsafWban varchar(12), @Year int)
RETURNS TABLE AS
RETURN 
SELECT * from 
	( SELECT st.id_weather_station, max(rc.temperature) MAX, min(rc.temperature) as MIN, avg(rc.temperature) as AVG 
		FROM dbo.Raw_weather_data rc
		JOIN Weather_station st 
			on rc.id_station = st.id_weather_station 
		WHERE 
			usaf_wban = @UsafWban and 
			YEAR(rc.time) = @Year
		GROUP BY id_weather_station) tmp
GO

Select * from [dbo].[AggregateTemperatures]('000123-99999', 2005)

GO

ALTER FUNCTION [dbo].[MostWindedForCountry] (@Country_code varchar(2), @TimeStart datetime, @TimeEnd datetime)
RETURNS TABLE AS
RETURN 
	SELECT * FROM (
		--Средние показатели ветра станции
		SELECT	
			st.id_weather_station 
			, st.usaf_wban ,
			st.name,
			AVG(wind_speed) as Avg_wind
		FROM 
			Raw_weather_data  rc
			, Weather_station st 
        WHERE 
				st.id_weather_station = rc.id_station 
			AND time >= @TimeStart 
			AND time <= @TimeEnd
			AND st.country_code  = @Country_code
		GROUP BY 
			st.id_weather_station 
			, st.usaf_wban   
			, st.name ) 
	AS Avg_wind_for_station
WHERE Avg_wind >= 
	--Средние показатели ветра по стране
	(SELECT AVG(wind_speed) as Avg_wind
	FROM Weather_station st
	INNER JOIN Raw_weather_data rc
		ON	st.id_weather_station  = rc.id_station 
	WHERE 
			time >= @TimeStart  
		AND time <= @TimeEnd 
		AND st.country_code  = @Country_code 
	GROUP BY st.country_code )

GO


Select * from [dbo].MostWindedForCountry('BR', '2000-01-01', '2016-01-01')

GO

ALTER FUNCTION ClosestStationByTempAndWind (@UsafWban varchar(12), @Country_code varchar(2))
RETURNS TABLE AS
RETURN 


Select * from (

Select inpStation.id_station, inpStation.dayWithTime, inpStation.AvgTemp,
inpCountry.id_station inpCountryStation, inpCountry.dayWithTime inpCountryDayWithTime, 
inpCountry.AvgTemp inpCountryAvgtemp
 from 
(
	--Группируем записи, относ-еся к одной станции по дням
Select  rc.id_station, DATEADD(dd, 0, DATEDIFF(dd, 0, rc.time)) as dayWithTime,  AVG(rc.temperature) as AvgTemp from dbo.Raw_weather_data rc
JOIN Weather_station st on rc.id_station = st.id_weather_station
where st.usaf_wban =  @UsafWban
group by id_station, DATEADD(dd, 0, DATEDIFF(dd, 0, rc.time)) ) inpStation

JOIN (

--Группировка станций из определенной страны по дню с высчетом средней температуры
Select * from(
Select rc.id_station, DATEADD(dd, 0, DATEDIFF(dd, 0, rc.time)) as dayWithTime,  AVG(rc.temperature) as AvgTemp
	FROM Raw_weather_data rc
	JOIN  ( Select * from Weather_station st
		where st.country_code = @Country_code 
		) c_st on rc.id_station = c_st.id_weather_station

	 group by DATEADD(dd, 0, DATEDIFF(dd, 0, rc.time)), id_station
	 ) tmp ) inpCountry 
	 
	on inpStation.dayWithTime = inpCountry.dayWithTime 
) finalJoin

where id_station <> inpCountryStation 
and abs(AvgTemp - inpCountryAvgtemp) < abs(AvgTemp * 0.15)
 
GO

Select * from ClosestStationByTempAndWind('000123-99999','BR')

