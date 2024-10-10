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
  4.   5. [SolidJS](/docs/guides/getting-started/quickstarts/solidjs)
  6. 

# Use Supabase with SolidJS

## Learn how to create a Supabase project, add some sample data to your
database, and query the data from a SolidJS app.

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

### Create a SolidJS app

Create a SolidJS app using the `degit` command.

Terminal

`  

_10

npx degit solidjs/templates/js my-app

  
`

3

### Install the Supabase client library

The fastest way to get started is to use the `supabase-js` client library
which provides a convenient interface for working with Supabase from a SolidJS
app.

Navigate to the SolidJS app and install `supabase-js`.

Terminal

`  

_10

cd my-app && npm install @supabase/supabase-js

  
`

4

### Query data from the app

In `App.jsx`, create a Supabase client using your project URL and public API
(anon) key:

###### Project URL

Loading...

###### Anon key

Loading...

Add a `getCountries` function to fetch the data and display the query result
to the page.

src/App.jsx

`  

_21

import { createClient } from "@supabase/supabase-js";

_21

import { createResource, For } from "solid-js";

_21

_21

const supabase = createClient('https://<project>.supabase.co', '<your-anon-
key>');

_21

_21

async function getCountries() {

_21

const { data } = await supabase.from("countries").select();

_21

return data;

_21

}

_21

_21

function App() {

_21

const [countries] = createResource(getCountries);

_21

_21

return (

_21

<ul>

_21

<For each={countries()}>{(country) => <li>{country.name}</li>}</For>

_21

</ul>

_21

);

_21

}

_21

_21

export default App;

  
`

5

### Start the app

Start the app and go to <http://localhost:3000> in a browser and you should
see the list of countries.

Terminal

`  

_10

npm run dev

  
`

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/quickstarts/solidjs.mdx)

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

