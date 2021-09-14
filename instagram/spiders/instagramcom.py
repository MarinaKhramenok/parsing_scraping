import json
import re
import scrapy
from scrapy.http import HtmlResponse
from instagram.items import InstagramItem


class InstagramcomSpider(scrapy.Spider):
    name = 'instagramcom'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    insta_login = 'Onliskill_udm'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1629825416:ASpQAMvl1EAdo0NdRZNcM1/pjlU9rRg4n4cjCM00SDGSV5pDN6XbC93ZbYN67HUOHkXZnGGe2gIWPU2qtQY0HAkIjR5U5syu+lv8qtqeI7cyy2ua6WmBV6AngVo1apn3eJ6O3UAFVgb+q5HtHsQ='
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    user_parse = ['shkya_shootkikaifjashperitsa', 'elivosk']
    api_url = 'https://i.instagram.com/api/v1/friendships/'

    def parse(self, response:HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pass},
                                 headers={'X-CSRFToken': csrf})

    def user_login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body['authenticated']:
            for user in self.user_parse:
                yield response.follow(f'/{user}',
                                  callback=self.u_parse,
                                  cb_kwargs={'username': user})

    def u_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        url_followers = f'{self.api_url}{user_id}/followers/?count=12&search_surface=follow_list_page'
        yield response.follow(url_followers,
                                callback=self.followers_parse,
                                cb_kwargs={'username': username,
                                            'user_id': user_id,
                                            'followers_all': 'followers'},
                                headers={'User-Agent': 'Instagram 155.0.0.37.107'}
        )

        url_following = f'{self.api_url}{user_id}/following/?count=12&search_surface=follow_list_page'
        yield response.follow(url_following,
                                callback=self.followers_parse,
                                cb_kwargs={'username': username,
                                            'user_id': user_id,
                                            'followers_all': 'following'},
                                headers={'User-Agent': 'Instagram 155.0.0.37.107'}
        )

    def followers_parse(self, response: HtmlResponse, username, user_id, followers_all):
        j_resp = response.json()
        if j_resp['next_max_id']:
            max_id = j_resp['next_max_id']
            url_followers = f'{self.api_url}{user_id}/{followers_all}/?count=12&max_id={max_id}&search_surface=follow_list_page'
            yield response.follow(url_followers,
                                    callback=self.followers_parse,
                                    cb_kwargs={'username': username,
                                                'user_id': user_id,
                                                'followers_all': 'followers_all'},
                                    headers={'User-Agent': 'Instagram 155.0.0.37.107'}
            )

        for user in j_resp['users']:
            item = InstagramItem(followers=followers_all,
                                user_id=user['pk'],
                                username=user['username'],
                                photos=user['profile_pic_url'],
                                main_user=username,
            )
            yield item

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
