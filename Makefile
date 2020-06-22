NAME      := MACSio
SRC_EXT   := gz

PR_REPOS := $(shell set -x; git show -s --format=%B | sed -ne 's/^PR-repos: *\(.*\)/\1/p')

include packaging/Makefile_packaging.mk

test:
	$(call install_repos,$(NAME)@$(BRANCH_NAME):$(BUILD_NUMBER))
	yum -y install $(NAME)
