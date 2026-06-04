import pandas as pd
import telethon
import regex as re
import numpy as np
import telethon
from tabulate import tabulate
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChat

# Replace YOUR_API_ID and YOUR_API_HASH with the values you obtained when creating a new app on the telegram website
api_id = 26312279
api_hash = '3dbc063649f5de59b912452d058e1c08'

# Create a new client using the API ID and API Hash
client = TelegramClient('NonStop', api_id, api_hash)

# Start the client and use the phone_number and password you used to register your telegram account
client.start()

# Join the channel by its username (without the "@" symbol)
channel_username = 'nonstopdeals'
channel_entity = client.get_entity(channel_username)

my_offers = pd.DataFrame(columns = ['offer_timestamp', 'offer'])
with client:
    for msg in client.iter_messages(channel_entity, 10):
        offer = msg.text
        offer_list = re.split('\n', offer)
        offer_timestamp = msg.date
        data = {'offer_timestamp':offer_timestamp, 'offer': offer_list}
        my_offers1 = my_offers.append(data, ignore_index = True)
        my_offers = my_offers1.copy()

# expliting the links from offer column
my_offers_new = my_offers.offer.apply(pd.Series).merge(my_offers, right_index = True, left_index = True)

# cleaning the data
my_offers_new = my_offers_new.replace('', np.nan)
my_offers_new = my_offers_new.dropna(axis=1, how='all')
my_offers_new['offer_timestamp'] = my_offers_new['offer_timestamp'].astype(str)

#subset_df = my_offers_new.loc[:, my_offers_new.isnull().all()]
#print(my_offers_new[1].isnull().values.all())
#print(pd.isna(my_offers_new[1][0]))


print(my_offers_new.head())
my_offers_new.to_excel('my_teledata.xlsx')
#print(tabulate(my_offers_new.head(), headers='keys', tablefmt='psql'))


# Stop the client
client.disconnect()