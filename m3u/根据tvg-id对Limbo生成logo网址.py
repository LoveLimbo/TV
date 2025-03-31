# 导入所需模块
import os

# 指定输入文件名为 Limbo.m3u
m3u_name = "Limbo.m3u"

# 检查文件是否存在
if not os.path.exists(m3u_name):
    print(f"错误：文件 '{m3u_name}' 不存在！")
    exit(1)

# 读取 Limbo.m3u 文件
with open(m3u_name, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 准备新的 m3u 内容
new_lines = []
logo_base_url = "https://raw.githubusercontent.com/LoveLimbo/TV/main/logo/"

for line in lines:
    # 如果是 #EXTM3U，直接添加
    if line.startswith("#EXTM3U"):
        new_lines.append(line)
        continue
    
    # 处理 #EXTINF 行
    if line.startswith("#EXTINF"):
        # 提取 tvg-id
        tvg_id = None
        if 'tvg-id="' in line:
            start = line.index('tvg-id="') + 8
            end = line.index('"', start)
            tvg_id = line[start:end]
        
        # 如果有 tvg-id，生成 logo 链接
        if tvg_id:
            logo_url = f"{logo_base_url}{tvg_id.replace(' ', '%20')}.png"
            # 检查是否已有 tvg-logo
            if 'tvg-logo="' in line:
                # 替换现有的 tvg-logo
                start = line.index('tvg-logo="') + 10
                end = line.index('"', start)
                line = line[:start] + logo_url + line[end:]
            else:
                # 添加新的 tvg-logo
                insert_pos = line.index('",') + 1
                line = line[:insert_pos] + f' tvg-logo="{logo_url}"' + line[insert_pos:]
        new_lines.append(line)
    else:
        # 其他行（通常是 URL），直接添加
        new_lines.append(line)

# 写入新的 m3u 文件
output_name = f"logo_{m3u_name}"
with open(output_name, 'w', encoding='utf-8') as file:
    file.writelines(new_lines)

print(f"已生成新文件：'{output_name}'，包含 logo 链接。")
