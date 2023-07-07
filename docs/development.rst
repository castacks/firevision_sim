Development
=====
For those who like to know more about our simulation or contribute to it, here we talk about its implementation. We'll first walk through accessing the project through Unreal Engine 5 editor then go into the implementation and how to add more into the environment such as fires or crew. 

Set up the Project
----
The FIReVision uproject can be found on our GitHub `repository <https://github.com/castacks/firevision_sim>`_. The simulator uses AirSim, which is also on the repository in the uproject folder. However, in case you need to download and build AirSim, follow the steps `here <https://sublime-and-sphinx-guide.readthedocs.io/en/latest/references.html>`_.

.. note:: When opening the project through Unreal Engine 5 without AirSim, an error may occur but you can still open it without AirSim.

Once the project is downloaded, remember to build the project. The following are the instructions to build the project:

    - Locate the FIReVision folder and find file ending in .sln (e.g., FIReVision.sln). 
    - Inside the file, look at the top and click on "Build and Build Solution". If no compiling errors occur, you are ready to open the FIReVision uproject. It can also be opened inside of the Unreal Engine application.
Then, when you're in the project via the editor, go to the top left and click on "File > Open Level" and select "FIReVision (Level)".

Debugging and Sanity Checks
---------------------

- Ensure the following are configured properly (likely not necessary)

    - 1 - AirSim Gamemode is set Properly

        - In the top right corner of Unreal Engine should be "Settings", click on it and select "World Settings". It should prompt a new panel for "World Settings" and search for "GameMode Override". By default it should be set to "None". Change it to "AirSimGameMode".

    - 2 - Material is properly applied to AirSim Camera

        - At the bottom of the Unreal Engine Editor, click “Content Browser”.
        - Click “Settings” and ensure “Show Plugin Content” is enabled.
        - In the "Content Drawer", go into “Plugins > AirSim Content > Blueprints”
        - Open "BP_PIP Camera" (not the flying pawn drone)
        - On the left side there should be a "Components" section. In the search bar search for "FireVisionThermalCaptureComponent". If it’s not available, add a "Scene Capture Component 2D", rename it and proceed with the documentation.
        - On the right side there should be a "Details". In the search bar look up "material", you should be prompted with "Post Process Materials". Add an element, choose "Asset Reference" and apply our "PPThermal_Vision_2 material".

    - 3 - Custom Depth Enabled 

        - Go into "Project Settings > Engine - Rendering and find Custom Depth-Stencil Pass". Set this to "Enable with Stencil" to use custom depth and stencil values
        
Implementation
----
Post Process Thermal Imaging Material
-----
- To detect objects as hot and cold, we used a post processing material with a gray-scale gradient. Currently, there are designated stencil values for each object in the world.
- However, if you would like to add objects into the environment and have those be detected as well, you would need to…

    - Enable Custom Depth on the object, which can be done by navigating to the details of the object, searching for Custom Depth and checking off the box. 
    - Then, near Custom Depth should be Stencil Value. Note: each object is allowed a stencil value from 0-255 (with some extra control by looking at specific bits). 

        - Currently, our post processing material only detects fire, trees, humans, vehicles, and the ground. 

    - Therefore, to also detect your object, you would need to alter the post process material, specifically the section for masking.  

        - Add two Constant nodes: one for the stencil and the other for the corresponding heat value. 
        - Next, add an if node and connect the stencil constant to B and heat value to A == B. Locate the Stencil Mask block and connect the output of the Mask (R) node to A in the if node. 
        - Connect Constant nodes with values of 0 to A > B and A < B.
        - Finally, take the output of the if node and plug it into a sum node and the other input should be the latest output of a sum node. Note: there’s a pattern in the structure so it should be easy to match it 
- To replace the AirSim's thermal imaging material with our own, please follow the tutorial below. 
.. youtube:: dGOkNIL12O0
  :width: 1000
  :height: 800

Vehicle and Crew AI
-----
- To represent firefighters and vehicles, we have implemented Crew AI that move within the environment as well as spline paths which allow vehicles to move around.

- If you would like to add more vehicles, you would need to...

    - Navigate into Content > AssetsvilleTown > Meshes > Vehicles and drag the desired vehicle into the environment. This will add the vehicle into the environment but it will be stationary.
    
        - In order to get the vehicle to follow a path, you must navigate to Content > Splines and drag the SplinePathBP into the environment.
        - Next, select a spline point and ALT + LMB drag the cursor towards the direction that you desire. 
        - Once you have finished placing all the segments in the environment, it is advised that you snap all the spline points to the floor to ensure that the vehicle will stay on the ground as it follows the path. This can be done by selecting a spline point, right click, and select "Snap to Ground".
        - Finally, navigate into Content > Splines and drag VehicleBP and set it ontop of the first spline point. Once the environment is live, the vehicle will move and adhere to your new spline path.
        - If you would like to change the vehicle appearance, you may do so by adding a different mesh ontop of the existing blueprint inside the Viewport.
        

Adding more Crew and Fire 
-----
The content folder of the project should contain folders MWBurnedDeadForest/Foliage, MWBurnedDeadForest/Particles, and Forest_Fire_Fighter-_-_Don_3D_Model_CGTrader. 

    - MWBurnedDeadForest/Foliage is where all the foliage (e.g., trees) items are located. 
    - MWBurnedDeadForest/Particles is where the different fires (e.g., small, medium, and large) are stored. 
    - Finally, Forest_Fire_Fighter-_-_Don_3D_Model_CGTrader is where the crew is stored. 
    To add crew and fire, it's simple as dragging and dropping into the environment. Foliage items, on the other hand, are a little different. In the top left corner should be "Select Mode". Switch this "Foliage". In MWBurnedDeadForest/Foliage, drag and drop the desired foliage items. Then, select all items and switch the scaling to free. We change the scale z by setting max to 0.55 and min to 0.39 (subcanopy level trees). Finally, select "Paint" and hold the left mouse button over the region to place foliage.
.. youtube:: Ha-hDImNopU
  :width: 1000
  :height: 800

