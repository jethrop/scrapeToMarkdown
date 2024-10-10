[Back](/blog)

[Blog](/blog)

# Slack Consolidate: a slackbot built with Python and Supabase

09 Aug 2022

•

15 minute read

[![Rodrigo Mansueli
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fmansueli.png&w=96&q=75)Rodrigo
MansueliSupport Engineer](https://github.com/mansueli)

![Slack Consolidate: a slackbot built with Python and
Supabase](/_next/image?url=%2Fimages%2Fblog%2Fslackbot-consolidate%2Fslackbot-
thumb.jpg&w=3840&q=100)

Supabase is a platform-as-a-service built on top of PostgreSQL and [many other
amazing open-source tools](https://supabase.com/docs/guides/getting-
started/architecture). It’s a fantastic option to create data-intensive apps
and tooling. Taking advantage of the community-made [Python
SDK](https://github.com/supabase-community/supabase-py) and [Slack's Python
SDK](https://slack.dev/python-slack-sdk/), you can automate tasks and build
apps for several use cases.

## Prerequisites#

Before we dive in, let’s look at some prerequisites you'll need:

  * [Supabase Client](https://pypi.org/project/supabase/)
    * The SDK only supports Python > 3.7. You can download a supported Python version from [here](https://www.python.org/downloads/). `pip install supabase`
  * [Python dotenv](https://pypi.org/project/python-dotenv/) to handle API keys without exposing them in the code
    * This is optional, but it will avoid issues of package dependencies and version conflicts. **`pip install python-dotenv`**
  * [Slack SDK](https://pypi.org/project/slack-sdk/) for Python
    * This is needed to create the Slack bot **`pip install slack-sdk`**

### Creating the App in Slack#

Now, it is time to create the bot in Slack and get the API Keys (after
granting the required scopes)

<https://api.slack.com/apps>

Green arrow pointing to the ‘Create New App’ button.

Then, select to create an app from a manifest (this will already set the
required permissions) for the app:

Green arrow pointing to the option ‘From an app manifest’ inside the “Create
an app” menu.

Select the Slack workspace to deploy:

The picture shows a dropdown UI with Supabase selected as the workspace.

`Manifest.yaml`

`  

_30

display_information:

_30

name: SlackConsolidate

_30

features:

_30

bot_user:

_30

display_name: SlackConsolidate

_30

always_online: false

_30

oauth_config:

_30

scopes:

_30

user:

_30

- channels:history

_30

- channels:read

_30

- channels:write

_30

- chat:write

_30

- links:read

_30

- users:read

_30

- groups:history

_30

- groups:read

_30

- mpim:history

_30

- im:history

_30

bot:

_30

- channels:history

_30

- channels:read

_30

- links:read

_30

- chat:write.public

_30

- chat:write

_30

- channels:join

_30

settings:

_30

org_deploy_enabled: false

_30

socket_mode_enabled: false

_30

token_rotation_enabled: false

  
`

Enter the manifest above when asked:

The picture shows the place where you have to paste the manifest file included
in the repo.

Then, confirm to create the bot:

You can see a summary screen to confirm the creation of the bot and the scopes
assigned.

## Granting access to the bot:#

Install the app on the workspace:

The picture shows the button to Install the App to the Slack Workspace.

Inviting the bot to the channels, it will post messages on:

The command to invite the bot is below:

`/invite @SlackConsolidate`

The picture shows the command /invite @Slackbot in the channel #team-support.

Now, we are done with Slack for now. Let's create some buffer tables in
Supabase.

## Creating Tables in Supabase#

Create an account [here](https://supabase.com/dashboard/) (if you don't have
one yet).

We will be using Supabase's
[database](https://supabase.com/docs/guides/database) and the Python [client
Libraries](https://supabase.com/docs/guides/client-libraries#managing-data).
First, we will create one table to store the channels that are being watched
and where they are going to send the message which works analogously to a
multiplexer circuit. Since you may want to watch several channels but split
them into a smaller buffer e.g VIP / Enterprise, etc.

Go to the SQL Editor and run this:

`  

_18

CREATE TABLE slack_channels (

_18

id SERIAL PRIMARY KEY,

_18

channel text,

_18

channel_id text,

_18

p_level text DEFAULT ''::text NOT NULL,

_18

dest_channel text,

_18

dest_channel_id text,

_18

private int DEFAULT '0'::int NOT NULL

_18

);

_18

_18

CREATE TABLE slack_watcher (

_18

channel_name text,

_18

channel_id text NOT NULL,

_18

message text,

_18

ts timestamp with time zone NOT NULL,

_18

ts_ms text NOT NULL,

_18

CONSTRAINT pk_slackwatcher PRIMARY KEY (channel_id, ts, ts_ms)

_18

);

  
`

## Adding channels to the watch list and setting the destination channel:#

You may want to call
[conversations.list](https://api.slack.com/methods/conversations.list) to dump
all the channels and channel IDs into a CSV file, then use it to populate the
table `slack_channels`. You can also manually get the data, but copying the
links to messages in the channels:

After right-clicking a message in Slack, you can see the option to select the
link.

Slack links have the following format:

https://ORGANIZATION.slack.com/archives/ channel_id/pmessage_id

  
Organization: subdomain used in Slack  

Channel ID: It is the string that you'll need to enter in slack channels as
the channel id e.g C0000ABC02DE

The name of the channel is not needed. But it is recommended to set, it so you
can filter and find this information later on if needed. You can ignore
everything else when setting the table for `slack_channels`

### Examples of adding data to the channel's list:#

**Method 1:**

Using Supabase UI (easier):

The green arrow points to insert row button inside Supabase.

Then, enter the information as needed:

The picture shows the UI in Supabase to insert a new row to the database
table.

**Method 2:**

Go to [SQL Editor](https://supabase.com/dashboard/project/_/sql) and run
insert commands:

Inserting a public channel named #support-channel to be monitored:

`  

_10

insert into slack_channels

_10

(channel, channel_id, p_level, dest_channel, dest_channel_id, private)

_10

values

_10

('support-channel', 'C0000ABC02DE', 'Support msgs', 'all_them_messages',
'C0000ABC02DF', 0);

  
`

Inserting a **private** channel named #support-enterprise to be monitored:

`  

_11

insert into slack_channels

_11

(channel, channel_id, p_level, dest_channel, dest_channel_id, private)

_11

values

_11

(

_11

'support-enterprise',

_11

'C0000ABC02DC',

_11

'Enterprise Support msgs',

_11

'all_them_messages',

_11

'C0000ABC02DF',

_11

1

_11

);

  
`

Notes:

`p_level` is an optional message that will be included in with the message e.g
**VIP customer.**

`private` is an integer field that should be set to 1 if the channel has a
🔒padlock before the name (not a public channel).

`channel_id` is the source channel ID and `dest_channel_id` is the ID of the
channel where the bot will post the message.

## Setting up the environment File:#

You need to get the supabase URL and API keys from here:

<https://supabase.com/dashboard/project/_/settings/api>

The picture illustrates where to get the URL and the service key to setup the
environment variables.

Slack environment variables:

Then, copy the bot and person API Tokens for the bot:

The picture has arrows pointing to the tokens that will be used as environment
variables from Slack.

Now, you have everything needed to set up the environment file. Please note
that Slack ORG is the subdomain of your slack organization i.e supabase for
supabase.slack.com

The environment file:

`  

_10

SUPABASE_URL=https://XXXX.supabase.co

_10

SUPABASE_KEY=eyJhbGc_SUP4N4CH0_IkpXVCJ9.SUPAKEY_*

_10

SLACK_TOKEN=xoxp-Slack_PERSON_TOKEN

_10

SLACK_BOT_TOKEN=xoxb-Slack_BOT_TOKEN

_10

SLACK_ORG=slack_sub_domain

  
`

## Now, we can run the bot:#

It works in a similar fashion to Arduino / PIC processors of an infinity loop
looking for new data and performing tasks.

`  

_155

import time

_155

import logging

_155

from slack_sdk import WebClient

_155

from slack_sdk.errors import SlackApiError

_155

from supabase import create_client, Client

_155

from datetime import datetime

_155

from dotenv import dotenv_values

_155

logger = logging.getLogger(__name__)

_155

config = dotenv_values(".env")

_155

bot_client = WebClient(token=config['SLACK_BOT_TOKEN'])

_155

client = WebClient(token=config['SLACK_TOKEN'])

_155

SUPABASE_URL=config['SUPABASE_URL']

_155

SUPABASE_KEY=config['SUPABASE_KEY']

_155

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

_155

SLACK_ORG = config['SLACK_ORG']

_155

SLACK_ORG_LINK = f"https://{SLACK_ORG}.slack.com/archives/"

_155

############

_155

# Config:

_155

############

_155

# 1.4 seconds should be the minimum to avoid passing Slack API limits.

_155

# https://api.slack.com/docs/rate-limits#tier_t3

_155

POOLING_DELAY = 1.4

_155

# Check if new channels were added each hour.

_155

SCAN_CHANNELS_DELAY = 3600.0

_155

BUFFER_SIZE = 20

_155

_155

class SlackChannel:

_155

def __init__(self, id, name, p_level, dest_channel_id, dest_channel, private):

_155

"""_summary_

_155

_155

Args:

_155

id (str): Slack channel ID from the source channel

_155

name (str): Name of the source channel (used in logging)

_155

p_level (str): (Optional message) added when posting

_155

dest_channel_id (str): Slack channel ID for the destination channel

_155

dest_channel (str): Name of the destination channel (used in logging)

_155

private (int): Integer to check if the channel is private (private==1) or
public channel

_155

Returns:

_155

SlackChannel: object

_155

"""

_155

self.id = id

_155

self.name = name

_155

self.p_level = p_level

_155

self.dest_channel = dest_channel

_155

self.dest_channel_id = dest_channel_id

_155

self.private = private

_155

_155

def setup():

_155

"""_summary_

_155

Fetches the list of channels from Supabase and returns them in a dict()

_155

Returns:

_155

dict: Dictionary with SlackChannel objects.

_155

"""

_155

channels = dict()

_155

data = supabase.from_("slack_channels").select("channel_id, channel, p_level,
dest_channel, dest_channel_id, private").execute().data

_155

data_dic = data

_155

for row in data_dic:

_155

channels[row['channel_id']] = SlackChannel(id = row['channel_id'],

_155

name = row['channel'],

_155

p_level = row['p_level'],

_155

dest_channel = row['dest_channel'],

_155

dest_channel_id = row['dest_channel_id'],

_155

private = row['private'])

_155

return channels

_155

_155

def post(src_channel, link, message):

_155

"""_summary_

_155

Post a message from a source channel into the destination channel

_155

Args:

_155

src_channel (SlackChannel): SlackChannel object

_155

link (_type_): The link of the message in slack

_155

message (_type_): _description_

_155

_155

Returns:

_155

_type_: _description_

_155

"""

_155

try:

_155

aux_text = ""

_155

if src_channel.private != 1:

_155

aux_text = ("Message on <#"+src_channel.id+

_155

">. "+src_channel.p_level+" \n"+link)

_155

else:

_155

aux_text = ("Message on <#"+src_channel.id+

_155

">."+src_channel.p_level+" \n"+message+" \n"+link)

_155

result = bot_client.chat_postMessage(

_155

channel= src_channel.dest_channel_id,

_155

text=aux_text

_155

)

_155

logger.info(result)

_155

except SlackApiError as e:

_155

logger.error(f"Error posting message: {e}")

_155

_155

def ts_to_strtime(ts):

_155

"""_summary_

_155

Converts the UNIX time in timestamp to ISO format.

_155

Args:

_155

ts (int): TS datetime

_155

_155

Returns:

_155

str: ISO format datetime string for compatibility with Postgres.

_155

"""

_155

aux_ts = int(ts)

_155

return str(datetime.utcfromtimestamp(aux_ts).isoformat())

_155

_155

def loop_through_channels(channels):

_155

"""_summary_

_155

Loop through the channels and post messages on postgres if they aren't cached.

_155

Args:

_155

channels (dict): dict() with SlackChannel objects

_155

"""

_155

for channel_id in channels:

_155

channel = channels[channel_id]

_155

conversation_history = []

_155

try:

_155

result = client.conversations_history(channel=channel.id, limit = BUFFER_SIZE)

_155

conversation_history = result["messages"]

_155

logger.info("{} messages found in {}".format(len(conversation_history), id))

_155

except SlackApiError as e:

_155

logger.error("Error creating conversation: {}".format(e))

_155

for message in conversation_history:

_155

try:

_155

msg_dic = dict()

_155

msg_dic['channel_name'] = channel.name

_155

msg_dic['channel_id'] = channel.id

_155

aux_msg = "<@"+message['user']+"> wrote: \n"

_155

msg_dic['message'] = aux_msg + message['text']

_155

ts_aux = message['ts'].split(".")

_155

msg_dic['ts'] = ts_to_strtime(ts_aux[0])

_155

msg_dic['ts_ms'] = ts_aux[1]

_155

supabase.table("slack_watcher").insert(msg_dic).execute()

_155

auxint = ts_aux[0]+ts_aux[1]

_155

auxint = auxint.replace(".","")

_155

link = SLACK_ORG_LINK+channel.id+"/p"+auxint

_155

post(channel, link, msg_dic['message'])

_155

except Exception as e:

_155

pass

_155

time.sleep(POOLING_DELAY)

_155

_155

def main():

_155

"""_summary_

_155

Main loop to infinitely keep pooling data from channels and posting on Slack.

_155

It also checks for new channels every hour.

_155

"""

_155

channels = setup()

_155

start = time.time()

_155

while True:

_155

end = time.time()

_155

if ((end - start) > SCAN_CHANNELS_DELAY):

_155

start = time.time()

_155

channels = setup()

_155

else:

_155

loop_through_channels(channels)

_155

_155

if __name__ == '__main__':

_155

main()

  
`

Of course, we aren't doing a proper Python example if we don't make a test
notebook available:

[Open in
Colab](https://colab.research.google.com/github/mansueli/SlackConsolidate/blob/main/SlackConsolidate_bot.ipynb)

## Conclusion#

Using Supabase and Slack SDK, it is very easy to create a bot that
consolidates data according to the rules set. It just takes some steps to get
started with the Python SDK and you can even run a demo directly in [Google
Colab](https://colab.research.google.com/drive/1-sM23eQPE1Me4vl10KKoa9xzLYIgkgyQ?usp=sharing).

If you have any questions please reach out via
[Twitter](https://twitter.com/supabase) or join our
[Discord](https://discord.supabase.com/).

## More Python and Supabase resources#

  * [Python data loading with Supabase](https://supabase.com/blog/loading-data-supabase-python)
  * [Visualizing Supabase Data using Metabase](https://supabase.com/blog/visualizing-supabase-data-using-metabase)
  * [Supabase-py (Database) on Replit](https://replit.com/@Supabase/Supabase-py-Database?v=1)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fslack-
consolidate-slackbot-to-consolidate-
messages&text=Slack%20Consolidate%3A%20a%20slackbot%20built%20with%20Python%20and%20Supabase)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fslack-
consolidate-slackbot-to-consolidate-
messages&text=Slack%20Consolidate%3A%20a%20slackbot%20built%20with%20Python%20and%20Supabase)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fslack-
consolidate-slackbot-to-consolidate-
messages&t=Slack%20Consolidate%3A%20a%20slackbot%20built%20with%20Python%20and%20Supabase)

[Last postLaunch Week 5 Hackathon10 August 2022](/blog/launch-
week-5-hackathon)

[Next postSupabase Beta July 20223 August 2022](/blog/supabase-beta-update-
july-2022)

[slack](/blog/tags/slack)[python](/blog/tags/python)[api](/blog/tags/api)[automation](/blog/tags/automation)

On this page

  * Prerequisites
    * Creating the App in Slack
  * Granting access to the bot:
  * Creating Tables in Supabase
  * Adding channels to the watch list and setting the destination channel:
    * Examples of adding data to the channel's list:
  * Setting up the environment File:
  * Now, we can run the bot:
  * Conclusion
  * More Python and Supabase resources

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fslack-
consolidate-slackbot-to-consolidate-
messages&text=Slack%20Consolidate%3A%20a%20slackbot%20built%20with%20Python%20and%20Supabase)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fslack-
consolidate-slackbot-to-consolidate-
messages&text=Slack%20Consolidate%3A%20a%20slackbot%20built%20with%20Python%20and%20Supabase)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fslack-
consolidate-slackbot-to-consolidate-
messages&t=Slack%20Consolidate%3A%20a%20slackbot%20built%20with%20Python%20and%20Supabase)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

