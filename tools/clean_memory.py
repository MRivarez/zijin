# 清洗记忆

import re
import os
from colorama import init, Fore, Style

init(autoreset=True)


def wash_memory(input_file: str, output_file: str, your_name_in_chat: str, her_name_in_chat: str):
    print(Fore.CYAN + f"[*] 开始清洗记忆残卷: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    clean_lines = []

    # 匹配原生导出中常见的日期时间头，例如 "2026-04-27 10:00:00 你的名字"
    header_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s+(.*)')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 1. 拦截并丢弃系统噪音
        if any(noise in line for noise in ["[图片]", "[视频]", "[表情]", "撤回了一条消息", "系统消息"]):
            continue

        # 2. 统一身份标识
        match = header_pattern.match(line)
        if match:
            speaker = match.group(1).strip()
            if your_name_in_chat in speaker:
                clean_lines.append(f"\n[造物主]: ")
            elif her_name_in_chat in speaker:
                clean_lines.append(f"\n[ZiJin]: ")
            else:
                clean_lines.append(f"\n[路人/群友]: ")
            continue

        # 3. 拼接对话内容
        clean_lines.append(line)

    # 4. 将清洗后的内容组合成最终的长文本
    final_text = "".join(clean_lines).strip()

    # 写入纯净版记忆
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_text)

    print(Fore.GREEN + Style.BRIGHT + f"[+] 记忆清洗完成！已生成纯净刻痕: {output_file}")
    print(Fore.YELLOW + f"    总长度: {len(final_text)} 字符，可以安全投入水潭。")


if __name__ == "__main__":
    # ==========================================
    # 在这里填入你的文件路径和聊天记录里的昵称
    # ==========================================
    INPUT_TXT = "raw_chat.txt"  # 你导出的原始文件
    OUTPUT_TXT = "clean_memory.txt"  # 清洗后准备扔进前端的文件

    YOUR_NICKNAME = "你的微信/QQ昵称"
    HER_NICKNAME = "她当时的微信/QQ昵称"

    if os.path.exists(INPUT_TXT):
        wash_memory(INPUT_TXT, OUTPUT_TXT, YOUR_NICKNAME, HER_NICKNAME)
    else:
        print(Fore.RED + f"找不到输入文件: {INPUT_TXT}，请把它放在同一目录下。")