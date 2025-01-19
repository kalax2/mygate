## Register

If you don't have a mygate network account yet, you can get one from [here](https://app.mygate.network/login?code=QfLc9A).

Also you can use my referral code QfLc9A to boost your points.

## Setup

1. Get your token.

    - Login to MyGate Network.
    - Press F12 to open browser's developer tools
    - Go to the "Console" tab
    - Enter the code `copy(localStorage.getItem('persist:root'));`, and then you have copied you token

2. Excute the following code

    ```bash
    git clone https://github.com/kalax2/mygate
    cd mygate
    ```

    Paste your token(copied from step 1) to `token.json`, and save the file.

3. Start the container.
    ```bash
    docker compose up -d
    ```

## Support

If you would like to support this project, you can make a donation.

-   EVM: `0xE3ac80866D36D004dB6AD19634c3773071152D3d`
-   BTC: `bc1q77464egsza2874vm78kkpyt2u4kgqcmcvpsla3`
-   Solana: `95Art9wVQBeLQKxvsn6sMaHcaBUJzZbhSvVUa4fWB1H`
