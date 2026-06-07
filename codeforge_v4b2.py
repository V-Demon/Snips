#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════╗
║  CODEFORGE v2.1  —  INGEN SYSTEMS WORKSTATION                     ║
║  Visual Program Composer  /  Node-Based CodeGen Engine            ║
║  *** MODERN UI EDITION ***                                        ║
║  Features: Nodal Flow · Undo-Tree · Auto-Layout · Clean Design    ║
║  Languages: C# · PowerShell · JavaScript · Python · Bash          ║
╚═══════════════════════════════════════════════════════════════════╝
"""
import sys
import json
import os
import re
import copy
import uuid
import math
from collections import defaultdict, deque
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QSplitter, QTreeWidget, QTreeWidgetItem, QLabel, QFrame,
    QScrollArea, QPushButton, QTextEdit, QLineEdit, QComboBox,
    QMessageBox, QFileDialog, QTabWidget, QGroupBox, QFormLayout,
    QDialog, QDialogButtonBox, QStatusBar, QAction, QMenuBar,
    QToolBar, QSizePolicy, QAbstractItemView, QHeaderView,
    QGraphicsDropShadowEffect, QSpinBox, QCheckBox, QGraphicsOpacityEffect,
    QShortcut, QInputDialog, QProgressBar
)
from PyQt5.QtCore import (
    Qt, QTimer, QPoint, QRect, QMimeData, QThread, pyqtSignal,
    QPropertyAnimation, QEasingCurve, QSize, QByteArray, QObject,
    QLineF, QPointF, QTime
)
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QPainter, QBrush, QPen, QPixmap,
    QFontDatabase, QLinearGradient, QTextCharFormat, QSyntaxHighlighter,
    QTextDocument, QCursor, QDrag, QIcon, QPainterPath, QKeySequence,
    QRadialGradient, QTransform
)

# ═══════════════════════════════════════════════════════════════════
#  COLOUR PALETTE  —  MODERN IDE DARK THEME (VS Code inspired)
# ═══════════════════════════════════════════════════════════════════
C = {
    'bg':           '#1e1e1e',       # Main background
    'bg_panel':     '#252526',       # Sidebar/Panel background
    'bg_card':      '#2d2d2d',       # Card/Block background
    'bg_hover':     '#3e3e42',       # Hover state
    'border':       '#3e3e42',       # Subtle border
    'border_bright':'#007acc',       # Accent border
    'accent':       '#007acc',       # Primary accent (Blue)
    'accent_dim':   '#005a9e',
    'text':         '#d4d4d4',       # Main text
    'text_dim':     '#858585',       # Dimmed text
    'amber':        '#ce9178',       # Strings
    'amber_dim':    '#a06c56',
    'amber_bright': '#d9a406',
    'green':        '#4ec9b0',       # Types/Classes
    'green_dim':    '#3a9685',
    'green_mid':    '#4ec9b0',
    'green_bright': '#6ee7d0',
    'red':          '#f44747',       # Errors
    'red_dim':      '#c43636',
    'cyan':         '#569cd6',       # Keywords
    'cyan_dim':     '#437caa',
    'white':        '#ffffff',
    'white_dim':    '#858585',
    'fn_color':     '#dcdcaa',       # Functions
    'var_color':    '#9cdcfe',       # Variables
    'ctrl_color':   '#c586c0',       # Control flow
    'flow_color':   '#d4d4d4',       # Flow lines
    'comment':      '#6a9955',       # Comments
    'phosphor_glow':'#007acc22',     # Repurposed as subtle accent glow
    'glass':        '#ffffff08',
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {C['bg']};
    color: {C['text']};
    font-family: 'Segoe UI', 'Roboto', 'Helvetica', sans-serif;
    font-size: 12px;
}}
QMenuBar {{
    background-color: {C['bg_panel']};
    color: {C['text']};
    border-bottom: 1px solid {C['border']};
    font-size: 12px;
    padding: 4px;
}}
QMenuBar::item:selected {{
    background-color: {C['bg_hover']};
    color: {C['white']};
    border-radius: 4px;
}}
QMenu {{
    background-color: {C['bg_panel']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 4px;
}}
QMenu::item:selected {{
    background-color: {C['accent']};
    color: {C['white']};
    border-radius: 4px;
}}
QSplitter::handle {{
    background-color: {C['border']};
    width: 1px;
}}
QScrollBar:vertical {{
    background: {C['bg']};
    width: 10px;
    border: none;
    border-radius: 5px;
}}
QScrollBar::handle:vertical {{
    background: {C['bg_hover']};
    min-height: 20px;
    border-radius: 5px;
}}
QScrollBar::handle:vertical:hover {{
    background: {C['text_dim']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    background: {C['bg']};
    height: 10px;
    border: none;
    border-radius: 5px;
}}
QScrollBar::handle:horizontal {{
    background: {C['bg_hover']};
    min-width: 20px;
    border-radius: 5px;
}}
QToolBar {{
    background-color: {C['bg_panel']};
    border-bottom: 1px solid {C['border']};
    spacing: 8px;
    padding: 4px 8px;
}}
QStatusBar {{
    background-color: {C['bg_panel']};
    color: {C['text']};
    border-top: 1px solid {C['border']};
    font-size: 11px;
    padding: 2px 8px;
}}
QTabWidget::pane {{
    border: 1px solid {C['border']};
    border-radius: 4px;
    background: {C['bg']};
    top: -1px;
}}
QTabBar::tab {{
    background: {C['bg_panel']};
    color: {C['text_dim']};
    border: 1px solid {C['border']};
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 6px 16px;
    font-size: 11px;
    font-family: 'Segoe UI', sans-serif;
}}
QTabBar::tab:selected {{
    background: {C['bg']};
    color: {C['white']};
    border-color: {C['border']};
    border-bottom: 1px solid {C['bg']};
}}
QLineEdit, QSpinBox, QComboBox {{
    background-color: {C['bg_card']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 4px;
    padding: 4px 8px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
    selection-background-color: {C['accent']};
}}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border-color: {C['accent']};
}}
QComboBox::drop-down {{
    border: none;
    background: transparent;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background-color: {C['bg_panel']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 4px;
    selection-background-color: {C['accent']};
    selection-color: {C['white']};
}}
QTreeWidget {{
    background-color: {C['bg_panel']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 4px;
    alternate-background-color: {C['bg_card']};
    font-size: 12px;
}}
QTreeWidget::item:hover {{
    background-color: {C['bg_hover']};
}}
QTreeWidget::item:selected {{
    background-color: {C['accent']};
    color: {C['white']};
    border-radius: 4px;
}}
QHeaderView::section {{
    background-color: {C['bg_panel']};
    color: {C['text_dim']};
    border: none;
    border-bottom: 1px solid {C['border']};
    padding: 6px;
    font-size: 11px;
    font-weight: bold;
}}
QGroupBox {{
    border: 1px solid {C['border']};
    border-radius: 6px;
    margin-top: 16px;
    color: {C['text']};
    font-size: 11px;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: {C['accent']};
}}
QCheckBox {{
    color: {C['text']};
    spacing: 6px;
}}
QCheckBox::indicator {{
    width: 14px;
    height: 14px;
    border: 1px solid {C['border']};
    border-radius: 3px;
    background: {C['bg_card']};
}}
QCheckBox::indicator:checked {{
    background: {C['accent']};
    border-color: {C['accent']};
}}
QProgressBar {{
    background: {C['bg_card']};
    border: 1px solid {C['border']};
    border-radius: 4px;
    color: {C['text']};
    text-align: center;
    font-size: 10px;
}}
QProgressBar::chunk {{
    background: {C['accent']};
    border-radius: 3px;
}}
"""

