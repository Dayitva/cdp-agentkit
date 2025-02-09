ifneq (,$(wildcard ./.env))
	include .env
endif

export

.PHONY: run
run:
	poetry env remove python && \
	poetry install && \
	poetry run python chatbot.py
