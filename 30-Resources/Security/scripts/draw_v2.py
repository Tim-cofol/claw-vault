import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse

plt.rcParams['font.family'] = ['WenQuanYi Zen Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 调色板 —— 思科偏冷的深色基调
C_BG     = '#f5f6f8'
C_FRAME  = '#1b3a5b'   # 深蓝灰
C_IN     = '#0b6e9e'   # Armorblox 蓝
C_CORE   = '#049fd9'   # Splunk 品牌青蓝
C_AI     = '#7e3f98'   # AI Defense 紫
C_ID     = '#118a5b'   # Identity 绿
C_KG     = '#b13a2a'   # 知识图谱 红
C_TEXT   = '#1a1a1a'
C_SUB    = '#5a6470'
C_LINE   = '#3a4a5a'

fig, ax = plt.subplots(figsize=(15, 10.5), dpi=160)
ax.set_xlim(0, 15); ax.set_ylim(0, 10.5); ax.set_aspect('equal'); ax.axis('off')
fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)

# ---------- 标题 ----------
ax.text(7.5, 10.2, '思科 AI 安全 × 身份图谱 架构草图',
        ha='center', va='center', fontsize=16, fontweight='bold', color=C_FRAME)
ax.text(7.5, 9.78, 'Splunk-centric · AI Defense · Identity Graph',
        ha='center', va='center', fontsize=10.5, color=C_SUB, style='italic')

# ---------- 外圈大框架 ----------
outer = Ellipse((7.5, 5.0), 14.6, 9.2, fill=False,
                edgecolor='#b6bdc7', linewidth=1.8, linestyle=(0,(5,4)), zorder=1)
ax.add_patch(outer)
ax.text(14.85, 9.55, 'Cisco Security Cloud + Identity',
        ha='right', va='top', fontsize=9, color='#8a8f96', style='italic')

# ---------- 工具函数 ----------
def rbox(x, y, w, h, fc, ec, title, sub='', titlec=C_TEXT, subc=C_SUB,
         fs_t=11.5, fs_s=9, lw=1.8, z=3, pad=0.04, r=0.20):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad={pad},rounding_size={r}",
        linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z))
    ax.text(x + w/2, y + h*0.62, title, ha='center', va='center',
            color=titlec, fontsize=fs_t, fontweight='bold', zorder=z+1)
    if sub:
        ax.text(x + w/2, y + h*0.26, sub, ha='center', va='center',
                color=subc, fontsize=fs_s, zorder=z+1)

def arr(p_from, p_to, color=C_LINE, lw=1.7, rad=0.0, z=5, m=14):
    ax.add_patch(FancyArrowPatch(p_from, p_to,
        arrowstyle='-|>', mutation_scale=m, color=color, linewidth=lw,
        connectionstyle=f"arc3,rad={rad}", zorder=z))

# ---------- ① 左上：AI for Security + Armorblox ----------
rbox(0.55, 7.85, 3.0, 1.35, '#e6f1f7', C_IN,
     'AI for Security', '以 AI 驱动安全运营',
     titlec=C_IN, subc='#1a4a66', fs_t=11.5, fs_s=9)

rbox(0.55, 6.30, 3.0, 1.20, '#e6f1f7', C_IN,
     'Armorblox', 'AI 邮件/协作安全 (NLP 反钓鱼/DLP)',
     titlec=C_IN, subc='#1a4a66', fs_t=11, fs_s=8.5)

# ---------- ② 中央核心：Splunk ----------
core = FancyBboxPatch((5.85, 4.25), 3.30, 1.75,
    boxstyle="round,pad=0.05,rounding_size=0.30",
    linewidth=2.4, edgecolor=C_CORE, facecolor=C_CORE, zorder=4)
ax.add_patch(core)
ax.text(7.50, 5.55, 'Splunk', ha='center', va='center',
        color='white', fontsize=22, fontweight='bold', zorder=5, family='DejaVu Sans')
ax.text(7.50, 4.95, 'Security & Observability Data Platform',
        ha='center', va='center', color='#e0f3fb', fontsize=10, style='italic', zorder=5)
ax.text(7.50, 4.55, '数据中枢 · 事件 · 遥测 · 关联',
        ha='center', va='center', color='#bfe3f3', fontsize=8.5, zorder=5)

# ---------- ③ 右上：AI 安全闭环（紫色域） ----------
ai_oval = Ellipse((11.85, 7.55), 5.4, 2.9, fill=False,
                  edgecolor=C_AI, linewidth=1.8, linestyle='-', zorder=2)
ax.add_patch(ai_oval)
ax.text(11.85, 8.65, 'AI Security Loop', ha='center', va='center',
        color=C_AI, fontsize=12, fontweight='bold')

rbox(9.20, 7.65, 2.55, 0.85, '#f1e8f5', C_AI,
     'Robust Intelligence', 'AI 红队 · 模型评估 (思科已收购)',
     titlec=C_AI, subc='#5a2a72', fs_t=10.5, fs_s=8.0)
rbox(11.85, 7.65, 2.50, 0.85, '#f1e8f5', C_AI,
     'AI Defense', '思科 AI 防护产品',
     titlec=C_AI, subc='#5a2a72', fs_t=10.5, fs_s=8.0)
