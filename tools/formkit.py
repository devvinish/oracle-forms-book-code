# formkit: builds the book's forms with the Forms Java API (JDAPI), from Jython.
# A form script (lab/specs/<name>.py) calls these helpers and ends with save(); mkform.sh then
# compiles the module with frmcmp_batch. Coordinates are in the module's default coordinate
# system (points).
from oracle.forms.jdapi import (Jdapi, FormModule, Window, Canvas, Block, Item, Trigger, LOV,
    LOVColumnMapping, RecordGroup, ProgramUnit, Alert, JdapiTypes as T, Relation, ModuleParameter,
    TabPage, RadioButton, VisualAttribute, Editor, Graphics, AttachedLibrary, MenuModule,
    CompoundText, TextSegment, PropertyClass, Menu, MenuItem, ObjectLibrary, ObjectLibraryTab,
    ObjectGroup, ObjectGroupChild, Event)
import os

_started = [False]

def start(connect=None):
    if not _started[0]:
        Jdapi.startup(False, False, False)
        _started[0] = True
    if connect or os.environ.get('BOOK_CONNECT'):
        Jdapi.connectToDatabase(connect or os.environ['BOOK_CONNECT'])

def form(name, title=None):
    start()
    f = FormModule(name)
    if title: f.setTitle(title)
    return f

def window(f, name='MAIN_WIN', title=None, width=560, height=320, x=0, y=0, dialog=False, modal=False):
    # a new module comes with a window WINDOW1: the first window of a form takes it over
    w = _find(Window, f, 'WINDOW1') if name == 'MAIN_WIN' else None
    if w is not None: w.setName(name)
    else: w = Window(f, name)
    if title: w.setTitle(title)
    w.setWidth(width); w.setHeight(height); w.setXPosition(x); w.setYPosition(y)
    if dialog: w.setWindowStyle(T.WIST_DIALOG_CTID)
    if modal: w.setModal(True)
    return w

def canvas(f, name='MAIN_CNV', win='MAIN_WIN', width=560, height=320, kind='content', x=0, y=0,
           vw=None, vh=None):
    c = Canvas(f, name)
    c.setCanvasType({'content': T.CNTY_CONTENT_CTID, 'stacked': T.CNTY_STACKED_CTID,
                     'tab': T.CNTY_TAB_CTID, 'htoolbar': T.CNTY_HTOOLBAR_CTID,
                     'vtoolbar': T.CNTY_VTOOLBAR_CTID}[kind])
    c.setWindowName(win)
    c.setWidth(width); c.setHeight(height)
    if kind == 'stacked':
        c.setViewportXPosition(x); c.setViewportYPosition(y)
        c.setViewportWidth(vw or width); c.setViewportHeight(vh or height)
    if kind == 'tab':
        c.setViewportXPosition(x); c.setViewportYPosition(y)
        c.setViewportWidth(vw or width); c.setViewportHeight(vh or height)
    return c

def from_template(template, name, title=None, width=None, height=None):
    """A new form from a template form (File > New > Form Using Template): its objects, triggers,
    attached libraries, and menu, under a new name. The template keeps MAIN_WIN and MAIN_CNV."""
    start()
    f = FormModule.open(template)
    f.setName(name)
    w, c = _find(Window, f, 'MAIN_WIN'), Canvas.find(f, 'MAIN_CNV')
    if title: w.setTitle(title)
    if width: w.setWidth(width); c.setWidth(width)
    if height: w.setHeight(height); c.setHeight(height)
    return f

def main(f, title, width=560, height=320):
    """The usual pair: a document window MAIN_WIN with its content canvas MAIN_CNV."""
    w = window(f, 'MAIN_WIN', title, width, height)
    c = canvas(f, 'MAIN_CNV', 'MAIN_WIN', width, height)
    w.setPrimaryCanvas('MAIN_CNV')
    f.setConsoleWindow('MAIN_WIN')          # the new module's default, WINDOW1, doesn't exist
    return w, c

