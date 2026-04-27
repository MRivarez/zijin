<script setup>
import { ref } from 'vue'

const props = defineProps({ isActive: Boolean, creatorName: String })
const emits = defineEmits(['slide-next'])

const isDragging = ref(false)
const uploadedFile = ref(null)
const isLoading = ref(false)

const handleDrop = (e) => {
  isDragging.value = false
  const files = e.dataTransfer.files
  if (files.length > 0 && files[0].name.endsWith('.txt')) {
    uploadedFile.value = files[0]
  } else {
    alert('子衿只能读取 .txt 格式的记忆刻痕...')
  }
}

const injectMemory = async () => {
  if (!uploadedFile.value) return

  const formData = new FormData()
  formData.append('file', uploadedFile.value)
  if (props.creatorName) {
    formData.append('creatorName', props.creatorName)
  }

  isLoading.value = true
  try {
    console.log(`[记忆捕获] 正在向深渊传输: ${uploadedFile.value.name}`)
    const res = await fetch('http://127.0.0.1:8000/api/memory/upload', {
      method: 'POST',
      body: formData 
    })
    const data = await res.json()
    console.log("🌊 [记忆吞噬] 后端响应:", data.message)
    emits('slide-next') 
  } catch (error) {
    alert("记忆融汇失败！")
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <section class="screen" :class="{ 'is-active': isActive }">
    <div class="content-box fade-up">
      <h2 class="title-ink color-white-shadow">忆 往</h2>
      <p class="subtitle-ink color-white-shadow">将过往聊天的只言片语，倾倒于此</p>
      
      <div
          class="memory-well"
          :class="{ 'well-active': isDragging, 'well-filled': uploadedFile }"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
      >
        <div class="well-border"></div>
        <div v-if="isLoading" class="pool-hint">
          <span class="icon glow-pulse">༄</span>
          <p>记忆融汇中，静候片刻...</p>
        </div>
        <div v-else-if="!uploadedFile" class="pool-hint">
          <span class="icon">༄</span>
          <p>将 .txt 记忆刻卷拖至井中</p>
        </div>
        <div v-else class="pool-success">
          <span class="icon">✦</span>
          <p class="filename">{{ uploadedFile.name }}</p>
          <p class="hint-small">记忆已沉淀</p>
        </div>
      </div>
      
      <Transition name="fade">
        <button v-if="uploadedFile && !isLoading" class="btn-stamp-float" @click="injectMemory">融汇记忆</button>
      </Transition>
    </div>
  </section>
</template>

<style scoped>
/* ==========================================
   忆往水潭
   ========================================== */
.memory-well { 
  position: relative;
  width: clamp(280px, 40vw, 450px); height: clamp(280px, 40vw, 450px); 
  border-radius: 50%;
  display: flex; justify-content: center; align-items: center; 
  transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1); 
  background: rgba(255, 255, 255, 0.1); 
  backdrop-filter: blur(5px);
  cursor: pointer; 
  box-shadow: inset 0 0 50px rgba(255,255,255,0.2), 0 20px 40px rgba(0,0,0,0.2);
}
/* 东窗棂式八角或圆形边框 */
.well-border {
  position: absolute; inset: -10px; border-radius: 50%;
  border: 1px dashed rgba(255, 255, 255, 0.6);
  animation: spinSlow 30s linear infinite;
}
@keyframes spinSlow { 100% { transform: rotate(360deg); } }

.memory-well.well-active { 
  transform: scale(1.05) translateY(-10px); background: rgba(255, 255, 255, 0.25);
}

/* ==== 增加忆往中古井的文字和图案醒目度 ==== */
.pool-hint, .pool-success { 
  text-align: center; 
  color: #fff; /* 以纯白色辅以极重极厚的纯黑阴影打底 */
  text-shadow: 0 4px 15px rgba(0,0,0,1), 0 0 25px rgba(0,0,0,0.8); 
  font-weight: 600;
  letter-spacing: 2px;
}
.pool-hint p, .pool-success p { font-size: 1.2rem; }
.pool-success .filename { font-size: 1.4rem; color: #e8dcc4; margin-bottom: 5px; }

.icon { 
  font-size: 4rem; 
  display: block; 
  margin-bottom: 12px; 
  color: #c9372c; /* 朱砂色点缀 */
  filter: drop-shadow(0 0 10px rgba(255,255,255,0.7)); /* 赋予图标光晕 */
  animation: floatIcon 3s ease-in-out infinite; 
}

.glow-pulse {
  animation: windGlow 1.5s ease-in-out infinite alternate !important;
}
@keyframes windGlow { 
  0% { filter: drop-shadow(0 0 5px rgba(201, 55, 44, 0.4)); transform: scale(1); opacity: 0.7; } 
  100% { filter: drop-shadow(0 0 25px rgba(255, 255, 255, 0.9)); transform: scale(1.15); opacity: 1; } 
}
@keyframes floatIcon { 0%, 100% { transform: translateY(0) scale(1); filter: drop-shadow(0 0 5px rgba(255,255,255,0.4)); } 50% { transform: translateY(-10px) scale(1.1); filter: drop-shadow(0 0 15px rgba(255,255,255,0.9)); } }

.btn-stamp-float {
  padding: 10px 20px; background: transparent; color: #0b1115; border: none;
  font-family: 'Noto Serif SC', serif; font-weight: 600; font-size: 1.5rem; letter-spacing: 8px; cursor: pointer;
  transition: all 0.5s ease; position: relative; text-shadow: 0 0 12px rgba(255,255,255,0.9);
}
.btn-stamp-float::after {
  content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
  width: 0%; height: 3px; background: #c9372c; border-radius: 5px; transition: width 0.5s cubic-bezier(0.7, 0, 0.3, 1);
}
.btn-stamp-float:hover { color: #c9372c; letter-spacing: 12px; text-shadow: 0 0 15px rgba(255,255,255,1); }
.btn-stamp-float:hover::after { width: 80%; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.5s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
