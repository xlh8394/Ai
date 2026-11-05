#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import re
from datetime import datetime, timezone

SOURCE_URL = "https://magicrule.pages.dev/data/_shared/artifacts/GlobalAI_rules_188406728e7abf06.list"
OUTPUT_FILE = "AI.list"
POLICY_GROUP = "AI"

CN_KEYWORDS = [
    "baidu.com", "baidubce.com", "ernie.baidu", "yiyan.baidu", "qianfan.baidu",
    "aliyun.com", "aliyuncs.com", "dashscope", "bailian.console.aliyun",
    "tongyi.", "qianwen.", "qoder.",
    "tencent.com", "tencentcloudapi.com", "hunyuan.tencent", "yuanbao.tencent", "yuanqi.tencent",
    "volces.com", "volcengine", "bytedance.com", "byteintlapi.com", "byteoversea.com",
    "zijieapi.com", "bytelemon.com", "doubao.com", "bytednsdoc.com",
    "zhipuai.cn", "zhipucn.com", "bigmodel.cn", "chatglm.cn",
    "moonshot.", "kimi.ai", "kimi.com",
    "minimax.", "minimaxi.com", "hailuoai.com",
    "stepfun.",
    "modelscope.", "siliconflow.",
    "deepseek",
    "coze.cn", "cozebaas.cn", "cozefn.cn", "cozeide.cn",
    "marscode.", "trae.cn", "trae.com.cn",
    "ppio.cn", "yoma.cn", "mcprev.cn",
    "xiaoaiassist.com", "xiaomimimo.com", "xingyeai.com",
    "anthropic.com.cn",
    "ark.cn-beijing.volces",
    "qodercn-jb.oss-cn-hangzhou",
    "api.hunyuan.cloud.tencent",
    "hunyuan.tencentcloudapi",
    "starling.zijieapi",
    "abtestvm-sg.bytedance",
    "lf3-static.bytednsdoc",
    "tron-sg.bytelemon",
    "bytegate-sg.byteintlapi",
    "api.minimaxi.com",
]


def is_cn_domain(line: str) -> bool:
    line_lower = line.lower()
    if any(kw in line_lower for kw in CN_KEYWORDS):
        return True
    if re.search(r'\.cn,|\.com\.cn,', line_lower):
        return True
    return False


def main():
    print(f"⏳ Downloading: {SOURCE_URL}")

    req = urllib.request.Request(
        SOURCE_URL,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode("utf-8")

    lines = content.splitlines()
    proxy_rules = []
    removed = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if is_cn_domain(line):
            removed += 1
            continue
        new_line = re.sub(r',GlobalAI$', f',{POLICY_GROUP}', line)
        new_line = new_line.replace("HOST-SUFFIX,", "DOMAIN-SUFFIX,")
        new_line = new_line.replace("HOST-KEYWORD,", "DOMAIN-KEYWORD,")
        new_line = new_line.replace("HOST,", "DOMAIN,")
        proxy_rules.append(new_line)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    header = f"""# NAME: AI
# SOURCE: MagicRule GlobalAI (auto filtered)
# UPDATED: {now}
# NOTE: 已自动移除国内不需要代理的域名
# RULES: {len(proxy_rules)} (removed {removed} CN domains)
# POLICY: {POLICY_GROUP}

"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("\n".join(proxy_rules))
        f.write("\n")

    print(f"✅ Done. Kept {len(proxy_rules)} rules, removed {removed} CN domains")


if __name__ == "__main__":
    main()
