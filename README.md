# Lost Ark - Price Market History
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Mongo](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)



!!! THIS IS A UNFINISHED PROJECT, ITS WORKING BUT YOU WILL NEED A TECHNICAL KNOWLEDGE !!!

This project is an application that can get market values from itens on Lost Ark game market. It uses BOT's to get 
screenshots from inside the game and get the data from those images and save on a database.

To convert images to text I use [Tesseract](https://github.com/tesseract-ocr/tesseract), an open source text recognition (OCR) Engine.

Here is the step-by-step on how it works:
1. It opens a bot inside Lost Ark
2. The bot open the market inside game, and starting making clicks need to see all the pages
3. The bot closes, and all images are processed to get the data
4. All data is save on a database.


## Requirements
You will need those tools to run the code:

* [Docker](https://www.docker.com/products/docker-desktop/)
* [Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)
* [Python](https://www.python.org/downloads/)
* A character lvl 30 to open the market inside game.

## All-in-One VIDEO TUTORIAL
