import discord
import pandas as pd
import os
import config

# Function to retrieve top 10 posts and return a DataFrame

async def red_func(topic):
    posts = []
    try:
        all_posts = await config.reddit.subreddit(topic)
        hot_posts = all_posts.hot(limit=10)

        async for post in hot_posts:
            posts.append([post.title, post.id,  post.subreddit, post.url, post.selftext, post.num_comments])

        posts = pd.DataFrame(posts, columns=['title', 'id', 'subreddit', 'url', 'description', 'num_comments'], index=None)
        return posts
    except:
        return 

# Discord Configuration
client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('RB'):
        topic = message.content.replace("RB ", "")
        if topic.count(" ") > 0:
            await message.channel.send("Invalid search query, Subreddits do not contain spaces")
        else:
            result = await red_func(topic)
            if type(result) == "<class 'pandas.core.frame.DataFrame'>":
                try:
                    with open(topic + ".csv", "w") as file:
                        file.write(result.to_csv())

                    with open(topic + ".csv", "rb") as file:
                        await message.channel.send("Here is the top 10 hot posts on your search", file = discord.File(file, topic + ".csv"))
                except:
                    await message.channel.send("Search results contained invalid characters, please try searching something else")

                os.remove(topic+".csv")
            else:
                await message.channel.send("No results found")
client.run(config.TOKEN)