# TimeCapsule 
#### <em>Made by: TheAiCarambas🤠 - Interhack Dec. 2021</em> 🤍

# Required Libraries to be Installed:
- ```pip install "fastapi[all]"```
- ```pip install "uvicorn[standard]"```
    -  You might need to install Gunicorn as well: ```pip install gunicorn```
- ```npm install -g truffle```


# Starting the application

1. Open the project in your preferred IDE
2. Run your local Ganache application
2. Open terminal inside the project and type: 
    - ```truffle compile```
    - ```truffle migrate```
    - ```truffle test```
4. To start the BE app, type in terminal: ```sudo uvicorn main:app --reload```
5. To start the FE app, cd into ```/client``` folder and type in terminal: ```npm run start```




# Making requests - WIP
## Directly to BE
POST http://localhost:8000/message

  - BODY ```{ "message": "First Message" }```
  

  
