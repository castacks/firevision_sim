Development
=====
For those who like to know more about our simulation or contribute to it, here we talk about its implementation. We'll first walk through accessing the project through Unreal Engine 5 editor then go into the implementation and how to add more into the environment such as fires or crew. 

Set up the Project
----
The FIReVision uproject can be found on our GitHub `repository <https://github.com/castacks/firevision_sim>`_. The simulator uses AirSim, which is also on the repository. However, in case you need to download and build AirSim, follow the steps `here <https://sublime-and-sphinx-guide.readthedocs.io/en/latest/references.html>`_.

.. note:: When opening the project through Unreal Engine 5 without AirSim, an error may occur but you can still open it without AirSim.

Once the project is downloaded, remember to build the project. The following are the instructions to build the project:

    - Locate the FIReVision folder and find file ending in .sln (e.g., FIReVision.sln). 
    - Inside the file, look at the top and click on Build and Build Solution. If no compiling errors occur, you are ready to open the FIReVision uproject. It can also be opened inside of the Unreal Engine application.
Then, when you're in the project via the editor, go to the top left and click on File > Open Level and select FIReVision (Level).

Debugging and Sanity Checks
---------------------

- Ensure the following are configured properly (likely not necessary)

    - 1 - AirSim Gamemode is set Properly

        - In the top right corner of Unreal Engine should be Settings, click on it and select World Settings. It should prompt a new panel for World Settings and search for GameMode Override. By default it should be set to None. Change it to AirSimGameMode.

    - 2 - Material is properly applied to AirSim Camera

        - At the bottom of the Unreal Engine Editor, click “Content Browser”.
        - Click “Settings” and ensure “Show Plugin Content” is enabled.
        - In the Content Drawer, go into “Plugins > AirSim Content > Blueprints”
        - Open BP_PIP Camera(not the flying pawn drone)
        - On the left side there should be a Components section. In the search bar search for FireVisionThermalCaptureComponent. If it’s not available, add a Scene Capture Component 2D, rename it and proceed with the documentation.
        - On the right side there should be a Details. In the search bar look up ‘material,’ you should be prompted with Post Process Materials. Add an element, choose Asset Reference and apply our PPThermal_Vision_2 material.

    - 3 - Custom Depth Enabled 

        - Go into Project Settings > Engine - Rendering and find Custom Depth-Stencil Pass. Set this to Enable with Stencil to use custom depth and stencil values
        
Implementation
----
Post Process Thermal Imaging Material
-----
- To detect objects as hot and cold, we used a post processing material. Currently, there are designated stencil values for each object in the world.
- However, if you would like to add objects into the environment and have those be detected as well, you would need to…

    - Enable Custom Depth on the object, which can be done by navigating to the details of the object, searching for Custom Depth and checking off the box. 
    - Then, near Custom Depth should be Stencil Value. Note: each object is allowed a stencil value from 0-255 (with some extra control by looking at specific bits). 

        - Currently, our post processing material only detects fire, trees, humans, vehicles, and the ground. 

    - Therefore, to also detect your object, you would need to alter the post process material, specifically the section for masking.  

        - Add two Constant nodes: one for the stencil and the other for the corresponding heat value. 
        - Next, add an if node and connect the stencil constant to B and heat value to A == B. Locate the Stencil Mask block and connect the output of the Mask (R) node to A in the if node. 
        - Connect Constant nodes with values of 0 to A > B and A < B.
        - Finally, take the output of the if node and plug it into a sum node and the other input should be the latest output of a sum node. Note: there’s a pattern in the structure so it should be easy to match it 
        
Vehicle and Crew AI
-----
To be filled out...

Adding more Crew and Fire 
-----
To be filled out...


