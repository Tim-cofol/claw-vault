import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Circle
import numpy as np

plt.rcParams['font.family'] = ['WenQuanYi Zen Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 调色
C_BG    = '#f5f6f8'
C_LEFT  = '#0b6e9e'   # AI for Security
C_RIGHT = '#7e3f98'   # Security for AI
C_CORE  = '#049fd9'   # Splunk
C_ID    = '#118a5b'   # Identity
C_NHI   = '#b8470b'   # NHI 强调
C_KG    = '#5b3a8a'   # 知识图谱
C_TEXT  = '#1a1a1a'
C_SUB   = '#5a6470'
C_LINE  = '#3a4a5a'

fig, ax = plt.subplots(figsize=(16, 11), dpi=160)
ax.set_xlim(0, 16); ax.set_ylim(0, 11); ax.set_aspect('equal'); ax.axis('off')
fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)

# 标题
ax.text(8.0, 10.65, '思科 NHI 体系下的 AI 安全产品矩阵',
        ha='center', va='center', fontsize=17, fontweight='bold', color='#1b3a5b')
ax.text(8.0, 10.20, 'Cisco · Non-Human Identity (NHI) Security · AI for Security ↔ Security for AI',
        ha='center', va='center', fontsize=10.5, color=C_SUB, style='italic')

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

def arr(p_from, p_to, color=C_LINE, lw=1.7, rad=0.0, z=5, m=14, style='-|>'):
    ax.add_patch(FancyArrowPatch(p_from, p_to,
        arrowstyle=style, mutation_scale=m, color=color, linewidth=lw,
        connectionstyle=f"arc3,rad={rad}", zorder=z))

# ================== ① 左侧大圈: AI for Security ==================
left_cx, left_cy, left_rx, left_ry = 3.6, 5.6, 3.4, 3.7
left_oval = Ellipse((left_cx, left_cy), left_rx*2, left_ry*2,
                    fill=False, edgecolor=C_LEFT, linewidth=2.2, zorder=2)
ax.add_patch(left_oval)
ax.text(left_cx, left_cy + left_ry - 0.05, 'AI for Security',
        ha='center', va='top', fontsize=13, fontweight='bold', color=C_LEFT)
ax.text(left_cx, left_cy + left_ry - 0.50,
        '用 AI 增强安全运营 · AI 驱动的检测 / 响应 / 防护',
        ha='center', va='top', fontsize=9, color=C_LEFT, style='italic')

# Armorblox 子模块
rbox(2.00, 4.85, 3.20, 1.25, '#e6f1f7', C_LEFT,
     'Armorblox', 'NLP 反钓鱼 / 邮件与协作安全',
     titlec=C_LEFT, subc='#1a4a66', fs_t=12, fs_s=8.5, lw=1.8)

# 小字提示
ax.text(left_cx, 3.10, '收购拼图  →  Splunk 汇聚',
        ha='center', va='center', fontsize=8.5, color=C_LEFT, style='italic')

# ================== ② 右侧大圈: Security for AI ==================
right_cx, right_cy, right_rx, right_ry = 12.4, 5.6, 3.4, 3.7
right_oval = Ellipse((right_cx, right_cy), right_rx*2, right_ry*2,
                     fill=False, edgecolor=C_RIGHT, linewidth=2.2, zorder=2)
ax.add_patch(right_oval)
ax.text(right_cx, right_cy + right_ry - 0.05, 'Security for AI',
        ha='center', va='top', fontsize=13, fontweight='bold', color=C_RIGHT)
ax.text(right_cx, right_cy + right_ry - 0.50,
        '保护 AI 模型与应用 · 评估 / 防御 / 观测',
        ha='center', va='top', fontsize=9, color=C_RIGHT, style='italic')

# 三个并列模块: Robust Intelligence / AI Defense / Galileo
rbox(10.55, 6.05, 1.80, 1.05, '#f1e8f5', C_RIGHT,
     'Robust\nIntelligence', 'AI 红队 · 模型评估',
     titlec=C_RIGHT, subc='#5a2a72', fs_t=10.5, fs_s=8.0, lw=1.6)
rbox(12.50, 6.05, 1.80, 1.05, '#f1e8f5', C_RIGHT,
     'AI Defense', 'AI 应用 / 模型防护',
     titlec=C_RIGHT, subc='#5a2a72', fs_t=10.5, fs_s=8.0, lw=1.6)
rbox(11.50, 4.55, 1.80, 1.05, '#f1e8f5', C_RIGHT,
     'Galileo', 'LLM / Agent 可观测与评估',
     titlec=C_RIGHT, subc='#5a2a72', fs_t=10.5, fs_s=8.0, lw=1.6)

# 三个块之间的连线（横向 + 三角形）
arr((12.35, 6.58), (12.50, 6.58), color=C_RIGHT, lw=1.4)
arr((11.50, 5.60), (11.00, 6.05), color=C_RIGHT, lw=1.0, rad=0.0)
arr((12.50, 5.60), (13.00, 6.05), color=C_RIGHT, lw=1.0, rad=0.0)

# ================== ③ 中央核心: Splunk ==================
core = FancyBboxPatch((6.50, 4.75), 3.00, 1.55,
    boxstyle="round,pad=0.05,rounding_size=0.28",
    linewidth=2.4, edgecolor=C_CORE, facecolor=C_CORE, zorder=4)
