# Baseboards Workflow

- Blender baseboard setup

## Step One

- Create planes from the walls
- Create child object named `baseboard_placeholder`
- For every room we need child object named in order, e.g `a_room1_bph`
- Plane placeholder should be child of corresponding room object, the name should follow room's name e.g `a_room1_bph_1`
![Screenshot 2024-08-13 at 2 18 33 PM](https://github.com/user-attachments/assets/7699324a-9a76-4ae9-9574-7f45980bb09b)

---

## Step Two

- Replacing plane objects with baseboards
- Add baseboard glb into the scene
- Copy name of the corresponding plane

### Transform

- Copy location
- Change rotation mode for baseboard from `Quaternion` to `XYZ euler`
- Tweak the rotation to face the wall
- Set the scale to match the wall, double check with measurement tool (Scale must be always POSITVE number)
![Screenshot 2024-08-13 at 2 18 51 PM](https://github.com/user-attachments/assets/c7ca1922-0d8f-4ad9-b493-d7a68f0783d1)
![Screenshot 2024-08-13 at 2 18 26 PM](https://github.com/user-attachments/assets/1f2f1859-da3b-4b65-93aa-51864a573996)

 ---

- Reparent the baseboard to corresponding room
- Delete plane placeholder object 
- Export Floorplan 
