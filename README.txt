Hello,

FitApp is a little project made by me for personal use. The reasons behind this project were multiple:
- to deepen my understanding of Python
- to get my hands on some kind of GUI 
- to learn basics of Git/GitHUb
- to get familiar with Linux
- to get familiar with the process of deploying a mobile app
- and to have fun doing it :-)

For this project I chose to create a very basic mobile app for tracking my progress in a gym. The app is not that beautiful to look at, however it does its job.
As a GUI library for Python (version 3.8.0) I chose Kivy (version v2.0.0rc3), Buildozer library for building the app (version 1.2.0) and Linux Ubuntu (version 20.04). My mobile phone is Xiaomi Redmi 8 with Android 10, MIUI Global 11.0.3.

How does it work:
After first start of the app, default exercise database is created with zeros as values. User is then asked to enter the date of training. There are 6 different exercises hardcoded - bench press, overhead press, squat, deadlift, row and a farmer's walk. These exercises are shown as 6 tiles with the weight and number of reps from previous training's last set so that the user know what weight to put on a barbell and how many reps should be done to outperform the previous training.

After clicking on an exercise tile, user adds the weight lifted and then number of repetitions done. On the top of the screen are complete data (all three sets) for that exercise from previous training shown. After adding the number of reps done, automatic timer starts itself so that the user can track rest period. After three sets are done, the exercise tile turns green and user continues to another exercise.

During the training, weights or exercises can be changed at any time. After the whole workout is done, the app calculates the difference between finished training and the previous one. If the weight for an exercise differs from previous training, comparison cannot be done, otherwise difference in number of reps (either + or - or 0) for every exercise and every set is shown. Then all the data gathered in current training is saved and appended to a database.csv file.

