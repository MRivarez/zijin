<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'

import ScreenQingQing from './components/ScreenQingQing.vue'
import ScreenLingShu from './components/ScreenLingShu.vue'
import ScreenFuHun from './components/ScreenFuHun.vue'
import ScreenYiWang from './components/ScreenYiWang.vue'
import ScreenGuanXin from './components/ScreenGuanXin.vue'

// ==========================================
// 1. 全局流体滑轨控制器
// ==========================================
const currentScreen = ref(0)
let isAnimating = false

const handleWheel = (e) => {
  if (isAnimating) return
  if (e.deltaY > 50 && currentScreen.value < 4) slideTo(currentScreen.value + 1)
  else if (e.deltaY < -50 && currentScreen.value > 0) slideTo(currentScreen.value - 1)
}

const slideTo = (index) => {
  currentScreen.value = index
  isAnimating = true
  setTimeout(() => { isAnimating = false }, 1200)
}

onMounted(() => window.addEventListener('wheel', handleWheel, { passive: false }))
onUnmounted(() => window.removeEventListener('wheel', handleWheel))

// 数据闭环
const envConfig = reactive({
  LLM_MODEL: 'glm-4-flash',
  EMBEDDING_MODEL: 'BAAI/bge-small-zh-v1.5',
  LLM_BASE_URL: 'https://open.bigmodel.cn/api/paas/v4/',
  LLM_API_KEY: '', CREATOR_QQ: '', NAPCAT_TOKEN: '',
  NEO4J_URI: 'bolt://localhost:7687', NEO4J_USER: 'neo4j', NEO4J_PASS: ''
})

const emotionTensor = reactive({ loneliness: 0.85, arousal: 0.62, valence: 0.45, tension: 0.30 })

let heartbeatTimer = null
onMounted(() => {
  heartbeatTimer = setInterval(async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/sensor/emotion')
      const data = await res.json()
      if (data.status === 'success') Object.assign(emotionTensor, data)
    } catch (err) { }
  }, 1000)
})
onUnmounted(() => { if (heartbeatTimer) clearInterval(heartbeatTimer) })
</script>

