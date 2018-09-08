PRWUI : Python Reactive Web User Interface
==========================================

Is it enough buzz-words ? I think _asynchronous_ is missing :'(

What does it do ?
-----------------

Have you heard what is a virtual DOM ? Did you use websockets ? Do you like non-stateless stuff ? And what about hating JS and loving Python ?

Well here you are ! 

This allow you to generate a the virtual DOM in python and render it on a web page. The virtual DOM and events are passed with a websocket.

Why ?
-----

Why not ?

Seriously, I wanted a way to show various kind of data mostly for debug purposes. First, I used print, but it quickly became unusable (and logs too),
then I though about classical GUI with stuff like Tkinter but I did not liked how I should have done the updates and the place it take in a program (it is not simply a light thing you add to show the internal of a program), after I though about ncurses and the stuff around it for remote purposes
(like running it on a raspberry pi and getting the data on my laptop) but it has the same kind of problems than GUI.
Next there was building a web UI with stuff like Vue.js but it add too much of to develop and the binding of the web part and the main program is not easy and clean.

So here it is, the possibility to add a simple method to each object to allow them to be displayed even if there are complex. The perfs are lame but the goal is not to handle thousands of users.
