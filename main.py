import subprocess
import requests
import re
import winreg
import os
import vdf


def get_vdf_file_path(steam_path):
    vdf_file_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")

    if not os.path.exists(vdf_file_path):
        raise FileNotFoundError("ERROR: libraryfolders.vdf file does not exist.")

    return vdf_file_path


def get_steam_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Valve\\Steam")
        steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
        winreg.CloseKey(key)
    except FileNotFoundError:
        raise FileNotFoundError("ERROR: Steam is not installed.")

    if not os.path.exists(steam_path):
        raise FileNotFoundError("ERROR: The Steam path does not exist or is not accessible.")

    return steam_path


def get_app_path(steam_path, app_id):
    vdf_file_path = get_vdf_file_path(steam_path)

    try:
        with open(vdf_file_path, 'r') as file:
            data = file.read()
    except Exception as e:
        raise IOError(f"ERROR: Unable to read the libraryfolders.vdf file. {e}")

    try:
        parsed = vdf.loads(data)
        print(parsed)
    except Exception as e:
        raise ValueError(f"ERROR: Error parsing the VDF file. {e}")

    libraryfolders = parsed.get('libraryfolders', {})

    app_path = None

    for folder in libraryfolders.values():
        if isinstance(folder, dict) and 'apps' in folder and str(app_id) in folder['apps']:
            app_path = folder.get('path')
            if app_path and os.path.exists(app_path):  # 경로 존재 여부 확인
                break

    if app_path is None:
        raise FileNotFoundError(f"ERROR: Could not find the installation path for app {app_id}.")

    return app_path


def get_game_path(steam_path, app_id, game_name):
    app_path = get_app_path(steam_path, app_id)
    game_path = os.path.join(app_path, 'steamapps', 'common', game_name)

    if not os.path.exists(game_path):
        raise FileNotFoundError(
            f"ERROR: The game path does not exist. Check if the game name '{game_name}' is correct and the game is properly installed.")

    return game_path

def reg_file_download(duck_game_path, url_to_file):
    # Делаем Get запрос через Drive API, потому что просто так скачать из Drive нельзя
    google_drive_url = "https://drive.usercontent.google.com/download"
    file_id = re.search( r'id=([-\w]+)', url_to_file).group(1)
    parametrs = {
        "id": file_id,
        "confirm": "t"
    }
    response_download = requests.get(google_drive_url, params=parametrs)
    regsfile_path = rf"{duck_game_path}\settings.reg"
    if response_download.status_code == 200:
        with open(regsfile_path, 'wb') as f:
            f.write(response_download.content)
        print("\nSuccessfully! Regis file downloaded")
    else:
        print("Error, regis file not downloaded!")
    return regsfile_path


def get_reg_data(regfile_path):
    data = {}
    with open(regfile_path, 'r',encoding='utf-16') as reg_file:
        for string in reg_file:
            if '=' in string:
                params = re.match(r'"([^"]+)"=([^"]+):([0-9]{8})', string)
                if params:
                    name = params.group(1)
                    type = params.group(2)
                    num = params.group(3)
                    data[name] = (num, type)
            elif string.startswith('['):
                hkeys_path = string.strip()[1:-1]

    return hkeys_path, data


# Set data from register file in Windows system register
def set_register_data(hkeys_path, data):
    try:
        hkeys_parts = hkeys_path.split('\\', 1)
        hkeys = winreg.__dict__[hkeys_parts[0]]
        path = hkeys_parts[1]
        hkeys = winreg.OpenKey(hkeys, path, 0, winreg.KEY_SET_VALUE)
        for name_key, paramets in data.items():
            param_type = rf"REG_{paramets[1].upper()}"
            # Take correct type from regis
            param_type = winreg.__dict__[param_type]
            winreg.SetValueEx(hkeys, name_key, 0, param_type, int(paramets[0], 16))
        winreg.CloseKey(hkeys)
        print("Successfully set settings.reg data in System")
    except:
        print("Error, reg file data wasn't set!")

# Main operations if start file
if __name__ == "__main__":
    id_game = "1568590"
    steam_path = get_steam_path()
    print(steam_path)
    steam_exe_path = rf"{steam_path}\steam.exe"
    game_path = get_game_path(steam_path, id_game, "Goose Goose Duck")
    game_path_exe = rf'"{game_path}\Goose Goose Duck.exe"'
    reg_file_path = reg_file_download(game_path, "https://drive.google.com/uc?export=download&id=1IGENwFzLm8bBEboISadYSNEdxbnjz1fH")
    print(rf"Regis path: {reg_file_path}")
    hkey_path, reg_data = get_reg_data(reg_file_path)
    set_register_data(hkey_path, reg_data)
    print(rf"Exe game file path: {game_path_exe}")
    subprocess.run([steam_exe_path, "-applaunch", id_game])

