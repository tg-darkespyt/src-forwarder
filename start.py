from telethon import TelegramClient, events
import re
import sqlite3
import os
import pyzipper
import zipfile
import shutil

API_ID = '21814194'
API_HASH = '9535a6cee1e1d8e3a97a245f73b2d52a'
TARGET_CHANNELS = ['@DARKESPYT', '@Source_Leak', '@Source_HUB', '@BADBOY_MAIN']
SOURCE_CHANNELS = ['@backuprrrrrr', '@Dazai_FreeSrc', '@CAPTAINSRC', '@KINGMODEVIPSRC', '@VIP_SRC_Leakers', '@LEAK_SRC_ALL', '@Tharki_Pushpa', '@SRC_BGMI_GL_KR_VNG', '@SrcEsp', '@PrivateFileTg', '@KNIGHTMODSSRCS', '@NOBITA_SRC', '@VIP_SRC_LEEKAR', '@Yarasa_Src', '@SrcLeakerVip', '@MadSrcLeakers', '@PRIVATE_SRC', '@SrcTeam']

client = TelegramClient('SRC_FORWARDER', API_ID, API_HASH)
DB_FILE = 'passwords.db'
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (post_id INTEGER PRIMARY KEY, password TEXT NOT NULL)''')
conn.commit()

async def main():
    await client.start()
    print("Client Started")

def save_password(post_id, password):
    cursor.execute('''INSERT OR REPLACE INTO passwords (post_id, password) VALUES (?, ?)''', (post_id, password))
    conn.commit()

def get_password(post_id):
    cursor.execute('SELECT password FROM passwords WHERE post_id = ?', (post_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def list_all_passwords():
    cursor.execute('SELECT post_id, password FROM passwords')
    results = cursor.fetchall()
    return results

def extract_password(text):
    pattern = r"(?i)(password|pass)\s*[:\-]?\s*(.+)"
    matches = re.findall(pattern, text)
    if matches:
        return matches[-1][1]
    return None

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_message(event):
    try:
        message_text = event.message.message or ''
        post_id = event.message.id
        password = extract_password(message_text)
        caption = message_text
        if password is not None:
            save_password(post_id, password)
            caption = re.sub(re.escape(password), "`JOIN : @DARKESPYT`", caption)
        caption = re.sub(r"http\S+|https\S+|@\w+", "@DARKESPYT", caption)
        if event.document and event.document.mime_type == 'application/zip':
            doc_name = event.document.attributes[0].file_name if event.document.attributes else ''
            if re.search(r'\b(src|source|imgui|java|hud|sdk)\b', doc_name, re.IGNORECASE) or re.search(r'\b(src|source|imgui|java|hud|sdk)\b', message_text, re.IGNORECASE):
                file_path = await event.message.download_media()
                extracted_folder = os.path.join(os.path.dirname(file_path), f"extracted_{post_id}")
                os.makedirs(extracted_folder, exist_ok=True)
                try:
                    with pyzipper.AESZipFile(file_path, 'r') as zf:
                        zf.pwd = password.encode('utf-8')  # Use the extracted password to open the zip
                        for file_info in zf.infolist():
                            if file_info.filename.endswith('.gitignore'):
                                print(f"Skipping .gitignore file: {file_info.filename}")
                                continue
                            zf.extract(file_info, extracted_folder)
                    if not os.listdir(extracted_folder):
                        raise Exception("No files extracted. Check password or file integrity.")
                except (RuntimeError, zipfile.BadZipFile, pyzipper.BadZipFile, pyzipper.LargeZipFile) as e:
                    print(f"Error during extraction: {e}")
                    return
                recompressed_path = os.path.join(os.path.dirname(file_path), f"@DARKESPYT_{doc_name}")
                with pyzipper.AESZipFile(recompressed_path, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
                    zf.setpassword(b'JOIN : @DARKESPYT')
                    for root, _, files in os.walk(extracted_folder):
                        for file in files:
                            file_full_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_full_path, extracted_folder)
                            zf.write(file_full_path, arcname)
                shutil.rmtree(extracted_folder)
                os.remove(file_path)
                caption += f"\n\n**Note:** if the given password is not works or file is corrupted kindly send this `https://t.me/DARKESPYT/{post_id}` to @USIR_DIED_REAL. So my Master will help you!\n\nJoin For More : @DARKESPYT [ 𝑹𝒆-𝑩𝒖𝒊𝒍𝒅𝒊𝒏𝒈 ]"
                for target_channel in TARGET_CHANNELS:
                    await client.send_file(target_channel, recompressed_path, caption=caption)
                os.remove(recompressed_path)
        if event.photo and re.search(r'\bSRC|SOURCE|UI\b', message_text, re.IGNORECASE):
            caption += "\n\nJoin For More : @DARKESPYT [ 𝑹𝒆-𝑩𝒖𝒊𝒍𝒅𝒊𝒏𝒈 ]"
            for target_channel in TARGET_CHANNELS:
                await client.send_file(target_channel, event.message.media, caption=caption)
    except Exception as e:
        print(f"An error occurred: {e}")

@client.on(events.NewMessage(func=lambda e: e.is_private))
async def handle_dm(event):
    try:
        dm_text = event.message.message or ''
        post_id_match = re.search(r'https://t\.me/DARKESPYT/(\d+)', dm_text)
        if post_id_match:
            post_id = int(post_id_match.group(1))
            password = get_password(post_id)
            if password:
                await event.respond(f"Password for post ID {post_id}: `{password}`\n\nJoin For More : @DARKESPYT [ 𝑹𝒆-𝑩𝒖𝒊𝒍𝒅𝒊𝒏𝒈 ]")
            else:
                await event.respond(f"No password found for post ID {post_id}.\n\nJoin For More : @DARKESPYT [ 𝑹𝒆-𝑩𝒖𝒊𝒍𝒅𝒊𝒏𝒈 ]")
    except Exception as e:
        print(f"An error occurred in DM handling: {e}")

client.start()
client.run_until_disconnected()
