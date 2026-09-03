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