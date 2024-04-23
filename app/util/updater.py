import os, requests


class Updater():
    def __init__(self, logs_perf):
        self._REPO_OWNER = 'shadow3731'
        self._REPO_NAME = 'Network-Folders'
        
        self.updatable = False
        
        self.logs_perf = logs_perf
        
    def check_for_update(self, current_version):
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.CHECK_NEW_VER_MESS_ID)
        
        release_info = self._fetch_latest_release()
        
        if release_info:
            latest_version = release_info['tag_name']
            
            if current_version != latest_version:
                self.logs_perf.log(self.logs_perf.WARN, self.logs_perf.NEW_VER_MESS_ID, (latest_version,))
                
                asset_url = release_info['assets'][0]['browser_download_url']
                release_filename = os.path.basename(asset_url)
                save_path = os.path.join(os.getcwd(), release_filename)
                downloaded = self._download_release_asset(asset_url, save_path)
                
                if downloaded:
                    self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.DOWNLOAD_NEW_VER_SUCC_MESS_ID)
                
                    self.updatable = True
                
                else:
                    self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.DOWNLOAD_NEW_VER_FAIL_MESS_ID)

        else:
            self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.NO_NEW_VER_MESS_ID)
        
    def _fetch_latest_release(self):
        url = f'https://api.github.com/repos/{self._REPO_OWNER}/{self._REPO_NAME}/releases/latest'
        response = requests.get(url)
        
        if response.status_code == 200:
            self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.CHECK_RES_CODE_SUCC_MESS_ID)
            
            return response.json()
        
        else:
            self.logs_perf.log(self.logs_perf.ERR, self.logs_perf.CHECK_RES_CODE_FAIL_MESS_ID, (response.status_code,))
            
            return None
    
    def _download_release_asset(self, asset_url, save_path):
        response = requests.get(asset_url)
        
        if response.status_code == 200:
            self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.DOWNLOAD_NEW_VER_RES_CODE_SUCC_MESS_ID)
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
                
                return True
        
        else:
            self.logs_perf.log(self.logs_perf.ERR, self.logs_perf.DOWNLOAD_NEW_VER_RES_CODE_FAIL_MESS_ID, (response.status_code,))    
            
            return False