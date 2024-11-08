import bpy
import math

#def leaf(length, radius):

length = 10
radius = 1
a = round(radius*2*math.pi, 2)
bpy.ops.mesh.primitive_plane_add(size = a, align = 'WORLD', location = (0, 0, 0))
    
mesh = bpy.context.active_object
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

bpy.context.scene.tool_settings.use_proportional_edit = True
bpy.context.scene.tool_settings.proportional_edit_falloff = 'SHARP'
bpy.context.scene.tool_settings.proportional_size = a/2

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

# 평면에 커브 수정자 추가
curve_modifier = mesh.modifiers.new(name="Curve", type='CURVE')

# 커브 수정자 설정
curve_modifier.object = circle_curve
curve_modifier.deform_axis = 'POS_X'
