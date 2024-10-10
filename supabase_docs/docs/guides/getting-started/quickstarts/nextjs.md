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
  4.   5. [Next.js](/docs/guides/getting-started/quickstarts/nextjs)
  6. 

# Use Supabase with Next.js

## Learn how to create a Supabase project, add some sample data, and query
from a Next.js app.

* * *

1

### Create a Supabase project

Go to [database.new](https://database.new) and create a new Supabase project.

When your project is up and running, go to the [Table
Editor](https://supabase.com/dashboard/project/_/editor), create a new table
and insert some data.

Alternatively, you can run the following snippet in your project's [SQL
Editor](https://supabase.com/dashboard/project/_/sql/new). This will create a
`notes` table with some sample data.

SQL_EDITOR

`  

_14

-- Create the table

_14

create table notes (

_14

id bigint primary key generated always as identity,

_14

title text not null

_14

);

_14

_14

-- Insert some sample data into the table

_14

insert into notes (title)

_14

values

_14

('Today I created a Supabase project.'),

_14

('I added some data and queried it from Next.js.'),

_14

('It was awesome!');

_14

_14

alter table notes enable row level security;

  
`

###

Make the data in your table publicly readable by adding an RLS policy:

SQL_EDITOR

`  

_10

create policy "public can read notes"

_10

on public.notes

_10

for select to anon

_10

using (true);

  
`

2

### Create a Next.js app

Use the `create-next-app` command and the `with-supabase` template, to create
a Next.js app pre-configured with:

  * [Cookie-based Auth](https://supabase.com/docs/guides/auth/auth-helpers/nextjs)
  * [TypeScript](https://www.typescriptlang.org/)
  * [Tailwind CSS](https://tailwindcss.com/)

Terminal

`  

_10

npx create-next-app -e with-supabase

  
`

3

### Declare Supabase Environment Variables

Rename `.env.example` to `.env.local` and populate with your Supabase
connection variables:

###### Project URL

Loading...

###### Anon key

Loading...

.env.local

`  

_10

NEXT_PUBLIC_SUPABASE_URL=<SUBSTITUTE_SUPABASE_URL>

_10

NEXT_PUBLIC_SUPABASE_ANON_KEY=<SUBSTITUTE_SUPABASE_ANON_KEY>

  
`

4

### Query Supabase data from Next.js

Create a new file at `app/notes/page.tsx` and populate with the following.

This will select all the rows from the `notes` table in Supabase and render
them on the page.

app/notes/page.tsx

utils/supabase/server.ts

`  

_10

import { createClient } from '@/utils/supabase/server';

_10

_10

export default async function Notes() {

_10

const supabase = createClient();

_10

const { data: notes } = await supabase.from("notes").select();

_10

_10

return <pre>{JSON.stringify(notes, null, 2)}</pre>

_10

}

  
`

5

### Start the app

Run the development server, go to <http://localhost:3000/notes> in a browser
and you should see the list of notes.

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
started/quickstarts/nextjs.mdx)

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

