# mcp_server.py
# 专门用于 RAG 检索的 MCP Server
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import sys
import os

# 强制使用国内镜像站下载模型，速度快且能连通
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import torch
import json

# --- LlamaIndex 引用 ---
from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever

# ==========================================
# 1. 配置加载
# ==========================================
# 优先加载当前目录下的 .env
current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root is DDBcoding/
project_root = os.path.dirname(os.path.dirname(current_dir))

load_dotenv(os.path.join(current_dir, ".env"))

MCP_SERVER_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_SERVER_PORT = int(os.getenv("MCP_PORT", 7731))
MCP_NAME = "DDB_RAG_Service"

env_persist = os.getenv("PERSIST_DIR", "./storage_data")
env_db_uri = os.getenv("DB_URI", "./lancedb_data")

PERSIST_DIR = os.path.abspath(os.path.join(project_root, env_persist))
DB_URI = os.path.abspath(os.path.join(project_root, env_db_uri))
MODEL_NAME = "BAAI/bge-m3"

# ==========================================
# 2. 初始化资源
# ==========================================
print("🚀 正在启动 RAG MCP Server...")

device_type = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🖥️  Compute Device: {device_type.upper()}")

Settings.llm = None
Settings.embedding_model = HuggingFaceEmbedding(
    model_name=MODEL_NAME, 
    device=device_type
)
Settings.chunk_size = 512

global_retriever = None

try:
    if not os.path.exists(PERSIST_DIR) or not os.path.exists(DB_URI):
        print("⚠️  Warning: Index not found. Please run 'ingest.py' first.")
    else:
        print("📂 Loading Vector Store...")
        vector_store = LanceDBVectorStore(uri=DB_URI, table_name="my_vectors")
        storage_context = StorageContext.from_defaults(
            persist_dir=PERSIST_DIR, 
            vector_store=vector_store
        )
        
        index = VectorStoreIndex.from_vector_store(
            vector_store, 
            storage_context=storage_context,
            embed_model=Settings.embedding_model
        )
        
        vector_retriever = index.as_retriever(similarity_top_k=10)
        
        all_nodes = list(storage_context.docstore.docs.values())
        if all_nodes:
            bm25_retriever = BM25Retriever.from_defaults(
                nodes=all_nodes, 
                similarity_top_k=10,
                verbose=False
            )
            
            global_retriever = QueryFusionRetriever(
                [vector_retriever, bm25_retriever],
                similarity_top_k=10,
                num_queries=1, 
                use_async=False,
            )
            print("✅ Hybrid Retrieval System Ready!")
        else:
            print("⚠️  Docstore is empty.")
except Exception as e:
    print(f"❌ Initialization Failed: {e}")

# ==========================================
# 3. 定义 MCP Tool
# ==========================================
mcp = FastMCP(
    name=MCP_NAME, 
    host=MCP_SERVER_HOST, 
    port=MCP_SERVER_PORT
)

@mcp.tool()
def search_knowledge_base(query: str) -> str:
    """
    Search the local markdown knowledge base for relevant snippets.
    Use this to find documentation, examples, or guides before writing code.
    Running on GPU for fast embedding generation.
    """
    print(f"🔍 [Search] Query: {query}")
    
    if global_retriever is None:
        return "Error: Retrieval system not initialized. Please run ingest.py first."
    try:
        results = global_retriever.retrieve(query)
        output = []
        for node in results:
            output.append({
                "score": round(node.score, 4),
                "file": node.metadata.get("file_name"),
                "content": node.text
            })
        return json.dumps(output, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Search Error: {str(e)}"

if __name__ == "__main__":
    print(f"📡 MCP Server Listening on {MCP_SERVER_HOST}:{MCP_SERVER_PORT}")
    mcp.run()
