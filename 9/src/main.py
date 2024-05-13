from ngen.engine import Loader, Application, Preferences
from ngen.api import CameraPerspective, LightDirectional, LightSource, Scene, Entity, Transform

INITIAL_POSITION_OFFSET = 20.0

car1_velocity = 1.5
car2_velocity = 2.0
car3_velocity = 2.5
car4_velocity = 2.75
car5_velocity = 2.25
car6_velocity = 1.75

def callback_car1_update_movement(entity: Entity, delta_time: float) -> None:
    global car1_velocity
    entity.get_transform().translate([car1_velocity * delta_time, 0, 0])

    if abs(entity.get_transform().get_position()[Transform.X]) > INITIAL_POSITION_OFFSET:
        car1_velocity *= -1
        entity.get_transform().set_rotation([0.0, -(entity.get_transform().get_rotation()[Transform.Y]), 0.0])

        if entity.get_transform().get_position()[Transform.X] > 0:
            entity.get_transform().set_position([INITIAL_POSITION_OFFSET, entity.get_transform().get_position()[Transform.Y], 0.0])
        else:
            entity.get_transform().set_position([-INITIAL_POSITION_OFFSET, entity.get_transform().get_position()[Transform.Y], 0.0])

def callback_car2_update_movement(entity: Entity, delta_time: float) -> None:
    global car2_velocity
    entity.get_transform().translate([car2_velocity * delta_time, 0, 0])

    if abs(entity.get_transform().get_position()[Transform.X]) > INITIAL_POSITION_OFFSET:
        car2_velocity *= -1
        entity.get_transform().set_rotation([0.0, -(entity.get_transform().get_rotation()[Transform.Y]), 0.0])

        if entity.get_transform().get_position()[Transform.X] > 0:
            entity.get_transform().set_position([INITIAL_POSITION_OFFSET, entity.get_transform().get_position()[Transform.Y], 0.0])
        else:
            entity.get_transform().set_position([-INITIAL_POSITION_OFFSET, entity.get_transform().get_position()[Transform.Y], 0.0])

def callback_car3_update_movement(entity: Entity, delta_time: float) -> None:
    global car3_velocity
    entity.get_transform().translate([car3_velocity * delta_time, 0, 0])

    if abs(entity.get_transform().get_position()[Transform.X]) > INITIAL_POSITION_OFFSET:
        car3_velocity *= -1
        entity.get_transform().set_rotation([0.0, -(entity.get_transform().get_rotation()[Transform.Y]), 0.0])

        if entity.get_transform().get_position()[Transform.X] > 0:
            entity.get_transform().set_position([INITIAL_POSITION_OFFSET, entity.get_transform().get_position()[Transform.Y], 0.0])
        else:
            entity.get_transform().set_position([-INITIAL_POSITION_OFFSET, entity.get_transform().get_position()[Transform.Y], 0.0])

def callback_car4_update_movement(entity: Entity, delta_time: float) -> None:
    global car4_velocity
    entity.get_transform().translate([car4_velocity * delta_time, 0, 0])

    if abs(entity.get_transform().get_position()[Transform.X]) > INITIAL_POSITION_OFFSET:
        car4_velocity *= -1
        entity.get_transform().set_rotation([0.0, -(entity.get_transform().get_rotation()[Transform.Y]), 0.0])

        if entity.get_transform().get_position()[Transform.X] > 0:
            entity.get_transform().set_position([INITIAL_POSITION_OFFSET, entity.get_transform().get_position()[Transform.Y], 0.0])
        else:
            entity.get_transform().set_position([-INITIAL_POSITION_OFFSET, entity.get_transform().get_position()[Transform.Y], 0.0])

