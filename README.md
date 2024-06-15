# A Discord bot full of various random tools which is useful to me.
**Uses Slash Commands**
## Requires an .env with these API variables:
DISCORD_TOKEN,\
OWNER_ID, (this is Discord ID)\
OPENAI_API_KEY\
APEX_API_KEY

## Current features:
### Translation:
Attempts to translate either text or a provided image via facebook's nllb-200-distilled-600M model.  
Uses tesseract to extract text from images.\
Requires tesseract to be downloaded to ``C:\Program Files\Tesseract-OCR\tesseract.exe``\
Requires manual download of [this](https://dl.fbaipublicfiles.com/nllb/lid/lid218e.bin) towards the models/ folder due to git limits

### YouTube Downloader:
**Downloads videos from YouTube:**\
If downloaded video is < 25mb, send to discord channel directly.\
If downloaded video is > 25mb, host on LitterBox and send the link directly.\
Downloads to MP4 format, but can also download to MP3.

### Shazam:
**Attempts to identify songs from an audio file, or through a YouTube link:**\
Uses ShazamIO library to do the recognition and data collection \
Attempts to detect song through a local file\
Re-uses the YouTube MP3 downloader to download the file locally, and uses the local file method to do detection.

### Filters:
**Attempts to apply a simple face filter over detected facial images:***\
Only supports upright faces\
Uses YuNet included in OpenCV to do better facial recognition, with basic landmarks identified.\
Has a few options for filters that I have manually calculated the positioning for.\
Filters are in the filters folder

### Twitter video downloader:
**Uses an [API](https://twitsave.com) to download twitter videos**.\
Uses BeautifulSoup to get the download link\
Sends the file to Discord, I assume the videos are not THAT big for me to use LitterBox.

### Yandex Reverse Image Search:
**Performs a reverse image search and returns the results via Yandex**\
Primarily used to check if the image is original or not\
Returns a discord embed with a paginator to cycle through a couple of results.\
Very simple

### Twitter/TikTok embedder:
**Returns a fxtwitter/fixupx/vxtiktok link of the input so the video can be played through discord**\
I believe Twitter and TikTok does not allow videos to be played outside the site, so FX/VX domains helps return the raw mp4\
The Twitter option has a few more parameters that can be used to translate the tweet, and or reveal the media only.

### TikTok TTS:
**Generates a text-to-speech mp3 file to Discord, using popular TikTok TTS models**\
Uses [this](https://tiktok-tts.weilbyte.dev/) website's API to do this simply

### Generate Image via Dall-E:
**Generates any image through the input prompt, but is for me only, as the API costs money**\
Downloads the image locally, sends to Discord channel, and deletes it.

### Apex Legends Stats:
**Returns Apex Legends map rotation and user statistics**\
Uses [this](https://apexlegendsapi.com/) API to get the data \
Relevant parameters such as platform and user name added for API to work

### Video Tool:
**Does very simple video editing via MoviePY**\
Can remove background audio, add background music overlay, and extract audio from a video.

### Define a word:
**Defines a word using [this](https://dictionaryapi.dev/) API**\
Self explanatory, wants a Discord input, gives the result.









