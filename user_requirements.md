## ToDo [[Link](https://docs.google.com/spreadsheets/d/1o1dc7TTswlsjFRUhHcf7Ymqdv9zmEl4Xhxjp8m4bUUY/edit?usp=sharing)]

## User requirements

* The user should be able to execute in local and cloud environment
* The system should provide an interactive session and batch session
    - Interaction: Observe (visualization), online model change, take / go back to snapshot
* The system should support seven primitives (division, apoptosis, dynamic attributes, movement, growth, synapses, physical processes, spike)
* The user should be able to define the simulation describing a workflow
    - support parameter sweep
* Sharing the initial simulation definition and results ( e.g. support for NeuroML) – Import Export feature supporting a variety of formats
* The system should support checkpoints that the user can revert to.
* As a user I want to specify the termination criterion (number of iterations, or more complex criterion (e.g. connectivity pattern) and constraints ( based on cost and resources )
* As a user I want different levels of granularity for diffusion calculation.
* As a user I want to validate my results against libraries, scans, images, …
* As a user I want a common interface to interact with the system ( no matter where the simulation is executed in the end)
* As a user I want a detailed documentation explaining installation, usage on different platforms.
* As a user I want that the software runs on Linux (e.g. Ubuntu), Windows and macOS
* As a user I want to easily share simulations ( e.g. source code ) with colleagues
* As a user I want a community website to interact and discuss with colleagues
* As a user I want to integrate external applications that exchange data every N time steps with BioDynaMo

Electrophysiology:
* Detailed model in BioDynaMo with propagation over every neurite segment
* Simplified model using NEST – implemented using the export / import feature of BDM
