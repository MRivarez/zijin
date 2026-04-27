<script setup>
const props = defineProps({ 
  isActive: Boolean,
  config: Object
})
const emits = defineEmits(['save'])

const saveConfig = async () => {
  console.log("⚡ [灵枢运转] 准备写入配置:", props.config)
  try {
    const res = await fetch('http://127.0.0.1:8000/api/config/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(props.config)
    })
    const data = await res.json()
    console.log("⚡ [灵枢运转] 后端响应:", data.message)
    emits('save')
  } catch (error) {
    alert("灵枢连接失败，请检查FastAPI后端是否启动！")
    console.error(error)
  }
}
</script>

<template>
  <section class="screen" :class="{ 'is-active': isActive }">
    <div class="content-box fade-up">
      <div class="scroll-panel">
        <div class="panel-header">
          <h2 class="title-ink">灵 枢</h2>
          <p class="subtitle-ink">打通天地经脉，锚定物理坐标</p>
        </div>

        <div class="config-grid">
          <div class="config-group">
            <h3>智脑枢纽 (算力坍缩)</h3>
            <p class="config-desc">定义数字生命的认知模型。大语言模型决定其「思维深度」，向量化模型决定其「记忆广度」。</p>
            <div class="input-row">
              <span class="label-with-hint">大语言模型<br><small>(思考核心)</small></span>
              <input type="text" v-model="config.LLM_MODEL" placeholder="如: glm-4-flash" />
            </div>
            <div class="input-row">
              <span class="label-with-hint">向量化模型<br><small>(海马体驱动)</small></span>
              <input type="text" v-model="config.EMBEDDING_MODEL" placeholder="如: BAAI/bge-small-zh-v1.5" />
            </div>
            <div class="input-row">
              <span>API_KEY</span>
              <input type="password" v-model="config.LLM_API_KEY" placeholder="sk-xxxxxxxxxxx" />
            </div>
            <div class="input-row">
              <span>BASE_URL</span>
              <input type="text" v-model="config.LLM_BASE_URL" />
            </div>
          </div>

          <div class="config-group">
            <h3>物理躯壳</h3>
            <div class="input-row">
              <span>造物主QQ</span>
              <input type="text" v-model="config.CREATOR_QQ" placeholder="接收消息的账号" />
            </div>
            <div class="input-row">
              <span>网关Token</span>
              <input type="password" v-model="config.NAPCAT_TOKEN" placeholder="若未设置可留空" />
            </div>
          </div>

          <div class="config-group">
            <h3>图谱灵脉</h3>
            <div class="input-row">
              <span>URI / USER</span>
              <input type="text" v-model="config.NEO4J_URI" class="half-input"/>
              <input type="text" v-model="config.NEO4J_USER" class="half-input"/>
            </div>
            <div class="input-row">
              <span>PASSWORD</span>
              <input type="password" v-model="config.NEO4J_PASS" placeholder="数据库密码" />
            </div>
          </div>
        </div>
        
        <div style="text-align: center; margin-top: 20px;">
          <button class="sys-btn-stamp" @click="saveConfig">贯通经脉</button>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* ==========================================
   卷轴/信笺拟态 (灵枢、赋魂专用防污染类)
   ========================================== */
.scroll-panel {
  width: clamp(340px, 65vw, 800px);
  background: rgba(250, 248, 243, 0.9); /* 米黄色宣纸底 */
  border: 1px solid rgba(0,0,0,0.05);
  border-radius: 4px;
  padding: 40px;
  box-shadow: 
    0 15px 40px rgba(28, 48, 56, 0.1),
    inset 0 0 50px rgba(180, 170, 150, 0.1); 
  text-align: left;
  position: relative;
}

/* 顶部画轴隐喻 */
.scroll-panel::before {
  content: ''; position: absolute; top: 0; left: -20px; right: -20px; height: 10px;
  background: linear-gradient(to bottom, #d2cdb5, #aba58a);
  border-radius: 5px;
  box-shadow: 0 5px 10px rgba(0,0,0,0.1);
}

.panel-header { text-align: center; margin-bottom: 30px; }

.config-group { margin-bottom: 25px; }
.config-group h3 { font-size: 1.1rem; color: #1c3038; margin-bottom: 15px; font-weight: 600; border-bottom: 1px dotted #829a9f; padding-bottom: 5px; }

.input-row { display: flex; align-items: center; margin-bottom: 15px; }
.input-row span { width: 120px; font-size: 0.95rem; color: #5a7b86; }

/* 毛笔划痕输入框 */
.input-row input {
  flex: 1; padding: 8px 12px; border: none; background: transparent;
  color: #1c3038; font-family: 'Noto Serif SC', serif; font-size: 1rem;
  border-bottom: 2px solid transparent; outline: none; transition: all 0.4s;
  /* 水墨底纹 */
  background-image: linear-gradient(#b0c6ce, #b0c6ce);
  background-size: 0% 2px; background-repeat: no-repeat; background-position: left bottom;
}
.input-row input:focus {
  background-size: 100% 2px;
}
.input-row input::placeholder { color: #a4b6bc; }
.half-input { width: 48%; margin-right: 4%; }
.half-input:last-child { margin-right: 0; }

.sys-btn-stamp {
  padding: 10px 20px; background: transparent; color: #1c3038; border: none;
  font-family: 'Noto Serif SC', serif; font-weight: 600; font-size: 1.5rem; letter-spacing: 8px; cursor: pointer;
  transition: all 0.5s ease; position: relative; 
}
.sys-btn-stamp::after {
  content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
  width: 0%; height: 3px; background: #c9372c; border-radius: 5px; transition: width 0.5s cubic-bezier(0.7, 0, 0.3, 1);
}
.sys-btn-stamp:hover { color: #c9372c; letter-spacing: 12px; }
.sys-btn-stamp:hover::after { width: 80%; }
.config-desc {
  font-size: 0.85rem;
  color: #5a7b86; /* 加深颜色，从 829a9f 调深 */
  margin-top: -10px;
  margin-bottom: 20px;
  line-height: 1.4;
}

.label-with-hint {
  line-height: 1.2;
}

.label-with-hint small {
  font-size: 0.75rem;
  color: #6a8b96; /* 同样加深 hint 颜色 */
  font-weight: normal;
}
</style>
