# PuppetTool
Puppet Tool is used to record animation of selected objects or controllers and reapply it on same object with different options.
This can be used to change parenting option of ik's anytime while animating or to change the direction of whole animation without
changing the global control .

Installation
------------
Download the python file and copy paste the script to your script editor under python tab.
or load the script through script editor.
for convenience you can make it as shelf button. 


Usage
-----
once you got the UI running..
1) select the objects or controlls for which you wanna record the animation.
2) Hit the record animation button in puppet tool UI with desired options for recording.
    This will create duplicates of selected objects or controlls and put them under one parent called "cogGroupParent"
    which gets selected by the end of record process. This parent can be moved or rotated to change the animation direction and the
    duplicated objects will give you the visual help to know which direction the animation is gonna go.
3) select the objects or controlls on which you wanna apply the animation. If you dont select anything then it will apply animation to objects for which 
    record option was used.

could be better
---------------

working to make recording and reapply procedure faster.
    
Credits
-------
the puppet tool (https://github.com/RakeshChakraborty/PuppetTool) was Written by [Rakesh Chakraborty]
special thanks to my friends (https://github.com/ankmachine) [Ankit Sinha] and (https://github.com/in-17) [Ranjit]. They helped me a lot with this tool script.
