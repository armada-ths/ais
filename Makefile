dev:
	docker compose up

build-dev:
	docker compose up --build

setup: 
	@echo "########################\n* NVM (node version manager)\n* NodeJS\n* pnpm (npm install -g pnpm)\n* Docker\n* python3 (with pip)\n########################"
	@echo "Have you installed everything listed above? [y/n] " && read ans && [ $${ans:-N} = y ]
	cp .env.example .env
	@echo "Insert production database, follow step #4 in the README.md"
	@echo "Are you ready to proceed? [y/n] " && read ans && [ $${ans:-N} = y ]
	@echo "Installing dependencies"
	npm install && npm run build
	cd apps/dashboard && pnpm install && pnpm build
	@echo "Run 'make dev' in another terminal to start the development server"
	@echo "Is the development server up? [y/n] " && read ans && [ $${ans:-N} = y ]
	./init-dev-environment.sh
