# Epic RPG Bot Captcha Solver

This bot can automate hunting and working in Epic RPG on Discord.

It can solve captcha (~95% accuracy) by Epic Guard.

## Requiremenents
- Python 3.7 (I recommend using pyenv to install it)
- pipenv
- Chrome Browser
- Strong enough computer to run the AI model

## Installation
1. Clone this repo - `git clone https://github.com/LeagueOfPoro/EpicRPGCaptcha.git`
2. Move to its folder - `cd EpicRPGCaptcha`
3. Install the virtual environment - `pipenv install`
4. Create a new Chrome profile
5. Log in to Dicord in the profile
6. Copy the profile path from `chrome://version/` - e.g. `C:\Users\PC\AppData\Local\Google\Chrome\User Data\Profile 1`
7. [Configure the bot](#configuration)
8. Run the bot - `pipenv run python .\main.py`

## Configuration
Edit [main.py](main.py) to change the following options:
- Set `DATA_DIR` to Chrome's User Data directory, e.g. `C:/Users/PC/AppData/Local/Google/Chrome/User Data`
- Set `PROFILE_DIR` to Chrome's profile name, e.g. `Profile 1`
- Set `DISCORD_CHANNEL` to URL where the bot will operate, e.g. `https://discord.com/channels/493694955184926720/931492715865397073`

## Tips
- Bot will pause if it detect the word `jail` in the last 10 messages
    - It resumes if it detects `I solemnly swear that I am up to no good`
    - It kills itself if it detects `Mischief managed`
- Change work command by `chwrk rpg chainsaw`
- Heal after every hunt by `Start healing` (and stop it by `Stop healing`)

## Notes
- The AI model might not load if you don't have enough GPU memory
- You take full responsibility for using the bot

## Support the project
If you like my work, [become a member on my YouTube channel](https://www.youtube.com/c/LeagueOfPoro/join)
