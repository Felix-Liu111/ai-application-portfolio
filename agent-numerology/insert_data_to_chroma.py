from langchain_chroma import Chroma
from models import get_embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ====================== 配置 ======================
PERSIST_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "local_documents"

# ====================== 风水知识数据 ======================
office_fengshui_data = [
    "办公室座位不宜背对大门，容易让人缺乏安全感，影响工作专注力。",
    "办公室座位不宜在横梁下方，横梁压顶会造成精神压力大，工作不顺。",
    "办公桌上不宜堆放杂乱物品，整洁的桌面能提升气场，提高工作效率。",
    "办公室光线要充足，阴暗环境容易导致情绪低落，思维不清晰。",
    "座位不宜正对厕所，厕所浊气会影响健康与工作运势。",
    "办公座位宜有实墙依靠，代表有贵人相助，工作稳定。",
    "办公室不宜摆放尖锐植物，如仙人掌，易引发是非口角。",
    "办公桌上可摆放绿植，如绿萝、发财树，提升生机与财运。",
    "文件资料应及时收纳，不宜散乱，代表思路清晰、运势顺畅。",
    "办公室颜色宜柔和，避免过于刺眼的颜色，利于情绪稳定。",
    "座位不宜正对镜子，容易心神不宁，影响决策判断。",
    "办公室保持空气流通，清新空气能提升团队士气和工作状态。",
    "财位宜明亮整洁，不宜受压，办公室财位通常在进门对角线位置。",
    "避免坐在通道直冲的位置，容易受干扰，难以集中精神。",
    "电脑、电器不宜过多集中摆放，磁场过强易让人疲劳烦躁。"
]

# ====================== 初始化向量库 ======================
embedding = get_embeddings()

vectordb = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=embedding,
    collection_name=COLLECTION_NAME
)

# ====================== 文本切割（适配长文本） ======================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

split_docs = text_splitter.create_documents(office_fengshui_data)

# ====================== 插入向量库 ======================
print("正在插入办公室风水知识到 Chroma 向量库...")
vectordb.add_documents(split_docs)

print(f"插入完成！共插入 {len(split_docs)} 条风水知识数据。")
print("向量库已保存到：", PERSIST_DIRECTORY)
