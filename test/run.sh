for py_file in $(find test -name *_test.py)
do
    python $py_file
done

