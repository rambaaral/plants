import bpy
import math
import pandas as pd

def leaf(length, radius, w_list, idx):

    ### 엽마다 지정할 컬렉션 생성
    # 컬렉션 생성
    new_collection = bpy.data.collections.new(f"leaf{idx}")

    # 씬에 추가
    bpy.context.scene.collection.children.link(new_collection)
    
    ## 엽의 줄기의 둘레
    a = w_list[idx-1]
    ## 엽을 생성할 높이
    h = sum(w_list[0:idx-1])
    # 엽이 될 오브젝트 생성
    bpy.ops.mesh.primitive_plane_add(size = a, align = 'WORLD', location = (0, 0, h))
    
    # 오브젝트를 변수로 지정해주고 이름지정
    mesh = bpy.context.active_object
    mesh.name = f"leaf{idx}"
    
    # 오브젝트의 소속 컬렉션을 옮김
    new_collection.objects.link(mesh)
    
    bpy.context.collection.objects.unlink(mesh)

    ### 엽이 될 오브젝트를 엽 모양으로 바꾸는 과정

    # 오브젝트 회전
    mesh.rotation_euler[0] = math.pi/2
        
    # 편집 모드 진입
    bpy.ops.object.mode_set(mode='EDIT')
    # 모든 꼭짓점 선택
    bpy.ops.mesh.select_all(action='SELECT')
    # Z축 기준으로 이등분, 안쪽 면 제거
    bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True, clear_outer=False)
    # 오브젝트를의 폴리곤을 늘려서 부드럽게 바꿈
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=63)

    # 5번 꼭짓점 선택
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    mesh.data.vertices[5].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')

    # 선택한 꼭짓점을 엽의 길이만큼 당겨줌
    bpy.ops.transform.translate(value=(0, 0, length), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=True, proportional_edit_falloff='SHARP', proportional_size=a/2)

    # 객체 모드로 전환
    bpy.ops.object.mode_set(mode='OBJECT')

    ### 오브젝트를 좌우대칭으로 만들어서 관리하기 편하게 만듦
    # 미러 수정자 추가
    bpy.ops.object.modifier_add(type='MIRROR')

    # 클리핑 옵션 활성화
    bpy.context.object.modifiers["Mirror"].use_clip = True


    # 원형 커브 생성 - 이 커브를 따라서 오브젝트를 변형함
    bpy.ops.curve.primitive_bezier_circle_add(radius=radius, enter_editmode=False, align='WORLD', location=(0, 0, h))
    circle_curve = bpy.context.active_object
    circle_curve.name = f"leaf_circle{idx}"
    
    
    new_collection.objects.link(circle_curve)
    
    bpy.context.collection.objects.unlink(circle_curve)
    
    circle_curve.rotation_euler.x = math.pi*idx

    # 오브젝트에 커브 수정자 추가
    curve_modifier = mesh.modifiers.new(name="Curve", type='CURVE')
    
    # 커브 수정자 설정
    curve_modifier.object = circle_curve
    curve_modifier.deform_axis = 'POS_X'
    
    
    
    bpy.ops.object.add(type='LATTICE', enter_editmode=False, align='WORLD', location=(0, 0, (length/2)+h))
    leaf_curve = bpy.context.active_object
    leaf_curve.name = f"leaf_curve{idx}"
    
    new_collection.objects.link(leaf_curve)
    bpy.context.collection.objects.unlink(leaf_curve)

    bpy.context.object.data.points_u = 1
    bpy.context.object.data.points_v = 1

    bpy.context.object.scale[2] = length + a

    bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.modifier_add(type='LATTICE')
    bpy.context.object.modifiers["Lattice"].object = bpy.data.objects[f"leaf_curve{idx}"]

    bpy.context.view_layer.objects.active = leaf_curve
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.context.object.data.points[0].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.transform.translate(value=(0, 0, -h), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')

    #1번 엽 y좌표 음수
    #반지름 길이 length
    #반지름 기준점 (0, 0, a/2 + h)
    bpy.context.view_layer.objects.active = leaf_curve
    bpy.context.object.data.points_w = 64

    ## 임시로 90도로 잎의 꼭짓점을 이동했지만 잎의 곡선을 살리는 과정에서 길이가 늘어남.
    ## 이 현상은 잎의 길이가 길면 길 수록 차이가 커짐
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.context.object.data.points[63].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.transform.translate(value=(0, ((-1)**(idx+1))*length*0.8, -length), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', use_proportional_edit=True, proportional_edit_falloff='SHARP', proportional_size=length)





#데이터 불러와서 변수로 지정
#일단 길이 먼저

def main():
    leaf_length_df = pd.read_csv("C:/Users/robot/Documents/blender/length.csv") #기간 설정이 가능한데 일단 9월1일부터
    leaf_area_df = pd.read_csv("C:/Users/robot/Documents/blender/area.csv")
    green_area_df = pd.read_csv("C:/Users/robot/Documents/blender/green_area.csv")
    # senescence_ratio_df = pd.read_csv(C:/Users/robot/Documents/blender/senescence_ratio.csv) #아직 안씀
    # date = input("날짜입력(09-01부터 07-06)")

    id = 300

    leaf_length = leaf_length_df.iloc[id]
    leaf_area = leaf_area_df.iloc[id]
    # senescence_ratio = senescence_ratio_df.iloc[id]

    rowmax = len(leaf_length)

    length_list = []
    radius_list = []

    for i in range(1, rowmax): #리스트 채우기
    
        try:
            length = float(leaf_length[i])
            length_list.append(length)
        except ValueError:
            length_list.append(0)

        try:
             radius = float(leaf_area[i]/(length*math.pi)*math.sqrt(2))
             radius_list.append(radius)
        except ValueError:
            radius_list.append(0)
            
    #반지름 리스트 재가공
    midx = length_list.index(max(length_list))
    max_radius = radius_list[midx]
    real_leaf = len([i for i in length_list if i > 0])

    for i in range(real_leaf):
        radius_list[i] = max_radius * (real_leaf/(real_leaf + i))
        #radius_list[i] = max_radius * ((real_leaf-i)/real_leaf) #
    
        
    width_list = []

    for i in range(rowmax-1):
        try:
             width = radius_list[i]*2*math.pi
             width_list.append(width)
        except ValueError:
            width_list.append(0)
        
        
    for i in range(rowmax-1):

        leaf(length_list[i], radius_list[i], width_list, i+1)
        
        
    bpy.context.scene.frame_end = 60
    bpy.ops.ptcache.bake_all(bake=True)



    #print(leaf_length, leaf_area, radius_list, real_leaf)


if __name__ == "__main__":
    main()
