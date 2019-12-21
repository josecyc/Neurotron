# Godot

The rendering aspect of the project is done with the godot game engine. <br>
The prediction data from the model is sent via a UDP IP socket to the godot listener. <br>
We then proceed to locate each of the joints and render the hand pose estimation. <br>

If --compare flag is used in `render_from_data.py` then both godot and godot_2 programs must be running, each one will receive the information via a unique port.<br> 

# requirements
[Godot 3.1] (https://godotengine.org/download/linux)

# usage
1. open godot
2. select project folder
3. press play to run in the upper right corner<br>
    (if the model is running the prediction will show accordingly)
