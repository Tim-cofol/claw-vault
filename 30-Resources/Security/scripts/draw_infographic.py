import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse

plt.rcParams['font.family'] = ['WenQuanYi Zen Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 10.5), dpi=160)
ax.set_xlim(0, 14); ax.set_ylim(0, 10.5); ax.set_aspect('equal'); ax.axis('off')

C_BG='#fbfaf6'; C_CENTER='#1f2a44'; C_IN='#2f5fbf'; C_CAP='#0f7b6c'
C_MOD='#b35a1e'; C_OB='#7a1f5a'; C_SCENE='#3a4a6a'

fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)

# Outer ecosystem ellipse
ax.add_patch(Ellipse((7,5), 12.6, 8.6, fill=False, edgecolor='#cfcfcf',
                     linewidth=2, linestyle=(0,(6,4)), zorder=1))
ax.text(13.55, 9.55, 'AI Security Ecosystem', ha='right', va='top',
        fontsize=10, color='#999', style='italic')

# Center Hub
ax.add_patch(FancyBboxPatch((5.6,4.1), 2.8, 1.6,
    boxstyle="round,pad=0.04,rounding_size=0.25",
    linewidth=2.2, edgecolor=C_CENTER, facecolor=C_CENTER, zorder=4))
ax.text(7.0, 5.05, 'Security Platform', ha='center', va='center',
        color='white', fontsize=13, fontweight='bold', zorder=5)
ax.text(7.0, 4.55, 'Hub  /  Splunk?', ha='center', va='center',
        color='#cfd8e8', fontsize=10, style='italic', zorder=5)
ax.text(7.0, 4.22, '— 数据中枢 —', ha='center', va='center',
        color='#9fb0cc', fontsize=8, zorder=5)

def box(x,y,w,h,ec,fc,title,sub,titlec='#000',subc='#555',fs_t=11,fs_s=8.5,z=3):
    ax.add_patch(FancyBboxPatch((x,y),w,h,
        boxstyle="round,pad=0.04,rounding_size=0.18",
        linewidth=1.8, edgecolor=ec, facecolor=fc, zorder=z))
    ax.text(x+w/2, y+h*0.65, title, ha='center', va='center',
            color=titlec, fontsize=fs_t, fontweight='bold', zorder=z+1)
    ax.text(x+w/2, y+h*0.25, sub, ha='center', va='center',
            color=subc, fontsize=fs_s, zorder=z+1)

# Left: idea
box(0.6, 7.7, 2.8, 1.2, C_IN, '#eaf0fb',
    'AI for Security', '以 AI 驱动安全运营',
    titlec=C_IN, subc='#3b4d77', fs_t=11)

# Right: capabilities oval
ax.add_patch(Ellipse((11.3,7.6), 4.4, 2.6, fill=False,
                     edgecolor=C_CAP, linewidth=1.8, zorder=2))
ax.text(11.3, 8.65, 'Capabilities', ha='center', va='center',
        color=C_CAP, fontsize=11, fontweight='bold')
box(9.20, 7.55, 2.20, 0.70, C_CAP, '#e6f3ef',
    'Robust Intelligence', '鲁棒智能', titlec=C_CAP, subc='#3a6b62', fs_t=10, fs_s=8)
box(11.50, 7.55, 2.20, 0.70, C_CAP, '#e6f3ef',
    'AI Defense', 'AI 防御', titlec=C_CAP, subc='#3a6b62', fs_t=10, fs_s=8)
box(10.30, 6.65, 2.30, 0.70, C_CAP, '#e6f3ef',
    'Fail-safe / Resilience', '失败兜底 · 可恢复',
    titlec=C_CAP, subc='#3a6b62', fs_t=9.5, fs_s=8)
ax.text(11.30, 6.25, 'sec · AI', ha='center', va='center',
        color=C_CAP, fontsize=9, style='italic')

# Bottom-left: modules
box(0.6, 2.4, 2.6, 1.1, C_MOD, '#fbeede',
    'DevOps', '持续交付 / 运维', titlec=C_MOD, subc='#7a3f1a')
box(3.6, 2.4, 2.6, 1.1, C_MOD, '#fbeede',
    'DevSec', '开发期安全', titlec=C_MOD, subc='#7a3f1a')
box(6.6, 2.4, 2.6, 1.1, C_MOD, '#fbeede',
    'DevSecOps', '一体化流水线', titlec=C_MOD, subc='#7a3f1a')

# Bottom-right: Intelligent Identity
ax.add_patch(Ellipse((11.3,2.95), 4.4, 2.0, fill=False,
                     edgecolor=C_OB, linewidth=1.8))