ax.add_patch(core)
ax.text(8.00, 5.85, 'Splunk', ha='center', va='center',
        color='white', fontsize=20, fontweight='bold', zorder=5, family='DejaVu Sans')
ax.text(8.00, 5.32, 'Security & Observability',
        ha='center', va='center', color='#e0f3fb', fontsize=9.5, style='italic', zorder=5)
ax.text(8.00, 4.98, '事件 · 遥测 · 关联 · 编排',
        ha='center', va='center', color='#bfe3f3', fontsize=8.5, zorder=5)

# ================== ④ 下方: NHI 身份栈（核心叙事） ==================
# 标题条
ax.add_patch(FancyBboxPatch((0.50, 1.85), 15.0, 0.55,
    boxstyle="round,pad=0.02,rounding_size=0.15",
    linewidth=1.6, edgecolor=C_NHI, facecolor='#fbeadd', zorder=3))
ax.text(8.0, 2.13, 'NHI (Non-Human Identity)  身份栈  ·  人 × 机器 × Agent × API',
        ha='center', va='center', fontsize=12, fontweight='bold', color=C_NHI)

# 四个产品
rbox(0.70, 0.55, 3.40, 1.10, '#fbecdb', C_NHI,
     'Oort', 'ITDR · 身份威胁检测与响应',
     titlec=C_NHI, subc='#7a2a0a', fs_t=12, fs_s=8.5, lw=1.7)
rbox(4.30, 0.55, 3.40, 1.10, '#fbecdb', C_NHI,
     'Duo', 'MFA · 零信任认证',
     titlec=C_NHI, subc='#7a2a0a', fs_t=12, fs_s=8.5, lw=1.7)
rbox(7.90, 0.55, 3.40, 1.10, '#fbecdb', C_NHI,
     'ISE', 'Identity Services Engine · 访问控制',
     titlec=C_NHI, subc='#7a2a0a', fs_t=12, fs_s=8.5, lw=1.7)
rbox(11.50, 0.55, 3.40, 1.10, '#fbecdb', C_NHI,
     'Astrix', 'NHI 治理 · DSPM · Agent 身份',
     titlec=C_NHI, subc='#7a2a0a', fs_t=12, fs_s=8.5, lw=1.7)

# 副标语
ax.text(8.0, 0.28, 'Intelligence Identity  ·  串联四块形成可观测的身份图谱',
        ha='center', va='center', fontsize=9, color=C_NHI, style='italic')

# ================== ⑤ 底部: 身份图谱 + 知识图谱 ==================
# (为了不挤压，省略独立底条，改为左下角小注脚)
# 用一个飘带表达"沉淀为图谱"
ax.add_patch(FancyBboxPatch((11.10, 1.95), 4.00, 0.45,
    boxstyle="round,pad=0.02,rounding_size=0.12",
    linewidth=1.2, edgecolor=C_KG, facecolor='#ece5f3', zorder=3))
ax.text(13.10, 2.18, '→  身份图谱  ⊕  知识图谱',
        ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_KG)

# ================== 连线 ==================
# ① Armorblox → Splunk
arr((5.20, 5.30), (6.55, 5.50), color=C_LEFT, lw=1.8)
# ② 右侧三件 → Splunk
arr((10.55, 5.30), (9.50, 5.40), color=C_RIGHT, lw=1.5)
arr((12.40, 4.55), (9.40, 5.20), color=C_RIGHT, lw=1.3)
# ③ Splunk → 下方 NHI 四件 (汇聚)
for x in [2.40, 6.00, 9.60, 13.20]:
    arr((8.0, 4.75), (x, 1.65), color=C_ID, lw=1.0, rad=0.0)
# ④ NHI 四件 → 图谱
arr((13.10, 1.65), (13.10, 1.95), color=C_KG, lw=1.2, m=10)

# ⑤ 左侧大圈 → 右侧大圈（在顶部用虚线表达 AI ↔ Security for AI 互锁）
ax.plot([5.0, 11.0], [9.10, 9.10], color='#888', lw=1.2, linestyle=(0,(4,3)), zorder=2)
ax.text(8.0, 9.25, '双向互锁：AI 既是武器也是攻击面',
        ha='center', va='center', fontsize=9, color='#666', style='italic')

# ================== 图例 ==================
handles = [
    patches.Patch(facecolor='#e6f1f7', edgecolor=C_LEFT,  label='AI for Security'),
    patches.Patch(facecolor=C_CORE,     edgecolor=C_CORE,  label='Splunk 数据中枢'),
    patches.Patch(facecolor='#f1e8f5', edgecolor=C_RIGHT, label='Security for AI'),
    patches.Patch(facecolor='#fbecdb', edgecolor=C_NHI,   label='NHI 身份栈'),
    patches.Patch(facecolor='#ece5f3', edgecolor=C_KG,    label='身份/知识图谱'),
]
leg = ax.legend(handles=handles, loc='lower left',
                bbox_to_anchor=(0.005, 0.005), ncol=5,
                frameon=True, fontsize=9, framealpha=0.95)
leg.get_frame().set_edgecolor('#bbb')

# 脚注
ax.text(15.95, 0.08, '重绘自手稿 · Cisco NHI 体系叙事 · v3',
        fontsize=7.5, color='#999', style='italic', ha='right')

plt.tight_layout()
out = '/tmp/cisco_nhi_v3.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor=C_BG)
import os
print("saved:", out, "size:", os.path.getsize(out))
