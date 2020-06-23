NAME      := MACSio
SRC_EXT   := gz

include packaging/Makefile_packaging.mk

test:
	$(call install_repos,$(NAME)@$(BRANCH_NAME):$(BUILD_NUMBER) json-cwx)
	yum -y install $(NAME)