def block(f, name, table=None, records=1, where=None, order=None, scroll=False, cnv='MAIN_CNV'):
    """A data block on a table (table=...), or a control block (table=None)."""
    b = Block(f, name)
    if table:
        b.setDatabaseBlock(True)
        b.setQueryDataSourceType(T.QRDA_TABLE_CTID)
        b.setQueryDataSourceName(table)
    else:
        b.setDatabaseBlock(False)
    b.setRecordsDisplayCount(records)
    if where: b.setWhereClause(where)
    if order: b.setOrderByClause(order)
    if scroll:
        b.setShowScrollbar(True); b.setScrollbarCanvasName(cnv)
    return b

_DT = {'char': 'DATY_CHARACTER_CTID', 'number': 'DATY_NUMBER_CTID', 'date': 'DATY_DATE_CTID',
       'datetime': 'DATY_DATETIME_CTID', 'integer': 'DATY_INTEGER_CTID', 'long': 'DATY_LONG_CTID'}

def item(b, name, prompt=None, x=0, y=0, width=80, height=16, dt='char', length=None, column=None,
         kind='text', cnv='MAIN_CNV', db=None, edge='top', **props):
    """kind: text, display, button, check, list, radio, image, calc (a calculated display item)."""
    it = Item(b, name)
    types = {'text': T.ITTY_TI_CTID, 'display': T.ITTY_DI_CTID, 'button': T.ITTY_PB_CTID,
             'check': T.ITTY_CB_CTID, 'list': T.ITTY_LS_CTID, 'radio': T.ITTY_RD_CTID,
             'image': T.ITTY_IM_CTID, 'tree': T.ITTY_TREE_CTID, 'bean': T.ITTY_BA_CTID,
             'chart': T.ITTY_CA_CTID}
    it.setItemType(types[kind])
    if cnv: it.setCanvasName(cnv)
    it.setXPosition(x); it.setYPosition(y); it.setWidth(width); it.setHeight(height)
    if kind in ('text', 'display', 'list', 'radio', 'check'):
        it.setDataType(getattr(T, _DT[dt]))
        if length: it.setMaximumLength(length)
        elif dt == 'char': it.setMaximumLength(40)
    if prompt and kind not in ('button', 'check'):
        it.setPrompt(prompt)
        it.setPromptAttachmentEdge(T.PRAT_TOP_CTID if edge == 'top' else T.PRAT_START_CTID)
        if edge == 'start': it.setPromptAttachmentOffset(6)
    if kind == 'button': it.setLabel(prompt or name)
    if kind == 'check': it.setLabel(prompt or name)
    isdb = db if db is not None else (b.isDatabaseBlock() and kind not in ('button', 'display'))
    it.setDatabaseItem(bool(isdb))
    if isdb: it.setColumnName(column or name)
    for k, v in props.items():
        getattr(it, 'set' + k[0].upper() + k[1:])(v)
    return it

EXAMPLES = '/work/examples'

def code_of(path):
    """The code of an example file (examples/<chapter>/<name>.pls), without its '-- @' lines:
    the same text the book prints."""
    if not path.startswith('/'): path = EXAMPLES + '/' + path
    lines = [l for l in open(path).read().decode('utf-8').split(u'\n') if not l.lstrip().startswith('-- @')]  # UTF-8 files
    return '\n'.join(lines).strip('\n')

def trigger(owner, name, code=None, file=None):
    t = Trigger(owner, name)
    t.setTriggerText(code_of(file) if file else code.strip('\n'))
    return t

def unit(f, name, code=None, file=None):
    """A program unit; Forms takes its kind (procedure, function, package spec or body) from the text."""
    pu = ProgramUnit(f, name)
    pu.setProgramUnitText(code_of(file) if file else code.strip('\n'))
    return pu

def record_group(f, name, query):
    rg = RecordGroup(f, name)
    rg.setRecordGroupType(T.REGR_QUERY_CTID)
    rg.setRecordGroupQuery(query)
    return rg

def lov(f, name, query, columns, title=None, width=260, height=200, rg=None):
    """columns: list of (column, title, display_width, return_item or None)."""
    g = record_group(f, rg or ('RG_' + name.replace('LOV_', '')), query)
    l = LOV(f, name)
    l.setRecordGroupName(g.getName())
    if title: l.setTitle(title)
    l.setWidth(width); l.setHeight(height)
    for col, ttl, w, ret in columns:
        m = LOVColumnMapping(l, col)
        m.setTitle(ttl); m.setDisplayWidth(w)
        if ret: m.setReturnItem(ret)
    return l

