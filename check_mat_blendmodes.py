import unreal
import argparse
import enum


class BlendMode(enum.Enum):
    OPAQUE = unreal.BlendMode.BLEND_OPAQUE
    MASKED = unreal.BlendMode.BLEND_MASKED
    TRANSLUCENT = unreal.BlendMode.BLEND_TRANSLUCENT
    ADDITIVE = unreal.BlendMode.BLEND_ADDITIVE
    MODULATE = unreal.BlendMode.BLEND_MODULATE
    ALPHA_COMPOSITE = unreal.BlendMode.BLEND_ALPHA_COMPOSITE
    ALPHA_HOLDOUT = unreal.BlendMode.BLEND_ALPHA_HOLDOUT


def classify_by_blendmode(mats):
    classifier = {}
    for mat in mats:
        if mat.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_MASKED:
            classifier.setdefault('masked', []).append(mat)
        elif mat.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_TRANSLUCENT:
            classifier.setdefault('translucent', []).append(mat)
        elif mat.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_OPAQUE:
            classifier.setdefault('opaque', []).append(mat)
        elif mat.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_ADDITIVE:
            classifier.setdefault('additive', []).append(mat)
        elif mat.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_MODULATE:
            classifier.setdefault('modulate', []).append(mat)
        elif mat.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_ALPHA_COMPOSITE:
            classifier.setdefault('alpha_composite', []).append(mat)
        elif mat.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_ALPHA_HOLDOUT:
            classifier.setdefault('alpha_holdout', []).append(mat)

    return classifier

def print_summary(classifier):
    for key, value in classifier.items():
        print('-----------')
        unreal.log_warning(f'{key}: {len(value)}')
        

def filter_blendmode_translucent(mat, blend_mode):
    '''Filter materials that have BLEND_MASKED blend mode'''
    blend_mode = mat.get_editor_property('blend_mode')

    return blend_mode == blend_mode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--show', type=str, help='Show materials with specified blend mode:"opaque, masked, translucent, additive, modulate, alpha_composite, alpha_holdout"')
    
    args = parser.parse_args()

    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    mats = list(filter(lambda a:type(a) == unreal.Material, selected_assets))

    if args.show == 'opaque':
        unreal.log_warning('Showing opaque materials')
        mats = list(filter(lambda a:a.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_OPAQUE, mats))
    elif args.show == 'masked':
        unreal.log_warning('Showing masked materials')
        mats = list(filter(lambda a:a.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_MASKED, mats))
    elif args.show == 'translucent':
        unreal.log_warning('Showing translucent materials')
        mats = list(filter(lambda a:a.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_TRANSLUCENT, mats))
    elif args.show == 'additive':
        unreal.log_warning('Showing additive materials')
        mats = list(filter(lambda a:a.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_ADDITIVE, mats))
    elif args.show == 'modulate':
        unreal.log_warning('Showing modulate materials')
        mats = list(filter(lambda a:a.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_MODULATE, mats))
    elif args.show == 'alpha_composite':
        unreal.log_warning('Showing alpha_composite materials')
        mats = list(filter(lambda a:a.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_ALPHA_COMPOSITE, mats))
    elif args.show == 'alpha_holdout':
        unreal.log_warning('Showing alpha_holdout materials')
        mats = list(filter(lambda a:a.get_editor_property('blend_mode') == unreal.BlendMode.BLEND_ALPHA_HOLDOUT, mats))
    

    classifier = classify_by_blendmode(mats)
    print(classifier)
    print_summary(classifier)


main()