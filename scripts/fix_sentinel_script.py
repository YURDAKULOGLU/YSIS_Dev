
with open('src/agentic/core/plugins/sentinel.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 49. satırı (index 48) hedefle
target_line = '            is_system = any(path_str.replace("\\", "/").endswith(s) for s in self.SYSTEM_IGNORE_LIST)'
lines[48] = target_line

with open('src/agentic/core/plugins/sentinel.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Sentinel fixed successfully.")