def alert(f, name, title, message, style='note', buttons=('OK',)):
    a = Alert(f, name)
    a.setTitle(title); a.setAlertMessage(message)
    a.setAlertStyle({'stop': T.ALST_STOP_CTID, 'caution': T.ALST_CAUTION_CTID, 'note': T.ALST_NOTE_CTID}[style])
    labels = list(buttons) + [None, None]
    a.setButton1Label(labels[0])
    a.setButton2Label(labels[1] or '')
    a.setButton3Label(labels[2] or '')
    return a

def save(f, path=None):
    ext = 'mmb' if isinstance(f, MenuModule) else 'olb' if isinstance(f, ObjectLibrary) else 'fmb'
    path = path or '/work/forms/%s.%s' % (f.getName().lower(), ext)
    f.save(path)
    print('saved ' + path)
    return path

# ---- master-detail relations with the code Forms Builder writes for them -------------------
# A Relation made with the JDAPI has no coordination code (Forms Builder writes it, not the
# runtime), so relations() writes the same triggers and program units as Forms Builder 14.1.2:
# ON-POPULATE-DETAILS and ON-CHECK-DELETE-MASTER / PRE-DELETE on the master, ON-CLEAR-DETAILS
# on the form, and CHECK_PACKAGE_FAILURE, QUERY_MASTER_DETAILS, CLEAR_ALL_MASTER_DETAILS
# (lab/tools/relcode, copied from a form whose relation the Data Block Wizard created).
RELCODE = '/work/tools/relcode/'

def _find(cls, owner, name):
    try: return cls.find(owner, name)
    except: return None

