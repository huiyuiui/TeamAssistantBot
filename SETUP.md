# Setup Guide for LINE Bot Template
<div align="right">
last updated: 2023/10/20
</div>

### 1. Got a LINE Bot API devloper account

- Register on [LINE developer console](https://developers.line.biz/console/).
- Create new `Messaging Channel`.
- Get `Channel Secret` on `Basic Setting` tab.
- Press the button `Issue` to get `Channel Access Token` on `Messaging API` tab.
- Open `LINE Official Account manager` from "Basic Setting" tab.
- Go to `回應設定` in `LINE Official Account manager`, enable `Webhook`, and disable `自動回應功能`.
- For our chatbot, we need to join groups. Go to `帳號設定`, `功能切換`, enable `加入群組或多人聊天室`.

### 2. Obtain an OpenAI API token

- From our Line group, our apply on <https://beta.openai.com/>.

### 3. Set environment variables

- Copy `.env.sample` to `.env `then filled all blank.
- `API_ENV`: The environment of the application, can be 'production' or 'develop', default is develop.
- `LOG`: The level of logging, such as 'WARNING', 'INFO', 'DEBUG', etc.
- `LINE_CHANNEL_ACCESS_TOKEN`: From step 1 in the `Messaging API` tab.
- `LINE_CHANNEL_SECRET`: From step 1 in the `Basic Setting` tab.
- `OPENAI_API_KEY`: From step 2.
- `PORT`: default is 8080.

### 4. Run the program

- Setup virtual environment using conda.
    ``` bash
    conda create --name ENV_NAME python==3.11.4
    conda activate ENV_NAME
    pip install -r requirements.txt
    ```
- Or using venv. (You might use git bash on Windows)
    ``` bash
    python -m venv ENV_NAME
    source ENV_NAME/Scripts/activate
    pip install -r requirements.txt
    ```
- Run the program.
    ``` bash
    python main.py
    ```

### 5. Deploy the bot

- Use ngrok, download it form <https://ngrok.com/download>.
- Sign up and get the authtoken from <https://dashboard.ngrok.com/auth/your-authtoken>.
- Unzip and run the exe file, there will be a command line interface.
- Connect your account using authtoken, run the following command in the exe file:
    ``` bash
    ngrok config add-authtoken YOUR_AUTHTOKEN
    ```
- Run the following command in the exe file, the port number should be the same as the one in `.env`.
    ``` bash
    ngrok http 8080
    ```

### 6. Set webhook URL

- Copy the https URL of `Forwarding` and paste it in the `Messaging API`, `Webhooh Settings`, `Webhook URL` in LINE developer console. (something end with ".app")
- Add `/webhooks/line` at the end of the URL.
- Click `Verify` to verify the URL, if it shows `Success`, it means the URL is correct.
- Enable `Use webhook` in the `Messaging API`, `Webhooh Settings` in LINE developer console.

### 7. Add the bot as a friend

- Scan the QR code in the `Messaging API` tab in LINE developer console.
- Or add the bot the ID in the `Messaging API` tab in LINE developer console.