# ═══════════════════════════════════════════════════════════════════
#  STYLED BUTTON (Modern Flat Design)
# ═══════════════════════════════════════════════════════════════════
class ForgeButton(QPushButton):
    def __init__(self, text, variant='primary', parent=None):
        super().__init__(text, parent)
        self.variant = variant
        self._apply_style()
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def _apply_style(self):
        styles = {
            'green':   (C['accent'], C['white'], C['accent_dim'], '#004578'),
            'amber':   ('#d9a406', '#1e1e1e', '#b88a00', '#997200'),
            'red':     (C['red'], C['white'], '#d32f2f', '#b71c1c'),
            'cyan':    ('#0088cc', C['white'], '#006699', '#004d73'),
            'ghost':   (C['bg_card'], C['text'], C['border'], C['bg_hover']),
            'pink':    ('#c586c0', C['white'], '#a66ca5', '#8a558a'),
            'primary': (C['accent'], C['white'], C['accent_dim'], '#004578'),
        }
        bg, fg, border, pressed_bg = styles.get(self.variant, styles['primary'])
        hover_bg = QColor(bg).lighter(115).name() if self.variant != 'ghost' else C['bg_hover']
        hover_fg = fg if self.variant != 'ghost' else C['white']
        hover_border = QColor(border).lighter(115).name() if self.variant != 'ghost' else C['text_dim']

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border: 1px solid {border};
                border-radius: 4px;
                padding: 6px 16px;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
                color: {hover_fg};
                border-color: {hover_border};
            }}
            QPushButton:pressed {{
                background-color: {pressed_bg};
            }}
            QPushButton:disabled {{
                background-color: {C['bg_card']};
                color: {C['text_dim']};
                border-color: {C['border']};
            }}
        """)

# ═══════════════════════════════════════════════════════════════════
#  SYNTAX HIGHLIGHTER (Modern Colors + Python + Bash)
# ═══════════════════════════════════════════════════════════════════
class CodeHighlighter(QSyntaxHighlighter):
    def __init__(self, document, language='CSharp'):
        super().__init__(document)
        self.language = language
        self._build_rules()

    def _fmt(self, color, bold=False, italic=False):
        f = QTextCharFormat()
        f.setForeground(QColor(color))
        if bold:   f.setFontWeight(QFont.Bold)
        if italic: f.setFontItalic(True)
        return f

    def _build_rules(self):
        self.rules = []
        kw_cs = r'\b(public|private|static|void|string|int|bool|var|new|return|if|else|for|foreach|while|try|catch|throw|using|class|namespace|async|await|true|false|null|this|let|const|decimal|float|double|long|short|byte|char|object|interface|enum|struct|readonly|virtual|override|abstract|sealed|partial|internal|protected|extern|unsafe|fixed|implicit|explicit|operator|event|delegate|yield|where|from|select|group|into|orderby|join|let|on|equals|by|ascending|descending)\b'
        kw_ps = r'\b(function|param|begin|process|end|if|else|foreach|while|return|try|catch|throw|\$[a-zA-Z_]\w*|Write-Host|Write-Log|Get-|Set-|New-|Remove-|Invoke-|Where-|ForEach-|Select-|Sort-|Measure-|Group-|Format-|Out-|Import-|Export-|ConvertTo-|ConvertFrom-|Start-|Stop-|Restart-|Test-|Get-Date|Write-Output|Write-Error|Write-Warning|Write-Verbose|Write-Debug|Write-Progress|Read-Host|Clear-Host|Out-Null|Out-String|Out-File|Out-GridView|Format-Table|Format-List|Select-Object|Where-Object|ForEach-Object|Sort-Object|Group-Object|Measure-Object|Import-Csv|Export-Csv|ConvertTo-Json|ConvertFrom-Json|Invoke-RestMethod|Invoke-WebRequest|Start-Process|Stop-Process|Get-Process|Get-Service|Start-Service|Stop-Service|Restart-Service|Get-ChildItem|Get-Content|Set-Content|Add-Content|Test-Path|New-Item|Remove-Item|Copy-Item|Move-Item|Rename-Item|Get-Location|Set-Location|Push-Location|Pop-Location|Join-Path|Split-Path|Resolve-Path|Split-Path|Get-Variable|Set-Variable|Remove-Variable|Clear-Variable|New-Variable|Get-Alias|Set-Alias|Export-Alias|Import-Alias)\b'
        kw_js = r'\b(function|async|await|const|let|var|return|if|else|for|while|try|catch|throw|new|true|false|null|undefined|this|of|in|class|import|from|export|default|extends|super|static|get|set|constructor|typeof|instanceof|delete|void|yield|with|debugger|switch|case|break|continue|do|finally|label|package|interface|implements|public|private|protected|enum)\b'
        kw_py = r'\b(def|class|if|elif|else|for|while|try|except|finally|with|as|return|yield|raise|assert|break|continue|pass|lambda|global|nonlocal|del|import|from|in|is|not|and|or|True|False|None|self|cls|super|print|input|len|range|enumerate|zip|map|filter|reduce|sum|min|max|abs|round|pow|divmod|chr|ord|hex|oct|bin|int|float|str|list|tuple|dict|set|frozenset|bool|bytes|bytearray|memoryview|type|isinstance|hasattr|getattr|setattr|delattr|vars|dir|help|repr|ascii|format|open|read|write|close|seek|tell|flush|readline|readlines|writelines|next|iter|callable|staticmethod|classmethod|property|abstractmethod|dataclass|namedtuple|deque|Counter|defaultdict|OrderedDict|ChainMap|UserDict|UserList|UserString|Pattern|Match|compile|search|match|findall|finditer|sub|split|escape|fullmatch|subn|escape|purge|template|error|JSONDecodeError|loads|dumps|load|dump|Encoder|Decoder|HTTPError|URLError|request|urlopen|Request|urlretrieve|install_opener|build_opener|pathname2url|url2pathname|getproxies|parse|unquote|quote|urlencode|urlparse|urlunparse|urljoin|urlsplit|urlunsplit|parse_qs|parse_qsl|robotparser|Thread|Lock|RLock|Semaphore|BoundedSemaphore|Condition|Event|Barrier|Timer|ThreadPoolExecutor|ProcessPoolExecutor|as_completed|wait|Future|Queue|LifoQueue|PriorityQueue|SimpleQueue|Pool|Process|cpu_count|active_children|freeze_support|set_start_method|get_start_method|get_all_start_methods|Manager|Value|Array|Pipe|connection|Listener|Client|AuthenticationError|BufferTooShort|TimeoutError|ssl|socket|select|selectors|asyncio|threading|multiprocessing|concurrent|subprocess|os|sys|json|re|math|random|datetime|time|collections|itertools|functools|operator|typing|pathlib|shutil|glob|fnmatch|tempfile|hashlib|base64|binascii|struct|string|textwrap|unicodedata|codecs|io|pickle|copy|deepcopy|weakref|gc|atexit|signal|warnings|contextlib|abc|inspect|types|enum|dataclasses|csv|xml|html|http|urllib|ftplib|smtplib|email|mailbox|mimetypes|base64|quopri|uu|zlib|gzip|bz2|lzma|zipfile|tarfile|sqlite3|dbm|shelve|configparser|argparse|optparse|getopt|logging|unittest|doctest|pdb|profile|cProfile|timeit|trace|tracemalloc|statistics|fractions|decimal|numbers|array|bisect|heapq|copy|pprint|reprlib|numbers|contextvars|dataclasses|enum|typing|zoneinfo|graphlib|tomllib|wsgiref|uuid|ipaddress|netrc|plistlib|msilib|winreg|winsound|msvcrt|_winapi)\b'
        kw_sh = r'\b(if|then|elif|else|fi|for|while|do|done|case|esac|in|select|until|function|return|exit|break|continue|shift|source|\.\s|alias|unalias|declare|typeset|local|export|readonly|unset|set|shopt|trap|wait|bg|fg|jobs|kill|disown|suspend|times|umask|ulimit|hash|type|command|builtin|enable|eval|exec|pwd|cd|echo|printf|read|test|\[|\]|true|false|seq|sleep|dirname|basename|realpath|readlink|ln|cp|mv|rm|mkdir|rmdir|touch|cat|tac|head|tail|cut|sort|uniq|wc|grep|egrep|fgrep|sed|awk|find|xargs|tar|gzip|gunzip|zip|unzip|chmod|chown|chgrp|ls|ps|top|htop|killall|pkill|pgrep|nice|renice|df|du|free|uptime|uname|hostname|whoami|id|groups|passwd|su|sudo|curl|wget|ssh|scp|rsync|git|docker|kubectl|systemctl|service|crontab|at|batch|mail|sendmail|postfix|nginx|apache|mysql|psql|mongo|redis|python|python3|pip|pip3|node|npm|yarn|make|cmake|gcc|g\+\+|clang|javac|java|go|rustc|cargo)\b'

        kw_map = {
            'CSharp': kw_cs, 
            'PowerShell': kw_ps, 
            'JavaScript': kw_js,
            'Python': kw_py,
            'Bash': kw_sh
        }
        kw = kw_map.get(self.language, kw_cs)

        self.rules += [
            (re.compile(kw),                     self._fmt(C['cyan'], bold=True)),
            (re.compile(r'"[^"\\]*(?:\\.[^"\\]*)*"'), self._fmt(C['amber'])),
            (re.compile(r"'[^'\\]*(?:\\.[^'\\]*)*'"), self._fmt(C['amber'])),
            (re.compile(r'\b\d+(\.\d+)?\b'),     self._fmt(C['amber_bright'])),
            (re.compile(r'//[^\n]*'),            self._fmt(C['comment'], italic=True)),
            (re.compile(r'#[^\n]*'),             self._fmt(C['comment'], italic=True)),
            (re.compile(r'\b[A-Z][a-zA-Z0-9_]*(?=\()'), self._fmt(C['green_bright'])),
            (re.compile(r'\$[a-zA-Z_]\w*'),      self._fmt(C['var_color'])),
            (re.compile(r'[{}()\[\];,.]'),        self._fmt(C['white_dim'])),
        ]

        # Language-specific additions
        if self.language == 'Python':
            self.rules.append((re.compile(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\''), self._fmt(C['comment'], italic=True)))
            self.rules.append((re.compile(r'\b\d+\.?\d*\b'), self._fmt(C['amber_bright'])))
            self.rules.append((re.compile(r'f"[^"\]*(?:\.[^"\]*)*"'), self._fmt(C['amber'])))
            self.rules.append((re.compile(r'@\w+'), self._fmt(C['ctrl_color'])))
        elif self.language == 'Bash':
            self.rules.append((re.compile(r'\$\{[^}]*\}|\$\([^)]*\)|\$\(\([^)]*\)\)|\$\w+|\$\@|\$\*|\$\#|\$\?|\$\!|\$\$|\$\-|\$\_|\$0|\$[1-9][0-9]*'), self._fmt(C['var_color'])))
            self.rules.append((re.compile(r'<<[\\-]?\\s*\\w+'), self._fmt(C['amber'])))
            self.rules.append((re.compile(r'`[^`]*`'), self._fmt(C['green_bright'])))
            self.rules.append((re.compile(r'2>&1|>/dev/null|&>|\|&|&&|\|\||;;|\|\||\|'), self._fmt(C['ctrl_color'])))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for m in pattern.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)

# ═══════════════════════════════════════════════════════════════════
#  NODE PORT
# ═══════════════════════════════════════════════════════════════════
class NodePort:
    PORT_FLOW = 'flow'
    PORT_DATA = 'data'

    def __init__(self, name, dtype, direction, port_type, parent_block, index=0, total=1):
        self.name = name
        self.dtype = dtype
        self.direction = direction
        self.port_type = port_type
        self.parent = parent_block
        self.index = index
        self.total = total
        self.connections = []
        self.radius = 6
        self._hot = False

    def rect(self):
        pw = self.parent.width()
        ph = self.parent.height()
        if self.port_type == self.PORT_FLOW:
            if self.direction == 'in':
                x = pw // 2 - self.radius
                y = -self.radius
            else:
                x = pw // 2 - self.radius
                y = ph - self.radius
        else:
            spacing = ph / (self.total + 1)
            y = int(spacing * (self.index + 1)) - self.radius
            if self.direction == 'in':
                x = -self.radius
            else:
                x = pw - self.radius
        return QRect(x, y, self.radius * 2, self.radius * 2)

    def center(self):
        r = self.rect()
        return QPoint(r.x() + r.width() // 2, r.y() + r.height() // 2)

    def global_center(self):
        c = self.center()
        return self.parent.mapToParent(c)

    def color(self):
        if self.port_type == self.PORT_FLOW:
            return C['flow_color']
        type_colors = {
            'string': C['amber'], 'int': C['green_bright'], 'bool': C['cyan'],
            'object': C['white'], 'void': C['white_dim'], 'Action': C['ctrl_color'],
            'FileInfo[]': C['amber_dim'], 'Promise<object>': C['cyan_dim'],
            'number': C['green_bright'], 'float': C['green_bright'], 'double': C['green_bright'],
            'list': C['amber'], 'dict': C['amber'], 'tuple': C['amber'], 'set': C['amber'],
            'PSObject': C['cyan'], 'hashtable': C['amber'], 'switch': C['cyan'],
            'ScriptBlock': C['fn_color'], 'PSCredential': C['amber'],
        }
        return type_colors.get(self.dtype, C['green'])

    def can_connect_to(self, other):
        if self.direction == other.direction or self.parent is other.parent or self.port_type != other.port_type:
            return False
        return True

# ═══════════════════════════════════════════════════════════════════
#  NODE CONNECTION
# ═══════════════════════════════════════════════════════════════════
class NodeConnection:
    def __init__(self, port_out, port_in):
        self.source = port_out
        self.target = port_in
        self.source.connections.append(self)
        self.target.connections.append(self)
        self._temp_end = None

    def delete(self):
        if self in self.source.connections: self.source.connections.remove(self)
        if self in self.target.connections: self.target.connections.remove(self)

    def path(self):
        if self._temp_end:
            p1, p2 = self.source.global_center(), self._temp_end
        else:
            p1, p2 = self.source.global_center(), self.target.global_center()

        path = QPainterPath(QPointF(p1))
        dx = abs(p2.x() - p1.x()) * 0.5
        if self.source.port_type == NodePort.PORT_FLOW:
            dy = abs(p2.y() - p1.y()) * 0.5
            ctrl1, ctrl2 = QPointF(p1.x(), p1.y() + dy), QPointF(p2.x(), p2.y() - dy)
        else:
            ctrl1, ctrl2 = QPointF(p1.x() + dx, p1.y()), QPointF(p2.x() - dx, p2.y())
        path.cubicTo(ctrl1, ctrl2, QPointF(p2))
        return path

    def color(self):
        if self._temp_end:
            return C['accent'] if self.source.can_connect_to(self.target) else C['red']
        if self.source.dtype != self.target.dtype and self.source.port_type == NodePort.PORT_DATA:
            return C['red']
        return self.source.color()

# ═══════════════════════════════════════════════════════════════════
#  UNDO SYSTEM
# ═══════════════════════════════════════════════════════════════════
class Command:
    def __init__(self, description=""):
        self.description = description
        self.timestamp = datetime.now()
    def execute(self): pass
    def undo(self): pass

class AddBlockCmd(Command):
    def __init__(self, canvas, data, block_type, pos):
        super().__init__(f"Add {block_type}")
        self.canvas, self.data, self.block_type, self.pos = canvas, data, block_type, pos
        self.block = None
    def execute(self): self.block = self.canvas._do_add_block(self.data, self.block_type, self.pos)
    def undo(self):
        if self.block: self.canvas._do_remove_block(self.block)

class RemoveBlockCmd(Command):
    def __init__(self, canvas, block):
        super().__init__(f"Remove {block.block_type}")
        self.canvas, self.block, self.data = canvas, block, block.data
        self.block_type, self.pos = block.block_type, block.pos()
        self.conns = [(c.source, c.target) for port in block.ports for c in port.connections[:]]
    def execute(self): self.canvas._do_remove_block(self.block)
    def undo(self):
        self.block = self.canvas._do_add_block(self.data, self.block_type, self.pos)
        for src, tgt in self.conns: self.canvas._do_connect(src, tgt)

class MoveBlockCmd(Command):
    def __init__(self, block, old_pos, new_pos):
        super().__init__("Move block")
        self.block, self.old_pos, self.new_pos = block, old_pos, new_pos
    def execute(self): self.block.move(self.new_pos)
    def undo(self): self.block.move(self.old_pos)

class ConnectCmd(Command):
    def __init__(self, canvas, port_out, port_in):
        super().__init__("Connect ports")
        self.canvas, self.port_out, self.port_in = canvas, port_out, port_in
        self.conn = None
    def execute(self): self.conn = self.canvas._do_connect(self.port_out, self.port_in)
    def undo(self):
        if self.conn: self.canvas._do_disconnect(self.conn)

class DisconnectCmd(Command):
    def __init__(self, canvas, conn):
        super().__init__("Disconnect ports")
        self.canvas, self.conn = canvas, conn
        self.src, self.tgt = conn.source, conn.target
    def execute(self): self.canvas._do_disconnect(self.conn)
    def undo(self): self.canvas._do_connect(self.src, self.tgt)

class GroupBlocksCmd(Command):
    def __init__(self, canvas, blocks, group_name):
        super().__init__(f"Group {len(blocks)} blocks")
        self.canvas, self.blocks, self.group_name = canvas, blocks, group_name
        self.group = None
    def execute(self): self.group = self.canvas._do_group(self.blocks, self.group_name)
    def undo(self):
        if self.group: self.canvas._do_ungroup(self.group)

class UndoManager(QObject):
    history_changed = pyqtSignal()
    def __init__(self, max_history=50):
        super().__init__()
        self.history, self.index, self.max_history = [], -1, max_history

    def push(self, cmd):
        if self.index < len(self.history) - 1:
            self.history = self.history[:self.index + 1]
        self.history.append(cmd)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.index += 1
        cmd.execute()
        self.history_changed.emit()

    def undo(self):
        if self.index >= 0:
            cmd = self.history[self.index]
            cmd.undo()
            self.index -= 1
            self.history_changed.emit()
            return cmd.description
        return None

    def redo(self):
        if self.index < len(self.history) - 1:
            self.index += 1
            cmd = self.history[self.index]
            cmd.execute()
            self.history_changed.emit()
            return cmd.description
        return None

    def can_undo(self): return self.index >= 0
    def can_redo(self): return self.index < len(self.history) - 1

# ═══════════════════════════════════════════════════════════════════
#  CANVAS BLOCK v2 (Clean Modern Design)
# ═══════════════════════════════════════════════════════════════════
class CanvasBlock(QFrame):
    BLOCK_FUNCTION  = 'function'
    BLOCK_VARIABLE  = 'variable'
    BLOCK_CONTROL   = 'control'
    BLOCK_GROUP     = 'group'

    selected_signal = pyqtSignal(object)
    remove_signal   = pyqtSignal(object)
    port_clicked    = pyqtSignal(object, object)
    moved_signal    = pyqtSignal(object, QPoint, QPoint)

    def __init__(self, data, block_type, parent=None):
        super().__init__(parent)
        self.data, self.block_type = data, block_type
        self.block_id = str(uuid.uuid4())[:8]
        self._selected, self._drag_pos, self._old_pos = False, None, None
        self.ports, self.is_group = [], block_type == self.BLOCK_GROUP
        self.group_children, self.collapsed = [], False
        self.setFixedWidth(260)
        self._build_ui()
        self._build_ports()
        self._apply_style()

    def _color(self):
        return {
            self.BLOCK_FUNCTION: C['fn_color'],
            self.BLOCK_VARIABLE: C['var_color'],
            self.BLOCK_CONTROL:  C['ctrl_color'],
            self.BLOCK_GROUP:    C['amber'],
        }.get(self.block_type, C['green'])

    def _icon(self):
        return {
            self.BLOCK_FUNCTION: '⚙',
            self.BLOCK_VARIABLE: '◈',
            self.BLOCK_CONTROL:  '⬡',
            self.BLOCK_GROUP:    '▣',
        }.get(self.block_type, '•')

    def _build_ports(self):
        self.ports.clear()
        if self.block_type == self.BLOCK_FUNCTION:
            self.ports.append(NodePort('flow_in', 'flow', 'in', NodePort.PORT_FLOW, self))
            self.ports.append(NodePort('flow_out', 'flow', 'out', NodePort.PORT_FLOW, self))
            params = self.data.get('parameters', [])
            for i, p in enumerate(params):
                self.ports.append(NodePort(p.get('name', f'arg{i}'), p.get('datatype', 'object'), 'in', NodePort.PORT_DATA, self, i, len(params)))
            ret = self.data.get('returns', {})
            if isinstance(ret, dict) and ret.get('datatype', 'void') != 'void':
                self.ports.append(NodePort('return', ret.get('datatype', 'object'), 'out', NodePort.PORT_DATA, self, 0, 1))
        elif self.block_type == self.BLOCK_VARIABLE:
            self.ports.append(NodePort('flow_in', 'flow', 'in', NodePort.PORT_FLOW, self))
            self.ports.append(NodePort('flow_out', 'flow', 'out', NodePort.PORT_FLOW, self))
            self.ports.append(NodePort(self.data.get('name', 'val'), self.data.get('datatype', 'object'), 'out', NodePort.PORT_DATA, self, 0, 1))
        elif self.block_type == self.BLOCK_CONTROL:
            self.ports.append(NodePort('flow_in', 'flow', 'in', NodePort.PORT_FLOW, self))
            struct = self.data.get('structure', '')
            if struct == 'if':
                self.ports.append(NodePort('flow_true', 'flow', 'out', NodePort.PORT_FLOW, self))
                self.ports.append(NodePort('flow_false', 'flow', 'out', NodePort.PORT_FLOW, self))
                self.ports.append(NodePort('condition', 'bool', 'in', NodePort.PORT_DATA, self, 0, 1))
            else:
                self.ports.append(NodePort('flow_out', 'flow', 'out', NodePort.PORT_FLOW, self))
                if struct in ('for', 'foreach', 'while'):
                    self.ports.append(NodePort('collection', 'object', 'in', NodePort.PORT_DATA, self, 0, 1))
        elif self.block_type == self.BLOCK_GROUP:
            self.ports.append(NodePort('flow_in', 'flow', 'in', NodePort.PORT_FLOW, self))
            self.ports.append(NodePort('flow_out', 'flow', 'out', NodePort.PORT_FLOW, self))

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)
        if self.is_group:
            self._build_group_ui(layout)
            return

        hdr = QHBoxLayout()
        icon_lbl = QLabel(self._icon())
        icon_lbl.setStyleSheet(f"color: {self._color()}; font-size: 14px;")
        name = self.data.get('name', self.data.get('structure', '?'))
        self.name_lbl = QLabel(name)
        self.name_lbl.setStyleSheet(f"color: {self._color()}; font-weight: bold; font-size: 12px;")
        self.close_btn = QPushButton('✕')
        self.close_btn.setFixedSize(16, 16)
        self.close_btn.setStyleSheet(f"QPushButton {{background: transparent; color: {C['text_dim']}; border: none; font-size: 10px; padding: 0;}} QPushButton:hover {{color: {C['red']};}}")
        self.close_btn.clicked.connect(lambda: self.remove_signal.emit(self))

        hdr.addWidget(icon_lbl)
        hdr.addWidget(self.name_lbl)
        hdr.addStretch()
        hdr.addWidget(self.close_btn)
        layout.addLayout(hdr)

        if self.block_type == self.BLOCK_FUNCTION:
            sub = QLabel(f"{self.data.get('language', '')}  │  {self.data.get('famille', '')}")
            sub.setStyleSheet(f"color: {C['text_dim']}; font-size: 9px;")
            layout.addWidget(sub)
        elif self.block_type == self.BLOCK_VARIABLE:
            sub = QLabel(f"{self.data.get('datatype', '')}  │  {self.data.get('scope', '')}")
            sub.setStyleSheet(f"color: {C['text_dim']}; font-size: 9px;")
            layout.addWidget(sub)
        elif self.block_type == self.BLOCK_CONTROL:
            sub = QLabel(self.data.get('description', ''))
            sub.setStyleSheet(f"color: {C['text_dim']}; font-size: 9px;")
            sub.setWordWrap(True)
            layout.addWidget(sub)

        type_badge = QLabel(f" {self.block_type.upper()} ")
        type_badge.setStyleSheet(f"background-color: {self._color()}22; color: {self._color()}; border: 1px solid {self._color()}44; font-size: 8px; padding: 1px 4px; border-radius: 3px;")
        layout.addWidget(type_badge)
        self.setMinimumHeight(layout.sizeHint().height() + 16)

    def _build_group_ui(self, layout):
        self.group_title = QLabel(self.data.get('name', 'GROUP'))
        self.group_title.setStyleSheet(f"color: {C['amber']}; font-weight: bold; font-size: 13px;")
        layout.addWidget(self.group_title)
        info = QLabel(f"[{len(self.group_children)} blocks]")
        info.setStyleSheet(f"color: {C['text_dim']}; font-size: 9px;")
        layout.addWidget(info)
        self.setStyleSheet(f"CanvasBlock {{ background-color: {C['bg_card']}; border: 2px dashed {C['accent']}66; border-radius: 8px; }}")
        self.setMinimumHeight(80)
        self.setMinimumWidth(300)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for port in self.ports:
            r = port.rect()
            color = QColor(C['white']) if port._hot else QColor(port.color())
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor(C['bg']), 1) if not port._hot else QPen(QColor(C['accent']), 2))

            if port.port_type == NodePort.PORT_FLOW:
                tri = QPainterPath()
                c = r.center()
                if port.direction == 'in':
                    tri.moveTo(c.x(), c.y() - 5); tri.lineTo(c.x() - 4, c.y() + 3); tri.lineTo(c.x() + 4, c.y() + 3)
                else:
                    tri.moveTo(c.x(), c.y() + 5); tri.lineTo(c.x() - 4, c.y() - 3); tri.lineTo(c.x() + 4, c.y() - 3)
                tri.closeSubpath()
                painter.drawPath(tri)
            else:
                painter.drawEllipse(r)

            painter.setPen(QColor(C['text_dim']))
            painter.setFont(QFont('Consolas', 8))
            if port.direction == 'in' and port.port_type == NodePort.PORT_DATA:
                painter.drawText(r.x() + 14, r.y() + 7, port.name[:10])
            elif port.direction == 'out' and port.port_type == NodePort.PORT_DATA:
                tw = painter.fontMetrics().width(port.name[:10])
                painter.drawText(r.x() - tw - 6, r.y() + 7, port.name[:10])
        painter.end()

    def port_at(self, pos):
        for port in self.ports:
            if port.rect().adjusted(-4, -4, 4, 4).contains(pos):
                return port
        return None

    def _apply_style(self):
        if self.is_group: return
        col = self._color()
        self.setStyleSheet(f"""
            CanvasBlock {{
                background-color: {C['bg_card']};
                border: 1px solid {C['border']};
                border-left: 4px solid {col};
                border-radius: 6px;
            }}
            CanvasBlock:hover {{
                background-color: {C['bg_hover']};
                border-color: {C['text_dim']};
                border-left: 4px solid {col};
            }}
        """)
        self.setCursor(QCursor(Qt.OpenHandCursor))

    def set_selected(self, selected):
        self._selected = selected
        col = self._color()
        if self.is_group: return

        if selected:
            self.setStyleSheet(f"CanvasBlock {{ background-color: {C['bg_panel']}; border: 1px solid {col}; border-left: 4px solid {col}; border-radius: 6px; }}")
            glow = QGraphicsDropShadowEffect(self)
            glow.setBlurRadius(12)
            glow.setColor(QColor(0, 0, 0, 80))
            glow.setOffset(0, 4)
            self.setGraphicsEffect(glow)
        else:
            self.setGraphicsEffect(None)
            self._apply_style()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            port = self.port_at(event.pos())
            if port:
                self.port_clicked.emit(self, port)
                return
            self._drag_pos = event.pos()
            self._old_pos = self.pos()
            self.selected_signal.emit(self)
            self.setCursor(QCursor(Qt.ClosedHandCursor))
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._drag_pos and self._old_pos and self.pos() != self._old_pos:
            self.moved_signal.emit(self, self._old_pos, self.pos())
        self._drag_pos = None
        self._old_pos = None
        self.setCursor(QCursor(Qt.OpenHandCursor))
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            delta = event.pos() - self._drag_pos
            new_pos = self.pos() + delta

            if self.parent() and hasattr(self.parent(), 'ensure_visible'):
                self.parent().ensure_visible(new_pos + QPoint(self.width(), self.height()))

            if self.parent():
                nx = max(0, new_pos.x())
                ny = max(0, new_pos.y())
                self.move(nx, ny)
                if self.is_group:
                    for child in self.group_children:
                        child.move(child.pos() + QPoint(nx, ny) - (self.pos() - delta))
        super().mouseMoveEvent(event)

# ═══════════════════════════════════════════════════════════════════
#  CANVAS WIDGET v2.1 (Scrollable, No CRT)
# ═══════════════════════════════════════════════════════════════════
class CanvasWidget(QWidget):
    selection_changed = pyqtSignal(object)
    canvas_changed    = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.blocks, self.connections, self.selected_blocks = [], [], []
        self.undo_manager = UndoManager(max_history=100)
        self.undo_manager.history_changed.connect(self._on_undo_state)
        self._dragging_conn, self._temp_conn_end = None, None
        self._marquee_rect, self._marquee_start = None, None

        self.setMinimumSize(2000, 1500)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

    def _on_undo_state(self):
        self.canvas_changed.emit()

    def ensure_visible(self, pos, margin=200):
        needed_w = pos.x() + margin
        needed_h = pos.y() + margin
        changed = False

        if needed_w > self.minimumWidth():
            self.setMinimumWidth(needed_w)
            changed = True
        if needed_h > self.minimumHeight():
            self.setMinimumHeight(needed_h)
            changed = True

        if changed:
            self.update()
            if self.parent() and hasattr(self.parent(), 'setMinimumSize'):
                self.parent().setMinimumSize(self.minimumSize())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(C['bg']))

        painter.setPen(QPen(QColor(C['border']), 1, Qt.DotLine))
        step = 40
        for x in range(0, self.width(), step):
            for y in range(0, self.height(), step):
                painter.drawPoint(x, y)

        for conn in self.connections:
            path = conn.path()
            pen = QPen(QColor(conn.color()), 2)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.drawPath(path)

        if self._dragging_conn:
            path = self._dragging_conn[1].path()
            pen = QPen(QColor(C['accent']), 2, Qt.DashLine)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.drawPath(path)

        if self._marquee_rect:
            painter.setPen(QPen(QColor(C['accent']), 1, Qt.DashLine))
            painter.setBrush(QBrush(QColor(C['accent'] + '22')))
            painter.drawRect(self._marquee_rect)

        painter.setPen(QColor(C['text_dim']))
        f = QFont('Segoe UI', 9)
        painter.setFont(f)
        painter.drawText(12, 24, "CODEFORGE v2.1 — NODAL CANVAS")
        painter.drawText(12, self.height() - 16, f"Blocks: {len(self.blocks)}  |  Connections: {len(self.connections)}")

        status = "Drag ports to connect  |  Ctrl+G: Group  |  A: Auto-Layout  |  Del: Remove"
        sw = painter.fontMetrics().width(status)
        painter.drawText(self.width() - sw - 12, self.height() - 16, status)

        if not self.blocks:
            painter.setPen(QColor(C['text_dim']))
            f2 = QFont('Segoe UI', 14, QFont.Light)
            painter.setFont(f2)
            msg = "Drag elements from the library and link their ports"
            w = painter.fontMetrics().width(msg)
            painter.drawText((self.width() - w) // 2, self.height() // 2, msg)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for block in self.blocks:
                local = block.mapFromParent(event.pos())
                port = block.port_at(local)
                if port and port.direction == 'out':
                    temp_conn = NodeConnection(port, port)
                    temp_conn._temp_end = event.pos()
                    self._dragging_conn = (port, temp_conn)
                    self._temp_conn_end = event.pos()
                    return

            clicked_block = next((b for b in reversed(self.blocks) if b.geometry().contains(event.pos())), None)
            if clicked_block:
                if not (event.modifiers() & Qt.ControlModifier):
                    self._clear_selection()
                self._select_block(clicked_block)
            else:
                self._clear_selection()
                self._marquee_start = event.pos()
                self._marquee_rect = QRect(event.pos(), QSize(0, 0))
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging_conn:
            self._temp_conn_end = event.pos()
            self._dragging_conn[1]._temp_end = event.pos()
            for block in self.blocks:
                for port in block.ports:
                    if port.direction == 'in' and port.parent != self._dragging_conn[0].parent:
                        local = block.mapFromParent(event.pos())
                        port._hot = port.rect().adjusted(-8, -8, 8, 8).contains(local)
                    else:
                        port._hot = False
                block.update()
            self.update()
            return
        if self._marquee_start:
            self._marquee_rect = QRect(self._marquee_start, event.pos()).normalized()
            self.update()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._dragging_conn:
            src_port = self._dragging_conn[0]
            for block in self.blocks:
                local = block.mapFromParent(event.pos())
                port = block.port_at(local)
                if port and port.direction == 'in' and port.parent != src_port.parent:
                    if src_port.can_connect_to(port):
                        if not any(c.source == src_port and c.target == port for c in self.connections):
                            self.undo_manager.push(ConnectCmd(self, src_port, port))
                            self.canvas_changed.emit()
                    break
            for block in self.blocks:
                for port in block.ports: port._hot = False
                block.update()
            self._dragging_conn = None
            self.update()
            return
        if self._marquee_rect:
            for block in self.blocks:
                if self._marquee_rect.intersects(block.geometry()):
                    self._select_block(block)
            self._marquee_rect = None
            self._marquee_start = None
            self.update()
            return
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        key, mods = event.key(), event.modifiers()
        if key in (Qt.Key_Delete, Qt.Key_Backspace): self._delete_selected()
        elif key == Qt.Key_G and (mods & Qt.ControlModifier) and (mods & Qt.ShiftModifier): self._ungroup_selected()
        elif key == Qt.Key_G and (mods & Qt.ControlModifier): self._group_selected()
        elif key == Qt.Key_A and (mods & Qt.ControlModifier): self._select_all()
        elif key == Qt.Key_L and (mods & Qt.ControlModifier): self.auto_layout()
        elif key == Qt.Key_Z and (mods & Qt.ControlModifier) and (mods & Qt.ShiftModifier):
            desc = self.undo_manager.redo()
            if desc: self._emit_status(f"Redo: {desc}")
        elif key == Qt.Key_Z and (mods & Qt.ControlModifier):
            desc = self.undo_manager.undo()
            if desc: self._emit_status(f"Undo: {desc}")
        elif key == Qt.Key_Y and (mods & Qt.ControlModifier):
            desc = self.undo_manager.redo()
            if desc: self._emit_status(f"Redo: {desc}")
        else:
            super().keyPressEvent(event)

    def _emit_status(self, msg): pass
    def _clear_selection(self):
        for b in self.selected_blocks: b.set_selected(False)
        self.selected_blocks.clear()
        self.selection_changed.emit(None)

    def _select_block(self, block):
        if block not in self.selected_blocks:
            self.selected_blocks.append(block)
            block.set_selected(True)
            self.selection_changed.emit(block)

    def _delete_selected(self):
        if not self.selected_blocks: return
        for block in list(self.selected_blocks):
            self.undo_manager.push(RemoveBlockCmd(self, block))
        self._clear_selection()
        self.canvas_changed.emit()

    def _group_selected(self):
        if len(self.selected_blocks) < 2: return
        name, ok = QInputDialog.getText(self, "Group Blocks", "Group name:", text="Macro_01")
        if ok and name:
            self.undo_manager.push(GroupBlocksCmd(self, list(self.selected_blocks), name))
            self._clear_selection()
            self.canvas_changed.emit()

    def _ungroup_selected(self):
        for block in list(self.selected_blocks):
            if block.is_group:
                self.undo_manager.push(DisconnectGroupCmd(self, block))
        self._clear_selection()

    def _select_all(self):
        self._clear_selection()
        for b in self.blocks: self._select_block(b)

    def _do_add_block(self, data, block_type, pos):
        block = CanvasBlock(data, block_type, self)
        block.selected_signal.connect(self._on_block_selected)
        block.remove_signal.connect(self._do_remove_block)
        block.port_clicked.connect(self._on_port_clicked)
        block.moved_signal.connect(self._on_block_moved)
        block.move(pos.x(), pos.y())

        self.ensure_visible(pos + QPoint(block.width(), block.height()))

        block.show()
        self.blocks.append(block)
        self.canvas_changed.emit()
        return block

    def _do_remove_block(self, block):
        if block in self.blocks:
            for port in block.ports:
                for c in port.connections[:]: self._do_disconnect(c)
            self.blocks.remove(block)
            if block in self.selected_blocks: self.selected_blocks.remove(block)
            block.hide()
            block.deleteLater()
            self.canvas_changed.emit()

    def _do_connect(self, port_out, port_in):
        conn = NodeConnection(port_out, port_in)
        self.connections.append(conn)
        self.update()
        return conn

    def _do_disconnect(self, conn):
        if conn in self.connections:
            conn.delete()
            self.connections.remove(conn)
            self.update()

    def _do_group(self, blocks, name):
        xs, ys, ws, hs = [b.x() for b in blocks], [b.y() for b in blocks], [b.width() for b in blocks], [b.height() for b in blocks]
        margin = 20
        gx, gy = min(xs) - margin, min(ys) - margin
        gw = max([x + w for x, w in zip(xs, ws)]) - min(xs) + margin * 2
        gh = max([y + h for y, h in zip(ys, hs)]) - min(ys) + margin * 2

        group = CanvasBlock({'name': name, 'type': 'group'}, CanvasBlock.BLOCK_GROUP, self)
        group.move(gx, gy)
        group.setFixedSize(gw, gh)
        group.group_children = blocks
        group.show()
        for b in blocks: group.stackUnder(b)
        self.blocks.append(group)
        self.update()
        return group

    def _do_ungroup(self, group):
        if group in self.blocks:
            self.blocks.remove(group)
            group.hide()
            group.deleteLater()
            self.update()

    def _on_block_selected(self, block):
        if not (QApplication.keyboardModifiers() & Qt.ControlModifier):
            self._clear_selection()
        self._select_block(block)

    def _on_port_clicked(self, block, port): pass

    def _on_block_moved(self, block, old_pos, new_pos):
        self.undo_manager.push(MoveBlockCmd(block, old_pos, new_pos))

    def add_block(self, data, block_type):
        pos = QPoint(20 + (len(self.blocks) % 3) * 280, 20 + (len(self.blocks) // 3) * 160)
        cmd = AddBlockCmd(self, data, block_type, pos)
        self.undo_manager.push(cmd)
        return cmd.block

    def clear(self):
        self.undo_manager = UndoManager(max_history=100)
        self.undo_manager.history_changed.connect(self._on_undo_state)
        for b in list(self.blocks):
            b.hide()
            b.deleteLater()
        self.blocks.clear()
        self.connections.clear()
        self.selected_blocks.clear()
        self.selection_changed.emit(None)
        self.canvas_changed.emit()
        self.setMinimumSize(2000, 1500)
        if self.parent() and hasattr(self.parent(), 'setMinimumSize'):
            self.parent().setMinimumSize(2000, 1500)
        self.update()

    def auto_layout(self):
        if not self.blocks: return
        adj, indeg = defaultdict(list), defaultdict(int)
        all_blocks = set(self.blocks)
        for conn in self.connections:
            if conn.source.port_type == NodePort.PORT_FLOW and conn.source.direction == 'out':
                src, tgt = conn.source.parent, conn.target.parent
                if src in all_blocks and tgt in all_blocks:
                    adj[src].append(tgt)
                    indeg[tgt] += 1
        for b in self.blocks:
            if b not in indeg: indeg[b] = 0

        queue = deque([b for b in self.blocks if indeg[b] == 0])
        layers, layer_idx = {}, 0
        while queue:
            for _ in range(len(queue)):
                b = queue.popleft()
                layers[b] = layer_idx
                for nb in adj[b]:
                    indeg[nb] -= 1
                    if indeg[nb] == 0: queue.append(nb)
            layer_idx += 1
        for b in self.blocks:
            if b not in layers: layers[b] = layer_idx

        layer_counts = defaultdict(int)
        for b in self.blocks:
            li = layers[b]
            b.move(40 + li * 320, 40 + layer_counts[li] * 180)
            layer_counts[li] += 1

        if self.blocks:
            max_x = max(b.x() + b.width() for b in self.blocks) + 200
            max_y = max(b.y() + b.height() for b in self.blocks) + 200
            self.setMinimumWidth(max(max_x, 2000))
            self.setMinimumHeight(max(max_y, 1500))
            if self.parent() and hasattr(self.parent(), 'setMinimumSize'):
                self.parent().setMinimumSize(self.minimumSize())

        self.update()

    def get_ordered_blocks(self):
        if not any(c.source.port_type == NodePort.PORT_FLOW for c in self.connections):
            return sorted(self.blocks, key=lambda b: (b.y(), b.x()))
        adj, indeg = defaultdict(list), defaultdict(int)
        for conn in self.connections:
            if conn.source.port_type == NodePort.PORT_FLOW:
                adj[conn.source.parent].append(conn.target.parent)
                indeg[conn.target.parent] += 1
        for b in self.blocks:
            if b not in indeg: indeg[b] = 0

        queue = deque([b for b in self.blocks if indeg[b] == 0])
        ordered = []
        while queue:
            b = queue.popleft()
            ordered.append(b)
            for nb in adj[b]:
                indeg[nb] -= 1
                if indeg[nb] == 0: queue.append(nb)
        return ordered + sorted([b for b in self.blocks if b not in ordered], key=lambda b: (b.y(), b.x()))

    def to_dict(self):
        return {
            'blocks': [{'block_id': b.block_id, 'block_type': b.block_type, 'data': b.data, 'pos': {'x': b.x(), 'y': b.y()}, 'is_group': b.is_group, 'children_ids': [c.block_id for c in b.group_children] if b.is_group else []} for b in self.blocks],
            'connections': [{'src_block': c.source.parent.block_id, 'src_port': c.source.name, 'tgt_block': c.target.parent.block_id, 'tgt_port': c.target.name} for c in self.connections],
        }

    def from_dict(self, data):
        self.clear()
        block_map = {}
        for bd in data.get('blocks', []):
            block = self._do_add_block(bd['data'], bd['block_type'], QPoint(bd['pos']['x'], bd['pos']['y']))
            block_map[block.block_id] = block
            if bd.get('is_group'):
                block.is_group = True
                block.group_children = []
        for bd in data.get('blocks', []):
            if bd.get('is_group'):
                bid = bd.get('block_id')
                if bid in block_map:
                    for cid in bd.get('children_ids', []):
                        if cid in block_map: block_map[bid].group_children.append(block_map[cid])
        for cd in data.get('connections', []):
            src_b, tgt_b = block_map.get(cd['src_block']), block_map.get(cd['tgt_block'])
            if src_b and tgt_b:
                src_p = next((p for p in src_b.ports if p.name == cd['src_port']), None)
                tgt_p = next((p for p in tgt_b.ports if p.name == cd['tgt_port']), None)
                if src_p and tgt_p: self._do_connect(src_p, tgt_p)
        self.update()

# ═══════════════════════════════════════════════════════════════════
#  CODE GENERATOR v2.1 (C#, PS, JS, Python, Bash)
# ═══════════════════════════════════════════════════════════════════
class CodeGenerator:
    _temp_counter = 0

    @staticmethod
    def generate(canvas_blocks, connections, language, program_name='GeneratedProgram', wrap_class=True):
        ordered = canvas_blocks
        lang = language
        data_src, flow_next = {}, defaultdict(list)
        for c in connections:
            if c.source.port_type == NodePort.PORT_DATA: data_src[c.target] = c.source
            elif c.source.port_type == NodePort.PORT_FLOW and c.source.direction == 'out':
                flow_next[c.source.parent].append(c.target.parent)

        fns = [b for b in ordered if b.block_type == CanvasBlock.BLOCK_FUNCTION and b.data.get('language', lang) == lang]
        vars_ = [b for b in ordered if b.block_type == CanvasBlock.BLOCK_VARIABLE and b.data.get('language', lang) == lang]
        ctrls = [b for b in ordered if b.block_type == CanvasBlock.BLOCK_CONTROL]
        groups = [b for b in ordered if b.block_type == CanvasBlock.BLOCK_GROUP]
        CodeGenerator._temp_counter = 0

        if lang == 'CSharp': return CodeGenerator._gen_csharp_v2(ordered, fns, vars_, ctrls, groups, data_src, flow_next, program_name, wrap_class)
        elif lang == 'PowerShell': return CodeGenerator._gen_ps_v2(ordered, fns, vars_, ctrls, groups, data_src, flow_next, program_name)
        elif lang == 'JavaScript': return CodeGenerator._gen_js_v2(ordered, fns, vars_, ctrls, groups, data_src, flow_next, program_name)
        elif lang == 'Python': return CodeGenerator._gen_py_v2(ordered, fns, vars_, ctrls, groups, data_src, flow_next, program_name)
        elif lang == 'Bash': return CodeGenerator._gen_bash_v2(ordered, fns, vars_, ctrls, groups, data_src, flow_next, program_name)
        return f"# ERROR: Unsupported language '{lang}'"

    @staticmethod
    def _temp_var():
        CodeGenerator._temp_counter += 1
        return f"__auto_{CodeGenerator._temp_counter}"

    @staticmethod
    def _resolve_input(port, data_src, emitted):
        if port not in data_src: return None
        src = data_src[port]
        if src.parent.block_type == CanvasBlock.BLOCK_VARIABLE: return src.parent.data.get('name', 'var')
        return emitted.get(src) if src in emitted else None

    @staticmethod
    def _gen_csharp_v2(ordered, fns, vars_, ctrls, groups, data_src, flow_next, name, wrap_class):
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        lines = [f"// Generated by CODEFORGE v2.1 [NODAL] - {ts}", "", "using System;", "using System.IO;", "using System.Collections.Generic;", ""]
        if wrap_class: lines += [f"namespace CodeForge.Generated {{ public class {name} {{"]
        indent = "    " if wrap_class else ""

        if vars_:
            lines.append(indent + "// ─── Variables ───────────────────────────────")
            for b in vars_:
                d = b.data
                scope = 'public static' if d.get('scope') == 'global' else 'private static'
                lines.append(f"{indent}{scope} {d.get('datatype', 'object')} {d.get('name', 'variable')} = {d.get('default_value', 'null')};")
            lines.append("")

        if fns:
            lines.append(indent + "// ─── Function Definitions ──────────────────")
            for b in fns:
                for line in b.data.get('source', '// [source not available]').split('\n'):
                    lines.append(indent + line)
            lines.append("")

        lines.append(indent + "// ─── Entry Point (Dataflow) ───────────────")
        lines.append(indent + "public static void Main(string[] args) {")
        lines.append(f'{indent}    Console.WriteLine("[INFO] Starting {name}");')
        emitted = {}
        for b in ordered:
            if b.block_type == CanvasBlock.BLOCK_VARIABLE: continue
            elif b.block_type == CanvasBlock.BLOCK_FUNCTION:
                d = b.data
                args_list = []
                for p in d.get('parameters', []):
                    port = next((port for port in b.ports if port.name == p.get('name') and port.direction == 'in'), None)
                    if port and port in data_src:
                        val = CodeGenerator._resolve_input(port, data_src, emitted)
                        args_list.append(val if val else (p.get('default', 'null') if not p.get('required') else 'null'))
                    else:
                        args_list.append(p.get('default', 'null') if not p.get('required') else 'null')

                ret = d.get('returns', {})
                has_ret = isinstance(ret, dict) and ret.get('datatype', 'void') != 'void'
                if has_ret:
                    ret_port = next((p for p in b.ports if p.name == 'return' and p.direction == 'out'), None)
                    # CORRECTION: vérifier si le port de retour est utilisé dans data_src (comme source)
                    if ret_port and ret_port in data_src.values():
                        tv = CodeGenerator._temp_var()
                        emitted[ret_port] = tv
                        lines.append(f"{indent}    var {tv} = {d.get('name', 'Func')}({', '.join(args_list)});")
                    else:
                        lines.append(f"{indent}    {d.get('name', 'Func')}({', '.join(args_list)});")
                else:
                    lines.append(f"{indent}    {d.get('name', 'Func')}({', '.join(args_list)});")
            elif b.block_type == CanvasBlock.BLOCK_CONTROL:
                CodeGenerator._emit_ctrl_cs_v2(lines, b.data.get('structure', ''), b.data, b, data_src, flow_next, indent + "    ", emitted)
        lines.append(f'{indent}    Console.WriteLine("[INFO] {name} completed.");')
        lines.append(indent + "}")
        if wrap_class: lines += ["    }", "}"]
        return '\n'.join(lines)

    @staticmethod
    def _emit_ctrl_cs_v2(lines, struct, data, block, data_src, flow_next, indent, emitted):
        if struct == 'if':
            cond_port = next((p for p in block.ports if p.name == 'condition'), None)
            cond = CodeGenerator._resolve_input(cond_port, data_src, emitted) if cond_port and cond_port in data_src else data.get('condition', 'true')
            lines.extend([f"{indent}if ({cond}) {{", f"{indent}    // TODO: true branch", f"{indent}}}"])
        elif struct == 'for':
            lines.extend([f"{indent}for (int {data.get('var', 'i')} = 0; {data.get('var', 'i')} < {data.get('limit', '10')}; {data.get('var', 'i')}++) {{", f"{indent}    // TODO: loop body", f"{indent}}}"])
        elif struct == 'foreach':
            coll_port = next((p for p in block.ports if p.name == 'collection'), None)
            coll = CodeGenerator._resolve_input(coll_port, data_src, emitted) if coll_port and coll_port in data_src else data.get('collection', 'collection')
            lines.extend([f"{indent}foreach (var {data.get('item', 'item')} in {coll}) {{", f"{indent}    // TODO: foreach body", f"{indent}}}"])
        elif struct == 'while':
            lines.extend([f"{indent}while ({data.get('condition', 'true')}) {{", f"{indent}    // TODO: while body", f"{indent}}}"])
        elif struct == 'try_catch':
            lines.extend([f"{indent}try {{", f"{indent}    // TODO: try block", f"{indent}}} catch ({data.get('exception', 'Exception')} ex) {{", f'{indent}    Console.WriteLine($"Error: {{ex.Message}}");', f"{indent}}}"])

    @staticmethod
    def _gen_ps_v2(ordered, fns, vars_, ctrls, groups, data_src, flow_next, name):
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        lines = [f"# Generated by CODEFORGE v2.1 [NODAL] - {ts}", "#Requires -Version 5.1", "Set-StrictMode -Version Latest", "$ErrorActionPreference = 'Stop'", ""]
        if vars_:
            lines.append("# ─── Variables ───────────────────────────────────")
            for b in vars_:
                d = b.data
                lines.append(f"${d.get('name', 'var')} = {d.get('default_value', '$null')}")
            lines.append("")
        if fns:
            lines.append("# ─── Functions ───────────────────────────────────")
            for b in fns: lines += b.data.get('source', '# [none]').split('\n')
            lines.append("")
        lines.extend(["# ─── Main Execution ──────────────────────────────", f'Write-Host "[INFO] Starting {name}" -ForegroundColor Green', ""])
        emitted = {}
        for b in ordered:
            if b.block_type == CanvasBlock.BLOCK_VARIABLE: continue
            elif b.block_type == CanvasBlock.BLOCK_FUNCTION:
                d = b.data
                args_list = []
                for p in d.get('parameters', []):
                    port = next((port for port in b.ports if port.name == p.get('name') and port.direction == 'in'), None)
                    if port and port in data_src:
                        val = CodeGenerator._resolve_input(port, data_src, emitted)
                        args_list.append(f"${val}" if val else (p.get('default', '$null') if not p.get('required') else '$null'))
                    else:
                        args_list.append(p.get('default', '$null') if not p.get('required') else '$null')
                ret = d.get('returns', {})
                has_ret = isinstance(ret, dict) and ret.get('datatype', 'void') != 'void'
                if has_ret:
                    ret_port = next((p for p in b.ports if p.name == 'return' and p.direction == 'out'), None)
                    # CORRECTION: vérifier si le port de retour est utilisé comme source
                    if ret_port and ret_port in data_src.values():
                        tv = CodeGenerator._temp_var()
                        emitted[ret_port] = tv
                        lines.append(f"${tv} = {d.get('name', 'Func')} {', '.join(args_list)}")
                    else:
                        lines.append(f"{d.get('name', 'Func')} {', '.join(args_list)}")
                else:
                    lines.append(f"{d.get('name', 'Func')} {', '.join(args_list)}")
            elif b.block_type == CanvasBlock.BLOCK_CONTROL:
                CodeGenerator._emit_ctrl_ps_v2(lines, b.data.get('structure', ''), b.data)
        lines.append(f'Write-Host "[INFO] {name} completed." -ForegroundColor Green')
        return '\n'.join(lines)

    @staticmethod
    def _emit_ctrl_ps_v2(lines, struct, data, indent=0):
        pad = ' ' * indent
        if struct == 'if': lines.extend([f"{pad}if ({data.get('condition', '$true')}) {{", f"{pad}    # TODO", f"{pad}}}"])
        elif struct == 'for': lines.extend([f"{pad}for (${data.get('var', 'i')} = 0; ${data.get('var', 'i')} -lt {data.get('limit', '10')}; ${data.get('var', 'i')}++) {{", f"{pad}    # TODO", f"{pad}}}"])
        elif struct == 'foreach': lines.extend([f"{pad}foreach (${data.get('item', 'item')} in {data.get('collection', '$collection')}) {{", f"{pad}    # TODO", f"{pad}}}"])
        elif struct == 'while': lines.extend([f"{pad}while ({data.get('condition', '$true')}) {{", f"{pad}    # TODO", f"{pad}}}"])
        elif struct == 'try_catch': lines.extend([f"{pad}try {{", f"{pad}    # TODO", f"{pad}}} catch {{", f"{pad}    Write-Error $_.Exception.Message", f"{pad}}}"])

    @staticmethod
    def _gen_js_v2(ordered, fns, vars_, ctrls, groups, data_src, flow_next, name):
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        lines = [f"// Generated by CODEFORGE v2.1 [NODAL] - {ts}", "'use strict';", ""]
        if vars_:
            lines.append("// ─── Variables ───────────────────────────────────")
            for b in vars_:
                d = b.data
                lines.append(f"{'const' if d.get('scope') == 'global' else 'let'} {d.get('name', 'variable')} = {d.get('default_value', 'null')};")
            lines.append("")
        if fns:
            lines.append("// ─── Functions ───────────────────────────────────")
            for b in fns: lines += b.data.get('source', '// [none]').split('\n')
            lines.append("")
        lines.extend(["// ─── Main Execution ──────────────────────────────", f"(async function {name}() {{", f'  console.log("[INFO] Starting {name}");', ""])
        emitted = {}
        for b in ordered:
            if b.block_type == CanvasBlock.BLOCK_VARIABLE: continue
            elif b.block_type == CanvasBlock.BLOCK_FUNCTION:
                d = b.data
                args_list = []
                for p in d.get('parameters', []):
                    port = next((port for port in b.ports if port.name == p.get('name') and port.direction == 'in'), None)
                    if port and port in data_src:
                        val = CodeGenerator._resolve_input(port, data_src, emitted)
                        args_list.append(val if val else 'null')
                    else:
                        args_list.append('null')
                ret = d.get('returns', {})
                has_ret = isinstance(ret, dict) and ret.get('datatype', 'void') != 'void'
                if has_ret:
                    ret_port = next((p for p in b.ports if p.name == 'return' and p.direction == 'out'), None)
                    # CORRECTION: vérifier si le port de retour est utilisé comme source
                    if ret_port and ret_port in data_src.values():
                        tv = CodeGenerator._temp_var()
                        emitted[ret_port] = tv
                        lines.append(f"  const {tv} = await {d.get('name', 'func')}({', '.join(args_list)});")
                    else:
                        lines.append(f"  await {d.get('name', 'func')}({', '.join(args_list)});")
                else:
                    lines.append(f"  await {d.get('name', 'func')}({', '.join(args_list)});")
            elif b.block_type == CanvasBlock.BLOCK_CONTROL:
                CodeGenerator._emit_ctrl_js_v2(lines, b.data.get('structure', ''), b.data)
        lines.extend([f'  console.log("[INFO] {name} completed.");', "})();"])
        return '\n'.join(lines)

    @staticmethod
    def _emit_ctrl_js_v2(lines, struct, data, indent=2):
        pad = ' ' * indent
        if struct == 'if': lines.extend([f"{pad}if ({data.get('condition', 'true')}) {{", f"{pad}  // TODO", f"{pad}}}"])
        elif struct == 'for': lines.extend([f"{pad}for (let {data.get('var', 'i')} = 0; {data.get('var', 'i')} < {data.get('limit', '10')}; {data.get('var', 'i')}++) {{", f"{pad}  // TODO", f"{pad}}}"])
        elif struct == 'foreach': lines.extend([f"{pad}for (const {data.get('item', 'item')} of {data.get('collection', 'collection')}) {{", f"{pad}  // TODO", f"{pad}}}"])
        elif struct == 'while': lines.extend([f"{pad}while ({data.get('condition', 'true')}) {{", f"{pad}  // TODO", f"{pad}}}"])
        elif struct == 'try_catch': lines.extend([f"{pad}try {{", f"{pad}  // TODO", f"{pad}}} catch (err) {{", f"{pad}  console.error('[ERROR]', err.message);", f"{pad}}}"])

    @staticmethod
    def _gen_py_v2(ordered, fns, vars_, ctrls, groups, data_src, flow_next, name):
        """Generate Python code from nodal canvas."""
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        lines = [
            f"# Generated by CODEFORGE v2.1 [NODAL] - {ts}",
            f"# Program: {name}",
            "",
            "import sys",
            "import os",
            "import json",
            "import logging",
            "from datetime import datetime",
            "from typing import Any, Dict, List, Optional, Tuple, Union",
            "",
            "logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')",
            "logger = logging.getLogger(__name__)",
            "",
        ]

        if vars_:
            lines.append("# ─── Variables ───────────────────────────────────")
            for b in vars_:
                d = b.data
                scope = "" if d.get('scope') == 'local' else "# global"
                val = d.get('default_value', 'None')
                lines.append(f"{d.get('name', 'variable')} = {val}  {scope}")
            lines.append("")

        if fns:
            lines.append("# ─── Function Definitions ────────────────────────")
            for b in fns:
                src = b.data.get('source', '# [source not available]')
                lines += src.split('\n')
                lines.append("")
            lines.append("")

        lines.extend([
            "# ─── Main Execution ──────────────────────────────",
            f"def main() -> None:",
            f'    logger.info("Starting {name}")',
            "",
        ])

        emitted = {}
        indent = "    "

        for b in ordered:
            if b.block_type == CanvasBlock.BLOCK_VARIABLE:
                continue
            elif b.block_type == CanvasBlock.BLOCK_FUNCTION:
                d = b.data
                args_list = []
                for p in d.get('parameters', []):
                    port = next((port for port in b.ports if port.name == p.get('name') and port.direction == 'in'), None)
                    if port and port in data_src:
                        val = CodeGenerator._resolve_input(port, data_src, emitted)
                        args_list.append(val if val else str(p.get('default', 'None')))
                    else:
                        args_list.append(str(p.get('default', 'None')))

                ret = d.get('returns', {})
                has_ret = isinstance(ret, dict) and ret.get('datatype', 'void') not in ('void', 'None', 'NoneType', '')
                fn_name = d.get('name', 'func')

                if has_ret:
                    ret_port = next((p for p in b.ports if p.name == 'return' and p.direction == 'out'), None)
                    # CORRECTION: vérifier si le port de retour est utilisé comme source
                    if ret_port and ret_port in data_src.values():
                        tv = CodeGenerator._temp_var()
                        emitted[ret_port] = tv
                        lines.append(f"{indent}{tv} = {fn_name}({', '.join(args_list)})")
                    else:
                        lines.append(f"{indent}{fn_name}({', '.join(args_list)})")
                else:
                    lines.append(f"{indent}{fn_name}({', '.join(args_list)})")

            elif b.block_type == CanvasBlock.BLOCK_CONTROL:
                CodeGenerator._emit_ctrl_py_v2(lines, b.data.get('structure', ''), b.data, indent, emitted)

        lines.extend([
            f'    logger.info("{name} completed.")',
            "",
            'if __name__ == "__main__":',
            "    main()",
        ])
        return '\n'.join(lines)

    @staticmethod
    def _emit_ctrl_py_v2(lines, struct, data, indent="    ", emitted=None):
        if struct == 'if':
            cond = data.get('condition', 'True')
            lines.extend([
                f"{indent}if {cond}:",
                f"{indent}    pass  # TODO: true branch",
            ])
        elif struct == 'for':
            var = data.get('var', 'i')
            limit = data.get('limit', '10')
            lines.extend([
                f"{indent}for {var} in range({limit}):",
                f"{indent}    pass  # TODO: loop body",
            ])
        elif struct == 'foreach':
            item = data.get('item', 'item')
            coll = data.get('collection', 'collection')
            lines.extend([
                f"{indent}for {item} in {coll}:",
                f"{indent}    pass  # TODO: foreach body",
            ])
        elif struct == 'while':
            cond = data.get('condition', 'True')
            lines.extend([
                f"{indent}while {cond}:",
                f"{indent}    pass  # TODO: while body",
            ])
        elif struct == 'try_catch':
            exc = data.get('exception', 'Exception')
            lines.extend([
                f"{indent}try:",
                f"{indent}    pass  # TODO: try block",
                f"{indent}except {exc} as e:",
                f'{indent}    logger.error(f"Error: {{e}}")',
            ])

    @staticmethod
    def _gen_bash_v2(ordered, fns, vars_, ctrls, groups, data_src, flow_next, name):
        """Generate Bash code from nodal canvas."""
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        lines = [
            f"#!/usr/bin/env bash",
            f"# Generated by CODEFORGE v2.1 [NODAL] - {ts}",
            f"# Program: {name}",
            "",
            'set -euo pipefail',
            'IFS=$\'\n\t\'',
            "",
        ]

        if vars_:
            lines.append("# ─── Variables ───────────────────────────────────")
            for b in vars_:
                d = b.data
                scope = "local" if d.get('scope') == 'local' else ""
                val = d.get('default_value', '""')
                var_name = d.get('name', 'var')
                if scope:
                    lines.append(f'{scope} {var_name}={val}')
                else:
                    lines.append(f'{var_name}={val}')
            lines.append("")

        if fns:
            lines.append("# ─── Function Definitions ────────────────────────")
            for b in fns:
                src = b.data.get('source', '# [source not available]')
                lines += src.split('\n')
                lines.append("")
            lines.append("")

        lines.extend([
            "# ─── Main Execution ──────────────────────────────",
            f'echo "[INFO] Starting {name}"',
            "",
        ])

        emitted = {}
        indent = ""

        for b in ordered:
            if b.block_type == CanvasBlock.BLOCK_VARIABLE:
                continue
            elif b.block_type == CanvasBlock.BLOCK_FUNCTION:
                d = b.data
                args_list = []
                for p in d.get('parameters', []):
                    port = next((port for port in b.ports if port.name == p.get('name') and port.direction == 'in'), None)
                    if port and port in data_src:
                        val = CodeGenerator._resolve_input(port, data_src, emitted)
                        args_list.append(f'"${{{val}}}"' if val else f'"${{{p.get("default", "")}}}"')
                    else:
                        default = p.get('default', '""')
                        args_list.append(f'"${{{default}}}"')

                fn_name = d.get('name', 'func')
                ret = d.get('returns', {})
                has_ret = isinstance(ret, dict) and ret.get('datatype', 'void') != 'void'
                if has_ret:
                    ret_port = next((p for p in b.ports if p.name == 'return' and p.direction == 'out'), None)
                    # CORRECTION: vérifier si le port de retour est utilisé comme source
                    if ret_port and ret_port in data_src.values():
                        tv = CodeGenerator._temp_var()
                        emitted[ret_port] = tv
                        lines.append(f"{indent}{tv}=$({fn_name} {' '.join(args_list)})")
                    else:
                        lines.append(f"{indent}{fn_name} {' '.join(args_list)}")
                else:
                    lines.append(f"{indent}{fn_name} {' '.join(args_list)}")

            elif b.block_type == CanvasBlock.BLOCK_CONTROL:
                CodeGenerator._emit_ctrl_bash_v2(lines, b.data.get('structure', ''), b.data, indent)

        lines.extend([
            f'echo "[INFO] {name} completed."',
        ])
        return '\n'.join(lines)

    @staticmethod
    def _emit_ctrl_bash_v2(lines, struct, data, indent=""):
        if struct == 'if':
            cond = data.get('condition', 'true')
            lines.extend([
                f"{indent}if [[ {cond} ]]; then",
                f"{indent}    : # TODO: true branch",
                f"{indent}fi",
            ])
        elif struct == 'for':
            var = data.get('var', 'i')
            limit = data.get('limit', '10')
            lines.extend([
                f"{indent}for (( {var}=0; {var}<{limit}; {var}++ )); do",
                f"{indent}    : # TODO: loop body",
                f"{indent}done",
            ])
        elif struct == 'foreach':
            item = data.get('item', 'item')
            coll = data.get('collection', 'collection')
            lines.extend([
                f"{indent}for {item} in {coll}; do",
                f"{indent}    : # TODO: foreach body",
                f"{indent}done",
            ])
        elif struct == 'while':
            cond = data.get('condition', 'true')
            lines.extend([
                f"{indent}while [[ {cond} ]]; do",
                f"{indent}    : # TODO: while body",
                f"{indent}done",
            ])
        elif struct == 'try_catch':
            lines.extend([
                f"{indent}try {{",
                f"{indent}    : # TODO: try block",
                f"{indent}}} catch {{",
                f'{indent}    echo "[ERROR] $_.Exception.Message"',
                f"{indent}}}",
            ])

# ═══════════════════════════════════════════════════════════════════
#  DISCONNECT GROUP COMMAND
# ═══════════════════════════════════════════════════════════════════
class DisconnectGroupCmd(Command):
    def __init__(self, canvas, group):
        super().__init__("Ungroup")
        self.canvas, self.group = canvas, group
        self.children = list(group.group_children)
        self.name, self.pos, self.size = group.data.get('name', 'Group'), group.pos(), group.size()

    def execute(self): self.canvas._do_ungroup(self.group)
    def undo(self):
        group = self.canvas._do_add_block({'name': self.name, 'type': 'group'}, CanvasBlock.BLOCK_GROUP, self.pos)
        group.setFixedSize(self.size)
        group.group_children = self.children
        for c in self.children: group.stackUnder(c)
        self.group = group

# ═══════════════════════════════════════════════════════════════════
#  CONTROL STRUCTURE DIALOG
# ═══════════════════════════════════════════════════════════════════
class ControlDialog(QDialog):
    STRUCTURES = {
        'if': ('IF condition', ['condition']),
        'for': ('FOR loop', ['var', 'limit']),
        'foreach': ('FOREACH loop', ['item', 'collection']),
        'while': ('WHILE loop', ['condition']),
        'try_catch': ('TRY/CATCH block', []),
    }
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('ADD CONTROL STRUCTURE')
        self.setStyleSheet(STYLESHEET)
        self.setMinimumWidth(420)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        hdr = QLabel("⬡  CONTROL STRUCTURE COMPOSER")
        hdr.setStyleSheet(f"color: {C['ctrl_color']}; font-size: 13px; font-weight: bold; padding: 8px;")
        layout.addWidget(hdr)

        struct_grp = QGroupBox("STRUCTURE TYPE")
        sg_layout = QVBoxLayout(struct_grp)
        self.struct_combo = QComboBox()
        for key, (label, _) in self.STRUCTURES.items():
            self.struct_combo.addItem(label, key)
        self.struct_combo.currentIndexChanged.connect(self._refresh_fields)
        sg_layout.addWidget(self.struct_combo)
        layout.addWidget(struct_grp)

        self.fields_grp = QGroupBox("PARAMETERS")
        self.fields_layout = QFormLayout(self.fields_grp)
        layout.addWidget(self.fields_grp)
        self.field_widgets = {}
        self._refresh_fields()

        ok_btn = ForgeButton("ADD TO CANVAS", 'cyan')
        ok_btn.clicked.connect(self.accept)
        cancel_btn = ForgeButton("CANCEL", 'ghost')
        cancel_btn.clicked.connect(self.reject)
        btns_layout = QHBoxLayout()
        btns_layout.addWidget(cancel_btn)
        btns_layout.addWidget(ok_btn)
        layout.addLayout(btns_layout)

    def _refresh_fields(self):
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self.field_widgets.clear()
        key = self.struct_combo.currentData()
        if key in self.STRUCTURES:
            _, fields = self.STRUCTURES[key]
            for f in fields:
                lbl = QLabel(f.upper() + ":")
                lbl.setStyleSheet(f"color: {C['amber']}; font-size: 10px;")
                w = QLineEdit()
                w.setPlaceholderText(f"e.g. {f}")
                self.fields_layout.addRow(lbl, w)
                self.field_widgets[f] = w

    def get_data(self):
        key = self.struct_combo.currentData()
        label, fields = self.STRUCTURES[key]
        data = {'type': 'control', 'structure': key, 'name': label, 'description': label, 'language': 'any'}
        for f, w in self.field_widgets.items():
            data[f] = w.text().strip() or f
        return data

# ═══════════════════════════════════════════════════════════════════
#  LIBRARY PANEL (with Python & Bash support)
# ═══════════════════════════════════════════════════════════════════
class LibraryPanel(QWidget):
    add_to_canvas = pyqtSignal(dict, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.library = {'functions': [], 'variables': []}
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        hdr = QLabel("▸ ELEMENT LIBRARY")
        hdr.setStyleSheet(f"color: {C['amber']}; font-weight: bold; font-size: 12px; padding: 4px;")
        layout.addWidget(hdr)

        self.search = QLineEdit()
        self.search.setPlaceholderText("/ search elements...")
        self.search.textChanged.connect(self._filter)
        layout.addWidget(self.search)

        self.lang_filter = QComboBox()
        self.lang_filter.addItems(['ALL', 'CSharp', 'PowerShell', 'JavaScript', 'Python', 'Bash'])
        self.lang_filter.currentTextChanged.connect(self._filter)
        layout.addWidget(self.lang_filter)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(['ELEMENT', 'LANG', 'FAMILY'])
        self.tree.setColumnWidth(0, 160)
        self.tree.setColumnWidth(1, 70)
        self.tree.setAlternatingRowColors(True)
        self.tree.setDragEnabled(True)
        self.tree.itemDoubleClicked.connect(self._on_double_click)
        layout.addWidget(self.tree)

        add_btn = ForgeButton("⊕  ADD TO CANVAS", 'green')
        add_btn.clicked.connect(self._on_add_click)
        layout.addWidget(add_btn)

        self.stats_lbl = QLabel("0 functions  /  0 variables")
        self.stats_lbl.setStyleSheet(f"color: {C['text_dim']}; font-size: 9px; padding: 2px;")
        layout.addWidget(self.stats_lbl)

    def load_library(self, data):
        self.library = data
        self._populate()

    def _populate(self):
        self.tree.clear()
        lang_f, search = self.lang_filter.currentText(), self.search.text().lower()
        fn_root, var_root = QTreeWidgetItem(self.tree, ['⚙ FUNCTIONS', '', '']), QTreeWidgetItem(self.tree, ['◈ VARIABLES', '', ''])
        fn_root.setForeground(0, QColor(C['fn_color'])); fn_root.setExpanded(True)
        var_root.setForeground(0, QColor(C['var_color'])); var_root.setExpanded(True)

        fn_count = var_count = 0
        for fn in self.library.get('functions', []):
            lang = fn.get('language', '')
            if lang_f != 'ALL' and lang != lang_f: continue
            if search and search not in fn.get('name', '').lower() and search not in fn.get('famille', '').lower(): continue
            item = QTreeWidgetItem(fn_root, [fn.get('name', ''), lang, fn.get('famille', '')])
            item.setData(0, Qt.UserRole, ('function', fn))
            item.setForeground(0, QColor(C['fn_color']))
            item.setToolTip(0, fn.get('description', ''))
            fn_count += 1

        for var in self.library.get('variables', []):
            lang = var.get('language', '')
            if lang_f != 'ALL' and lang != lang_f: continue
            if search and search not in var.get('name', '').lower(): continue
            item = QTreeWidgetItem(var_root, [var.get('name', ''), lang, var.get('famille', '')])
            item.setData(0, Qt.UserRole, ('variable', var))
            item.setForeground(0, QColor(C['var_color']))
            item.setToolTip(0, var.get('description', ''))
            var_count += 1

        self.stats_lbl.setText(f"{fn_count} functions  /  {var_count} variables")
        fn_root.setText(0, f"⚙ FUNCTIONS [{fn_count}]")
        var_root.setText(0, f"◈ VARIABLES [{var_count}]")

    def _filter(self): self._populate()
    def _get_selected_element(self):
        items = self.tree.selectedItems()
        if items: return items[0].data(0, Qt.UserRole)
        return None, None
    def _on_add_click(self):
        btype, bdata = self._get_selected_element()
        if btype and bdata: self.add_to_canvas.emit(bdata, btype)
    def _on_double_click(self, item, col):
        data = item.data(0, Qt.UserRole)
        if data: self.add_to_canvas.emit(data[1], data[0])

# ═══════════════════════════════════════════════════════════════════
#  PROPERTIES PANEL v2
# ═══════════════════════════════════════════════════════════════════
class PropertiesPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        hdr = QLabel("▸ PROPERTIES")
        hdr.setStyleSheet(f"color: {C['amber']}; font-weight: bold; font-size: 12px; padding: 4px;")
        layout.addWidget(hdr)

        self.tab = QTabWidget()
        layout.addWidget(self.tab)

        style = f"QTextEdit {{ background: {C['bg_panel']}; color: {C['text']}; border: 1px solid {C['border']}; border-radius: 4px; font-family: 'Consolas', monospace; font-size: 11px; }}"
        self.info_text, self.src_text, self.ports_text = QTextEdit(), QTextEdit(), QTextEdit()
        for w in (self.info_text, self.src_text, self.ports_text):
            w.setReadOnly(True)
            w.setStyleSheet(style)

        self.tab.addTab(self.info_text, "INFO")
        self.tab.addTab(self.src_text, "SOURCE")
        self.tab.addTab(self.ports_text, "PORTS")
        self.clear_selection()

    def show_block(self, block):
        if block is None:
            self.clear_selection()
            return
        d, btype = block.data, block.block_type
        lines = [f"TYPE    : {btype.upper()}", f"NAME    : {d.get('name', d.get('structure', 'N/A'))}", f"ID      : {block.block_id}", f"LANG    : {d.get('language', 'N/A')}", f"FAMILY  : {d.get('famille', 'N/A')}", f"DESC    : {d.get('description', 'N/A')}", ""]

        if btype == CanvasBlock.BLOCK_FUNCTION:
            params = d.get('parameters', [])
            lines.append(f"PARAMETERS ({len(params)}):")
            for p in params:
                req = '✓' if p.get('required') else '○'
                default = f" = {p.get('default', '')}" if not p.get('required') else ''
                lines.append(f"  {req} {p.get('name','')} : {p.get('datatype','')}{default}")
            ret = d.get('returns', {})
            if isinstance(ret, dict): lines.extend(["", f"RETURNS : {ret.get('datatype', 'void')}", f"  {ret.get('description', '')}"])
        elif btype == CanvasBlock.BLOCK_VARIABLE:
            lines.extend([f"DATATYPE : {d.get('datatype', 'N/A')}", f"SCOPE    : {d.get('scope', 'N/A')}", f"DEFAULT  : {d.get('default_value', 'N/A')}"])
        elif btype == CanvasBlock.BLOCK_CONTROL:
            lines.append(f"STRUCTURE : {d.get('structure', 'N/A')}")
        elif btype == CanvasBlock.BLOCK_GROUP:
            lines.append(f"CHILDREN  : {len(block.group_children)} blocks")

        self.info_text.setPlainText('\n'.join(lines))
        self.src_text.setPlainText(d.get('source', '// No source available'))
        CodeHighlighter(self.src_text.document(), d.get('language', 'CSharp'))

        port_lines = [f"{'▸' if p.direction == 'out' else '◂'} {'⬢' if p.port_type == NodePort.PORT_FLOW else '◆'} {p.name:12} : {p.dtype:10} [{len(p.connections)} link(s)]" for p in block.ports]
        self.ports_text.setPlainText('\n'.join(port_lines) if port_lines else "// No ports")

    def clear_selection(self):
        self.info_text.setPlainText("// Select a block to view properties")
        self.src_text.setPlainText("// No element selected")
        self.ports_text.setPlainText("// No element selected")

# ═══════════════════════════════════════════════════════════════════
#  OUTPUT PANEL v2.1 (Python & Bash support)
# ═══════════════════════════════════════════════════════════════════
class OutputPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._highlighter = None
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        tb = QHBoxLayout()
        hdr = QLabel("▸ GENERATED CODE")
        hdr.setStyleSheet(f"color: {C['amber']}; font-weight: bold; font-size: 12px; padding: 4px;")
        tb.addWidget(hdr)

        self.lang_select = QComboBox()
        self.lang_select.addItems(['CSharp', 'PowerShell', 'JavaScript', 'Python', 'Bash'])
        self.lang_select.setFixedWidth(130)
        tb.addWidget(QLabel("LANG:")); tb.addWidget(self.lang_select)

        self.name_input = QLineEdit("GeneratedProgram")
        self.name_input.setFixedWidth(160)
        tb.addWidget(QLabel("NAME:")); tb.addWidget(self.name_input)
        tb.addStretch()

        for text, variant in [("⚡ GENERATE", 'green'), ("⎘ COPY", 'amber'), ("↓ SAVE CODE", 'cyan'), ("✓ VALIDATE", 'pink')]:
            btn = ForgeButton(text, variant)
            tb.addWidget(btn)
            setattr(self, f"{'gen' if 'GENERATE' in text else 'copy' if 'COPY' in text else 'save' if 'SAVE' in text else 'validate'}_btn", btn)

        layout.addLayout(tb)

        self.editor = QTextEdit()
        self.editor.setStyleSheet(f"QTextEdit {{ background: {C['bg_panel']}; color: {C['text']}; border: 1px solid {C['border']}; border-radius: 4px; font-family: 'Consolas', monospace; font-size: 12px; selection-background-color: {C['accent']}; }}")
        self.editor.setPlaceholderText("// Place elements on canvas, wire ports, then hit ⚡ GENERATE")
        layout.addWidget(self.editor)

        self.status = QLabel("Ready.")
        self.status.setStyleSheet(f"color: {C['text_dim']}; font-size: 9px; padding: 2px;")
        layout.addWidget(self.status)

    def set_code(self, code, language='CSharp'):
        self.editor.setPlainText(code)
        if self._highlighter: self._highlighter.setDocument(None)
        self._highlighter = CodeHighlighter(self.editor.document(), language)
        self.status.setText(f"Lines: {code.count(chr(10)) + 1}  /  Chars: {len(code)}  /  Lang: {language}")

    def get_code(self): return self.editor.toPlainText()
    def get_language(self): return self.lang_select.currentText()
    def get_name(self): return self.name_input.text().strip() or 'GeneratedProgram'

# ═══════════════════════════════════════════════════════════════════
#  UNDO TREE PANEL
# ═══════════════════════════════════════════════════════════════════
class UndoTreePanel(QWidget):
    def __init__(self, undo_manager, parent=None):
        super().__init__(parent)
        self.undo_manager = undo_manager
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        hdr = QLabel("▸ TEMPORAL HISTORY")
        hdr.setStyleSheet(f"color: {C['amber']}; font-weight: bold; font-size: 12px; padding: 4px;")
        layout.addWidget(hdr)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(['#', 'ACTION', 'TIME'])
        self.tree.setColumnWidth(0, 30)
        self.tree.setColumnWidth(1, 160)
        self.tree.setColumnWidth(2, 70)
        self.tree.setAlternatingRowColors(True)
        self.tree.setStyleSheet(f"QTreeWidget {{ background: {C['bg_panel']}; color: {C['text']}; border: 1px solid {C['border']}; border-radius: 4px; font-size: 11px; }} QTreeWidget::item:selected {{ background: {C['accent']}; color: {C['white']}; border-radius: 4px; }}")
        layout.addWidget(self.tree)
        self.refresh()

    def refresh(self):
        self.tree.clear()
        for i, cmd in enumerate(self.undo_manager.history):
            active = i == self.undo_manager.index
            item = QTreeWidgetItem(self.tree, [str(i + 1), ('▶ ' if active else '  ') + cmd.description, cmd.timestamp.strftime('%H:%M:%S')])
            if active:
                item.setForeground(0, QColor(C['amber']))
                item.setForeground(1, QColor(C['white']))
                item.setBackground(0, QColor(C['accent'] + '44'))
            else:
                item.setForeground(1, QColor(C['text_dim']))
                item.setForeground(2, QColor(C['comment']))
        self.tree.scrollToBottom()

# ═══════════════════════════════════════════════════════════════════
#  MAIN WINDOW v2.1 (Scroll Fix + Python/Bash)
# ═══════════════════════════════════════════════════════════════════
class CodeForgeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.library_data = {}
        self.current_project_path = None
        self._boot_phase = 0
        self._setup_window()
        self._setup_menu()
        self._setup_toolbar()
        self._setup_central()
        self._setup_statusbar()
        self._connect_signals()
        self._setup_shortcuts()
        self._boot_sequence()

    def _setup_window(self):
        self.setWindowTitle("CODEFORGE v2.1  —  INGEN SYSTEMS WORKSTATION [NODAL]")
        self.setMinimumSize(1400, 900)
        self.setStyleSheet(STYLESHEET)

    def _setup_menu(self):
        mb = self.menuBar()
        fm = mb.addMenu("FILE")
        fm.addAction("⊕  New Project", self._new_project, 'Ctrl+N')
        fm.addAction("⊞  Open Project...", self._open_project, 'Ctrl+O')
        fm.addAction("↓  Save Project", self._save_project, 'Ctrl+S')
        fm.addAction("↓  Save As...", self._save_project_as)
        fm.addSeparator()
        fm.addAction("⊞  Load Library...", self._load_library, 'Ctrl+L')
        fm.addSeparator()
        fm.addAction("✕  Exit", self.close, 'Ctrl+Q')

        em = mb.addMenu("EDIT")
        em.addAction("↶  Undo", self._undo, 'Ctrl+Z')
        em.addAction("↷  Redo", self._redo, 'Ctrl+Shift+Z')
        em.addAction("⎘  Copy Code", self._copy_code, 'Ctrl+Shift+C')
        em.addAction("🗑  Clear Canvas", self._clear_canvas)
        em.addSeparator()
        em.addAction("▣  Group Selected", self._group_selected, 'Ctrl+G')
        em.addAction("□  Ungroup Selected", self._ungroup_selected, 'Ctrl+Shift+G')
        em.addSeparator()
        em.addAction("≋  Auto-Layout", self._auto_layout, 'Ctrl+L')

        vm = mb.addMenu("VIEW")
        vm.addAction("⚡ Refresh Code", self._generate_code, 'F5')
        vm.addAction("📜 Show Undo Tree", self._toggle_undo_tree)

        hm = mb.addMenu("HELP")
        hm.addAction("ℹ  About CodeForge", self._show_about)
        hm.addAction("?  Shortcuts", self._show_shortcuts)

    def _setup_toolbar(self):
        tb = self.addToolBar("Main")
        tb.setIconSize(QSize(16, 16))
        tb.setMovable(False)
        for label, slot, variant in [
            ("⊞ LOAD LIB", self._load_library, 'amber'),
            ("⊕ CTRL BLOCK", self._add_ctrl_block, 'cyan'),
            ("▣ GROUP", self._group_selected, 'pink'),
            ("≋ AUTO-LAY", self._auto_layout, 'cyan'),
            ("⚡ GENERATE", self._generate_code, 'green'),
            ("↓ SAVE PROJ", self._save_project, 'amber'),
            ("↓ SAVE CODE", self._save_code, 'cyan'),
            ("🗑 CLEAR", self._clear_canvas, 'red'),
        ]:
            btn = ForgeButton(label, variant)
            btn.clicked.connect(slot)
            tb.addWidget(btn)
            tb.addSeparator()

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        tb.addWidget(spacer)

        self.clock_lbl = QLabel()
        self.clock_lbl.setStyleSheet(f"color: {C['text']}; font-family: 'Segoe UI'; font-size: 11px; padding: 4px;")
        tb.addWidget(self.clock_lbl)
        clock_timer = QTimer(self)
        clock_timer.timeout.connect(self._update_clock)
        clock_timer.start(1000)
        self._update_clock()

    def _update_clock(self):
        self.clock_lbl.setText(datetime.now().strftime("[ %Y-%m-%d  %H:%M:%S ]"))

    def _setup_central(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        hsplit = QSplitter(Qt.Horizontal)

        self.library_panel = LibraryPanel()
        self.library_panel.setMinimumWidth(260)
        self.library_panel.setMaximumWidth(380)
        hsplit.addWidget(self.library_panel)

        center_split = QSplitter(Qt.Vertical)

        self.canvas_scroll = QScrollArea()
        self.canvas_scroll.setWidgetResizable(True)
        self.canvas_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.canvas_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.canvas_container = QWidget()
        self.canvas_container.setMinimumSize(2000, 1500)
        self.canvas_container.setStyleSheet(f"background-color: {C['bg']};")

        self.canvas_layout = QVBoxLayout(self.canvas_container)
        self.canvas_layout.setContentsMargins(0, 0, 0, 0)
        self.canvas_layout.setSpacing(0)

        self.canvas = CanvasWidget()
        self.canvas.setMinimumSize(2000, 1500)
        self.canvas_layout.addWidget(self.canvas)

        self.canvas_scroll.setWidget(self.canvas_container)
        self.canvas_scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: {C['bg']}; }}
            QScrollBar:vertical {{ background: {C['bg']}; width: 12px; }}
            QScrollBar::handle:vertical {{ background: {C['bg_hover']}; border-radius: 6px; min-height: 30px; }}
            QScrollBar::handle:vertical:hover {{ background: {C['accent']}; }}
            QScrollBar:horizontal {{ background: {C['bg']}; height: 12px; }}
            QScrollBar::handle:horizontal {{ background: {C['bg_hover']}; border-radius: 6px; min-width: 30px; }}
            QScrollBar::handle:horizontal:hover {{ background: {C['accent']}; }}
            QScrollBar::add-line, QScrollBar::sub-line {{ height: 0px; width: 0px; }}
        """)

        center_split.addWidget(self.canvas_scroll)

        self.output_panel = OutputPanel()
        self.output_panel.setMinimumHeight(220)
        center_split.addWidget(self.output_panel)
        center_split.setSizes([600, 280])
        hsplit.addWidget(center_split)

        right_split = QSplitter(Qt.Vertical)
        self.props_panel = PropertiesPanel()
        self.props_panel.setMinimumWidth(260)
        self.props_panel.setMaximumWidth(400)
        right_split.addWidget(self.props_panel)

        self.undo_panel = UndoTreePanel(self.canvas.undo_manager)
        self.undo_panel.setMinimumHeight(150)
        self.undo_panel.setMaximumHeight(300)
        right_split.addWidget(self.undo_panel)
        right_split.setSizes([400, 200])
        hsplit.addWidget(right_split)
        hsplit.setSizes([280, 800, 300])
        main_layout.addWidget(hsplit)

    def _setup_statusbar(self):
        sb = self.statusBar()
        sb.setStyleSheet(f"background-color: {C['bg_panel']}; color: {C['text']}; border-top: 1px solid {C['border']};")
        self.status_main = QLabel("CodeForge v2.1 — Nodal Mode")
        self.status_blocks = QLabel("CANVAS: 0 blocks")
        self.status_undo = QLabel("UNDO: 0/0")
        sb.addWidget(self.status_main, 1)
        sb.addPermanentWidget(self.status_blocks)
        sb.addPermanentWidget(self.status_undo)

    def _connect_signals(self):
        self.library_panel.add_to_canvas.connect(self._add_to_canvas)
        self.canvas.selection_changed.connect(self.props_panel.show_block)
        self.canvas.canvas_changed.connect(self._on_canvas_changed)
        self.canvas.undo_manager.history_changed.connect(self._on_undo_changed)
        self.output_panel.gen_btn.clicked.connect(self._generate_code)
        self.output_panel.copy_btn.clicked.connect(self._copy_code)
        self.output_panel.save_btn.clicked.connect(self._save_code)
        self.output_panel.validate_btn.clicked.connect(self._validate_code)

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+Z"), self, self._undo)
        QShortcut(QKeySequence("Ctrl+Shift+Z"), self, self._redo)
        QShortcut(QKeySequence("Ctrl+Y"), self, self._redo)
        QShortcut(QKeySequence("Ctrl+G"), self, self._group_selected)
        QShortcut(QKeySequence("Ctrl+Shift+G"), self, self._ungroup_selected)
        QShortcut(QKeySequence("Ctrl+A"), self, self._select_all)
        QShortcut(QKeySequence("Ctrl+L"), self, self._auto_layout)
        QShortcut(QKeySequence("Delete"), self, self._delete_selected)
        QShortcut(QKeySequence("F5"), self, self._generate_code)

    def _add_to_canvas(self, data, block_type):
        block = self.canvas.add_block(data, block_type)
        self.status_main.setText(f"Added: {data.get('name', block_type)}")

    def _add_ctrl_block(self):
        dlg = ControlDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            self.canvas.add_block(data, CanvasBlock.BLOCK_CONTROL)
            self.status_main.setText(f"Control block added: {data.get('name', '')}")

    def _on_canvas_changed(self):
        self.status_blocks.setText(f"CANVAS: {len(self.canvas.blocks)} blk / {len(self.canvas.connections)} conn")

    def _on_undo_changed(self):
        um = self.canvas.undo_manager
        self.status_undo.setText(f"UNDO: {um.index + 1 if um.can_undo() else 0}/{len(um.history)}")
        self.undo_panel.refresh()

    def _undo(self):
        desc = self.canvas.undo_manager.undo()
        if desc: self.status_main.setText(f"↶ Undo: {desc}")

    def _redo(self):
        desc = self.canvas.undo_manager.redo()
        if desc: self.status_main.setText(f"↷ Redo: {desc}")

    def _group_selected(self): self.canvas._group_selected()
    def _ungroup_selected(self): self.canvas._ungroup_selected()
    def _select_all(self): self.canvas._select_all()
    def _delete_selected(self): self.canvas._delete_selected()

    def _auto_layout(self):
        self.canvas.auto_layout()
        self.status_main.setText("≋ Auto-layout applied (DAG topological)")

    def _generate_code(self):
        if not self.canvas.blocks:
            self.status_main.setText("⚠  No blocks on canvas")
            return
        lang = self.output_panel.get_language()
        name = self.output_panel.get_name()
        ordered = self.canvas.get_ordered_blocks()
        code = CodeGenerator.generate(ordered, self.canvas.connections, lang, name)
        self.output_panel.set_code(code, lang)
        self.status_main.setText(f"✓  Code generated  [{lang}] — {name} (dataflow-aware)")

    def _validate_code(self):
        code = self.output_panel.get_code()
        lang = self.output_panel.get_language()
        errors, warnings = [], []
        if not code.strip(): errors.append("Empty code buffer")

        if lang == 'CSharp':
            if 'class' not in code and 'namespace' not in code: warnings.append("No class/namespace wrapper detected")
            if code.count('{') != code.count('}'): errors.append("Brace mismatch")
        elif lang == 'JavaScript':
            if not code.startswith("'use strict'"): warnings.append("Missing 'use strict' directive")
            if code.count('(') != code.count(')'): errors.append("Parenthesis mismatch")
        elif lang == 'PowerShell':
            if '#Requires' not in code: warnings.append("Missing #Requires directive")
        elif lang == 'Python':
            if 'def main' not in code and '__name__' not in code: warnings.append("Missing main guard")
            if code.count('(') != code.count(')'): errors.append("Parenthesis mismatch")
        elif lang == 'Bash':
            if '#!/usr/bin/env bash' not in code: warnings.append("Missing shebang")
            if 'set -e' not in code: warnings.append("Missing 'set -e' error handling")

        for b in self.canvas.blocks:
            for p in b.ports:
                if p.direction == 'in' and p.port_type == NodePort.PORT_DATA and not p.connections and p.name != 'flow_in':
                    warnings.append(f"Unconnected input '{p.name}' on {b.data.get('name', 'block')}")

        msg = []
        if errors: msg.extend(["ERRORS:"] + [f"  ✗ {e}" for e in errors])
        if warnings: msg.extend(["WARNINGS:"] + [f"  ⚠ {w}" for w in warnings])
        if not errors and not warnings: msg.append("✓ VALIDATION PASSED — No issues detected")

        QMessageBox.information(self, "Validation Report", "\n".join(msg))
        self.status_main.setText(f"Validation: {len(errors)} errors, {len(warnings)} warnings")

    def _copy_code(self):
        code = self.output_panel.get_code()
        if code:
            QApplication.clipboard().setText(code)
            self.status_main.setText("✓  Code copied to clipboard")

    def _save_code(self):
        lang = self.output_panel.get_language()
        ext_map = {'CSharp': 'cs', 'PowerShell': 'ps1', 'JavaScript': 'js', 'Python': 'py', 'Bash': 'sh'}
        ext = ext_map.get(lang, 'txt')
        name = self.output_panel.get_name()
        path, _ = QFileDialog.getSaveFileName(self, "Save Code", f"{name}.{ext}", f"{lang} files (*.{ext})")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.output_panel.get_code())
            self.status_main.setText(f"✓  Code saved: {path}")

    def _load_library(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Library", ".", "JSON files (*.json)")
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.library_data = data
                self.library_panel.load_library(data)
                self.status_main.setText(f"✓  Library loaded: {len(data.get('functions', []))} functions, {len(data.get('variables', []))} variables")
            except Exception as e:
                QMessageBox.critical(self, "Load Error", f"Failed to load library:\n{e}")

    def _new_project(self):
        if self.canvas.blocks:
            if QMessageBox.question(self, "New Project", "Clear current canvas and start a new project?", QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
                return
        self.canvas.clear()
        self.current_project_path = None
        self.output_panel.editor.clear()
        self.setWindowTitle("CODEFORGE v2.1  —  INGEN SYSTEMS WORKSTATION [NODAL]  —  [New Project]")
        self.status_main.setText("New project started")

    def _open_project(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Project", ".", "CodeForge Project (*.cfproj)")
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    proj = json.load(f)
                if 'library' in proj:
                    self.library_data = proj['library']
                    self.library_panel.load_library(proj['library'])
                if 'canvas' in proj:
                    self.canvas.from_dict(proj['canvas'])
                if 'output' in proj:
                    self.output_panel.lang_select.setCurrentText(proj['output'].get('language', 'CSharp'))
                    self.output_panel.name_input.setText(proj['output'].get('name', 'GeneratedProgram'))
                self.current_project_path = path
                self.setWindowTitle(f"CODEFORGE v2.1  —  {os.path.basename(path)}")
                self.status_main.setText(f"✓  Project loaded: {path}")
            except Exception as e:
                QMessageBox.critical(self, "Open Error", f"Failed to open project:\n{e}")

    def _save_project(self):
        if not self.current_project_path:
            self._save_project_as()
        else:
            self._write_project(self.current_project_path)

    def _save_project_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Project As", "project.cfproj", "CodeForge Project (*.cfproj)")
        if path:
            self.current_project_path = path
            self._write_project(path)

    def _write_project(self, path):
        try:
            proj = {
                'codeforge_version': '2.1',
                'saved_at': datetime.now().isoformat(),
                'library': self.library_data,
                'canvas': self.canvas.to_dict(),
                'output': {'language': self.output_panel.get_language(), 'name': self.output_panel.get_name(), 'code': self.output_panel.get_code()}
            }
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(proj, f, indent=2, ensure_ascii=False)
            self.setWindowTitle(f"CODEFORGE v2.1  —  {os.path.basename(path)}")
            self.status_main.setText(f"✓  Project saved: {path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save project:\n{e}")

    def _clear_canvas(self):
        if self.canvas.blocks:
            if QMessageBox.question(self, "Clear Canvas", "Clear all blocks from canvas?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.canvas.clear()
                self.status_main.setText("Canvas cleared")

    def _toggle_undo_tree(self):
        self.undo_panel.setVisible(not self.undo_panel.isVisible())

    def _show_about(self):
        QMessageBox.information(self, "About CodeForge",
            "CODEFORGE v2.1 — NODAL EDITION\n"
            "INGEN Systems Workstation\n"
            "Visual Program Composer & Code Generator\n"
            "Features: Nodal Graph · Undo Tree · Auto-Layout · Modern UI\n"
            "Supports: C#, PowerShell, JavaScript, Python, Bash\n"
            "[ THE CODE FINDS A WAY ]"
        )

    def _show_shortcuts(self):
        QMessageBox.information(self, "Keyboard Shortcuts",
            "Ctrl+N      New Project\n"
            "Ctrl+O      Open Project\n"
            "Ctrl+S      Save Project\n"
            "Ctrl+L      Load Library / Auto-Layout\n"
            "Ctrl+Z      Undo\n"
            "Ctrl+Shift+Z  Redo\n"
            "Ctrl+G      Group Selected Blocks\n"
            "Ctrl+Shift+G  Ungroup Selected\n"
            "Ctrl+A      Select All\n"
            "Del         Delete Selected\n"
            "F5          Generate Code\n\n"
            "MOUSE: Drag blocks · Drag ports to connect · Marquee select"
        )

    def _boot_sequence(self):
        self._boot_messages = [
            "Initializing CodeForge Nodal kernel...",
            "Loading node graph engine... OK",
            "Loading temporal undo tree... OK",
            "Loading modern UI theme... OK",
            "Loading dataflow compiler... OK",
            "Loading auto-layout DAG solver... OK",
            "Mounting library interface... OK",
            "System ready. Welcome.",
            "Load a library JSON to begin. (FILE > Load Library)",
        ]
        self._boot_phase = 0
        self._boot_timer = QTimer(self)
        self._boot_timer.timeout.connect(self._next_boot_msg)
        self._boot_timer.start(200)

        default_lib = os.path.join(os.path.dirname(__file__), 'library.json')
        if os.path.exists(default_lib):
            try:
                with open(default_lib, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.library_data = data
                self.library_panel.load_library(data)
            except Exception:
                pass

    def _next_boot_msg(self):
        if self._boot_phase < len(self._boot_messages):
            self.status_main.setText(self._boot_messages[self._boot_phase])
            self._boot_phase += 1
        else:
            self._boot_timer.stop()

# ═══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("CodeForge")
    app.setOrganizationName("INGEN Systems")
    app.setFont(QFont('Segoe UI', 10))
    win = CodeForgeMainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()