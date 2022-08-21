## Decagon_test
### Run
1. ```make setup``` 
2. ```make install```
3. To start the process ```make run```

## Solution
#### a. List all the continents and the total number of countries in each—for example, Africa 100, Europe 10, etc. The continent's name and country count should be in a different column.
```select continents.name as Continent, count(countries.name) as 'Country Count' from continents left join countries on continents.continent_id = countries.continent_id group by continents.name;```