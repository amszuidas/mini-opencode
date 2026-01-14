install:
	uv sync

build:
	uv build

dev:
	uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.12 langgraph dev --no-browser --allow-blocking
