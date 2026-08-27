mkdir -p config_tests

# Test 1: Everything is right
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test1.json

# Test 2: Missing keys
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test2.json

# Test 3: Missing levels
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test3.json

# Test 4: Wrong value in 'highscore_filename'
echo '
{
    "highscore_filename": 123,
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test4.json

# Test 5: Empty value in 'highscore_filename'
echo '
{
    "highscore_filename": "",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test5.json

# Test 6: Wrong 'width' in 'level'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 12, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test6.json

# Test 7: Wrong value on 'width' in 'level'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": "abc", "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test7.json

# Test 8: Wrong 'height' in 'level'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 400, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test8.json

# Test 9: Wrong value on 'height' in 'level'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": "xyz", "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test9.json

# Test 10: Wrong 'number_of_pacgums' in 'level'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 400, "number_of_pacgums": 100},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test10.json

# Test 11: Wrong value on 'number_of_pacgums' in 'level'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": "xyz"},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test11.json

# Test 12: Wrong value in 'lives'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": -1,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test12.json

# Test 13: Wrong value in 'lives'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": "abc",
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test13.json

# Test 14: Wrong value in 'points_per_pacgum'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 1000,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test14.json

# Test 15: Wrong value in 'points_per_pacgum'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": "abc",
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test15.json

# Test 16: Wrong value in 'points_per_super_pacgum'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 10,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test16.json

# Test 17: Wrong value in 'points_per_super_pacgum'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": "xyz",
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test17.json

# Test 18: Wrong value in 'points_per_ghost'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 100,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test18.json

# Test 19: Wrong value in 'points_per_ghost'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": "200",
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test19.json

# Test 20: Wrong value in 'seed'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": -2,
    "level_max_time": 90
}' > config_tests/test20.json

# Test 21: Wrong value in 'seed'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": "42",
    "level_max_time": 90
}' > config_tests/test21.json

# Test 22: Wrong value in 'level_max_time'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 200
}' > config_tests/test22.json

# Test 23: Wrong value in 'level_max_time'
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": "90"
}' > config_tests/test23.json

# Test 24: Empty file
echo '' > config_tests/test24.json

# Test 25: No permission
echo '' > config_tests/test25.json
chmod 111 config_tests/test25.json

# Test 26: Filled with commentaries
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14, "height": 14, "number_of_pacgums": 174}, //Unnecessary comment
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        /* This block comment
        will be removed */
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ], # To be removed
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test26.json

# Test 27: Wrongly formatted
echo '
{
    "highscore_filename": "path_to_file",
    "level": [
        {"width": 14 "number_of_pacgums": 174},
        {"width": 16, "height": 16, "number_of_pacgums": 234},
        {"width": 18, "height": 18, "number_of_pacgums": 302},
        {"width": 20, "height": 20, "number_of_pacgums": 378},
        {"width": 22, "height": 22, "number_of_pacgums": 462},
        {"width": 24, "height": 24, "number_of_pacgums": 554},
        {"width": 26, "height": 26, "number_of_pacgums": 654},
        {"width": 28, "height": 28, "number_of_pacgums": 762},
        {"width": 30, "height": 30, "number_of_pacgums": 878},
        {"width": 32, "height": 32, "number_of_pacgums": 1002}
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}' > config_tests/test27.json

echo "Test 1 - All correct"
python3 test.py config_tests/test1.json
echo -e

echo "Test 2 - Missing key"
python3 test.py config_tests/test2.json
echo -e

echo "Test 3 - Missing levels"
python3 test.py config_tests/test3.json
echo -e

echo "Test 4 - Wrong value in 'highscore_filename'"
python3 test.py config_tests/test4.json
echo -e

echo "Test 5 - Empty value in 'highscore_filename'"
python3 test.py config_tests/test5.json
echo -e

echo "Test 6 - Wrong 'width' in 'level'"
python3 test.py config_tests/test6.json
echo -e

echo "Test 7 - Wrong value on 'width' in 'level'"
python3 test.py config_tests/test7.json
echo -e

echo "Test 8 - Wrong 'height' in 'level'"
python3 test.py config_tests/test8.json
echo -e

echo "Test 9 - Wrong value on 'height' in 'level'"
python3 test.py config_tests/test9.json
echo -e

echo "Test 10 - Wrong 'number_of_pacgums' in 'level'"
python3 test.py config_tests/test10.json
echo -e

echo "Test 11 - Wrong value on 'number_of_pacgums' in 'level'"
python3 test.py config_tests/test11.json
echo -e

echo "Test 12 - Wrong value in 'lives'"
python3 test.py config_tests/test12.json
echo -e

echo "Test 13 - Empty value in 'lives'"
python3 test.py config_tests/test13.json
echo -e

echo "Test 14 - Wrong value in 'points_per_pacgum'"
python3 test.py config_tests/test14.json
echo -e

echo "Test 15 - Empty value in 'points_per_pacgum'"
python3 test.py config_tests/test15.json
echo -e

echo "Test 16 - Wrong value in 'points_per_super_pacgum'"
python3 test.py config_tests/test16.json
echo -e

echo "Test 17 - Wrong value in 'points_per_super_pacgum'"
python3 test.py config_tests/test17.json
echo -e

echo "Test 18 - Wrong value in 'points_per_ghost'"
python3 test.py config_tests/test18.json
echo -e

echo "Test 19 - Wrong value in 'points_per_ghost'"
python3 test.py config_tests/test19.json
echo -e

echo "Test 20 - Wrong value in 'seed'"
python3 test.py config_tests/test20.json
echo -e

echo "Test 21 - Wrong value in 'seed'"
python3 test.py config_tests/test21.json
echo -e

echo "Test 22 - Wrong value in 'level_max_time'"
python3 test.py config_tests/test22.json
echo -e

echo "Test 23 - Wrong value in 'level_max_time'"
python3 test.py config_tests/test23.json
echo -e

echo "Test 24 - Empty file"
python3 test.py config_tests/test24.json
echo -e

echo "Test 25 - No permission"
python3 test.py config_tests/test25.json
echo -e

echo "Test 26 - Filled with commentaries, no error"
python3 test.py config_tests/test26.json
echo -e

echo "Test 27 - Wrongly formatted"
python3 test.py config_tests/test27.json
echo -e

echo "Test 28 - No file"
python3 test.py config_tests/non_existent.json
echo -e