def callback_car5_update_movement(entity: Entity, delta_time: float) -> None:
    global car5_velocity
    entity.get_transform().translate([car5_velocity * delta_time, 0, 0])

    if abs(entity.get_transform().get_position()[Transform.X]) > INITIAL_POSITION_OFFSET:
        car5_velocity *= -1
        entity.get_transform().set_rotation([0.0, -(entity.get_transform().get_rotation()[Transform.Y]), 0.0])

        if entity.get_transform().get_position()[Transform.X] > 0:
            entity.get_transform().set_position([INITIAL_POSITION_OFFSET, entity.get_transform().get_position()[Transform.Y], 0.0])
        else:
            entity.get_transform().set_position([-INITIAL_POSITION_OFFSET, entity.get_transform().get_position()[Transform.Y], 0.0])

def callback_car6_update_movement(entity: Entity, delta_time: float) -> None:
    global car6_velocity
    entity.get_transform().translate([car6_velocity * delta_time, 0, 0])

    if abs(entity.get_transform().get_position()[Transform.X]) > INITIAL_POSITION_OFFSET:
        car6_velocity *= -1
        entity.get_transform().set_rotation([0.0, -(entity.get_transform().get_rotation()[Transform.Y]), 0.0])

        if entity.get_transform().get_position()[Transform.X] > 0:
            entity.get_transform().set_position([INITIAL_POSITION_OFFSET, entity.get_transform().get_position()[Transform.Y], 0.0])
        else:
            entity.get_transform().set_position([-INITIAL_POSITION_OFFSET, entity.get_transform().get_position()[Transform.Y], 0.0])

def main() -> None:
    application = Application()

    Preferences.set_window_title("ІП-14 Бабіч Денис. Лабораторна робота № 9")

    directional_light = LightDirectional(Transform([0, 0, 0], [0, 0, 0], [1, 1, 1]), LightSource.LIGHT0, [1.0, 1.0, 1.0])

    camera = CameraPerspective(Transform([0.0, 0.0, -10.0], [0, 0, 0], [1, 1, 1]), 100.0, 0.01, 100.0, None)

    car1 = Entity(Transform([INITIAL_POSITION_OFFSET, 8.0, 0], [0, 90, 0], [1.0, 1.0, 1.0]), Loader.load_mesh("9/assets/car1/car1.obj"), Loader.load_texture("9/assets/car1/car1.png"), None, callback_car1_update_movement)
    car2 = Entity(Transform([-INITIAL_POSITION_OFFSET, 4, 0], [0, 90, 0], [1.0, 1.0, 1.0]), Loader.load_mesh("9/assets/car2/car2.obj"), Loader.load_texture("9/assets/car2/car2.png"), None, callback_car2_update_movement)
    car3 = Entity(Transform([INITIAL_POSITION_OFFSET, 0.5, 0], [0, 90, 0], [1.0, 1.0, 1.0]), Loader.load_mesh("9/assets/car3/car3.obj"), Loader.load_texture("9/assets/car3/car3.png"), None, callback_car3_update_movement)
    car4 = Entity(Transform([-INITIAL_POSITION_OFFSET, -2.5, 0], [0, 90, 0], [1.0, 1.0, 1.0]), Loader.load_mesh("9/assets/car4/car4.obj"), Loader.load_texture("9/assets/car4/car4.png"), None, callback_car4_update_movement)
    car5 = Entity(Transform([INITIAL_POSITION_OFFSET, -5.5, 0], [0, 90, 0], [1.0, 1.0, 1.0]), Loader.load_mesh("9/assets/car4/car4_taxi.obj"), Loader.load_texture("9/assets/car4/car4_taxi.png"), None, callback_car5_update_movement)
    car6 = Entity(Transform([-INITIAL_POSITION_OFFSET, -9.5, 0], [0, 90, 0], [1.0, 1.0, 1.0]), Loader.load_mesh("9/assets/car4/car4_police.obj"), Loader.load_texture("9/assets/car4/car4_police.png"), None, callback_car6_update_movement)

    scene = Scene([0.0, 0.694, 0.251, 1.0], camera, directional_light, car1, car2, car3, car4, car5, car6)

    application.load_scene(scene)

if __name__ == "__main__":
    main()