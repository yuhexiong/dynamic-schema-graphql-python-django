CREATE TABLE adventure_game_heroes (
    id INTEGER,
    join_date DATE,
    hero_name varchar(20),
    occupation varchar(20),
    level INTEGER,
    weapon_name varchar(20),
    weapon_type varchar(20),
    weapon_power double,
    equipment_status varchar(20)
) ENGINE=OLAP
UNIQUE KEY(`id`)
COMMENT 'adventure_game_heroes'
DISTRIBUTED BY HASH(`id`) BUCKETS AUTO
PROPERTIES (
    "replication_allocation" = "tag.location.default: 1",
    "is_being_synced" = "false",
    "storage_medium" = "hdd",
    "storage_format" = "V2",
    "enable_unique_key_merge_on_write" = "true",
    "light_schema_change" = "true",
    "store_row_column" = "true",
    "disable_auto_compaction" = "false",
    "enable_single_replica_compaction" = "false"
);

INSERT INTO adventure_game_heroes (id, hero_name, occupation, level, weapon_name, weapon_type, weapon_power, equipment_status, join_date)
VALUES
(1, 'Arthur', 'Warrior', 10, 'Sword of Destiny', 'Sword', 50.5, 'Equipped', '2023-01-01'),
(2, 'Merlin', 'Wizard', 12, 'Staff of Power', 'Staff', 45.3, 'Equipped', '2023-02-01'),
(3, 'Legolas', 'Archer', 8, 'Elven Bow', 'Bow', 40.0, 'Equipped', '2023-03-01'),
(4, 'Aragorn', 'Ranger', 11, 'Andúril', 'Sword', 55.2, 'Equipped', '2023-04-01'),
(5, 'Eowyn', 'Warrior', 9, 'Golden Shield', 'Shield', 35.8, 'Equipped', '2023-05-01'),
(6, 'Gandalf', 'Wizard', 15, 'Glamdring', 'Sword', 60.0, 'Equipped', '2023-06-01'),
(7, 'Robin Hood', 'Archer', 7, 'Longbow', 'Bow', 38.5, 'Equipped', '2023-07-01'),
(8, 'Thranduil', 'Elf', 10, 'Serpentine Dagger', 'Dagger', 42.1, 'Equipped', '2023-08-01'),
(9, 'Boromir', 'Warrior', 8, 'Gondorian Sword', 'Sword', 48.7, 'Equipped', '2023-09-01'),
(10, 'Frodo', 'Thief', 6, 'Sting', 'Dagger', 30.5, 'Equipped', '2023-10-01');
