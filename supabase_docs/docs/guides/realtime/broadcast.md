[![Supabase wordmark](/docs/_next/image?url=%2Fdocs%2Fsupabase-
dark.svg&w=256&q=75&dpl=dpl_BJ9ShNdrRifaAcUSP15Lr1pJVtdF)![Supabase
wordmark](/docs/_next/image?url=%2Fdocs%2Fsupabase-
light.svg&w=256&q=75&dpl=dpl_BJ9ShNdrRifaAcUSP15Lr1pJVtdF)DOCS](/docs)

  * [Start](/docs/guides/getting-started)
  * Products
  * Build
  * Manage
  * Reference
  * Resources

[![Supabase wordmark](/docs/_next/image?url=%2Fdocs%2Fsupabase-
dark.svg&w=256&q=75&dpl=dpl_BJ9ShNdrRifaAcUSP15Lr1pJVtdF)![Supabase
wordmark](/docs/_next/image?url=%2Fdocs%2Fsupabase-
light.svg&w=256&q=75&dpl=dpl_BJ9ShNdrRifaAcUSP15Lr1pJVtdF)DOCS](/docs)

Search docs...

K

Realtime

  1. [Realtime](/docs/guides/realtime)
  2.   3. Usage
  4.   5. [Broadcast](/docs/guides/realtime/broadcast)
  6. 

# Broadcast

## Send and receive messages using Realtime Broadcast

* * *

Let's explore how to implement Realtime Broadcast to send messages between
clients.

## Usage#

You can use the Supabase client libraries to send and receive Broadcast
messages.

### Initialize the client#

Go to your Supabase project's [API
Settings](https://supabase.com/dashboard/project/_/settings/api) and grab the
`URL` and `anon` public API key.

JavaScriptDartSwiftKotlinPython

`  

_10

import { createClient } from '@supabase/supabase-js'

_10

_10

const SUPABASE_URL = 'https://<project>.supabase.co'

_10

const SUPABASE_KEY = '<your-anon-key>'

_10

_10

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)

  
`

### Listening to broadcast messages#

You can provide a callback for the `broadcast` channel to receive message. In
this example we will receive any `broadcast` messages in `room-1`:

JavaScriptDartSwiftKotlinPython

`  

_16

// Join a room/topic. Can be anything except for 'realtime'.

_16

const channelA = supabase.channel('room-1')

_16

_16

// Simple function to log any messages we receive

_16

function messageReceived(payload) {

_16

console.log(payload)

_16

}

_16

_16

// Subscribe to the Channel

_16

channelA

_16

.on(

_16

'broadcast',

_16

{ event: 'test' },

_16

(payload) => messageReceived(payload)

_16

)

_16

.subscribe()

  
`

### Sending broadcast messages#

JavaScriptDartSwiftKotlinPython

We can send Broadcast messages using `channelB.send()`. Let's set up another
client to send messages.

`  

_16

// Join a room/topic. Can be anything except for 'realtime'.

_16

const channelB = supabase.channel('room-1')

_16

_16

channelB.subscribe((status) => {

_16

// Wait for successful connection

_16

if (status !== 'SUBSCRIBED') {

_16

return null

_16

}

_16

_16

// Send a message once the client is subscribed

_16

channelB.send({

_16

type: 'broadcast',

_16

event: 'test',

_16

payload: { message: 'hello, world' },

_16

})

_16

})

  
`

Before sending messages we need to ensure the client is connected, which we
have done within the `subscribe()` callback.

## Broadcast options#

You can pass configuration options while initializing the Supabase Client.

### Self-send messages#

JavaScriptDartSwiftKotlinPython

By default, broadcast messages are only sent to other clients. You can
broadcast messages back to the sender by setting Broadcast's `self` parameter
to `true`.

`  

_20

const myChannel = supabase.channel('room-2', {

_20

config: {

_20

broadcast: { self: true },

_20

},

_20

})

_20

_20

myChannel.on(

_20

'broadcast',

_20

{ event: 'test-my-messages' },

_20

(payload) => console.log(payload)

_20

)

_20

_20

myChannel.subscribe((status) => {

_20

if (status !== 'SUBSCRIBED') { return }

_20

channelC.send({

_20

type: 'broadcast',

_20

event: 'test-my-messages',

_20

payload: { message: 'talking to myself' },

_20

})

_20

})

  
`

### Acknowledge messages#

JavaScriptDartSwiftKotlinPython

You can confirm that Realtime received your message by setting Broadcast's
`ack` config to `true`.

`  

_17

const myChannel = supabase.channel('room-3', {

_17

config: {

_17

broadcast: { ack: true },

_17

},

_17

})

_17

_17

myChannel.subscribe(async (status) => {

_17

if (status !== 'SUBSCRIBED') { return }

_17

_17

const serverResponse = await myChannel.send({

_17

type: 'broadcast',

_17

event: 'acknowledge',

_17

payload: {},

_17

})

_17

_17

console.log('serverResponse', serverResponse)

_17

})

  
`

Use this to guarantee that the server has received the message before
resolving `channelD.send`'s promise. If the `ack` config is not set to `true`
when creating the channel, the promise returned by `channelD.send` will
resolve immediately.

### Send messages using REST calls#

You can also send a Broadcast message by making an HTTP request to Realtime
servers. This is useful when you want to send messages from your server or
client without having to first establish a WebSocket connection.

JavaScriptDartSwiftKotlinPython

This is currently available only in the Supabase JavaScript client version
2.37.0 and later.

`  

_15

const channel = supabase.channel('test-channel')

_15

_15

// No need to subscribe to channel

_15

_15

channel

_15

.send({

_15

type: 'broadcast',

_15

event: 'test',

_15

payload: { message: 'Hi' },

_15

})

_15

.then((resp) => console.log(resp))

_15

_15

// Remember to clean up the channel

_15

_15

supabase.removeChannel(channel)

  
`

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/realtime/broadcast.mdx)

  * Need some help?

[Contact support](https://supabase.com/support)

  * Latest product updates?

[See Changelog](https://supabase.com/changelog)

  * Something's not right?

[Check system status](https://status.supabase.com/)

* * *

[© Supabase
Inc](https://supabase.com/)—[Contributing](https://github.com/supabase/supabase/blob/master/apps/docs/DEVELOPERS.md)[Author
Styleguide](https://github.com/supabase/supabase/blob/master/apps/docs/CONTRIBUTING.md)[Open
Source](https://supabase.com/open-
source)[SupaSquad](https://supabase.com/supasquad)Privacy Settings

[GitHub](https://github.com/supabase/supabase)[Twitter](https://twitter.com/supabase)[Discord](https://discord.supabase.com/)

