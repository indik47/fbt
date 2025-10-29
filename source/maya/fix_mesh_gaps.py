import math


def _parse_meshes(sel):
    if len(sel) < 1:
        return None, None
        
    source, target = sel[0].split('.')[0], None
    for i in sel:
        mesh_name, edge = i.split('.')
        if mesh_name == source:
            continue
        else:
            target = mesh_name
            return source, target
    
    if not target:
        return None, None
        

def _parse_edge_selection(sel, source, target):
    if not source or not target:
        return None

    source_edges = []
    target_edges = []
    for edge in sel:
        if edge.startswith(source):
            source_edges.append(edge)
        if edge.startswith(target):
            target_edges.append(edge)
    
    return source_edges, target_edges
            

def vert_distance(v1, v2):
    v1_pos = cmds.xform(v1, q=True, translation=True, a=True, ws=True)
    v2_pos = cmds.xform(v2, q=True, translation=True, a=True, ws=True)

    return math.sqrt((v1_pos[0]-v2_pos[0])**2 + (v1_pos[1]-v2_pos[1])**2 + (v1_pos[2]-v2_pos[2])**2)


def find_matching(vert, verts_to_search):
    found = None
    curr_distance = 100000
    
    verts_to_search = cmds.ls(verts_to_search, flatten=True)
    #print(verts_to_search)
    for v in verts_to_search:
        distance = vert_distance(vert, v)
        if distance < curr_distance:
            curr_distance = distance    
            found = v
    
    return found
    
    
def copy_paste(selectedVerts):
    if len(selectedVerts) == 2:
        # Get normals from the first vertex
        sourceVertNormal = cmds.polyNormalPerVertex(selectedVerts[0], query=True, xyz=True)[0:3]
    
        # Apply the normals to the second vertex
        cmds.polyNormalPerVertex(selectedVerts[1], e=True, xyz=sourceVertNormal)
    
        # Save the position of the first vertex
        pos = cmds.pointPosition(selectedVerts[0], world=True)
    
        # Move the second vertex to the position of the first one
        cmds.move(pos[0], pos[1], pos[2], selectedVerts[1], absolute=True)
    
        #print("Normals successfully copied, and the second vertex has been moved to the position of the first one.")
    else:
        print("Select exactly two vertices.")


def auto_find_borders():
    """Legacy code. Used to autodetect border edges. Works on simple meshes but fails to work on complex characters. Needs rewrite to work properly"""
    sel = cmds.ls(sl=True)
    borders = dict()

    for mesh in sel:
        info = cmds.polyEvaluate(mesh, e=True)
        borders_per_mesh = []
        for i in range(info):
            myBorder = cmds.polySelect(mesh, eb=i, ns=True, ass=True)

            if myBorder and myBorder not in borders_per_mesh:            
                borders_per_mesh.append(myBorder) 
            
        borders[mesh] = borders_per_mesh
                    

    border_verts = dict()
    for mesh, border_edges in borders.items():
        border_verts_per_mesh = set()
        for edge in border_edges:
            
            _verts = cmds.polyListComponentConversion(edge, fromEdge=True, toVertex=True)
            _verts = cmds.ls(_verts, flatten=True)
            for v in _verts:       
                border_verts_per_mesh.add(v)
        
        border_verts[mesh] = border_verts_per_mesh

    mesh_source, mesh_target = border_verts.keys()  

    for v in border_verts[mesh_source]:
        found = find_matching(v, border_verts[mesh_target])
        if found:
            copy_paste([found, v])
            

def convert_edge_sel_to_vert(edges):
    verts = set()
    for edge in edges:
        _verts = cmds.polyListComponentConversion(edge, fromEdge=True, toVertex=True)    
        _verts = cmds.ls(_verts, flatten=True)
        for v in _verts:
            verts.add(v)
    
    return verts
    
    
sel = cmds.ls(sl=True)

source, target = _parse(sel)
source_edges, target_edges = _parse_edge_selection(sel, source, target)

sorce_verts = convert_edge_sel_to_vert(source_edges)
target_verts = convert_edge_sel_to_vert(target_edges)

for v in sorce_verts:
    found = find_matching(v, target_verts)
    if found:
        copy_paste([found, v])




