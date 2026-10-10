import sys
import random
from datetime import datetime, timezone

THEMES = {
    'midnight': {
        'label': 'midnight', 'bgFrom': '#0d1117', 'bgTo': '#161b22',
        'border': '#00FF9D', 'accent': '#00FF9D', 'accentSoft': '#00C97D',
        'secondary': '#FF5B67', 'text': '#f0f6fc', 'muted': '#8b949e', 'divider': '#30363d',
    },
    'matrix': {
        'label': 'matrix', 'bgFrom': '#000000', 'bgTo': '#0a140a',
        'border': '#00FF41', 'accent': '#00FF41', 'accentSoft': '#00B82E',
        'secondary': '#39FF14', 'text': '#D9FFD9', 'muted': '#4D9C4D', 'divider': '#1a3a1a',
    },
    'synthwave': {
        'label': 'synthwave', 'bgFrom': '#1a0633', 'bgTo': '#3a0a5e',
        'border': '#FF2A6D', 'accent': '#00F0FF', 'accentSoft': '#00B8D4',
        'secondary': '#FF2A6D', 'text': '#F8E8FF', 'muted': '#A479C4', 'divider': '#5C2A8A',
    },
    'inferno': {
        'label': 'inferno', 'bgFrom': '#1a0908', 'bgTo': '#2a1310',
        'border': '#FF6B35', 'accent': '#FFAA00', 'accentSoft': '#FF8C00',
        'secondary': '#FF3B30', 'text': '#FFF0E0', 'muted': '#B87355', 'divider': '#3a1a1a',
    },
    'frost': {
        'label': 'frost', 'bgFrom': '#f8fafc', 'bgTo': '#e2e8f0',
        'border': '#0EA5E9', 'accent': '#0284C7', 'accentSoft': '#0369A1',
        'secondary': '#6366F1', 'text': '#0f172a', 'muted': '#475569', 'divider': '#cbd5e1',
    },
    'crimson': {
        'label': 'crimson', 
        'bgFrom': '#000000',      
        'bgTo': '#0f0000',       
        'border': '#960000',      
        'accent': '#960000',    
        'accentSoft': '#cc0000',
        'secondary': '#ff3333',   
        'text': '#f5f5f5',        
        'muted': '#804040',      
        'divider': '#330000',    
    },
    'cherry_dark': {
        'label': 'cherry_dark',
        'bgFrom': '#120c0c',      
        'bgTo': '#1a1313',        
        'border': '#cf3d44',     
        'accent': '#cf3d44',      
        'accentSoft': '#e06c72',  
        'secondary': '#e88b8e',   
        'text': '#fdf4f4',        
        'muted': '#9e7375',       
        'divider': '#3b2425',     
    },
}

THEME_NAMES = list(THEMES.keys())

def utc_day_of_year() -> int:
    now = datetime.now(timezone.utc)
    start = datetime(now.year, 1, 1, tzinfo=timezone.utc)
    return (now - start).days

def pick_theme(input_val: str) -> str:
    val = (input_val or '').strip().lower()
    if val == 'random':
        return random.choice(THEME_NAMES)
    if val in ('rotate', ''):
        return THEME_NAMES[utc_day_of_year() % len(THEME_NAMES)]
    if val in THEMES:
        return val
    print(f"[thm-badge] Unknown theme \"{input_val}\", falling back to \"midnight\".", file=sys.stderr)
    return 'midnight'