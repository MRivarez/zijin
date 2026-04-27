# 🌌 ZiJin (子衿) | Intelligent Digital Life System

[![Version](https://img.shields.io/badge/version-2.0.0-blueviolet?style=for-the-badge&logo=github)](https://github.com/your-username/ZiJin/releases)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **“青青子衿，悠悠我心。”**
> ZiJin并非简单的对话大模型套壳，而是一个把大语言模型抽象为仅提供算力而构建的**自演化数字生命系统**。它通过构建全时域的长期记忆图谱与智能体感知闭环，致力于成为真正理解你的数字伴侣。

---

## ✨ 核心特性

### 🧠 图谱记忆与演化引擎
摒弃了传统的滑动窗口记忆。ZiJin深度整合了Neo4j等图数据库与向量检索技术，能够从海量非结构化交互中抽取实体关联，实现真正的“经验沉淀”与能力自发进化。

### 📡 边云协同架构
云端大模型和本地向量模型之间的动态调度，在保障数据隐私的同时实现极低延迟。

### 🎭 多维人格感知
打破机械式的问答。系统内置动态人格引擎，能够综合当前系统时间、交互频次与历史情感基调，赋予Agent具备温度、符合逻辑的情绪表达能力。

### 🛠️ 自主任务编排
具备系统级执行与工具调用能力。它能自主拆解复杂意图，驱动第三方API或本地脚本完成闭环任务。

---

## 🏗️ 架构现状

目前项目处于 **v2.0.0整合期**，采用单体结构（Monorepo）。前端静态资源目前由Python后端服务直接路由挂载，暂未做物理隔离，以确保快速验证与轻量化部署。

```text
ZiJin/
├── core/                   # 大脑+情感、记忆、性格、价值观系统
├── edge/                   # 小脑+心跳
├── gateways/               # 中枢：动作路由
├── genesis_web/            # 🚀 前端静态资源 (由后端直接代理)
├── zijin_os/               # 四肢：具体的动作
├── main.py                 # 服务入口
├── requirements.txt        # Python依赖清单
└── .env.example            # 环境变量配置模板
```

---

## 🚀 快速开始

### 1. 环境准备
* **Python 3.10+** 
* **数据库**: 建议本地部署或通过Docker运行Neo4j(用于知识图谱)

### 2. 获取源代码
```bash
git clone https://github.com/your-username/ZiJin.git
cd ZiJin
```

### 3. 安装依赖与配置
1. **安装核心依赖包**：
   ```bash
   pip install -r requirements.txt
   ```
2. **环境变量配置**：
   复制环境模板并填入你的大模型API Keys及图数据库连接信息：
   ```bash
   cp .env.example .env
   ```

### 4. 启动系统
执行主入口文件，启动服务（以常见的 ASGI 运行方式为例）：
```bash
python main.py
# 或使用 uvicorn: uvicorn main:app --host 0.0.0.0 --port 8000
```
服务启动后，直接在浏览器访问对应端口（如 `http://localhost:8000`）即可加载前端交互界面。

---

## 📅 未来展望

- [ ] **语音/视觉/听觉多模态接入**：基于TTS/OpenCV/Whisper等赋予系统更多的感知力。
- [ ] **记忆碎片自清理机制**：引入记忆衰退与遗忘算法，优化大规模图谱的检索性能。

---

