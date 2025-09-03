# Vector DB Interface Server
This Repository contains the FastAPI interface for Milvus DB.
You can perform the following operations
- Create Database
- Delete Database
- Create Collection
- Delete Collection
- Insert Chunk
- Retrieve Chunk
- Delete Chunk

## Clone the and run the repository
```bash
git clone https://github.com/vsuhas9/vector-db-interface.git
cd vector-db-interface
docker compose up --build -d
docker run -d --name ollama --network generic --restart always -v ollama:/root/.ollama -p 11434:11434 ollama/ollama
docker exec -it ollama /bin/bash -c "ollama pull nomic-embed-text"
```


## Optinal: Run using UV Package Manager
```bash
uv sync --locked
uv run main.py
```