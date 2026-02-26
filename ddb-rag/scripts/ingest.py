import os
# --- 新增这一行 ---
# 强制使用国内镜像站下载模型，速度快且能连通
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
import torch  # 引入 torch 用来检查 GPU
from llama_index.core import (
    SimpleDirectoryReader, 
    StorageContext, 
    VectorStoreIndex, 
    Settings
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# --- 核心修改部分开始 ---

# 1. 检查 GPU 是否可用
device_type = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 正在使用的计算设备: {device_type.upper()}")
if device_type == "cuda":
    print(f"   显卡型号: {torch.cuda.get_device_name(0)}")

# 2. 设置 Embedding 模型
# 既然有 A30，直接用 BAAI/bge-m3，效果比 small 好很多，支持多语言和长文本
# device参数强制让它跑在 GPU 上
Settings.embedding_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-m3", 
    device=device_type 
)
Settings.chunk_size = 512

# --- 核心修改部分结束 ---

# 准备存储路径
# 优先加载当前目录 .env
current_dir = os.path.dirname(os.path.abspath(__file__))
# current_dir is inside scripts/rag/
project_root = os.path.dirname(os.path.dirname(current_dir)) 
# project_root is DDBcoding/

# Load local .env
load_dotenv(os.path.join(current_dir, ".env"))

# Get paths from env or use defaults relative to project root
# .env might contain relative paths provided by user, usually relative to project root (CWD)
env_persist = os.getenv("PERSIST_DIR", "./storage_data")
env_db_uri = os.getenv("DB_URI", "./lancedb_data")
env_docs = os.getenv("DOCS_DIR", "./references")

# Convert to absolute paths based on project_root for safety
PERSIST_DIR = os.path.abspath(os.path.join(project_root, env_persist))
DB_URI = os.path.abspath(os.path.join(project_root, env_db_uri))
DOCS_DIR = os.path.abspath(os.path.join(project_root, env_docs))
MODEL_NAME = "BAAI/bge-m3"

def ingest_documents():
    print(f"开始扫描目录: {DOCS_DIR}")
    
    vector_store = LanceDBVectorStore(uri=DB_URI, table_name="my_vectors")
    
    try:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        docstore = storage_context.docstore
        print("✅ 加载了已有的 Docstore 状态。")
    except:
        docstore = SimpleDocumentStore()
        storage_context = StorageContext.from_defaults(docstore=docstore)
        print("🆕 创建了新的 Docstore。")

    try:
        # 读取文件
        documents = SimpleDirectoryReader(DOCS_DIR, recursive=True, required_exts=[".md"]).load_data()
        if not documents:
            print("⚠️ 目录中没有找到 .md 文件。")
            return
    except Exception as e:
        print(f"❌ 读取文件出错: {e}")
        return

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=50),
            Settings.embedding_model, # 这里会调用 GPU
        ],
        vector_store=vector_store,
        docstore=docstore,
        cache=IngestionCache(), 
    )

    print("🔥 开始运行管道 (GPU 加速中)...")
    nodes = pipeline.run(documents=documents, show_progress=True)
    
    storage_context.persist(persist_dir=PERSIST_DIR)
    
    print(f"🎉 处理完成！本次处理了 {len(nodes)} 个分块。")

if __name__ == "__main__":
    ingest_documents()
