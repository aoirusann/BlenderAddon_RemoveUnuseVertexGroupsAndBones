# What's this?
A blender addon used for removing empty vertex groups and bones with no corresponding vertex groups.

# Install
* Download from [github release](https://github.com/aoirusann/BlenderAddon_RemoveUnuseVertexGroupsAndBones/tags)
* Then just install the `.zip` file in the same way as other blender addons
* NOTE: You need to enable `Setting - Interface - Display - Develop Extras` to use this plugin. (thanks for @minitiv)

# Usage

## Remove unused vertex groups
1. Select some mesh objects whose vertex groups will be checked.
2. F3 - Remove Unused VeretxGroups
3. The empty vertex groups on the mesh objects should have been removed.

For example (in `demo.blend`):

* Vertex Group `Using` is being used
	* ![](pic/2023-11-21-22-13-53.png)
* Vertex Group `Unused` is empty
	* ![](pic/2023-11-21-22-14-12.png)
* Select `Cylinder`
* Press `F3`
* Type `Remove Unused VeretxGroups`
	* ![](pic/2023-11-21-22-15-35.png)
* Vertex Group `Unused` was removed
	* ![](pic/2023-11-21-22-16-20.png)
* Log can be found in `Window - Toggle System Console`
	* ![](pic/2023-11-21-22-17-10.png)


## Remove unused bones
1. Select some mesh objects whose vertex groups will be checked.
2. Ctrl+Click select an armature object whose bone will be removed. (Make sure the armature is the active object)
3. F3 - Remove Unused Bones
4. The bones on the armature object which are not referred by the vertex groups of mesh objects should have been removed.

For example (in `demo.blend`):

* Bone `Using` has the corresponding vertex group `Using` in the `Cylinder`
	* ![](pic/2023-11-21-22-22-09.png)
* Bone `UnusedBone` has no corresponding vertex group in the `Cylinder`
	* ![](pic/2023-11-21-22-22-28.png)
* Select `Cylinder`
* CTRL+Click Select `Armature`
* Press `F3`
* Type `Remove Unused Bone`
	* ![](pic/2023-11-21-22-23-34.png)
* Bone `UnusedBone` was removed
	* ![](pic/2023-11-21-22-24-01.png)
* Log can be found in `Window - Toggle System Console`
	* ![](pic/2023-11-21-22-24-17.png)
