from telethon import TelegramClient, events
import re

API_ID = '21814194'
API_HASH = '9535a6cee1e1d8e3a97a245f73b2d52a'
PHONE_NUMBER = '+918678996799'
TARGET_CHANNELS = ['@DARKESPYT', '@Source_Leak', '@Source_HUB']
SOURCE_CHANNELS = ['@backuprrrrrr', '@CAPTAINSRC', '@KINGMODEVIPSRC', '@VIP_SRC_Leakers', '@LEAK_SRC_ALL', '@Tharki_Pushpa', '@SRC_BGMI_GL_KR_VNG', '@SrcEsp', '@PrivateFileTg', '@KNIGHTMODSSRCS', '@NOBITA_SRC', '@VIP_SRC_LEEKAR', '@Yarasa_Src', '@SrcLeakerVip', '@MadSrcLeakers', '@PRIVATE_SRC', '@SrcTeam']
client = TelegramClient('SRC_FORWARDER', API_ID, API_HASH)

async def main():
    await client.start(PHONE_NUMBER)
    print("Client Started")
    print(f"All Source Channels: {SOURCE_CHANNELS}")

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_message(event):
    try:
        message_text = event.message.message or ''
        caption = re.sub(r"http\S+|https\S+|@\w+", "@DARKESPYT", message_text)
        if event.photo and re.search(r'\b(SRC|SOURCE|UI)\b', message_text, re.IGNORECASE):
            for target_channel in TARGET_CHANNELS:
                await client.send_file(target_channel, event.message.media, caption=caption)
        elif event.document and event.document.mime_type == 'application/zip' and re.search(r'\b(SRC|SOURCE)\b', message_text, re.IGNORECASE):
            for target_channel in TARGET_CHANNELS:
                await client.send_file(target_channel, event.message.media, caption=caption)
        elif re.search(r'\b(SRC|SOURCE)\b', message_text, re.IGNORECASE):
            text = re.sub(r"http\S+|https\S+|@\w+", "@DARKESPYT", event.message.message)
            for target_channel in TARGET_CHANNELS:
                await client.send_message(target_channel, text)
    except Exception as e:
        print(f"An error occurred: {e}")

client.start()
client.run_until_disconnected()