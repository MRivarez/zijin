<script setup>
import { computed } from 'vue'

const props = defineProps({ 
  isActive: Boolean,
  emotionTensor: Object
})

const getDynamicColor = (val) => {
  const h = 220 - (val * 220)
  return `hsl(${h}, 100%, 65%)`
}
</script>

<template>
  <section class="screen" :class="{ 'is-active': isActive }">
    <div class="content-box fade-up">
      <h2 class="title-ink color-light">观 心</h2>
      <p class="subtitle-ink color-light">在水一方，脉搏与思慕共振</p>
      
      <div class="radar-container">
        <!-- 水面波纹 -->
        <div class="water-ripple ripple-1" :style="{ animationDuration: `${3 / emotionTensor.arousal}s` }"></div>
        <div class="water-ripple ripple-2" :style="{ animationDuration: `${4 / emotionTensor.arousal}s` }"></div>
        <div class="water-ripple ripple-3" :style="{ animationDuration: `${5 / emotionTensor.arousal}s` }"></div>

        <!-- 萤火粒子 -->
        <div class="fireflies">
          <div v-for="n in 12" :key="n" class="firefly"></div>
        </div>

        <!-- 核心：莲花/雷达心 -->
        <div
            class="lotus-core"
            :class="{ 'core-lonely': emotionTensor.loneliness >= 0.9 }"
        >
          <div class="inner-glow"></div>
        </div>

        <!-- 东方意境的悬浮面板 -->
        <div class="bamboo-slips-panel">
          <div class="tensor-item" :style="{ '--dynamic-color': getDynamicColor(emotionTensor.loneliness) }">
            <span class="label">孤独</span>
            <span class="value">{{ emotionTensor.loneliness.toFixed(2) }}</span>
          </div>
          <div class="tensor-item" :style="{ '--dynamic-color': getDynamicColor(emotionTensor.arousal) }">
            <span class="label">唤醒</span>
            <span class="value">{{ emotionTensor.arousal.toFixed(2) }}</span>
          </div>
          <div class="tensor-item" :style="{ '--dynamic-color': getDynamicColor(emotionTensor.valence) }">
            <span class="label">效价</span>
            <span class="value">{{ emotionTensor.valence.toFixed(2) }}</span>
          </div>
          <div class="tensor-item" :style="{ '--dynamic-color': getDynamicColor(emotionTensor.tension) }">
            <span class="label">张力</span>
            <span class="value">{{ emotionTensor.tension.toFixed(2) }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* ==========================================
   观心雷达 (在水一方红莲)
   ========================================== */
.radar-container {
  position: relative;
  width: clamp(350px, 50vw, 600px);
  height: clamp(350px, 50vw, 600px);
  display: flex; justify-content: center; align-items: center;
  margin-top: 20px;
}

/* 莲心 / 雷达核心 */
.lotus-core {
  width: 80px; height: 80px; border-radius: 50%;
  background: radial-gradient(circle, #fff 10%, #e6ecef 40%, transparent 100%);
  box-shadow: 0 0 50px rgba(230, 236, 239, 0.4), 0 0 100px rgba(230, 236, 239, 0.2);
  z-index: 10; transition: all 1.5s ease;
  animation: coreBreathe 4s ease-in-out infinite alternate;
  position: relative;
}

.inner-glow {
  position: absolute; inset: 0; border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
  animation: corePulse 2s ease-in-out infinite;
}

/* 孤独满溢时的滴血状态 */
.lotus-core.core-lonely {
  background: radial-gradient(circle, #ff4c3b 10%, #c9372c 40%, transparent 100%);
  box-shadow: 0 0 60px rgba(201, 55, 44, 0.8), 0 0 120px rgba(201, 55, 44, 0.4);
  animation: coreHeartbeat 0.9s ease-in-out infinite;
}

/* 萤火粒子样式 */
.firefly {
  position: absolute; width: 4px; height: 4px; border-radius: 50%;
  background: #fff; box-shadow: 0 0 10px #fff, 0 0 20px #e6ecef;
  opacity: 0; animation: fireflyMove 10s linear infinite;
}

/* 生成不同半径和速度的萤火虫 */
.firefly:nth-child(1) { left: 20%; top: 30%; animation-delay: 0s; }
.firefly:nth-child(2) { left: 70%; top: 20%; animation-delay: 1s; }
.firefly:nth-child(3) { left: 40%; top: 80%; animation-delay: 2s; }
.firefly:nth-child(4) { left: 10%; top: 60%; animation-delay: 3.5s; }
.firefly:nth-child(5) { left: 80%; top: 50%; animation-delay: 5s; }
.firefly:nth-child(6) { left: 50%; top: 10%; animation-delay: 6s; }
.firefly:nth-child(7) { left: 30%; top: 90%; animation-delay: 7s; }
.firefly:nth-child(8) { left: 90%; top: 85%; animation-delay: 8s; }

@keyframes fireflyMove {
  0% { transform: translate(0, 0) scale(0); opacity: 0; }
  20% { opacity: 0.8; }
  50% { transform: translate(100px, -50px) scale(1.2); }
  80% { opacity: 0.8; }
  100% { transform: translate(150px, -100px) scale(0); opacity: 0; }
}

@keyframes corePulse {
  0%, 100% { opacity: 0.5; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1.1); }
}

/* 水波纹涟漪 */
.water-ripple {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  border-radius: 50%; border: 1.5px solid rgba(255, 255, 255, 0.2);
  background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%);
  width: 0; height: 0; opacity: 1;
  animation-name: rippleSpreadOut;
  animation-timing-function: cubic-bezier(0.2, 0.4, 0.4, 0.9);
  animation-iteration-count: infinite;
  filter: blur(1px);
}
.ripple-1 { animation-delay: 0s; }
.ripple-2 { animation-delay: 2s; }
.ripple-3 { animation-delay: 4s; }

@keyframes rippleSpreadOut {
  0% { width: 80px; height: 80px; opacity: 0; border-width: 3px; }
  10% { opacity: 0.8; }
  100% { width: 120%; height: 120%; opacity: 0; border-width: 0.5px; }
}

@keyframes coreBreathe { 0% { transform: scale(1); } 100% { transform: scale(1.15); } }
@keyframes coreHeartbeat { 0%, 100% { transform: scale(1); } 15% { transform: scale(1.3); } 30% { transform: scale(1); } 45% { transform: scale(1.2); } }

/* 竹简/玉牌面板 (观心参数动态色彩体系) */
.bamboo-slips-panel {
  position: absolute; bottom: -50px; display: flex; gap: 25px;
  background: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(11, 17, 21, 0.8), rgba(0, 0, 0, 0));
  border-top: 1px solid rgba(255,255,255,0.15);
  border-bottom: 1px solid rgba(255,255,255,0.15);
  padding: 15px 50px; z-index: 20; backdrop-filter: blur(8px);
  border-radius: 2px;
}

.tensor-item { 
  display: flex; flex-direction: column; align-items: center; min-width: 70px; 
  color: var(--dynamic-color) !important;
  text-shadow: 0 2px 10px rgba(0,0,0,1), 0 0 20px rgba(0,0,0,0.8);
  font-weight: 600;
  transition: all 0.4s ease;
}
.tensor-item .label { font-size: 0.9rem; margin-bottom: 8px; letter-spacing: 2px; opacity: 0.9; }
.tensor-item .value { font-family: 'Times New Roman', serif; font-size: 1.6rem; }
</style>