<template>
  <div class="viewport">
    <div class="paper-texture"></div>

    <div class="bg-container">
      <div class="bg-layer qingqing-bg" :class="{ 'hidden': currentScreen >= 3 }"></div>
      <div class="bg-layer zaishui-bg" :class="{ 'visible': currentScreen >= 3 }"></div>
    </div>

    <!-- 纯粹宏大的视效：全向乱流落英 -->
    <div class="art-decoration left-art">
      <div class="calligraphy-scroll-giant">
        <div class="verse-giant">青青子衿，悠悠我心。</div>
        <div class="verse-giant">纵我不往，子宁不嗣音？</div>
      </div>
      <div class="falling-nature-heavy">
        <!-- 不同轨迹的随机粒子 -->
        <div v-for="n in 30" :key="'l'+n" 
             :class="['giant-petal', n % 3 === 0 ? 'drift-left' : n % 3 === 1 ? 'drift-right' : 'drift-wild']"></div>
      </div>
    </div>
    
    <div class="art-decoration right-art">
      <div class="calligraphy-scroll-giant">
        <div class="verse-giant">青青子佩，悠悠我思。</div>
        <div class="verse-giant">纵我不往，子宁不来？</div>
      </div>
      <div class="falling-nature-heavy">
        <div v-for="n in 30" :key="'r'+n" 
             :class="['giant-petal', n % 4 === 0 ? 'drift-wild' : n % 4 === 1 ? 'drift-left' : 'drift-right']"></div>
      </div>
    </div>


    <div class="fluid-track" :style="{ transform: `translateY(-${currentScreen * 100}vh)` }">
      <ScreenQingQing :isActive="currentScreen === 0" />
      <ScreenLingShu :isActive="currentScreen === 1" :config="envConfig" @save="slideTo(2)" />
      <ScreenFuHun :isActive="currentScreen === 2" :soul="envConfig" @save="slideTo(3)" />
      <ScreenYiWang :isActive="currentScreen === 3" :creatorName="envConfig.creatorName" @slide-next="slideTo(4)" />
      <ScreenGuanXin :isActive="currentScreen === 4" :emotionTensor="emotionTensor" />
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600&display=swap');
:root { font-size: 16px; }
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html, body, #app { width: 100%; height: 100%; overflow: hidden; background-color: #fdfaf2; }
body { font-family: 'Noto Serif SC', serif; color: #1a2a30; }

.paper-texture { position: absolute; inset: 0; z-index: 50; pointer-events: none; opacity: 0.15; mix-blend-mode: multiply; background-image: url('data:image/svg+xml;utf8,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E'); }

.viewport { width: 100vw; height: 100vh; position: relative; overflow: hidden; }

/* 背景适配 */
.bg-container { position: absolute; inset: 0; z-index: 0; }
.bg-layer { position: absolute; inset: 0; background-size: contain; background-repeat: no-repeat; background-position: center; opacity: 0; transition: opacity 1.5s; z-index: 2; }
.bg-layer::after { content: ''; position: absolute; inset: 0; background: radial-gradient(circle, transparent 50%, #fdfaf2 92%); pointer-events: none; }
.qingqing-bg { background-image: url('/bg-zijin.png'); opacity: 1; }
.zaishui-bg { background-image: url('/bg-zaishui.png'); }
.qingqing-bg.hidden { opacity: 0; }
.zaishui-bg.visible { opacity: 1; }

/* 巨幕诗篇设计 */
.art-decoration { position: absolute; top: 0; bottom: 0; width: 22vw; z-index: 10; pointer-events: none; display: flex; flex-direction: column; justify-content: center; align-items: center; }
.left-art { left: 0; background: linear-gradient(to right, #fdfaf2, rgba(253, 250, 242, 0)); }
.right-art { right: 0; background: linear-gradient(to left, #fdfaf2, rgba(253, 250, 242, 0)); }

.calligraphy-scroll-giant { display: flex; flex-direction: column; gap: 60px; }
.verse-giant { 
  writing-mode: vertical-rl; font-size: 2.2rem; font-weight: 300; letter-spacing: 1.5rem; 
  color: #1a2a30; opacity: 0; animation: giantFade 8s ease-in-out infinite;
  text-shadow: 2px 2px 10px rgba(255,255,255,1);
}
.calligraphy-scroll-giant :nth-child(2) { animation-delay: 2s; color: #c9372c; font-weight: 400; }

@keyframes giantFade { 0%, 100% { opacity: 0; transform: scale(0.95); filter: blur(4px); } 30%, 70% { opacity: 0.4; transform: scale(1); filter: blur(0); } }

/* 极其震撼的落英粒子系统 (全向乱风版) */
.falling-nature-heavy { position: absolute; inset: 0; perspective: 1000px; }
.giant-petal {
  position: absolute; width: 22px; height: 35px;
  background: radial-gradient(circle at 35% 35%, #fff 10%, #fbd8da 85%);
  border-radius: 80% 10% 55% 50% / 55% 10% 80% 50%;
  box-shadow: 0 8px 25px rgba(255,192,203,0.3);
  opacity: 0; pointer-events: none;
}
.giant-petal:nth-child(3n) { 
  background: linear-gradient(135deg, #eaf5e1, #bad9a4); 
  width: 15px; height: 40px; border-radius: 30% 70%;
  box-shadow: 0 8px 25px rgba(186,217,164,0.3);
}

/* 轨迹 A: 向左慢飘流 */
.drift-left { animation: heavyFallLeft 14s linear infinite; }
@keyframes heavyFallLeft {
  0% { transform: translate(100px, -15vh) rotate(0deg) scale(0.6); opacity: 0; }
  15% { opacity: 0.9; }
  100% { transform: translate(-450px, 115vh) rotate(1080deg) scale(0.8); opacity: 0; }
}

/* 轨迹 B: 向右大幅摇摆流 */
.drift-right { animation: heavyFallRight 16s ease-in-out infinite; }
@keyframes heavyFallRight {
  0% { transform: translate(-200px, -15vh) rotate(0deg) scale(0.5); opacity: 0; }
  20% { opacity: 0.8; transform: translate(50px, 15vh) rotate(90deg) scale(1.1); }
  60% { transform: translate(250px, 60vh) rotate(360deg) scale(0.9); }
  100% { transform: translate(100px, 115vh) rotate(720deg) scale(0.7); opacity: 0; }
}

/* 轨迹 C: 乱序垂直气旋 */
.drift-wild { animation: heavyFallWild 12s cubic-bezier(0.445, 0.05, 0.55, 0.95) infinite; }
@keyframes heavyFallWild {
  0% { transform: translate(0, -15vh) rotateX(0) rotateY(0); opacity: 0; }
  20% { opacity: 1; transform: translate(-100px, 20vh) rotateX(180deg) rotateY(180deg); }
  50% { transform: translate(150px, 50vh) rotateX(360deg) rotateY(720deg); }
  80% { opacity: 0.8; transform: translate(-50px, 85vh) rotateX(540deg) rotateY(1080deg); }
  100% { transform: translate(0, 115vh) rotateX(720deg) rotateY(1440deg); opacity: 0; }
}

/* 随机化分布逻辑 */
.giant-petal:nth-child(n) { left: 10%; animation-delay: calc(var(--n, 1) * -1.8s); }
.giant-petal:nth-child(2n) { left: 35%; animation-delay: -2.3s; }
.giant-petal:nth-child(3n) { left: 65%; animation-delay: -5.1s; }
.giant-petal:nth-child(4n) { left: 85%; animation-delay: -9.4s; }
.giant-petal:nth-child(5n) { left: 20%; animation-delay: -12.7s; }
.giant-petal:nth-child(7n) { left: 50%; animation-delay: -3.6s; }

/* 滑轨容器 */
.fluid-track { position: absolute; top: 0; left: 0; width: 100vw; height: 500vh; z-index: 15; transition: transform 1.2s cubic-bezier(0.65, 0, 0.15, 1); }
.screen { width: 100vw; height: 100vh; display: flex; justify-content: center; align-items: center; }
.content-box { width: 100%; padding: 0 10vw; display: flex; flex-direction: column; align-items: center; gap: 30px; }
.fade-up { opacity: 0; transform: translateY(40px); transition: 1s ease; }
.is-active .fade-up { opacity: 1; transform: translateY(0); transition-delay: 0.4s; }
.title-ink { font-size: 3.5rem; letter-spacing: 20px; color: #1c3038; margin-bottom: 5px; }
.subtitle-ink { font-size: 1.2rem; color: #5a7b86; letter-spacing: 5px; }
</style>