import bpy
import math
import pandas as pd

def leaf(length, radius, idx):

    # 새로운 컬렉션을 만듭니다.
    new_collection = bpy.data.collections.new(f"leaf{idx}")

    # 씬에 컬렉션을 추가합니다.
    bpy.context.scene.collection.children.link(new_collection)

    a = round(radius*2*math.pi, 2)
    bpy.ops.mesh.primitive_plane_add(size = a, align = 'WORLD', location = (0, 0, 0))
        
    mesh = bpy.context.active_object
    mesh.name = f"leaf{idx}"
    
    new_collection.objects.link(mesh)
    
    bpy.context.collection.objects.unlink(mesh)
    
    mesh.rotation_euler[0] = math.pi/2
        
    # 편집 모드 진입
    bpy.ops.object.mode_set(mode='EDIT')

    # 모든 꼭짓점 선택
    bpy.ops.mesh.select_all(action='SELECT')

    # Z축 기준으로 이등분, 안쪽 면 제거
    bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False)

    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=10)

    # 5번 꼭짓점 선택
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    mesh.data.vertices[5].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')

    bpy.ops.transform.translate(value=(0, 0.1, length), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=True, proportional_edit_falloff='SHARP', proportional_size=a/2)


    # 객체 모드로 전환
    bpy.ops.object.mode_set(mode='OBJECT')

    # 미러 수정자 추가
    bpy.ops.object.modifier_add(type='MIRROR')

    # 클리핑 옵션 활성화
    bpy.context.object.modifiers["Mirror"].use_clip = True


    # 원형 커브 생성
    bpy.ops.curve.primitive_bezier_circle_add(radius=radius, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    circle_curve = bpy.context.active_object
    circle_curve.name = f"leaf_curve{idx}"
    
    
    new_collection.objects.link(circle_curve)
    
    bpy.context.collection.objects.unlink(circle_curve)
    
    circle_curve.rotation_euler.x = 3.14159*idx

    # 평면에 커브 수정자 추가
    curve_modifier = mesh.modifiers.new(name="Curve", type='CURVE')
    
    # 커브 수정자 설정
    curve_modifier.object = circle_curve
    curve_modifier.deform_axis = 'POS_X'
    
import bpy




#데이터 불러와서 변수로 지정
#일단 길이 먼저

def main():
    leaf_length_df = pd.read_csv("C:/Users/robot/Documents/galicmodel/length.csv") #기간 설정이 가능한데 일단 9월1일부터
    leaf_area_df = pd.read_csv("C:/Users/robot/Documents/galicmodel/area.csv")
    senescence_ratio_df = pd.read_csv("C:/Users/robot/Documents/galicmodel/senescence_ratio.csv")

    # date = input("날짜입력(09-01부터 07-06)")

    id = 300

    leaf_length = leaf_length_df.iloc[id]
    leaf_area = leaf_area_df.iloc[id]
    #senescence_ratio = senescence_ratio_df.iloc[id]

    rowmax = len(leaf_length)

    length_list = []
    radius_list = []

    for i in range(1, rowmax):
    
        try:
            length = float(leaf_length[i])
            length_list.append(length)
        except ValueError:
            length_list.append(0)

        try:
             radius = float(leaf_area[i]/(length*math.pi))
             radius_list.append(radius)
        except ValueError:
            radius_list.append(0)

    for i in range(rowmax-1):

        leaf(length_list[i], radius_list[i], i+1)





    # print(leaf_length, leaf_area, senescence_ratio, rowmax, id)



if __name__ == "__main__":
    main()
