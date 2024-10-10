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

Getting Started

  1. [Start with Supabase](/docs/guides/getting-started)
  2.   3. Framework Quickstarts
  4.   5. [SvelteKit](/docs/guides/getting-started/quickstarts/sveltekit)
  6. 

# Use Supabase with SvelteKit

## Learn how to create a Supabase project, add some sample data to your
database, and query the data from a SvelteKit app.

* * *

1

### Create a Supabase project

Go to [database.new](https://database.new) and create a new Supabase project.

When your project is up and running, go to the [Table
Editor](https://supabase.com/dashboard/project/_/editor), create a new table
and insert some data.

Alternatively, you can run the following snippet in your project's [SQL
Editor](https://supabase.com/dashboard/project/_/sql/new). This will create a
`countries` table with some sample data.

SQL_EDITOR

`  

_13

-- Create the table

_13

create table countries (

_13

id bigint primary key generated always as identity,

_13

name text not null

_13

);

_13

-- Insert some sample data into the table

_13

insert into countries (name)

_13

values

_13

('Canada'),

_13

('United States'),

_13

('Mexico');

_13

_13

alter table countries enable row level security;

  
`

###

Make the data in your table publicly readable by adding an RLS policy:

SQL_EDITOR

`  

_10

create policy "public can read countries"

_10

on public.countries

_10

for select to anon

_10

using (true);

  
`

2

### Create a SvelteKit app

Create a SvelteKit app using the `npm create` command.

Terminal

`  

_10

npm create svelte@latest myapp

  
`

3

### Install the Supabase client library

The fastest way to get started is to use the `supabase-js` client library
which provides a convenient interface for working with Supabase from a
SvelteKit app.

Navigate to the SvelteKit app and install `supabase-js`.

Terminal

`  

_10

cd myapp && npm install @supabase/supabase-js

  
`

4

### Create the Supabase client

Create a `/src/lib` directory in your SvelteKit app, create a file called
`supabaseClient.js` and add the following code to initialize the Supabase
client with your project URL and public API (anon) key:

###### Project URL

Loading...

###### Anon key

Loading...

src/lib/supabaseClient.js

`  

_10

import { createClient } from '@supabase/supabase-js'

_10

_10

export const supabase = createClient('https://<project>.supabase.co', '<your-
anon-key>')

  
`

5

### Query data from the app

Use `load` method to fetch the data server-side and display the query results
as a simple list.

Create `+page.server.js` file in the `routes` directory with the following
code.

src/routes/+page.server.js

`  

_10

import { supabase } from "$lib/supabaseClient";

_10

_10

export async function load() {

_10

const { data } = await supabase.from("countries").select();

_10

return {

_10

countries: data ?? [],

_10

};

_10

}

  
`

###

Replace the existing content in your `+page.svelte` file in the `routes`
directory with the following code.

src/routes/+page.svelte

`  

_10

<script>

_10

export let data;

_10

</script>

_10

_10

<ul>

_10

{#each data.countries as country}

_10

<li>{country.name}</li>

_10

{/each}

_10

</ul>

  
`

6

### Start the app

Start the app and go to <http://localhost:5173> in a browser and you should
see the list of countries.

Terminal

`  

_10

npm run dev

  
`

## Next steps#

  * Set up [Auth](/docs/guides/auth) for your app
  * [Insert more data](/docs/guides/database/import-data) into your database
  * Upload and serve static files using [Storage](/docs/guides/storage)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/quickstarts/sveltekit.mdx)

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

