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
  4.   5. [Flutter](/docs/guides/getting-started/quickstarts/flutter)
  6. 

# Use Supabase with Flutter

## Learn how to create a Supabase project, add some sample data to your
database, and query the data from a Flutter app.

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

### Create a Flutter app

Create a Flutter app using the `flutter create` command. You can skip this
step if you already have a working app.

Terminal

`  

_10

flutter create my_app

  
`

3

### Install the Supabase client library

The fastest way to get started is to use the
[`supabase_flutter`](https://pub.dev/packages/supabase_flutter) client library
which provides a convenient interface for working with Supabase from a Flutter
app.

Open the `pubspec.yaml` file inside your Flutter app and add
`supabase_flutter` as a dependency.

pubspec.yaml

`  

_10

supabase_flutter: ^2.0.0

  
`

4

### Initialize the Supabase client

Open `lib/main.dart` and edit the main function to initialize Supabase using
your project URL and public API (anon) key:

###### Project URL

Loading...

###### Anon key

Loading...

lib/main.dart

`  

_11

import 'package:supabase_flutter/supabase_flutter.dart';

_11

_11

Future<void> main() async {

_11

WidgetsFlutterBinding.ensureInitialized();

_11

_11

await Supabase.initialize(

_11

url: 'YOUR_SUPABASE_URL',

_11

anonKey: 'YOUR_SUPABASE_ANON_KEY',

_11

);

_11

runApp(MyApp());

_11

}

  
`

5

### Query data from the app

Use a `FutureBuilder` to fetch the data when the home page loads and display
the query result in a `ListView`.

Replace the default `MyApp` and `MyHomePage` classes with the following code.

lib/main.dart

`  

_48

class MyApp extends StatelessWidget {

_48

const MyApp({super.key});

_48

_48

@override

_48

Widget build(BuildContext context) {

_48

return const MaterialApp(

_48

title: 'Countries',

_48

home: HomePage(),

_48

);

_48

}

_48

}

_48

_48

class HomePage extends StatefulWidget {

_48

const HomePage({super.key});

_48

_48

@override

_48

State<HomePage> createState() => _HomePageState();

_48

}

_48

_48

class _HomePageState extends State<HomePage> {

_48

final _future = Supabase.instance.client

_48

.from('countries')

_48

.select();

_48

_48

@override

_48

Widget build(BuildContext context) {

_48

return Scaffold(

_48

body: FutureBuilder(

_48

future: _future,

_48

builder: (context, snapshot) {

_48

if (!snapshot.hasData) {

_48

return const Center(child: CircularProgressIndicator());

_48

}

_48

final countries = snapshot.data!;

_48

return ListView.builder(

_48

itemCount: countries.length,

_48

itemBuilder: ((context, index) {

_48

final country = countries[index];

_48

return ListTile(

_48

title: Text(country['name']),

_48

);

_48

}),

_48

);

_48

},

_48

),

_48

);

_48

}

_48

}

  
`

6

### Start the app

Run your app on a platform of your choosing! By default an app should launch
in your web browser.

Note that `supabase_flutter` is compatible with web, iOS, Android, macOS, and
Windows apps. Running the app on MacOS requires additional configuration to
[set the entitlements](https://docs.flutter.dev/development/platform-
integration/macos/building#setting-up-entitlements).

Terminal

`  

_10

flutter run

  
`

## Going to production#

### Android#

In production, your Android app needs explicit permission to use the internet
connection on the user's device which is required to communicate with Supabase
APIs. To do this, add the following line to the
`android/app/src/main/AndroidManifest.xml` file.

`  

_10

<manifest xmlns:android="http://schemas.android.com/apk/res/android">

_10

<!-- Required to fetch data from the internet. -->

_10

<uses-permission android:name="android.permission.INTERNET" />

_10

<!-- ... -->

_10

</manifest>

  
`

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/quickstarts/flutter.mdx)

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

