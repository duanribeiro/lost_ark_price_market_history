# Lost Ark - Price Market History (On progress...)
![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![windwos](https://img.shields.io/badge/Windows-017AD7?style=for-the-badge&logo=windows&logoColor=white)
![amazon](https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)


The objective of this project is a tool that collects information from [Lost Ark](https://www.playlostark.com/pt-br) game screenshots, interprets the text through 
[Amazon Rekognition](https://aws.amazon.com/pt/rekognition/) and saves the information in a cloud database to be searched by all players

**This code was designed not to interact directly with the game, through clicks or any type of action, precisely to 
avoid banning the user's account.**

**The code will interact with screenshots taken by the user and there is no need for the game to even be open for
information gathering.**

## Requirements
1. Only works on Windows.
2. [Docker](https://docs.docker.com/desktop/windows/install/) must be installed.
3. Must use in-game resolution 1800x900. (Because the code will crop the market text and other resolution will be offcenter and fail)

## Installation
1. Create a folder on path `C:\pics` (MAKE SURE IS ON C:)
2. Open your terminal and run `docker pull imagename`

Docker Desktop is an easy-to-install application for Windows environment that enables you to build and share applications.
After done this steps we are ready to take screenshots in-game.

## In-game Screenshots
1. Open the game as usual and login on any character.
2. When inside use hotkey `ALT+Y` to open the market.
3. Search for the itens you want to collect data and take a screenshot using hotkey `printscreen`
4. Take the screenshots on your steam folder `C:\SteamLibrary\steamapps\common\Lost Ark\EFGame\Screenshots` and move to the new folder `C:\pics`

!!! WARNING: DONT MOVE IN-GAME MARKET WINDOW, THE CODE WILL CROP THE TEXT AND IF YOU MOVE FROM DEFAULT POSITION WILL FAIL !!!

If you moved the market window for some reason, just switch characters or re-login to make the window on default location.


## Run the code
1. Open a terminal and run `docker run imagename`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

