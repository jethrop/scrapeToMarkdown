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
  4.   5. [refine](/docs/guides/getting-started/quickstarts/refine)
  6. 

# Use Supabase with refine

## Learn how to create a Supabase project, add some sample data to your
database, and query the data from a refine app.

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

### Create a refine app

Create a [refine](https://github.com/refinedev/refine) app using the [create
refine-app](https://refine.dev/docs/getting-started/quickstart/).

The `refine-supabase` preset adds `@refinedev/supabase` supplementary package
that supports Supabase in a refine app. `@refinedev/supabase` out-of-the-box
includes the Supabase dependency: [supabase-
js](https://github.com/supabase/supabase-js).

Terminal

`  

_10

npm create refine-app@latest -- --preset refine-supabase my-app

  
`

3

### Open your refine app in VS Code

You will develop your app, connect to the Supabase backend and run the refine
app in VS Code.

Terminal

`  

_10

cd my-app

_10

code .

  
`

4

### Start the app

Start the app, go to <http://localhost:5173> in a browser, and you should be
greeted with the refine Welcome page.

Terminal

`  

_10

npm run dev

  
`

![refine welcome page](/docs/img/refine-qs-welcome-page.png)

5

### Update `supabaseClient`

You now have to update the `supabaseClient` with the `SUPABASE_URL` and
`SUPABASE_KEY` of your Supabase API. The `supabaseClient` is used in auth
provider and data provider methods that allow the refine app to connect to
your Supabase backend.

###### Project URL

Loading...

###### Anon key

Loading...

src/utility/supabaseClient.ts

`  

_13

import { createClient } from "@refinedev/supabase";

_13

_13

const SUPABASE_URL = YOUR_SUPABASE_URL;

_13

const SUPABASE_KEY = YOUR_SUPABASE_KEY

_13

_13

export const supabaseClient = createClient(SUPABASE_URL, SUPABASE_KEY, {

_13

db: {

_13

schema: "public",

_13

},

_13

auth: {

_13

persistSession: true,

_13

},

_13

});

  
`

6

### Add countries resource and pages

You have to then configure resources and define pages for `countries`
resource.

Use the following command to automatically add resources and generate code for
pages for `countries` using refine Inferencer.

This defines pages for `list`, `create`, `show` and `edit` actions inside the
`src/pages/countries/` directory with `<HeadlessInferencer />` component.

The `<HeadlessInferencer />` component depends on `@refinedev/react-table` and
`@refinedev/react-hook-form` packages. In order to avoid errors, you should
install them as dependencies with `npm install @refinedev/react-table
@refinedev/react-hook-form`.

The `<HeadlessInferencer />` is a refine Inferencer component that
automatically generates necessary code for the `list`, `create`, `show` and
`edit` pages.

More on [how the Inferencer works is available in the docs
here](https://refine.dev/docs/packages/documentation/inferencer/).

Terminal

`  

_10

npm run refine create-resource countries

  
`

7

### Add routes for countries pages

Add routes for the `list`, `create`, `show`, and `edit` pages.

You should remove the `index` route for the Welcome page presented with the
`<Welcome />` component.

src/App.tsx

`  

_56

import { Refine, WelcomePage } from "@refinedev/core";

_56

import { RefineKbar, RefineKbarProvider } from "@refinedev/kbar";

_56

import routerBindings, {

_56

DocumentTitleHandler,

_56

NavigateToResource,

_56

UnsavedChangesNotifier,

_56

} from "@refinedev/react-router-v6";

_56

import { dataProvider, liveProvider } from "@refinedev/supabase";

_56

import { BrowserRouter, Route, Routes } from "react-router-dom";

_56

_56

import "./App.css";

_56

import authProvider from "./authProvider";

_56

import { supabaseClient } from "./utility";

_56

import { CountriesCreate, CountriesEdit, CountriesList, CountriesShow } from
"./pages/countries";

_56

_56

function App() {

_56

return (

_56

<BrowserRouter>

_56

<RefineKbarProvider>

_56

<Refine

_56

dataProvider={dataProvider(supabaseClient)}

_56

liveProvider={liveProvider(supabaseClient)}

_56

authProvider={authProvider}

_56

routerProvider={routerBindings}

_56

options={{

_56

syncWithLocation: true,

_56

warnWhenUnsavedChanges: true,

_56

}}

_56

resources={[{

_56

name: "countries",

_56

list: "/countries",

_56

create: "/countries/create",

_56

edit: "/countries/edit/:id",

_56

show: "/countries/show/:id"

_56

}]}>

_56

<Routes>

_56

<Route index

_56

element={<NavigateToResource resource="countries" />}

_56

/>

_56

<Route path="/countries">

_56

<Route index element={<CountriesList />} />

_56

<Route path="create" element={<CountriesCreate />} />

_56

<Route path="edit/:id" element={<CountriesEdit />} />

_56

<Route path="show/:id" element={<CountriesShow />} />

_56

</Route>

_56

</Routes>

_56

<RefineKbar />

_56

<UnsavedChangesNotifier />

_56

<DocumentTitleHandler />

_56

</Refine>

_56

</RefineKbarProvider>

_56

</BrowserRouter>

_56

);

_56

}

_56

_56

export default App;

  
`

8

### View countries pages

Now you should be able to see the countries pages along the `/countries`
routes. You may now edit and add new countries using the Inferencer generated
UI.

The Inferencer auto-generated code gives you a good starting point on which to
keep building your `list`, `create`, `show` and `edit` pages. They can be
obtained by clicking the `Show the auto-generated code` buttons in their
respective pages.

![refine List Page](/docs/img/refine-qs-countries-ui.png)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/quickstarts/refine.mdx)

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

