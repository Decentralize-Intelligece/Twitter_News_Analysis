import os
import uuid

import pandas as pd
from bs4 import BeautifulSoup

input_folder = "data/"

# creat dataframe to store the data with id, date, source, content, url, hashtags, datetime
df_final = pd.DataFrame(columns=['id', 'date', 'source', 'content', 'url', 'hashtags', 'datetime'])


def get_tweets(file_name, df, source="hirunews"):
    temp_df = pd.DataFrame(columns=['id', 'date', 'source', 'content', 'url', 'hashtags', 'datetime'])

    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()

    # split by <div class="css-1dbjc4n r-16y2uox r-1wbh5a2 r-1ny4l3l">
    split_content = content.split('<div class="css-1dbjc4n r-16y2uox r-1wbh5a2 r-1ny4l3l">')

    # print(len(split_content))

    # keep only the items with "<div class="css-1dbjc4n"><div class="css-1dbjc4n r-18u37iz"><div class="css-1dbjc4n r-1iusvr4 r-16y2uox r-ttdzmv"></div></div></div><div class="css-1dbjc4n r-18u37iz"><div class="css-1dbjc4n r-1awozwy r-onrtq4 r-18kxxzh r-1b7u577"><div class="css-1dbjc4n" data-testid="Tweet-User-Avatar"><div class="css-1dbjc4n r-18kxxzh r-1wbh5a2 r-13qz1uu"><div class="css-1dbjc4n r-1wbh5a2 r-dnmrzs"><div class="css-1dbjc4n r-1adg3ll r-bztko3" data-testid="UserAvatar-Container-hirunews" style="height: 40px; width: 40px;"><div class="r-1adg3ll r-13qz1uu" style="padding-bottom: 100%;"></div><div class="r-1p0dtai r-1pi2tsx r-1d2f490 r-u8s1d r-ipm5af r-13qz1uu"><div class="css-1dbjc4n r-1adg3ll r-1pi2tsx r-1wyvozj r-bztko3 r-u8s1d r-1v2oles r-desppf r-13qz1uu"><div class="r-1adg3ll r-13qz1uu" style="padding-bottom: 100%;"></div><div class="r-1p0dtai r-1pi2tsx r-1d2f490 r-u8s1d r-ipm5af r-13qz1uu"><div class="css-1dbjc4n r-sdzlij r-ggadg3 r-1udh08x r-u8s1d r-8jfcpp" style="height: calc(100% - -4px); width: calc(100% - -4px);"><a href="/hirunews" aria-hidden="true" role="link" tabindex="-1" class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1niwhzg r-1loqt21 r-1pi2tsx r-1ny4l3l r-o7ynqc r-6416eg r-13qz1uu"><div class="css-1dbjc4n r-sdzlij r-1wyvozj r-1udh08x r-633pao r-u8s1d r-1v2oles r-desppf" style="height: calc(100% - 4px); width: calc(100% - 4px);"><div class="css-1dbjc4n r-1niwhzg r-1pi2tsx r-13qz1uu"></div></div><div class="css-1dbjc4n r-sdzlij r-1wyvozj r-1udh08x r-633pao r-u8s1d r-1v2oles r-desppf" style="height: calc(100% - 4px); width: calc(100% - 4px);"><div class="css-1dbjc4n r-kemksi r-1pi2tsx r-13qz1uu"></div></div><div class="css-1dbjc4n r-kemksi r-sdzlij r-1wyvozj r-1udh08x r-633pao r-u8s1d r-1v2oles r-desppf" style="height: calc(100% - 4px); width: calc(100% - 4px);"><div class="css-1dbjc4n r-1adg3ll r-1udh08x" style=""><div class="r-1adg3ll r-13qz1uu" style="padding-bottom: 100%;"></div><div class="r-1p0dtai r-1pi2tsx r-1d2f490 r-u8s1d r-ipm5af r-13qz1uu"><div aria-label="" class="css-1dbjc4n r-1p0dtai r-1mlwlqe r-1d2f490 r-1udh08x r-u8s1d r-zchlnj r-ipm5af r-417010"><div class="css-1dbjc4n r-1niwhzg r-vvn4in r-u6sd8q r-4gszlv r-1p0dtai r-1pi2tsx r-1d2f490 r-u8s1d r-zchlnj r-ipm5af r-13qz1uu r-1wyyakw" style="background-image: url(&quot;https://pbs.twimg.com/profile_images/1261671246846144516/PN_-1D2B_bigger.jpg&quot;);"></div><img alt="" draggable="true" src="https://pbs.twimg.com/profile_images/1261671246846144516/PN_-1D2B_bigger.jpg" class="css-9pa8cd"></div></div></div></div><div class="css-1dbjc4n r-sdzlij r-1wyvozj r-1udh08x r-u8s1d r-1v2oles r-desppf" style="height: calc(100% - 4px); width: calc(100% - 4px);"><div class="css-1dbjc4n r-172uzmj r-1pi2tsx r-1ny4l3l r-o7ynqc r-6416eg r-13qz1uu"></div></div></a></div></div></div></div></div></div></div></div></div><div class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"><div class="css-1dbjc4n r-zl2h9q"><div class="css-1dbjc4n r-k4xj1c r-18u37iz r"
    check_content = r'<div class="css-1dbjc4n"><div class="css-1dbjc4n r-18u37iz"><div class="css-1dbjc4n r-1iusvr4 r-16y2uox r-ttdzmv"></div></div></div><div class="css-1dbjc4n r-18u37iz"><div class="css-1dbjc4n r-1awozwy r-onrtq4 r-18kxxzh r-1b7u577"><div class="css-1dbjc4n" data-testid="Tweet-User-Avatar"><div class="css-1dbjc4n r-18kxxzh r-1wbh5a2 r-13qz1uu"><div class="css-1dbjc4n r-1wbh5a2 r-dnmrzs"><div class="css-1dbjc4n r-1adg3ll r-bztko3" data-testid="UserAvatar-Container-hirunews" style="height: 40px; width: 40px;"><div class="r-1adg3ll r-13qz1uu" style="padding-bottom: 100%;"></div><div class="r-1p0dtai r-1pi2tsx r-1d2f490 r-u8s1d r-ipm5af r-13qz1uu"><div class="css-1dbjc4n r-1adg3ll r-1pi2tsx r-1wyvozj r-bztko3 r-u8s1d r-1v2oles r-desppf r-13qz1uu"><div class="r-1adg3ll r-13qz1uu" style="padding-bottom: 100%;"></div><div class="r-1p0dtai r-1pi2tsx r-1d2f490 r-u8s1d r-ipm5af r-13qz1uu"><div class="css-1dbjc4n r-sdzlij r-ggadg3 r-1udh08x r-u8s1d r-8jfcpp" style="height: calc(100% - -4px); width: calc(100% - -4px);"><a href="/hirunews" aria-hidden="true" role="link" tabindex="-1" class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1niwhzg r-1loqt21 r-1pi2tsx r-1ny4l3l r-o7ynqc r-6416eg r-13qz1uu"><div class="css-1dbjc4n r-sdzlij r-1wyvozj r-1udh08x r-633pao r-u8s1d r-1v2oles r-desppf" style="height: calc(100% - 4px); width: calc(100% - 4px);"><div class="css-1dbjc4n r-1niwhzg r-1pi2tsx r-13qz1uu"></div></div><div class="css-1dbjc4n r-sdzlij r-1wyvozj r-1udh08x r-633pao r-u8s1d r-1v2oles r-desppf" style="height: calc(100% - 4px); width: calc(100% - 4px);"><div class="css-1dbjc4n r-kemksi r-1pi2tsx r-13qz1uu"></div></div><div class="css-1dbjc4n r-kemksi r-sdzlij r-1wyvozj r-1udh08x r-633pao r-u8s1d r-1v2oles r-desppf" style="height: calc(100% - 4px); width: calc(100% - 4px);"><div class="css-1dbjc4n r-1adg3ll r-1udh08x" style=""><div class="r-1adg3ll r-13qz1uu" style="padding-bottom: 100%;"></div><div class="r-1p0dtai r-1pi2tsx r-1d2f490 r-u8s1d r-ipm5af r-13qz1uu"><div aria-label="" class="css-1dbjc4n r-1p0dtai r-1mlwlqe r-1d2f490 r-1udh08x r-u8s1d r-zchlnj r-ipm5af r-417010"><div class="css-1dbjc4n r-1niwhzg r-vvn4in r-u6sd8q r-4gszlv r-1p0dtai r-1pi2tsx r-1d2f490 r-u8s1d r-zchlnj r-ipm5af r-13qz1uu r-1wyyakw" style="background-image: url(&quot;https://pbs.twimg.com/profile_images/1261671246846144516/PN_-1D2B_bigger.jpg&quot;);"></div><img alt="" draggable="true" src="https://pbs.twimg.com/profile_images/1261671246846144516/PN_-1D2B_bigger.jpg" class="css-9pa8cd"></div></div></div></div><div class="css-1dbjc4n r-sdzlij r-1wyvozj r-1udh08x r-u8s1d r-1v2oles r-desppf" style="height: calc(100% - 4px); width: calc(100% - 4px);"><div class="css-1dbjc4n r-172uzmj r-1pi2tsx r-1ny4l3l r-o7ynqc r-6416eg r-13qz1uu"></div></div></a></div></div></div></div></div></div></div></div></div><div class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"><div class="css-1dbjc4n r-zl2h9q"><div class="css-1dbjc4n r-k4xj1c r-18u37iz r'
    for i in split_content:
        # if check_content is not included in split_content
        if check_content not in i:
            # remove i from split_content
            split_content.remove(i)

    # for i in range(3, 4):
    for i in range(0, len(split_content)):
        soup = BeautifulSoup(split_content[i], 'html.parser')
        # print(soup.prettify())

        # <time datetime="2023-07-07T03:59:16.000Z">
        # find above tag
        time_tag = soup.find("time")
        print(time_tag.get_text())  # Jul 7
        print(time_tag.get("datetime"))  # 2023-07-07T03:59:16.000Z

        # get <a class="css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1cvl2hr r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0" dir="ltr" href="
        # find above tag
        # Find <a> tags with specific class and dir attribute
        a_tags = soup.find_all("a",
                               class_="css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1cvl2hr r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0",
                               dir="ltr")
        # print(len(a_tags)) # 1

        # for a_tag in a_tags:
        #     print(a_tag.get_text())

        hastags = []

        # reomve http if there is any from a_tags list
        if len(a_tags) > 0:
            for a_tag in a_tags:
                if a_tag.get_text().startswith("http"):
                    pass
                    # a_tags.remove(a_tag)
                else:
                    hastags.append(a_tag.get_text())
            # print(len(a_tags))

        print(hastags)

        # <a class="css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1cvl2hr r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0" dir="ltr"
        a_tag = soup.find("a",
                          class_="css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1cvl2hr r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0")

        print(a_tag.get_text())

        # List of elements with a specific class
        element_list = soup.find_all("div",
                                     class_="css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0")
        # in the element_list, find ("span", class_="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")
        lst_2 = []
        for element in element_list:
            lst_2.append(element.find("span", class_="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0").get_text())

        # remove scape characters from lst_2
        lst_3 = []
        for i in lst_2:
            lst_3.append(i.replace("\n", ""))

        print(lst_3[0])
        # df = pd.DataFrame(columns=['id', 'date', 'source', 'content', 'url', 'hashtags', 'datetime'])
        # return dataframe
        df = pd.DataFrame({
            "id": uuid.uuid1(),
            "date": time_tag.get_text(),
            "source": source,
            "content": lst_3[0],
            "url": a_tag.get_text(),
            "hashtags": str(hastags),
            "datetime": time_tag.get("datetime"),
        },
            index=[0])
        # print(df)

        # add to temp dataframe with concat
        temp_df = pd.concat([temp_df, df], ignore_index=True)
        # print(temp_df)

    # save with uuid
    df.to_csv("out/twitter_data_{}.csv".format(uuid.uuid1()), index=False)

    return temp_df


def get_tweets_in_folder(input_folder, df_final):
    # read all txt files in input_folder
    for file_name in os.listdir(input_folder):
        # file_name = 'data/twitter_scrape-content-_HiruSinhalaNews_until_2023-07-09_since_2023-07-07-1 (3).txt'
        df_out = get_tweets(input_folder + file_name, df_final)

        # add to df_final
        df_final = pd.concat([df_final, df_out], ignore_index=True)

    return df_final


# get tweets in folder
df_final = get_tweets_in_folder("data/", df_final)

print(df_final)

# save df with uuid
df_final.to_csv("twitter_data_{}.csv".format(uuid.uuid1()), index=False)
