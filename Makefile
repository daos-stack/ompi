NAME    := ompi
SRC_EXT := gz
SOURCE   = https://github.com/open-mpi/$(NAME)/archive/v$(VERSION).tar.$(SRC_EXT)

PR_REPOS      := libfabric@PR-16
sl42_REPOS    := https://download.opensuse.org/repositories/science:/HPC/openSUSE_Leap_42.3/
sle12_REPOS   := https://download.opensuse.org/repositories/science:/HPC:/SLE12SP3_Missing/SLE_12_SP3/ \
	         $(sl42_REPOS)
sl15_REPOS    := https://download.opensuse.org/repositories/science:/HPC/openSUSE_Leap_15.1/

include packaging/Makefile_packaging.mk