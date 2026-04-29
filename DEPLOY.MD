# 🚀 ZiJin Digital Life System v2.1.0 部署指南
> ZiJin是一套基于大语言模型与双轨记忆（Neo4j长期图谱 + Mem0短期向量）的数字生命系统。
> 本版本已全面实现容器化（Docker Compose）部署，包含精神中枢（FastAPI）、物理躯壳网关（NapCatQQ）、记忆底层与创世卷轴（Vue3）。
# 📦 环境准备
在开始部署之前，请确保您的服务器或本地机器已安装以下基础运行环境：
- Git
- Docker(Engine版本 >= 20.10)
- Docker Compose(版本 >= 2.0)
# 第一步：获取源码
克隆本仓库到本地，并进入项目根目录：
```shell
git clone https://github.com/你的用户名/ZiJin.git
cd ZiJin
```
# 第二步：环境配置
系统需要基础的“身份与认知参数”才能启动。
使用文本编辑器打开`backend/.env`，并极其严谨地填写以下核心参数：
```shell
# ==========================================
# 1. 基础认知模型配置(此处以智谱GLM为例)
# ==========================================
LLM_API_KEY=你的大语言模型API KEY
LLM_MODEL=glm-4-flash
EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5

# ==========================================
# 2. 物理躯壳与造物主身份
# ==========================================
# 造物主的QQ号（极其重要，ZiJin将只理会该账号的消息）
CREATOR_QQ=123456789
# 内部通信安全密钥（需与后续NapCat WebUI中的Token保持绝对一致）
QQ_ACCESS_TOKEN=zijin2026

# ==========================================
# 3. 记忆图谱底层配置
# ==========================================
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASS=zijin2026
```
⚠️ `docker-compose.yml`中的相关配置务必与此保持一致。
# 第三步：容器启动
在项目根目录（包含 docker-compose.yml 的位置），执行以下命令拉起整个微服务集群。
```shell
docker-compose up -d --build
```
首次启动需要编译Python依赖和Vue前端，可能需要3~5分钟，请耐心等待。建议直接下载release中的完整版。
# 第四步：唤醒躯壳
此时，AI大脑已经在等待网关接通。我们需要完成QQ的扫码授权：
打开浏览器，访问NapCat管理后台：http://localhost:6099
使用准备作为“ZiJin躯壳”的QQ手机端，扫描网页上的二维码完成登录。
登录成功后，可以检查一下网络配置。
- 在左侧菜单点击【网络配置】(Network)。
- 找到配置列表中3001端口的WebSocket Server（正向WS）。
- ⚠️ 极其关键的一步：在配置详情的Token栏中，填入你在.env文件里写的QQ_ACCESS_TOKEN的值（例如：zijin2026）。
- 点击保存。
# 第五步：系统验收与心跳监测
检查各个神经节是否已成功贯通：
## 查看大脑日志
```shell
docker logs --tail 50 -f zijin_core
```
如果你看到[感知网关]脑机接口连接成功和[海马体]加载成功的绿色提示，说明灵肉已合一！
## 访问创世控制台
打开浏览器访问：http://localhost（或者直接访问 http://127.0.0.1:80）
即可进入创世卷轴，查看实时情绪张量面板与系统状态。
## 最终激活测试
用你的“造物主大号”向ZiJin发送一句：“青青子衿”，等待她的第一次回应！
# 📂 目录结构与数据持久化
系统运行后，会在根目录下自动生成data文件夹，该文件夹包含所有无法轻易抹除的记忆与状态：
```shell
Plaintext
ZiJin/
├── backend/            # 精神中枢
├── genesis_web/        # 创世卷轴前端
├── docker-compose.yml  # 编排图纸
└── data/               # 💾 持久化数据卷(请勿随意删除)
    ├── neo4j_data/     # 长期语义图谱
    ├── .mem0_db/       # 短期情节向量库
    ├── napcat_config/  # 躯壳网络配置
    └── napcat_qq/      # QQ 登录Session(保证重启免扫码)
```
# 💡 日常运维指令：
```shell
停止系统：docker-compose down

查看整体日志：docker-compose logs -f

重置记忆（危险）：docker-compose down -v
```