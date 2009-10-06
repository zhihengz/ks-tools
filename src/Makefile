all:	clean
clean:
	rm -fr *~
	rm -fr *.pyc
	cd rhks && $(MAKE) clean
	cd data && rm -fr *~ && rm -fr *.cfg
test:
	@echo "testing ksxml2cfg.py"
	@for f in data/*.xml; \
	do \
		echo "compiling $$f" && \
		python ksxml2cfg.py "$$f";\
	done
