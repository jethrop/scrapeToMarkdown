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
  4.   5. [Android Kotlin](/docs/guides/getting-started/quickstarts/kotlin)
  6. 

# Use Supabase with Android Kotlin

## Learn how to create a Supabase project, add some sample data to your
database, and query the data from an Android Kotlin app.

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

### Create an Android app with Android Studio

Open Android Studio > New > New Android Project.

3

### Install the Dependencies

Open `build.gradle.kts` (app) file and add the serialization plug, Ktor
client, and Supabase client.

Replace the version placeholders `$kotlin_version` with the Kotlin version of
the project, and `$supabase_version` and `$ktor_version` with the respective
latest versions.

The latest supabase-kt version can be found
[here](https://github.com/supabase-community/supabase-kt/releases) and Ktor
version can be found [here](https://ktor.io/docs/welcome.html).

`  

_11

plugins {

_11

...

_11

kotlin("plugin.serialization") version "$kotlin_version"

_11

}

_11

...

_11

dependencies {

_11

...

_11

implementation(platform("io.github.jan-
tennert.supabase:bom:$supabase_version"))

_11

implementation("io.github.jan-tennert.supabase:postgrest-kt")

_11

implementation("io.ktor:ktor-client-android:$ktor_version")

_11

}

  
`

4

### Add internet access permission

Add the following line to the `AndroidManifest.xml` file under the `manifest`
tag and outside the `application` tag.

`  

_10

...

_10

<uses-permission android:name="android.permission.INTERNET" />

_10

...

  
`

5

### Initialize the Supabase client

You can create a Supabase client whenever you need to perform an API call.

For the sake of simplicity, we will create a client in the `MainActivity.kt`
file at the top just below the imports.

Replace the `supabaseUrl` and `supabaseKey` with your own:

###### Project URL

Loading...

###### Anon key

Loading...

`  

_10

import ...

_10

_10

val supabase = createSupabaseClient(

_10

supabaseUrl = "https://xyzcompany.supabase.co",

_10

supabaseKey = "your_public_anon_key"

_10

) {

_10

install(Postgrest)

_10

}

_10

...

  
`

6

### Create a data model for countries

Create a serializable data class to represent the data from the database.

Add the following below the `createSupabaseClient` function in the
`MainActivity.kt` file.

`  

_10

@Serializable

_10

data class Country(

_10

val id: Int,

_10

val name: String,

_10

)

  
`

7

### Query data from the app

Use `LaunchedEffect` to fetch data from the database and display it in a
`LazyColumn`.

Replace the default `MainActivity` class with the following code.

Note that we are making a network request from our UI code. In production, you
should probably use a `ViewModel` to separate the UI and data fetching logic.

`  

_38

class MainActivity : ComponentActivity() {

_38

override fun onCreate(savedInstanceState: Bundle?) {

_38

super.onCreate(savedInstanceState)

_38

setContent {

_38

SupabaseTutorialTheme {

_38

// A surface container using the 'background' color from the theme

_38

Surface(

_38

modifier = Modifier.fillMaxSize(),

_38

color = MaterialTheme.colorScheme.background

_38

) {

_38

CountriesList()

_38

}

_38

}

_38

}

_38

}

_38

}

_38

_38

@Composable

_38

fun CountriesList() {

_38

var countries by remember { mutableStateOf<List<Country>>(listOf()) }

_38

LaunchedEffect(Unit) {

_38

withContext(Dispatchers.IO) {

_38

countries = supabase.from("countries")

_38

.select().decodeList<Country>()

_38

}

_38

}

_38

LazyColumn {

_38

items(

_38

countries,

_38

key = { country -> country.id },

_38

) { country ->

_38

Text(

_38

country.name,

_38

modifier = Modifier.padding(8.dp),

_38

)

_38

}

_38

}

_38

}

  
`

8

### Start the app

Run the app on an emulator or a physical device by clicking the `Run app`
button in Android Studio.

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/quickstarts/kotlin.mdx)

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

