from formkit import *
f = form('CH12_MEDICINES', 'CareWell Clinic')
main(f, 'Medicines', 560, 300)
TREE_QUERY = """select case when connect_by_isleaf = 1 then 0 when level = 1 then 1 else -1 end,
       level, label, case when kind = 'M' then 'pill' else 'folder' end, node_id
from  (select 'C' || category_id as node_id, 'C' || parent_id as parent_id,
              category_name as label, 'C' as kind
       from   medicine_categories
       union all
       select 'M' || medicine_id, 'C' || category_id, medicine_name || ' ' || strength, 'M'
       from   medicines)
start with parent_id = 'C'
connect by prior node_id = parent_id
order siblings by kind, label"""
nav = block(f, 'NAV')
tree = item(nav, 'TREE', None, 8, 8, 190, 280, kind='tree', treeDataQuery=TREE_QUERY,
            treeShowLines=True, treeShowSymbol=True, treeAllowEmpBranch=False, treeMultiSelect=False)
trigger(tree, 'WHEN-TREE-NODE-SELECTED', file='ch12/node-selected.pls')
m = block(f, 'MEDICINES', table='MEDICINES', records=12, order='medicine_name', scroll=True)
item(m, 'MEDICINE_NAME', 'Medicine', 206, 22, 110, length=40)
item(m, 'DOSAGE_FORM', 'Form', 318, 22, 62, length=12)
item(m, 'STRENGTH', 'Strength', 382, 22, 56, length=20)
item(m, 'UNIT_PRICE', 'Price', 440, 22, 44, dt='number', formatMask='9990D00', justification=T.JUSTIFICATION_RIGHT_CTID)
item(m, 'STOCK_QTY', 'Stock', 486, 22, 44, dt='number', justification=T.JUSTIFICATION_RIGHT_CTID)
m.setScrollbarXPosition(532); m.setScrollbarYPosition(22); m.setScrollbarLength(192); m.setScrollbarWidth(10)
trigger(f, 'WHEN-NEW-FORM-INSTANCE', "ftree.populate_tree('NAV.TREE');")
save(f)
