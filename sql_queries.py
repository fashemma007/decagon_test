table_names= ['countries','continents','currency','languages']
#=================CREATE==TABLES=================

create_table_countries= (
	"CREATE TABLE IF NOT EXISTS `countries` ("
	"`name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,"
	"`capital` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,"
	"`native_name` varchar(255) COLLATE utf8mb4_unicode_ci NULL,"
	"`country_id` varchar(255) NOT NULL,"
	"`country_id_3` varchar(255) NOT NULL,"
	"`country_code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,"
	"`currency_code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,"
	"`continent_id` varchar(255)COLLATE utf8mb4_unicode_ci NOT NULL,"
	"`language_id` varchar(255)COLLATE utf8mb4_unicode_ci NOT NULL,"
	"PRIMARY KEY (`name`)"
") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")


create_table_continents = (
		"CREATE TABLE IF NOT EXISTS `continents` ("
			"`continent_id` varchar(255) NOT NULL,"
			"`name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,"
			"PRIMARY KEY (`continent_id`)"
		") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")


create_table_currency = (
		"CREATE TABLE IF NOT EXISTS `currency` ("
			"`id` int COLLATE utf8mb4_unicode_ci NOT NULL,"
			"`currency_code` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,"
			"`country_id` varchar(255) COLLATE utf8mb4_unicode_ci NULL,"
			" PRIMARY KEY (`id`)"
			" ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")


create_table_languages = (
		"CREATE TABLE IF NOT EXISTS `languages` ("
			"`language_id` varchar(255) NOT NULL,"
			"`name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,"
			"`native_name` varchar(255) COLLATE utf8mb4_unicode_ci NULL,"
			"PRIMARY KEY (`language_id`)"
		") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")



create_table_queries= [create_table_countries,create_table_continents,create_table_currency,create_table_languages]