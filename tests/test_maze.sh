PYTHON="pacman/bin/python3"
SCRIPT="tests/test_maze.py"
TEST_FOLDER="tests/maze_tests"
SEED=42

mkdir -p "$TEST_FOLDER"

echo "Test 1 - Maze 14x14"
PYTHONPATH=. $PYTHON $SCRIPT 14 14 $SEED > "$TEST_FOLDER/test1_maze14x14.txt"
cat "$TEST_FOLDER/test1_maze14x14.txt"
echo -e

echo "Test 2 - Maze 14x15"
PYTHONPATH=. $PYTHON $SCRIPT 14 15 $SEED > "$TEST_FOLDER/test2_maze14x15.txt"
cat "$TEST_FOLDER/test2_maze14x15.txt"
echo -e

echo "Test 3 - Maze 15x14"
PYTHONPATH=. $PYTHON $SCRIPT 15 14 $SEED > "$TEST_FOLDER/test3_maze15x14.txt"
cat "$TEST_FOLDER/test3_maze15x14.txt"
echo -e

echo "Test 4 - Maze 15x15"
PYTHONPATH=. $PYTHON $SCRIPT 15 15 $SEED > "$TEST_FOLDER/test4_maze15x15.txt"
cat "$TEST_FOLDER/test4_maze15x15.txt"
echo -e

echo "Test 5 - Maze 32x32"
PYTHONPATH=. $PYTHON $SCRIPT 32 32 $SEED > "$TEST_FOLDER/test5_32x32.txt"
cat "$TEST_FOLDER/test5_32x32.txt"
echo -e

echo "Test 6 - Maze 31x31"
PYTHONPATH=. $PYTHON $SCRIPT 31 31 $SEED > "$TEST_FOLDER/test6_31x31.txt"
cat "$TEST_FOLDER/test6_31x31.txt"
echo -e

echo "Test 7 - Maze 16x32"
PYTHONPATH=. $PYTHON $SCRIPT 16 32 $SEED > "$TEST_FOLDER/test7_16x32.txt"
cat "$TEST_FOLDER/test7_16x32.txt"
echo -e

echo "Test 8 - Maze 32x16"
PYTHONPATH=. $PYTHON $SCRIPT 32 16 $SEED > "$TEST_FOLDER/test8_32x16.txt"
cat "$TEST_FOLDER/test8_32x16.txt"
echo -e

echo "Test 9 - Maze 14x21"
PYTHONPATH=. $PYTHON $SCRIPT 14 21 $SEED > "$TEST_FOLDER/test9_14x21.txt"
cat "$TEST_FOLDER/test9_14x21.txt"
echo -e

echo "Test 10 - Maze 21x14"
PYTHONPATH=. $PYTHON $SCRIPT 21 14 $SEED > "$TEST_FOLDER/test10_21x14.txt"
cat "$TEST_FOLDER/test10_21x14.txt"
echo -e

echo "Test 11 - Maze 15x25"
PYTHONPATH=. $PYTHON $SCRIPT 15 25 $SEED > "$TEST_FOLDER/test11_15x25.txt"
cat "$TEST_FOLDER/test11_15x25.txt"
echo -e

echo "Test 12 - Maze 25x15"
PYTHONPATH=. $PYTHON $SCRIPT 25 15 $SEED > "$TEST_FOLDER/test12_25x15.txt"
cat "$TEST_FOLDER/test12_25x15.txt"
echo -e
