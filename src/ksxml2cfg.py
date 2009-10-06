#!/usr/bin/python -t
import sys,os
def print_usage():
	print "usage: ksxml2cfg <xml file>"

def main():
	if len(sys.argv) < 2:
		print_usage()
		sys.exit(1)
	print "done"

if __name__ == "__main__":
	main()
