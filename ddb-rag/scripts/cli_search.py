import torch
import json
import os

# 强制使用国内镜像站下载模型，速度快且能连通
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from llama_index.core import (
    StorageContext, 
    VectorStoreIndex, 
    Settings
)
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever

# ================= 配置区域 =================
device_type = "cuda" if torch.cuda.is_available() else "cpu"

# 1. 禁用 LLM (防止报错)
Settings.llm = None 

# 2. 设置 Embedding
Settings.embedding_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-m3", 
    device=device_type
)
Settings.chunk_size = 512

PERSIST_DIR = "./storage_data" 
DB_URI = "./lancedb_data"      
# ===========================================

def search(query_text):
    print(f"🔎 正在搜索: {query_text}")

    if not os.path.exists(PERSIST_DIR) or not os.path.exists(DB_URI):
        print("❌ 错误：找不到数据文件。请先运行 ingest.py")
        return []

    vector_store = LanceDBVectorStore(uri=DB_URI, table_name="my_vectors")
    
    try:
        storage_context = StorageContext.from_defaults(
            persist_dir=PERSIST_DIR, 
            vector_store=vector_store
        )
        index = VectorStoreIndex.from_vector_store(
            vector_store, 
            storage_context=storage_context,
            embed_model=Settings.embedding_model
        )
    except Exception as e:
        print(f"❌ 加载索引失败: {e}")
        return []

    # 准备检索器
    vector_retriever = index.as_retriever(similarity_top_k=5)
    
    all_nodes = list(storage_context.docstore.docs.values())
    if not all_nodes:
        return []

    bm25_retriever = BM25Retriever.from_defaults(
        nodes=all_nodes, 
        similarity_top_k=5,
        verbose=False
    )

    # ==========================================
    # 【修复点】这里删除了 mode="reciprocal_rank"
    # ==========================================
    retriever = QueryFusionRetriever(
        [vector_retriever, bm25_retriever],
        similarity_top_k=5,
        num_queries=1, 
        # mode="reciprocal_rank",  <-- 删掉这一行，默认就是 RRF 算法
        use_async=False,
    )
    
    results = retriever.retrieve(query_text)
    
    output = []
    for node in results:
        output.append({
            "score": round(node.score, 4),
            "text": node.text, 
            "file_name": node.metadata.get("file_name")
        })
    return output

if __name__ == "__main__":
    import time
    import sys
    
    # 支持命令行参数
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "mavg" 
    
    start = time.time()
    try:
        res = search(query)
        end = time.time()
        print(f"\n⏱️ 耗时: {end - start:.4f} 秒")
        
        if res:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print("没有找到相关结果。")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
