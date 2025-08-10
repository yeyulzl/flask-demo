# 🌟 INFJ灵感管理器 - 微信小程序

> 专为INFJ人格打造的思想火花收集工具，随时随地记录灵感并智能分析

**在线体验**：扫码体验（生成小程序二维码贴在这里）  
**技术栈**：微信小程序前端 + Python Flask后端 + 微信云托管

## ✨ 功能亮点
1. **极速记录** - 语音转文字快速捕捉灵感  
2. **情感标记** - 自动分析记录时的情绪状态  
3. **安全同步** - 数据加密存储到云端  
4. **灵感孵化** - 定期提醒回顾重要灵感（开发中）

## 🛠 本地运行指南

### 前端准备
1. 安装微信开发者工具  
2. 克隆本仓库：`git clone https://github.com/你的账号/项目名.git`  
3. 导入`miniprogram`目录

### 后端部署
```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量（云托管自动注入）
export DB_URL="your_database_url"

# 启动服务
python app.py
```

## 🔧 项目结构
```
.
├── miniprogram/           # 小程序前端代码
│   ├── pages/             # 页面目录
│   └── app.js             # 全局逻辑
├── server/                # Python后端
│   ├── app.py             # 主程序入口
│   └── requirements.txt   # 依赖列表
└── README.md              # 你现在看的文档
```

## 🤝 参与贡献
1. Fork本仓库  
2. 新建分支：`git checkout -b feature/新功能`  
3. 提交代码并推送到分支  
4. 提交Pull Request

> **致敬INFJ的完美主义**：本项目欢迎文档优化类PR！
