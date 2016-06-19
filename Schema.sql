SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[Country_code](
	[id_country_code] [varchar](2) NOT NULL,
	[name] [varchar](90) NULL,
 CONSTRAINT [PK__Country___12216F6189B08EB3] PRIMARY KEY CLUSTERED 
(
	[id_country_code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO


ALTER TABLE [dbo].[Country_code] ADD  CONSTRAINT [PK__Country___12216F6189B08EB3] PRIMARY KEY CLUSTERED 
(
	[id_country_code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO



CREATE TABLE [dbo].[Sky_condition](
	[id_sky_condition] [int] NOT NULL,
	[name] [varchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[id_sky_condition] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO


/****** Object:  Index [PK__Sky_cond__F2F6931C2B5267F4]    Script Date: 20.06.2016 1:02:03 ******/
ALTER TABLE [dbo].[Sky_condition] ADD PRIMARY KEY CLUSTERED 
(
	[id_sky_condition] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO




CREATE TABLE [dbo].[Weather_station](
	[id_weather_station] [bigint] IDENTITY(1,1) NOT NULL,
	[name] [varchar](50) NULL,
	[country_code] [varchar](2) NULL,
	[state_code] [varchar](2) NULL,
	[call_sign] [varchar](5) NULL,
	[lat] [float] NULL,
	[long] [float] NULL,
	[elevation] [float] NULL,
	[usaf_wban] [varchar](12) NULL,
 CONSTRAINT [PK__Weather___A5CDD800D2932B1D] PRIMARY KEY CLUSTERED 
(
	[id_weather_station] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO


/****** Object:  Index [PK__Weather___A5CDD800D2932B1D]    Script Date: 20.06.2016 1:09:24 ******/
ALTER TABLE [dbo].[Weather_station] ADD  CONSTRAINT [PK__Weather___A5CDD800D2932B1D] PRIMARY KEY CLUSTERED 
(
	[id_weather_station] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO


CREATE TABLE [dbo].[Raw_weather_data](
	[id_station] [bigint] IDENTITY(1,1) NOT NULL,
	[time] [datetime] NOT NULL,
	[temperature] [float] NULL,
	[dewpoint] [float] NULL,
	[pressure] [float] NULL,
	[wind_direction] [int] NULL,
	[wind_speed] [float] NULL,
	[sky_condition] [int] NULL,
	[one_hour_precip] [float] NULL,
	[six_hour_precip] [float] NULL,
 CONSTRAINT [PK_Raw_Weather_Data] PRIMARY KEY CLUSTERED 
(
	[id_station] ASC,
	[time] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[Raw_weather_data] ADD  CONSTRAINT [PK_Raw_Weather_Data] PRIMARY KEY CLUSTERED 
(
	[id_station] ASC,
	[time] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO


ALTER TABLE Raw_weather_data 
ADD CONSTRAINT FK_RawWeatherData_WeatherStation FOREIGN KEY (id_station)
	REFERENCES Weather_station (id_weather_station)

GO

ALTER TABLE Weather_station 
ADD CONSTRAINT FK_RawWeatherData_CountryCode FOREIGN KEY (country_code)
	REFERENCES Country_code (id_country_code)
