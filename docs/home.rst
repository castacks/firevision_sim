
FIReVision Home
===============


Welcome to FIReVision
---------------------

Wildfires are becoming increasingly problematic due to hotter climates and dryer vegetation.
As wildfires grow in size and complexity, crew on the front lines need access to greater situational awareness of fire position and their own safety.
Unmanned aerial systems (UAS) offer the potential for such situational awareness, providing an eye in the sky while being relatively cost effective and portable. 
Greater levels of autonomy for unmanned aerial systems would make this tool easier to adopt at scale, requiring less training for human pilots and providing greater capability to monitor the environment.
Wildfires provide a rich environment for research in robotics and autonomy due to the complexity of fast dynamics, partial observability, and risk in this dangerous environment.
Yet few simulators exist for UAS in wildland fire environments, and of those that do exist, they are severely limited. Existing simulators are limited to two-dimensional space, lack realistic UAS dynamics, may not include other targets of interest such as crew and vehicles, and are devoid of any camera-based perception system.

In contrast, we propose a higher fidelity simulator based on AirSim (Colosseum) and Unreal Engine 5.
AirSim is an open source simulator for drones that offers realistic quadrotor physics and a plethora of automatic data collection tools for simulated sensors such as IMU, RGB, and LIDAR, for tasks like robot localization and visual recognition. AirSim integrates with Unreal Engine 4 (UE4) to render high fidelity physics-based visuals, allowing the simulation of lighting effects from weather phenomena such as glare, shadows, and fog.
In addition, beyond fire and vegetation, we also add dynamic firefighting crew and vehicles around the fire to serve as interests for situational awareness.
This unique combination of realistic fire and crew movement, visual rendering, and drone physics lets us deliver a rich playground for robotics research. 
We imagine our proposed environment to be useful for robotics tasks such as simultaneous localization and mapping (SLAM) and informative path planning, 
for applications including search and rescue, situational overwatch, and even fire extinguishing.
Our simulator is open source and we encourage further contribution from the community.

Head to our Getting Started page to learn how to install and run the simulator.
