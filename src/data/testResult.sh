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

test_comps_rhcs()
{
    local file=$1
    local expected=$2
    num=`cat $file | wc -l`
    if [ "$num" != "$expected" ]; then
	echo "$file shall has $expected line"
	exit 1
    fi
    
}
test_file_nonexists testDuplicateCommands.cfg
test_file_nonexists testDuplicateRepoCommands.cfg
test_file_nonexists testDuplicateIncludess.cfg
test_file_nonexists dupcmd.cfg
test_file_nonexists duppkgs.cfg
test_file_nonexists dupacts.cfg
test_file_exists testActions.cfg
test_file_exists testMultipleRepoCommands.cfg
test_file_exists testIncludes.cfg
test_file_exists testPackages.cfg
test_file_exists testFull.cfg
test_file_exists testMultipleCommands.cfg
test_file_exists testSingleCommand.cfg
test_file_exists merged.cfg
test_file_exists mpostacts.cfg
test_comps_rhcs compsRhcs.txt 37
test_comps_rhcs compsRhcsIgnored.txt 0
test_file_exists compsRhcsSingleMerge.txt
test_file_exists compsRhcsMultipleMerge.txt
test_file_exists compsUtf8.txt
test_file_nonexists compsRhcsDupMerge.txt
exit 0
