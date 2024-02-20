# Automatic solutions to A/B/C/D questions with AI

This program is adapted to help you solve problems from an IT theory exam (in Polish technical schools you need to pass two such examinations to get technician diploma) to speed up your preparation process.

Although you can basically use to all of closed questions when there are A/B/C/D answers and it should still work pretty well.

I’ve created this app with Python customtkinter GUI. It also includes pytesseract library in python which allow me to take text from the image of the question than you can paste or import from disk. I’m also using sydney-py library for communication with Bing AI. Generating response can take about 1-2 minutes. For handling images I implemented Pillow library. The last step was exporting solution to questions. For that I added odfpy functionalities to create a possibility to store all of the solutions in .odt files. There is help button inside the app to give you step by step instructions of how you should use this app.

There can be some problems with running this app on Windows because it was only tested on Debian 12. I will create Windows version soon.
