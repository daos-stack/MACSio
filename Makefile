NAME      := MACSio
SRC_EXT   := gz
TEST_PACKAGES := $(NAME) $(NAME)-mpich $(NAME)-openmpi3

include packaging/Makefile_packaging.mk