ax.text(11.30, 3.85, 'Intelligent Identity', ha='center', va='center',
        color=C_OB, fontsize=11, fontweight='bold')

def pill(x,y,w,h,ec,fc,text,color):
    ax.add_patch(FancyBboxPatch((x,y),w,h,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        linewidth=1.2, edgecolor=ec, facecolor=fc, zorder=3))
    ax.text(x+w/2, y+h/2, text, ha='center', va='center',
            color=color, fontsize=9, fontweight='bold', zorder=4)

pill(9.25, 2.85, 1.40, 0.55, C_OB, '#f5e3ee', 'IAM', C_OB)
pill(10.75, 2.85, 1.20, 0.55, C_OB, '#f5e3ee', 'Zero Trust', C_OB)
pill(12.05, 2.85, 1.40, 0.55, C_OB, '#f5e3ee', 'Risk Score', C_OB)
ax.text(11.30, 2.20, '身份 · 访问 · 信任', ha='center', va='center',
        color=C_OB, fontsize=8.5)

# Scenarios
ax.add_patch(FancyBboxPatch((2.0, 0.45), 10.0, 0.95,
    boxstyle="round,pad=0.02,rounding_size=0.18",
    linewidth=1.6, edgecolor=C_SCENE, facecolor='#eef0f6', zorder=3))
ax.text(7.0, 1.05, '应用场景 / Business Scenarios', ha='center', va='center',
        color=C_SCENE, fontsize=11, fontweight='bold', zorder=4)
ax.text(7.0, 0.70, '教育圈层 · 知识图谱    |    金融风控    |    政企安全运营',
        ha='center', va='center', color=C_SCENE, fontsize=9.5, zorder=4)

def arrow(p_from, p_to, color='#444', lw=1.6, rad=0.0, z=5):
    ax.add_patch(FancyArrowPatch(p_from, p_to,
        arrowstyle='-|>', mutation_scale=14, color=color, linewidth=lw,
        connectionstyle=f"arc3,rad={rad}", zorder=z))

arrow((3.45,8.1), (6.10,5.45), color=C_IN, lw=1.8)
arrow((10.4,7.0), (8.20,5.10), color=C_CAP, lw=1.5)
arrow((11.3,6.55), (8.30,4.85), color=C_CAP, lw=1.3)
arrow((6.5,4.10), (5.3,3.50), color=C_MOD, lw=1.4)
arrow((7.0,4.10), (6.6,3.50), color=C_MOD, lw=1.4)
arrow((7.5,4.10), (7.9,3.50), color=C_MOD, lw=1.4)
arrow((8.4,4.85), (10.4,3.50), color=C_OB, lw=1.4)
arrow((11.3,2.20), (10.0,1.40), color=C_SCENE, lw=1.2)
arrow((4.9,2.40), (5.5,1.40), color=C_MOD, lw=1.2)
arrow((7.9,2.40), (8.0,1.40), color=C_MOD, lw=1.2)
arrow((3.20,2.95), (3.60,2.95), color=C_MOD, lw=1.2)
arrow((6.20,2.95), (6.60,2.95), color=C_MOD, lw=1.2)
arrow((10.65,3.10), (10.75,3.10), color=C_OB, lw=1.0)
arrow((11.95,3.10), (12.05,3.10), color=C_OB, lw=1.0)

ax.text(0.4, 0.18, '重绘自手稿草图 · 部分词条为推测（置信度见对话）',
        fontsize=7.5, color='#888', style='italic')

# Legend
patches_list = [
    patches.Patch(facecolor='#eaf0fb', edgecolor=C_IN,    label='Idea / Input'),
    patches.Patch(facecolor=C_CENTER,  edgecolor=C_CENTER, label='Platform Hub'),
    patches.Patch(facecolor='#e6f3ef', edgecolor=C_CAP,   label='Capabilities'),
    patches.Patch(facecolor='#fbeede', edgecolor=C_MOD,   label='Modules'),
    patches.Patch(facecolor='#f5e3ee', edgecolor=C_OB,    label='Identity'),
    patches.Patch(facecolor='#eef0f6', edgecolor=C_SCENE, label='Scenarios'),
]
leg = ax.legend(handles=patches_list, loc='lower left',
                bbox_to_anchor=(0.0, 0.02), ncol=3,
                frameon=True, fontsize=8.5, framealpha=0.92)
leg.get_frame().set_edgecolor('#bbb')

plt.tight_layout()
out = '/tmp/ai_security_infographic.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor=C_BG)
print("saved:", out)

import os
print("size:", os.path.getsize(out))
