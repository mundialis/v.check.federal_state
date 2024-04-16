MODULE_TOPDIR = ../..

PGM = v.check.federal_state

include $(MODULE_TOPDIR)/include/Make/Script.make

python-requirements:
	pip install -r requirements.txt

default: python-requirements script
