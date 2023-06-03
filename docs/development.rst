Development
=====
For those who like to know more about our simulation or contribute to it, here we talk about its implementation. We'll first walk through accessing the project through Unreal Engine 5 editor then go into the implementation and how to add more into the environment such as fires or crew. 

Set up the Project
----
    - If our release build doesn’t come with AirSim, make sure there’s a copy of it in your Unreal Engine project folder. To build AirSim, follow the steps `here <https://sublime-and-sphinx-guide.readthedocs.io/en/latest/references.html>`_.
.. note:: When opening the project through Unreal Engine 5 without AirSim, an error may occur but you can still open it without AirSim.

Once the project is downloaded, remember to build the project. The following are the instructions to build the project:

    - Locate the FIReVision folder and find file ending in .sln (e.g., FIReVision.sln). 
    - Inside the file, look at the top and click on Build and Build Solution. If no compiling errors occur, you are ready to open the FIReVision uproject. It can also be opened inside of the Unreal Engine application.
Then, when you're in the project via the editor, go to the top left and click on File > Open Level and select FIReVision (Level).


Implementation
====
Post Process Thermal Imaging Material
-----
To be filled out...

Vehicle and Crew AI
-----
To be filled out...

Adding more Crew and Fire 
-----
To be filled out...

