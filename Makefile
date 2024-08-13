.PHONY: ps logs status start up stop kill

ps: status

logs:
	@docker-compose logs -f

status: 
	@docker-compose ps

start: up logs

up:
	@docker-compose up -d

stop:
	@docker-compose down

kill:
	@docker-compose kill
	@docker-compose rm -f
