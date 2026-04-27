<script setup>
const props = defineProps({ 
  isActive: Boolean,
  creatorName: String,
  zijinTrait: String,
  relation: String
})
const emits = defineEmits(['update:creatorName', 'update:zijinTrait', 'update:relation', 'forge'])

const forgeSoul = async () => {
  if (!props.creatorName || !props.zijinTrait || !props.relation) {
    alert('请将诗卷补全...')
    return
  }
  try {
    const res = await fetch('http://127.0.0.1:8000/api/persona/init', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        creatorName: props.creatorName,
        zijinTrait: props.zijinTrait,
        relation: props.relation
      })
    })
    const data = await res.json()
    console.log("🔥 [赋魂波动] 后端响应:", data.message)
    emits('forge')
  } catch (error) {
    alert("赋魂失败，通讯受阻！")
  }
}
</script>

<template>
  <section class="screen" :class="{ 'is-active': isActive }">
    <div class="content-box fade-up">
      <div class="letter-panel">
        <h2 class="title-ink text-center">赋 魂</h2>
        <p class="subtitle-ink text-center">于此落笔，定其心智</p>
        
        <div class="poetry-form">
          <div class="form-line">
            <span>吾名</span>
            <input 
              type="text" 
              :value="creatorName" 
              @input="$emit('update:creatorName', $event.target.value)" 
              class="brush-input" 
              placeholder="造物主" 
            />
            <span>，</span>
          </div>
          <div class="form-line">
            <span>愿予子衿</span>
            <input 
              type="text" 
              :value="zijinTrait" 
              @input="$emit('update:zijinTrait', $event.target.value)" 
              class="brush-input" 
              placeholder="如: 傲娇/温婉" 
            />
            <span>之性，</span>
          </div>
          <div class="form-line">
            <span>结为</span>
            <input 
              type="text" 
              :value="relation" 
              @input="$emit('update:relation', $event.target.value)" 
              class="brush-input" 
              placeholder="如: 挚友/宿敌" 
            />
            <span>之缘。</span>
          </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
          <button class="sys-btn-stamp" @click="forgeSoul">烙下真名</button>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.letter-panel {
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

.letter-panel::before {
  content: ''; position: absolute; top: 0; left: -20px; right: -20px; height: 10px;
  background: linear-gradient(to bottom, #d2cdb5, #aba58a);
  border-radius: 5px;
  box-shadow: 0 5px 10px rgba(0,0,0,0.1);
}

.poetry-form {
  font-size: clamp(1.2rem, 2vw, 1.8rem); line-height: 2.5; color: #1c3038;
  display: flex; flex-direction: column; align-items: center; gap: 20px; margin-top: 30px;
}
.form-line { display: flex; align-items: baseline; justify-content: center; }

.brush-input {
  border: none; border-bottom: 2px solid #5a7b86; background: transparent; outline: none;
  color: #c9372c; /* 朱砂红 */ text-align: center; 
  width: clamp(100px, 15vw, 220px); padding: 0 10px; margin: 0 10px;
  font-size: inherit; font-family: inherit; transition: all 0.4s ease;
}
.brush-input:focus { border-bottom-color: #c9372c; width: clamp(140px, 18vw, 260px); }
.brush-input::placeholder { color: rgba(201, 55, 44, 0.3); font-weight: 300; }

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
</style>
