[Back](/blog)

[Blog](/blog)

# Local-first Realtime Apps with Expo and Legend-State

23 Sep 2024

•

11 minute read

[![Jay Meistrich
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fjmeistrich.png&w=96&q=75)Jay
MeistrichGuest Author](https://x.com/jmeistrich)

[![Thor Schaeff
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fthorwebdev.png&w=96&q=75)Thor
SchaeffDevRel & DX](https://twitter.com/thorwebdev)

![Local-first Realtime Apps with Expo and Legend-
State](/_next/image?url=%2Fimages%2Fblog%2Flocal-first-expo-
legend_state%2Flocal-first-expo-legend_state-thumb.png&w=3840&q=100)

[Do you prefer audio-visual learning? Watch the video
guide!](https://supabase.link/local-first-expo-legend-state-yt)

[Or jump straight into the
code](https://github.com/expo/examples/tree/master/with-legend-state-supabase)

Or run `npx create-expo-app --example with-legend-state-supabase` to create a
new app with this example.

[Legend-State](https://legendapp.com/open-source/state/v3/) is a super fast
all-in-one state and sync library that lets you write less code to make faster
apps. Legend-State has four primary goals:

  1. As easy as possible to use.
  2. The fastest React state library.
  3. Fine-grained reactivity for minimal renders.
  4. Powerful sync and persistence (with Supabase support built in!)

And, to put the cherry on top, it works with Expo and React Native (via [React
Native Async Storage](https://github.com/react-native-async-storage/async-
storage?tab=readme-ov-file#react-native-async-storage)). This makes it a
perfect match for building local-first mobile and web apps.

## What is a Local-First Architecture?#

In local-first software, "the availability of another computer should never
prevent you from working" ([via Martin
Kleppmann](https://www.youtube.com/watch?v=NMq0vncHJvU)). When you are
offline, you can still read and write directly from/to a database on your
device. You can trust the software to work offline, and you know that when you
are connected to the internet, your data will be seamlessly synced and
available on any of your devices running the app. When you're online, this
architecture is well suited for "multiplayer" apps, as [popularized by
Figma](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/).

To dig deeper into what local-first is and how it works, refer to the [Expo
docs](https://docs.expo.dev/guides/local-first/).

## How Legend-State makes it work#

A primary goal of Legend-State is to make automatic persisting and syncing
both easy and very robust, as it's meant to be used to power all storage and
sync of complex apps.

Any changes made while offline are persisted between sessions to be retried
whenever connected. To do this, the sync system subscribes to changes on an
observable, then on change goes through a multi-step flow to ensure that
changes are persisted and synced.

  1. Save the pending changes to local persistence.
  2. Save the changes to local persistence.
  3. Save the changes to remote persistence.
  4. On remote save, set any needed changes (like updated_at) back into the observable and local persistence.
  5. Clear the pending changes in local persistence.

## Setting up the Project#

To set up a new React Native project you can use the `create-expo-app`
utility. You can create a blank app or choose from different
[examples](https://github.com/expo/examples).

For this tutorial, go ahead and create a new blank Expo app:

`  

_10

npx create-expo-app@latest --template blank

  
`

## Installing Dependencies#

The main dependencies you need are [Legend
State](https://www.npmjs.com/package/@legendapp/state) and [supabase-
js](https://www.npmjs.com/package/@supabase/supabase-js). Additionally, to
make things work for React Native, you will need [React Native Async
Storage](https://github.com/react-native-async-storage/async-
storage?tab=readme-ov-file#react-native-async-storage) and [react-native-get-
random-values](https://www.npmjs.com/package/react-native-get-random-values)
(to generate uuids).

Install the required dependencies via `expo install`:

`  

_10

npx expo install @legendapp/state@beta @supabase/supabase-js react-native-get-
random-values @react-native-async-storage/async-storage

  
`

## Configuring Supabase#

If you don't have a Supabase project already, head over to
[database.new](https://database.new) and create a new project.

Next, create a `.env.local` file in the root of your project and add the
following env vars. You can find these in your [Supabase
dashboard](https://supabase.com/dashboard/project/_/settings/api).

`  

_10

EXPO_PUBLIC_SUPABASE_URL=

_10

EXPO_PUBLIC_SUPABASE_ANON_KEY=

  
`

Next, set up a utils file to hold all the logic for interacting with Supabase,
we'll call it `utils/SupaLegend.ts`.

utils/SupaLegend.ts

`  

_10

import { createClient } from '@supabase/supabase-js'

_10

_10

const supabase = createClient(

_10

process.env.EXPO_PUBLIC_SUPABASE_URL,

_10

process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY

_10

)

  
`

## Configuring Legend-State#

Legend-State is very versatile and allows you to choose different persistence
and storage strategies. For this example, we'll use `React Native Async
Storage` for local persistence across platforms and `supabase` for remote
persistence.

Extend your `utils/SupaLegend.ts` file with the following configuration:

utils/SupaLegend.ts

`  

_46

import { createClient } from '@supabase/supabase-js'

_46

import { observable } from '@legendapp/state'

_46

import { syncedSupabase } from '@legendapp/state/sync-plugins/supabase'

_46

import { configureSynced } from '@legendapp/state/sync'

_46

import { observablePersistAsyncStorage } from '@legendapp/state/persist-
plugins/async-storage'

_46

import AsyncStorage from '@react-native-async-storage/async-storage'

_46

_46

const supabase = createClient(

_46

process.env.EXPO_PUBLIC_SUPABASE_URL,

_46

process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY

_46

)

_46

_46

// Create a configured sync function

_46

const customSynced = configureSynced(syncedSupabase, {

_46

// Use React Native Async Storage

_46

persist: {

_46

plugin: observablePersistAsyncStorage({

_46

AsyncStorage,

_46

}),

_46

},

_46

generateId,

_46

supabase,

_46

changesSince: 'last-sync',

_46

fieldCreatedAt: 'created_at',

_46

fieldUpdatedAt: 'updated_at',

_46

// Optionally enable soft deletes

_46

fieldDeleted: 'deleted',

_46

})

_46

_46

export const todos$ = observable(

_46

customSynced({

_46

supabase,

_46

collection: 'todos',

_46

select: (from) =>
from.select('id,counter,text,done,created_at,updated_at,deleted'),

_46

actions: ['read', 'create', 'update', 'delete'],

_46

realtime: true,

_46

// Persist data and pending changes locally

_46

persist: {

_46

name: 'todos',

_46

retrySync: true, // Persist pending changes and retry

_46

},

_46

retry: {

_46

infinite: true, // Retry changes with exponential backoff

_46

},

_46

})

_46

)

  
`

`syncedSupabase` is the Legend-State sync plugin for Supabase and adds some
default configuration for usage with supabase-js.

## Setting up the Database Schema#

If you haven't alread, install the [Supabase CLI](/docs/guides/cli/getting-
started) and run `supabase init` to initialize your project.

Next, create the initial database migration to set up the `todos` table:

`  

_10

supabase migrations new init

  
`

This will create a new SQL migration file in the `supabase/migrations`
directory. Open it and add the following SQL code:

`  

_34

create table todos (

_34

id uuid default gen_random_uuid() primary key,

_34

counter bigint generated by default as identity,

_34

text text,

_34

done boolean default false,

_34

created_at timestamptz default now(),

_34

updated_at timestamptz default now(),

_34

deleted boolean default false -- needed for soft deletes

_34

);

_34

_34

-- Enable realtime

_34

alter

_34

publication supabase_realtime add table todos;

_34

_34

-- Legend-State helper to facilitate "Sync only diffs" (changesSince: 'last-
sync') mode

_34

CREATE OR REPLACE FUNCTION handle_times()

_34

RETURNS trigger AS

_34

$$

_34

BEGIN

_34

IF (TG_OP = 'INSERT') THEN

_34

NEW.created_at := now();

_34

NEW.updated_at := now();

_34

ELSEIF (TG_OP = 'UPDATE') THEN

_34

NEW.created_at = OLD.created_at;

_34

NEW.updated_at = now();

_34

END IF;

_34

RETURN NEW;

_34

END;

_34

$$ language plpgsql;

_34

_34

CREATE TRIGGER handle_times

_34

BEFORE INSERT OR UPDATE ON todos

_34

FOR EACH ROW

_34

EXECUTE PROCEDURE handle_times();

  
`

The `created_at`, `updated_at`, and `deleted` columns are used by Legend-State
to track changes and sync efficiently. The `handle_times` function is used to
automatically set the `created_at` and `updated_at` columns when a new row is
inserted or an existing row is updated. This allows to efficiently sync only
the changes since the last sync.

Next, run `supabase link` to link your local project to your Supabase project
and run `supabase db push` to apply the init migration to your Supabase
database.

## Generating TypeScript Types#

Legend-State integrates with supabase-js to provide end-to-end type safety.
This means you can use the existing [Supabase CLI
workflow](/docs/guides/api/rest/generating-types) to generate TypeScript types
for your Supabase tables.

`  

_10

supabase start

_10

supabase gen types --lang=typescript --local > utils/database.types.ts

  
`

Next, in your `utils/SupaLegend.ts` file, import the generated types inject
them into the Supabase client.

utils/SupaLegend.ts

`  

_10

import { createClient } from '@supabase/supabase-js'

_10

import { Database } from './database.types'

_10

// [...]

_10

_10

const supabase = createClient<Database>(

_10

process.env.EXPO_PUBLIC_SUPABASE_URL,

_10

process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY

_10

)

_10

_10

// [...]

  
`

From here, Legend-State will automatically infer the types for your Supabase
tables and make them available within the observable.

## Fetching Data and subscribing to realtime updates#

Above, you've configured the `todos$` observable. You can now import this in
your `tsx` files to fetch and automatically sync changes.

App.tsx

`  

_12

import { observer } from '@legendapp/state/react'

_12

import { todos$ as _todos$ } from './utils/SupaLegend'

_12

_12

const Todos = observer(({ todos$ }: { todos$: typeof _todos$ }) => {

_12

// Get the todos from the state and subscribe to updates

_12

const todos = todos$.get()

_12

const renderItem = ({ item: todo }: { item: Tables<'todos'> }) => <Todo
todo={todo} />

_12

if (todos)

_12

return <FlatList data={Object.values(todos)} renderItem={renderItem}
style={styles.todos} />

_12

_12

return <></>

_12

})

  
`

`observer` is the suggested way of consuming observables for the best
performance and safety.

It turns the entire component into an observing context - it automatically
tracks observables for changes when `get()` is called, even from within hooks
or helper functions.

This means, as long as realtime is enabled on the respective table, the
component will automatically update when changes are made to the data!

Also, thanks to the persist and retry settings above, Legend-State will
automatically retry to sync changes if the connection is lost.

## Inserting, and updating data#

To add a new todo from the application, you will need to generate a uuid
locally to insert it into our todos observable. You can use the `uuid` package
to generate a uuid. For this to work in React Native you will also need the
`react-native-get-random-values` polyfill.

In your `SupaLegend.ts` file add the following:

utils/SupaLegend.ts

`  

_20

// [...]

_20

import 'react-native-get-random-values'

_20

import { v4 as uuidv4 } from 'uuid'

_20

// [...]

_20

_20

// Provide a function to generate ids locally

_20

const generateId = () => uuidv4()

_20

_20

export function addTodo(text: string) {

_20

const id = generateId()

_20

// Add keyed by id to the todos$ observable to trigger a create in Supabase

_20

todos$[id].assign({

_20

id,

_20

text,

_20

})

_20

}

_20

_20

export function toggleDone(id: string) {

_20

todos$[id].done.set((prev) => !prev)

_20

}

  
`

Now, in your `App.tsx` file, you can import the `addTodo` and `toggleDone`
methods and call them when the user submits a new todo or checks off one:

App.tsx

`  

_46

import { useState } from 'react'

_46

import { FlatList, StyleSheet, Text, TextInput, TouchableOpacity } from
'react-native'

_46

// [...]

_46

import { observer } from '@legendapp/state/react'

_46

import { addTodo, todos$ as _todos$, toggleDone } from './utils/SupaLegend'

_46

// [...]

_46

_46

// Emojis to decorate each todo.

_46

const NOT_DONE_ICON = String.fromCodePoint(0x1f7e0)

_46

const DONE_ICON = String.fromCodePoint(0x2705)

_46

_46

// The text input component to add a new todo.

_46

const NewTodo = () => {

_46

const [text, setText] = useState('')

_46

const handleSubmitEditing = ({ nativeEvent: { text } }) => {

_46

setText('')

_46

addTodo(text)

_46

}

_46

return (

_46

<TextInput

_46

value={text}

_46

onChangeText={(text) => setText(text)}

_46

onSubmitEditing={handleSubmitEditing}

_46

placeholder="What do you want to do today?"

_46

style={styles.input}

_46

/>

_46

)

_46

}

_46

_46

// A single todo component, either 'not done' or 'done': press to toggle.

_46

const Todo = ({ todo }: { todo: Tables<'todos'> }) => {

_46

const handlePress = () => {

_46

toggleDone(todo.id)

_46

}

_46

return (

_46

<TouchableOpacity

_46

key={todo.id}

_46

onPress={handlePress}

_46

style={[styles.todo, todo.done ? styles.done : null]}

_46

>

_46

<Text style={styles.todoText}>

_46

{todo.done ? DONE_ICON : NOT_DONE_ICON} {todo.text}

_46

</Text>

_46

</TouchableOpacity>

_46

)

_46

}

  
`

## Up next: Adding Auth#

Since Legend-State utilizes supabase-js under the hood, you can use [Supabase
Auth](/docs/guides/auth) and [row level
security](/docs/guides/database/postgres/row-level-security) to restrict
access to the data.

For a tutorial on how to add user management to your Expo React Native
application, refer to [this guide](/docs/guides/getting-
started/tutorials/with-expo-react-native).

## Conclusion#

Legend-State and Supabase are a powerful combination for building local-first
applications. Legend-State pairs nicely with supabase-js, Supabase Auth and
Supabase Realtime, allowing you to tap into the full power of the Supabase
Stack while building fast and delightful applications that work across web and
mobile platforms.

Want to learn more about Legend-State? Refer to their
[docs](https://legendapp.com/open-source/state/v3/) and make sure to follow
Jay Meistrich on [Twitter](https://twitter.com/jmeistrich)!

## More Supabase Resources#

  * [Expo User Management Tutorial](/docs/guides/getting-started/tutorials/with-expo-react-native)
  * [React Native Auth](/blog/react-native-authentication)
  * [React Native File Upload](/blog/react-native-storage)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Flocal-
first-expo-legend-state&text=Local-
first%20Realtime%20Apps%20with%20Expo%20and%20Legend-
State)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Flocal-
first-expo-legend-state&text=Local-
first%20Realtime%20Apps%20with%20Expo%20and%20Legend-
State)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Flocal-
first-expo-legend-state&t=Local-
first%20Realtime%20Apps%20with%20Expo%20and%20Legend-State)

[Last postSupabase Launch Week 12 Hackathon30 September
2024](/blog/lw12-hackathon-winners)

[Next postEdge Functions are now 2x smaller and boot 3x faster12 September
2024](/blog/edge-functions-faster-smaller)

[mobile](/blog/tags/mobile)[local-first](/blog/tags/local-first)[react-
native](/blog/tags/react-native)

On this page

  * What is a Local-First Architecture?
  * How Legend-State makes it work
  * Setting up the Project
  * Installing Dependencies
  * Configuring Supabase
  * Configuring Legend-State
  * Setting up the Database Schema
  * Generating TypeScript Types
  * Fetching Data and subscribing to realtime updates
  * Inserting, and updating data
  * Up next: Adding Auth
  * Conclusion
  * More Supabase Resources

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Flocal-
first-expo-legend-state&text=Local-
first%20Realtime%20Apps%20with%20Expo%20and%20Legend-
State)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Flocal-
first-expo-legend-state&text=Local-
first%20Realtime%20Apps%20with%20Expo%20and%20Legend-
State)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Flocal-
first-expo-legend-state&t=Local-
first%20Realtime%20Apps%20with%20Expo%20and%20Legend-State)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

