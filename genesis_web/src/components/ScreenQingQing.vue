<script setup>
const props = defineProps({ isActive: Boolean })
const emits = defineEmits(['slide-next'])
</script>

<template>
  <section class="screen" :class="{ 'is-active': isActive }">
    <div class="content-box fade-up">
      <div class="poetry-vertical-container">
        <h1 class="poetry-vertical">青青子衿<br>悠悠我心<br>纵我不往<br>子宁不嗣音</h1>
        <div class="seal-mark">国风</div>
      </div>
      <div class="intro-action">
        <button class="btn-stamp glowing-action" @click="emits('slide-next')">拂卷</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.poetry-vertical-container {
  display: flex;
  align-items: flex-end; /* 右下角对齐印章 */
  gap: 20px;
}

.poetry-vertical {
  writing-mode: vertical-rl;
  text-orientation: upright;
  font-family: 'Noto Serif SC', serif;
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 600; /* 加重字重以承载黑色 */
  letter-spacing: 20px;
  line-height: 1.8;
  color: #0b1115; /* 极致水墨黑 */
  /* 大型游戏常用的背光(Halo)文字烘托法：利用高强度的白色辉光剥离深色文字与复杂背景 */
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.9), 0 0 35px rgba(255, 255, 255, 0.6);
}

/* 落款印章 */
.seal-mark {
  writing-mode: vertical-rl;
  text-orientation: upright;
  font-size: 1.2rem;
  color: #c9372c; /* 朱砂红 */
  border: 2px solid #c9372c;
  padding: 10px 5px;
  border-radius: 5px 12px 4px 8px / 10px 4px 12px 6px; /* 不规则的古印边缘 */
  letter-spacing: 5px;
  opacity: 0.85;
  transform: translateY(-20px) rotate(-4deg); /* 微微倾斜 */
  box-shadow: inset 0 0 4px rgba(201, 55, 44, 0.5); /* 模拟印泥的不匀称 */
}

/* 一屏交互引导：拂卷的散晕指引 */
.intro-action {
  display: flex; justify-content: center; align-items: center;
  margin-top: 40px;
}

/* 印章/文字风格无框按钮 */
.btn-stamp {
  padding: 10px 20px; 
  background: transparent;
  color: #0b1115; /* 极致黑 */
  border: none;
  font-family: 'Noto Serif SC', serif;
  font-weight: 600;
  font-size: 1.5rem; letter-spacing: 8px; cursor: pointer;
  transition: all 0.5s ease; position: relative; 
  text-shadow: 0 0 12px rgba(255,255,255,0.9); /* 背光 */
}

/* 赋予该文字生命力（呼吸 + 墨漪散发） */
.glowing-action {
  animation: textBreathe 3s infinite alternate;
}
.glowing-action::before {
  content: ''; position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 100%; height: 100%;
  border-radius: 50%;
  border: 1px solid #c9372c; /* 朱砂红散晕 */
  opacity: 0; pointer-events: none;
  animation: btnPingRipple 2.5s infinite cubic-bezier(0.1, 0.8, 0.3, 1);
}

.btn-stamp::after {
  content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
  width: 0%; height: 3px; background: #c9372c; border-radius: 5px; 
  transition: width 0.5s cubic-bezier(0.7, 0, 0.3, 1);
}
.btn-stamp:hover { color: #c9372c; letter-spacing: 12px; text-shadow: 0 0 15px rgba(255,255,255,1); }
.btn-stamp:hover::after { width: 80%; }

@keyframes btnPingRipple {
  0% { padding: 0; opacity: 0.8; border-width: 2px; }
  100% { padding: 50px; opacity: 0; border-width: 0; }
}
@keyframes textBreathe {
  0% { transform: scale(1); text-shadow: 0 0 12px rgba(255,255,255,0.8); }
  100% { transform: scale(1.05); text-shadow: 0 0 25px rgba(255,255,255,1); }
}
</style>
