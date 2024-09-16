.PHONY: install dev build-dev

.DEFAULT_GOAL := install

dev:
	docker compose up

build-dev:
	docker compose up --build

install: prerequisites
	@echo "########################\n* NVM (node version manager)\n* Docker\n* python3 (with pip)\n########################"
	@echo "Have you installed everything listed above? [y/n] " && read ans && [ $${ans:-N} = y ]
	cp .env.example .env
	@echo "Insert production database, follow step #2 in the README"
	@echo "Are you ready to proceed? [y/n] " && read ans && [ $${ans:-N} = y ]
	@echo "Installing dependencies"
	source $(HOME)/.nvm/nvm.sh;\
	nvm install 16 && nvm use 16 && npm install && npm run build && \
	cd apps/dashboard && nvm install 20 && nvm use 20 && npm install -g pnpm && pnpm install && pnpm run build
	@echo "Run 'make dev' in another terminal to start the development server"
	@echo "Is the development server up? [y/n] " && read ans && [ $${ans:-N} = y ]
	./init-dev-environment.sh
