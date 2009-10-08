PYTHON_LIB=$(shell python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
BIN_BASE=/usr/bin
xml_data_files := $(wildcard data/*.xml)
data_prefixes := $(patsubst %.xml,%,${xml_data_files})
xml_merge_data_files := data/testIncludes.xml \
	data/testMultipleCommands.xml \
	data/testPackages.xml \
	data/testActions.xml
dup_cmds_data_files := data/testSingleCommand.xml data/testMultipleCommands.xml
dup_pkgs_data_files := data/testPackages.xml data/testPackages.xml
dup_acts_data_files := data/testActions.xml data/testActions.xml
all:	ksxml2cfg test
clean:
	rm -f ksxml2cfg
	rm -fr *~ tmp
	rm -fr *.pyc
	cd rhks && $(MAKE) clean
	cd data && rm -fr *~ && rm -fr *.cfg
test:
	@echo $(PYTHON_LIB)
	@echo "testing ksxml2cfg.py"
	@for f in $(data_prefixes); \
	do \
		echo "compiling $$f" ; \
		python ksxml2cfg.py -o $(addsuffix .cfg, $$f) $(addsuffix .xml, $$f);\
	done
	@echo "compiling $(dup_cmds_data_files)"; \
	python ksxml2cfg.py -o data/merged.cfg $(xml_merge_data_files)
	@echo "compiling $(dup_cmds_data_files)"; \
	python ksxml2cfg.py -o data/dupcmd.cfg $(dup_cmds_data_files) ; \
	echo "ignore failure anyway"
	@echo "compiling $(dup_pkgs_data_files)"; \
	python ksxml2cfg.py -o data/duppkgs.cfg $(dup_pkgs_data_files) ; \
	echo "ignore failure anyway"
	@echo "compiling $(dup_acts_data_files)"; \
	python ksxml2cfg.py -o data/dupacts.cfg $(dup_acts_data_files) ; \
	echo "ignore failure anyway"
	@echo "checking results..." && data/testResult.sh
ksxml2cfg:	ksxml2cfg.py
	@echo "creating shell script wrapper" && \
	echo "#!/usr/bin/python" >ksxml2cfg && \
	cat ksxml2cfg.py >>ksxml2cfg && chmod +x ksxml2cfg

install:
	mkdir -p $(DESTDIR)$(BIN_BASE)
	install -m 755 ksxml2cfg $(DESTDIR)$(BIN_BASE)
	mkdir -p $(DESTDIR)$(PYTHON_LIB)/rhks
	install -m 644 rhks/components.py $(DESTDIR)$(PYTHON_LIB)/rhks/components.py
	install -m 644 rhks/parser.py $(DESTDIR)$(PYTHON_LIB)/rhks/parser.py	
	install -m 644 rhks/__init__.py $(DESTDIR)$(PYTHON_LIB)/rhks/__init__.py
	install -m 644 rhks/log.py $(DESTDIR)$(PYTHON_LIB)/rhks/log.py
	install -m 644 rhks/error.py $(DESTDIR)$(PYTHON_LIB)/rhks/error.py

