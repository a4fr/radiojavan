import requests
import re


class MediaType:
    podcast = 'podcasts'
    mp3 = 'mp3s'


class RadioJavan:
    def __init__(self):
        pass

    def _get_media_type(self, media_url):
        """ Extract media type [podcasts, mp3s]
        :param media_url: str
        :return: MediaType object
        """
        media_type = re.split(r'/', media_url)[3]
        if media_type == MediaType.podcast:
            return MediaType.podcast
        elif media_type == MediaType.mp3:
            return MediaType.mp3
        else:
            return None

    def request_html(self, url, json=False):
        headers = {'User-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            if json:
                return r.json()
            else:
                return r.text
        else:
            raise Exception('Status Code!')

    def get_download_link(self, media_url):
        media_url = media_url.strip()
        media_type = self._get_media_type(media_url).strip()
        file_name = re.split(r'/', link)[5].strip()
        if not media_type:
            return None

        # require FILENAME
        server_base_url = {
            MediaType.podcast: 'https://www.radiojavan.com/podcasts/podcast_host/?id=%s',
            MediaType.mp3: 'https://www.radiojavan.com/mp3s/mp3_host/?id=%s',
        }
        # require SERVER + FILENAME
        dl_base_url = {
            MediaType.podcast: '%s/media/podcast/mp3-256/%s.mp3',
            MediaType.mp3: '%s/media/mp3/%s.mp3',
        }

        url = server_base_url[media_type] % file_name
        print('HOST URL: ', url)
        host = self.request_html(url, json=True)['host']
        dl_link = dl_base_url[media_type] % (host, file_name)
        return dl_link


if __name__ == "__main__":
    link = input("Enter link: ")
    rj = RadioJavan()
    print(rj.get_download_link(link))