def relations(f, master, details):
    """details: list of dicts: name, block (detail block name), table (detail table),
    join (list of (detail item, master item)), delete ('non-isolated'|'cascading'|'isolated')."""
    m = master.getName()
    pop_decl = ("--\n-- Begin default relation declare section\n--\nDECLARE\n"
                "  recstat     VARCHAR2(20)      := :System.record_status;   \n"
                "  startitm    VARCHAR2(61 CHAR) := :System.cursor_item;   \n"
                "  rel_id      Relation;\n--\n-- End default relation declare section\n--\n")
    pop = ("--\n-- Begin default relation program section\n--\nBEGIN\n"
           "  IF ( recstat = 'NEW' or recstat = 'INSERT' ) THEN   \n    RETURN;\n  END IF;\n")
    chk_decl, chk_body, casc = '', '', ''
    for d in details:
        r = Relation(master, d['name'])
        r.setDetailBlock(d['block'])
        cond = ' AND '.join('%s.%s = %s.%s' % (d['block'], di, m, mi) for di, mi in d['join'])
        r.setJoinCondition(cond)
        beh = d.get('delete', 'non-isolated')
        r.setDeleteRecord({'non-isolated': T.DERE_NON_ISOLATED_CTID, 'cascading': T.DERE_CASCADING_CTID,
                           'isolated': T.DERE_ISOLATED_CTID}[beh])
        r.setDeferred(d.get('deferred', False)); r.setAutoQuery(d.get('deferred', False))
        for di, mi in d['join']:
            Item.find(Block.find(f, d['block']), di).setCopyValueFromItem('%s.%s' % (m, mi))
        notnull = ' and '.join('(:%s.%s is not null)' % (m, mi) for di, mi in d['join'])
        b = d['block']
        pop += ("  --\n  -- Begin %s detail program section\n  --\n"
                "  IF ( %s ) THEN   \n"
                "    rel_id := Find_Relation('%s.%s');   \n"
                "    Query_Master_Details(rel_id, '%s');   \n  END IF;\n"
                "  --\n  -- End %s detail program section\n  --\n") % (b, notnull, m, d['name'], b, b)
        alias = d['table'][0]
        where = '\n    AND '.join('%s.%s = :%s.%s' % (alias, di, m, mi) for di, mi in d['join'])
        if beh == 'non-isolated':
            chk_decl += ("  --\n  -- Begin %s detail declare section\n  --\n"
                         "  CURSOR %s_cur IS      \n    SELECT 1 FROM %s %s     \n    WHERE %s;\n"
                         "  --\n  -- End %s detail declare section\n  --\n") % (b, b, d['table'], alias, where, b)
            chk_body += ("  --\n  -- Begin %s detail program section\n  --\n"
                         "  OPEN %s_cur;     \n  FETCH %s_cur INTO Dummy_Define;     \n"
                         "  IF ( %s_cur%%found ) THEN     \n"
                         "    Message('Cannot delete master record when matching detail records exist.');     \n"
                         "    CLOSE %s_cur;     \n    RAISE Form_Trigger_Failure;     \n  END IF;\n"
                         "  CLOSE %s_cur;\n  --\n  -- End %s detail program section\n  --\n") % (b, b, b, b, b, b, b)
        elif beh == 'cascading':
            casc += ("  --\n  -- Begin %s detail program section\n  --\n"
                     "   DELETE FROM %s %s\n   WHERE %s;\n"
                     "  --\n  -- End %s detail program section\n  --\n") % (b, d['table'], alias, where, b)
    pop += ("\n  IF ( :System.cursor_item <> startitm ) THEN     \n     Go_Item(startitm);     \n"
            "     Check_Package_Failure;     \n  END IF;\nEND;\n--\n-- End default relation program section\n--\n")
    Trigger(master, 'ON-POPULATE-DETAILS').setTriggerText(pop_decl + pop)
    if chk_body:
        Trigger(master, 'ON-CHECK-DELETE-MASTER').setTriggerText(
            "--\n-- Begin default relation declare section\n--\nDECLARE\n  Dummy_Define CHAR(1);\n" + chk_decl +
            "--\n-- End default relation declare section\n--\n--\n-- Begin default relation program section\n--\nBEGIN\n" +
            chk_body + "END;\n--\n-- End default relation program section\n--\n")
    if casc:
        Trigger(master, 'PRE-DELETE').setTriggerText(
            "--\n-- Begin default relation program section\n--\nBEGIN\n" + casc +
            "END;\n--\n-- End default relation program section\n--\n")
    if _find(Trigger, f, 'ON-CLEAR-DETAILS') is None:
        Trigger(f, 'ON-CLEAR-DETAILS').setTriggerText(open(RELCODE + 'on-clear-details.pls').read())
    for n in ('CHECK_PACKAGE_FAILURE', 'QUERY_MASTER_DETAILS', 'CLEAR_ALL_MASTER_DETAILS'):
        if _find(ProgramUnit, f, n) is None:
            ProgramUnit(f, n).setProgramUnitText(open(RELCODE + n.lower() + '.pls').read())

# ---- boilerplate: text and frames on a canvas ------------------------------------------------
def label(f, name, text, x, y, width=80, height=14, cnv='MAIN_CNV', size=900):
    """A text object (boilerplate text) on a canvas, such as the label of a radio group."""
    g = Graphics(Canvas.find(f, cnv), name)
    g.setGraphicsType(T.GRTY_TEXT_CTID)
    g.setXPosition(x); g.setYPosition(y); g.setWidth(width); g.setHeight(height)
    g.setFillPattern('none'); g.setEdgePattern('none')     # no box around the text
    ts = TextSegment(CompoundText(g, name + '_CT'), name + '_TS')
    ts.setText(text)
    ts.setFontName('Dialog'); ts.setFontSize(size)          # the prompts' font; size in hundredths of a point
    return g

def frame(f, name, title, x, y, width, height, cnv='MAIN_CNV'):
    """A frame (a titled rectangle) that groups items, not managed by the Layout Wizard."""
    g = Graphics(Canvas.find(f, cnv), name)
    g.setGraphicsType(T.GRTY_FRAME_CTID)
    g.setXPosition(x); g.setYPosition(y); g.setWidth(width); g.setHeight(height)
    if title:
        g.setFrameTitle(title)
        g.setFrameTitleFontName('Dialog'); g.setFrameTitleFontSize(900)
    return g
