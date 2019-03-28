weatherChannel = [PUT_YOUR_WEATHER_CHANNEL_HERE];
weatherAPIKey = 'PUT_YOUR_WEATHER_API_KEY_HERE';
rainfallField = [4];

tankChannel = [PUT_YOUR_WATERLEVEL_CHANNEL_HERE];
tankAPIKey = 'PUT_YOUR_WATERLEVEL_API_KEY_HERE';
tankLevelField = [1];


% Read rainfall
[rainfall, t1] = thingSpeakRead(weatherChannel, 'Fields', rainfallField, 'NumPoints', 8000, 'ReadKey', weatherAPIKey);

% Read tank water level
[waterLevel, t2] = thingSpeakRead(tankChannel, 'Fields', tankLevelField, 'NumPoints', 8000, 'ReadKey', tankAPIKey);

%% Visualize Data %%

% vectors must be the same length
n = min(numel(rainfall), numel(waterLevel))
t1 = t1(end-n+1:end)
rainfall = rainfall(end-n+1:end)
t2 = t2(end-n+1:end)
waterLevel = waterLevel(end-n+1:end)
waterLevel = movmean(waterLevel,40);

plotyy(t1, rainfall, t2, waterLevel)
