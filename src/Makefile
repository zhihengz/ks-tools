PYTHON_LIB=$(shell python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
BIN_BASE=/usr/bin
xml_data_files := $(wildcard data/test*.xml)
data_prefixes := $(patsubst %.xml,%,${xml_data_files})
xml_merge_data_files := data/testIncludes.xml \
	data/testMultipleCommands.xml \
	data/testPackages.xml \
	data/testActions.xml
dup_cmds_data_files := data/testSingleCommand.xml data/testMultipleCommands.xml
dup_pkgs_data_files := data/testPackages.xml data/testPackages.xml
dup_acts_data_files := data/testActions.xml data/testDuplicatePreAction.xml 
multiple_postacts_data_files := data/testActions.xml data/testMultiplePostAction.xml 
all:	ksxml2cfg kscomps test
clean:
	rm -f ksxml2cfg kscomps
	rm -fr *~ tmp
	rm -fr *.pyc
	cd rhks && $(MAKE) clean
	cd data && rm -fr *~ && rm -fr *.cfg *.txt
	cd docs && $(MAKE) clean
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
	@echo "compiling $(multiple_postacts_data_files)"; \
	python ksxml2cfg.py -o data/mpostacts.cfg $(multiple_postacts_data_files) ;
	@echo "testing kscomps.py"
	python kscomps.py -q data/compsRhcs.xml > data/compsRhcs.txt
	python kscomps.py -i rhcs -q data/compsRhcs.xml > data/compsRhcsIgnored.txt
	python kscomps.py -i rhcs -V data data/compsRhcs.xml
	python kscomps.py -o data/compsRhcsSingleMerge.txt -m data/compsRhcs.xml
	python kscomps.py -o data/compsRhcsMultipleMerge.txt -m data/compsRhcs.xml data/compsMockup.xml
	python kscomps.py -o data/compsRhcsDupMerge.txt -m data/compsRhcs.xml data/compsRhcs.xml ; \
	echo "ignore failure anyway"
	@echo "checking results..." && data/testResult.sh
ksxml2cfg:	ksxml2cfg.py
	@echo "creating shell script wrapper" && \
	echo "#!/usr/bin/python" >ksxml2cfg && \
	cat ksxml2cfg.py >>ksxml2cfg && chmod +x ksxml2cfg
kscomps:	kscomps.py
	@echo "creating shell script wrapper" && \
	echo "#!/usr/bin/python" >kscomps && \
	cat kscomps.py >>kscomps && chmod +x kscomps

install:
	mkdir -p $(DESTDIR)$(BIN_BASE)
	install -m 755 ksxml2cfg $(DESTDIR)$(BIN_BASE)
	install -m 755 kscomps $(DESTDIR)$(BIN_BASE)
	mkdir -p $(DESTDIR)$(PYTHON_LIB)/rhks
	install -m 644 rhks/components.py $(DESTDIR)$(PYTHON_LIB)/rhks/components.py
	install -m 644 rhks/parser.py $(DESTDIR)$(PYTHON_LIB)/rhks/parser.py	
	install -m 644 rhks/__init__.py $(DESTDIR)$(PYTHON_LIB)/rhks/__init__.py
	install -m 644 rhks/log.py $(DESTDIR)$(PYTHON_LIB)/rhks/log.py
	install -m 644 rhks/error.py $(DESTDIR)$(PYTHON_LIB)/rhks/error.py
	install -m 644 rhks/comps.py $(DESTDIR)$(PYTHON_LIB)/rhks/comps.py
	cd docs && $(MAKE) install DESTDIR=$(DESTDIR)
