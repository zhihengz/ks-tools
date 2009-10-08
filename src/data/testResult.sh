#!/bin/sh

dir=`dirname $0`
cd $dir

test_file_nonexists() 
{
    local file=$1
    if [ -f $file ]; then
	echo "shall not have $file"
	exit 1
    fi
}

test_file_exists()
{
    local file=$1
    if [ ! -f $file ]; then
	echo "shall have $file"
	exit 1
    fi

}

test_file_nonexists testDuplicateCommands.cfg
test_file_nonexists testDuplicateIncludess.cfg
test_file_exists testActions.cfg
test_file_exists testIncludes.cfg
test_file_exists testPackages.cfg
test_file_exists testFull.cfg
test_file_exists testMultipleCommands.cfg
test_file_exists testSingleCommand.cfg
exit 0
