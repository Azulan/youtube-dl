# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import (
    parse_duration,
    remove_end,
)


class LRTIE(InfoExtractor):
    IE_NAME = 'lrt.lt'
    _VALID_URL = r'https?://(?:www\.)?lrt\.lt/mediateka/irasas/(?P<id>[0-9]+)'
    _TEST = {
        'url': 'http://www.lrt.lt/mediateka/irasas/54391/',
        'info_dict': {
            'id': '54391',
            'ext': 'mp4',
            'title': 'Septynios Kauno dienos',
            'description': 'md5:24d84534c7dc76581e59f5689462411a',
            'duration': 1783,
        },
        'params': {
            'skip_download': True,  # m3u8 download
        },
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        title = remove_end(self._og_search_title(webpage), ' - LRT')
        m3u8_url = self._search_regex(
            r'file\s*:\s*(["\'])(?P<url>.+?)\1\s*\+\s*location\.hash\.substring\(1\)',
            webpage, 'm3u8 url', group='url')
        formats = self._extract_m3u8_formats(m3u8_url, video_id, 'mp4')

        thumbnail = self._og_search_thumbnail(webpage)
        description = self._og_search_description(webpage)
        duration = parse_duration(self._search_regex(
            r'var\s+record_len\s*=\s*(["\'])(?P<duration>[0-9]+:[0-9]+:[0-9]+)\1',
            webpage, 'duration', default=None, group='duration'))

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'thumbnail': thumbnail,
            'description': description,
            'duration': duration,
        }
