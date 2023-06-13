def get_linguistic_context(nlp, ques):
    doc = get_doc(ques, nlp)
    pos = get_pos(doc)
    dep = get_dep(doc)
    root = get_root_node(doc, dep)
    depth_list = get_dep_depth(root, [-1] * len(doc))
    return doc, pos, dep, depth_list

def get_doc(text, nlp):
    return nlp(text)


def get_pos(doc):
    return [token.pos_ for token in doc]


def get_dep(doc):
    return [token.dep_ for token in doc]


def get_root_node(doc, dep):
    return doc[dep.index("ROOT")]


def get_dep_depth(root, depth_list, depth=1):
    depth_list[root.i] = depth
    if len(list(root.children)) == 0:
        return depth_list
    for child in root.children:
        depth_list = get_dep_depth(child, depth_list, depth + 1)
    return depth_list
