# Baseboards Workflow

- Blender baseboard setup

## Step One

- Create planes from the walls
- Create child object named `baseboard_placeholder`
- For every room we need child object named in order, e.g `a_room1_bph`
- Plane placeholder should be child of corresponding room object, the name should follow room's name e.g `a_room1_bph_1`

---

## Step Two

- Replacing plane objects with baseboards
- Add baseboard glb into the scene
- Copy name of the corresponding plane

### Tranform

- Copy location
- Change rotation mode for baseboard from `Quaternion` to `XYZ euler`
- Tweak the rotation to face the wall
- Set the scale to match the wall, double check with measurement tool (Scale must be always POSITVE number)

 ---

- Reparent the baseboard to corresponding room
- Delete plane placeholder object 
- Export Floorplan 