rbox(10.50, 6.55, 2.55, 0.85, '#f1e8f5', C_AI,
     'Fail-safe / Resilience', '越狱 / 注入 / 模型兜底',
     titlec=C_AI, subc='#5a2a72', fs_t=10.5, fs_s=8.0)
ax.text(11.85, 6.20, 'sec · GenAI', ha='center', va='center',
        color=C_AI, fontsize=9.5, style='italic')

# ---------- ④ 下方：Identity 栈 (绿色域) ----------
id_oval = Ellipse((7.5, 2.55), 14.0, 2.4, fill=False,
                  edgecolor=C_ID, linewidth=1.8, zorder=2)
ax.add_patch(id_oval)
ax.text(7.5, 3.65, 'Intelligence Identity  ·  身份栈',
        ha='center', va='center', color=C_ID, fontsize=12, fontweight='bold')

# 四个并列身份产品
rbox(0.65, 2.10, 2.95, 1.20, '#e7f3ec', C_ID,
     'Oort', 'ITDR · 身份威胁检测与响应',
     titlec=C_ID, subc='#0d5c3d', fs_t=11.5, fs_s=8.5)
rbox(3.85, 2.10, 2.95, 1.20, '#e7f3ec', C_ID,
     'Duo', 'MFA · 零信任认证',
     titlec=C_ID, subc='#0d5c3d', fs_t=11.5, fs_s=8.5)
rbox(7.05, 2.10, 2.95, 1.20, '#e7f3ec', C_ID,
     'ISE', 'Identity Services Engine · 访问控制',
     titlec=C_ID, subc='#0d5c3d', fs_t=11.5, fs_s=8.5)
rbox(10.25, 2.10, 2.95, 1.20, '#e7f3ec', C_ID,
     'Astrix', '非人身份 (NHI) · DSPM',
     titlec=C_ID, subc='#0d5c3d', fs_t=11.5, fs_s=8.5)
ax.text(7.5, 1.78, '人 × 机器 × API · 身份关系图谱',
        ha='center', va='center', color=C_ID, fontsize=9.5, style='italic')

# ---------- ⑤ 底部：身份图谱 / 知识图谱 ----------
kg = FancyBboxPatch((1.20, 0.40), 12.6, 1.05,
    boxstyle="round,pad=0.04,rounding_size=0.22",
    linewidth=1.8, edgecolor=C_KG, facecolor='#f6e6e3', zorder=3)
ax.add_patch(kg)
ax.text(7.5, 1.05, '身份图谱   ⊕   知识图谱',
        ha='center', va='center', color=C_KG, fontsize=12, fontweight='bold')
ax.text(7.5, 0.65, 'Identity Graph  ·  Knowledge Graph    →    决策 / 响应 / 自助',
        ha='center', va='center', color='#7a2a1e', fontsize=9.5, style='italic')

# ---------- 连线 ----------
# Armorblox → Splunk
arr((3.55, 6.90), (5.85, 5.30), color=C_IN, lw=1.8)
# AI for Security 标识位（指向 Armorblox 上方）
arr((2.05, 7.85), (2.05, 7.50), color=C_IN, lw=1.2, m=10)
# 右上 AI 安全 → Splunk
arr((10.30, 7.20), (9.10, 5.55), color=C_AI, lw=1.5)
arr((12.30, 7.20), (9.20, 5.40), color=C_AI, lw=1.3)
arr((11.75, 6.55), (9.10, 4.95), color=C_AI, lw=1.2)
# Robust Intelligence → AI Defense (内部循环)
arr((11.75, 7.65), (11.85, 7.65), color=C_AI, lw=1.4)
# Splunk → 身份栈（向下辐射 4 条）
for x in [2.12, 5.32, 8.52, 11.72]:
    arr((7.5, 4.25), (x, 3.30), color=C_ID, lw=1.2)
# 身份四件 → 身份图谱
for x in [2.12, 5.32, 8.52, 11.72]:
    arr((x, 2.10), (x, 1.45), color=C_ID, lw=1.0)

# ---------- 图例 ----------
handles = [
    patches.Patch(facecolor='#e6f1f7', edgecolor=C_IN,  label='Armorblox 输入'),
    patches.Patch(facecolor=C_CORE,     edgecolor=C_CORE, label='Splunk 数据中枢'),
    patches.Patch(facecolor='#f1e8f5', edgecolor=C_AI,  label='AI 安全闭环'),
    patches.Patch(facecolor='#e7f3ec', edgecolor=C_ID,  label='Intelligence Identity'),
    patches.Patch(facecolor='#f6e6e3', edgecolor=C_KG,  label='身份/知识图谱'),
]
leg = ax.legend(handles=handles, loc='lower left',
                bbox_to_anchor=(0.005, 0.005), ncol=5,
                frameon=True, fontsize=8.5, framealpha=0.95)
leg.get_frame().set_edgecolor('#bbb')

# ---------- 脚注 ----------
ax.text(14.95, 0.18, '重绘自手稿 · 关键产品：Armorblox · Splunk · Robust Intelligence · AI Defense · Oort · Duo · ISE · Astrix',
        fontsize=7.5, color='#8a8f96', style='italic', ha='right')

plt.tight_layout()
out = '/tmp/cisco_ai_security_v2.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor=C_BG)
import os
print("saved:", out, "size:", os.path.getsize(out))
