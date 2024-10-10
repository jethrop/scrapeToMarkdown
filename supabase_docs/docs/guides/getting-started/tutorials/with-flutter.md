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
  2.   3. Mobile tutorials
  4.   5. [Flutter](/docs/guides/getting-started/tutorials/with-flutter)
  6. 

# Build a User Management App with Flutter

* * *

This tutorial demonstrates how to build a basic user management app. The app
authenticates and identifies the user, stores their profile information in the
database, and allows the user to log in, update their profile details, and
upload a profile photo. The app uses:

  * [Supabase Database](/docs/guides/database) \- a Postgres database for storing your user data and [Row Level Security](/docs/guides/auth#row-level-security) so data is protected and users can only access their own information.
  * [Supabase Auth](/docs/guides/auth) \- allow users to sign up and log in.
  * [Supabase Storage](/docs/guides/storage) \- users can upload a profile photo.

![Supabase User Management example](/docs/img/supabase-flutter-demo.png)

If you get stuck while working through this guide, refer to the [full example
on GitHub](https://github.com/supabase/supabase/tree/master/examples/user-
management/flutter-user-management).

## Project setup#

Before we start building we're going to set up our Database and API. This is
as simple as starting a new Project in Supabase and then creating a "schema"
inside the database.

### Create a project#

  1. [Create a new project](https://supabase.com/dashboard) in the Supabase Dashboard.
  2. Enter your project details.
  3. Wait for the new database to launch.

### Set up the database schema#

Now we are going to set up the database schema. We can use the "User
Management Starter" quickstart in the SQL Editor, or you can just copy/paste
the SQL from below and run it yourself.

DashboardSQL

  1. Go to the [SQL Editor](https://supabase.com/dashboard/project/_/sql) page in the Dashboard.
  2. Click **User Management Starter**.
  3. Click **Run**.

You can easily pull the database schema down to your local project by running
the `db pull` command. Read the [local development
docs](/docs/guides/cli/local-development#link-your-project) for detailed
instructions.

`  

_10

supabase link --project-ref <project-id>

_10

# You can get <project-id> from your project's dashboard URL:
https://supabase.com/dashboard/project/<project-id>

_10

supabase db pull

  
`

### Get the API Keys#

Now that you've created some database tables, you are ready to insert data
using the auto-generated API. We just need to get the Project URL and `anon`
key from the API settings.

  1. Go to the [API Settings](https://supabase.com/dashboard/project/_/settings/api) page in the Dashboard.
  2. Find your Project `URL`, `anon`, and `service_role` keys on this page.

## Building the app#

Let's start building the Flutter app from scratch.

### Initialize a Flutter app#

We can use [`flutter create`](https://flutter.dev/docs/get-started/test-drive)
to initialize an app called `supabase_quickstart`:

`  

_10

flutter create supabase_quickstart

  
`

Then let's install the only additional dependency:
[`supabase_flutter`](https://pub.dev/packages/supabase_flutter)

Copy and paste the following line in your pubspec.yaml to install the package:

`  

_10

supabase_flutter: ^2.0.0

  
`

Run `flutter pub get` to install the dependencies.

### Setup deep links#

Now that we have the dependencies installed let's setup deep links. Setting up
deep links is required to bring back the user to the app when they click on
the magic link to sign in. We can setup deep links with just a minor tweak on
our Flutter application.

We have to use `io.supabase.flutterquickstart` as the scheme. In this example,
we will use `login-callback` as the host for our deep link, but you can change
it to whatever you would like.

First, add `io.supabase.flutterquickstart://login-callback/` as a new
[redirect URL](https://supabase.com/dashboard/project/_/auth/url-
configuration) in the Dashboard.

![Supabase console deep link setting](/docs/img/deeplink-setting.png)

That is it on Supabase's end and the rest are platform specific settings:

iOSAndroidWeb

Edit the `ios/Runner/Info.plist` file.

Add CFBundleURLTypes to enable deep linking:

ios/Runner/Info.plist"

`  

_20

<!-- ... other tags -->

_20

<plist>

_20

<dict>

_20

<!-- ... other tags -->

_20

_20

<!-- Add this array for Deep Links -->

_20

<key>CFBundleURLTypes</key>

_20

<array>

_20

<dict>

_20

<key>CFBundleTypeRole</key>

_20

<string>Editor</string>

_20

<key>CFBundleURLSchemes</key>

_20

<array>

_20

<string>io.supabase.flutterquickstart</string>

_20

</array>

_20

</dict>

_20

</array>

_20

<!-- ... other tags -->

_20

</dict>

_20

</plist>

  
`

### Main function#

Now that we have deep links ready let's initialize the Supabase client inside
our `main` function with the API credentials that you copied earlier. These
variables will be exposed on the app, and that's completely fine since we have
[Row Level Security](/docs/guides/auth#row-level-security) enabled on our
Database.

lib/main.dart

`  

_34

import 'package:flutter/material.dart';

_34

import 'package:supabase_flutter/supabase_flutter.dart';

_34

_34

Future<void> main() async {

_34

await Supabase.initialize(

_34

url: 'YOUR_SUPABASE_URL',

_34

anonKey: 'YOUR_SUPABASE_ANON_KEY',

_34

);

_34

runApp(const MyApp());

_34

}

_34

_34

final supabase = Supabase.instance.client;

_34

_34

class MyApp extends StatelessWidget {

_34

const MyApp({super.key});

_34

_34

@override

_34

Widget build(BuildContext context) {

_34

return const MaterialApp(title: 'Supabase Flutter');

_34

}

_34

}

_34

_34

extension ContextExtension on BuildContext {

_34

void showSnackBar(String message, {bool isError = false}) {

_34

ScaffoldMessenger.of(this).showSnackBar(

_34

SnackBar(

_34

content: Text(message),

_34

backgroundColor: isError

_34

? Theme.of(this).colorScheme.error

_34

: Theme.of(this).snackBarTheme.backgroundColor,

_34

),

_34

);

_34

}

_34

}

  
`

Notice that we have a `showSnackBar` extension method that we will use to show
snack bars in the app. You could define this method in a separate file and
import it where needed, but for simplicity, we will define it here.

### Set up a login page#

Let's create a Flutter widget to manage logins and sign ups. We will use Magic
Links, so users can sign in with their email without using passwords.

Notice that this page sets up a listener on the user's auth state using
`onAuthStateChange`. A new event will fire when the user comes back to the app
by clicking their magic link, which this page can catch and redirect the user
accordingly.

lib/pages/login_page.dart

`  

_105

import 'dart:async';

_105

_105

import 'package:flutter/foundation.dart';

_105

import 'package:flutter/material.dart';

_105

import 'package:supabase_flutter/supabase_flutter.dart';

_105

import 'package:supabase_quickstart/main.dart';

_105

import 'package:supabase_quickstart/pages/account_page.dart';

_105

_105

class LoginPage extends StatefulWidget {

_105

const LoginPage({super.key});

_105

_105

@override

_105

State<LoginPage> createState() => _LoginPageState();

_105

}

_105

_105

class _LoginPageState extends State<LoginPage> {

_105

bool _isLoading = false;

_105

bool _redirecting = false;

_105

late final TextEditingController _emailController = TextEditingController();

_105

late final StreamSubscription<AuthState> _authStateSubscription;

_105

_105

Future<void> _signIn() async {

_105

try {

_105

setState(() {

_105

_isLoading = true;

_105

});

_105

await supabase.auth.signInWithOtp(

_105

email: _emailController.text.trim(),

_105

emailRedirectTo:

_105

kIsWeb ? null : 'io.supabase.flutterquickstart://login-callback/',

_105

);

_105

if (mounted) {

_105

context.showSnackBar('Check your email for a login link!');

_105

_105

_emailController.clear();

_105

}

_105

} on AuthException catch (error) {

_105

if (mounted) context.showSnackBar(error.message, isError: true);

_105

} catch (error) {

_105

if (mounted) {

_105

context.showSnackBar('Unexpected error occurred', isError: true);

_105

}

_105

} finally {

_105

if (mounted) {

_105

setState(() {

_105

_isLoading = false;

_105

});

_105

}

_105

}

_105

}

_105

_105

@override

_105

void initState() {

_105

_authStateSubscription = supabase.auth.onAuthStateChange.listen(

_105

(data) {

_105

if (_redirecting) return;

_105

final session = data.session;

_105

if (session != null) {

_105

_redirecting = true;

_105

Navigator.of(context).pushReplacement(

_105

MaterialPageRoute(builder: (context) => const AccountPage()),

_105

);

_105

}

_105

},

_105

onError: (error) {

_105

if (error is AuthException) {

_105

context.showSnackBar(error.message, isError: true);

_105

} else {

_105

context.showSnackBar('Unexpected error occurred', isError: true);

_105

}

_105

},

_105

);

_105

super.initState();

_105

}

_105

_105

@override

_105

void dispose() {

_105

_emailController.dispose();

_105

_authStateSubscription.cancel();

_105

super.dispose();

_105

}

_105

_105

@override

_105

Widget build(BuildContext context) {

_105

return Scaffold(

_105

appBar: AppBar(title: const Text('Sign In')),

_105

body: ListView(

_105

padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 12),

_105

children: [

_105

const Text('Sign in via the magic link with your email below'),

_105

const SizedBox(height: 18),

_105

TextFormField(

_105

controller: _emailController,

_105

decoration: const InputDecoration(labelText: 'Email'),

_105

),

_105

const SizedBox(height: 18),

_105

ElevatedButton(

_105

onPressed: _isLoading ? null : _signIn,

_105

child: Text(_isLoading ? 'Sending...' : 'Send Magic Link'),

_105

),

_105

],

_105

),

_105

);

_105

}

_105

}

  
`

### Set up account page#

After a user is signed in we can allow them to edit their profile details and
manage their account. Let's create a new widget called `account_page.dart` for
that.

lib/pages/account_page.dart"

`  

_138

import 'package:flutter/material.dart';

_138

import 'package:supabase_flutter/supabase_flutter.dart';

_138

import 'package:supabase_quickstart/main.dart';

_138

import 'package:supabase_quickstart/pages/login_page.dart';

_138

_138

class AccountPage extends StatefulWidget {

_138

const AccountPage({super.key});

_138

_138

@override

_138

State<AccountPage> createState() => _AccountPageState();

_138

}

_138

_138

class _AccountPageState extends State<AccountPage> {

_138

final _usernameController = TextEditingController();

_138

final _websiteController = TextEditingController();

_138

_138

String? _avatarUrl;

_138

var _loading = true;

_138

_138

/// Called once a user id is received within `onAuthenticated()`

_138

Future<void> _getProfile() async {

_138

setState(() {

_138

_loading = true;

_138

});

_138

_138

try {

_138

final userId = supabase.auth.currentSession!.user.id;

_138

final data =

_138

await supabase.from('profiles').select().eq('id', userId).single();

_138

_usernameController.text = (data['username'] ?? '') as String;

_138

_websiteController.text = (data['website'] ?? '') as String;

_138

_avatarUrl = (data['avatar_url'] ?? '') as String;

_138

} on PostgrestException catch (error) {

_138

if (mounted) context.showSnackBar(error.message, isError: true);

_138

} catch (error) {

_138

if (mounted) {

_138

context.showSnackBar('Unexpected error occurred', isError: true);

_138

}

_138

} finally {

_138

if (mounted) {

_138

setState(() {

_138

_loading = false;

_138

});

_138

}

_138

}

_138

}

_138

_138

/// Called when user taps `Update` button

_138

Future<void> _updateProfile() async {

_138

setState(() {

_138

_loading = true;

_138

});

_138

final userName = _usernameController.text.trim();

_138

final website = _websiteController.text.trim();

_138

final user = supabase.auth.currentUser;

_138

final updates = {

_138

'id': user!.id,

_138

'username': userName,

_138

'website': website,

_138

'updated_at': DateTime.now().toIso8601String(),

_138

};

_138

try {

_138

await supabase.from('profiles').upsert(updates);

_138

if (mounted) context.showSnackBar('Successfully updated profile!');

_138

} on PostgrestException catch (error) {

_138

if (mounted) context.showSnackBar(error.message, isError: true);

_138

} catch (error) {

_138

if (mounted) {

_138

context.showSnackBar('Unexpected error occurred', isError: true);

_138

}

_138

} finally {

_138

if (mounted) {

_138

setState(() {

_138

_loading = false;

_138

});

_138

}

_138

}

_138

}

_138

_138

Future<void> _signOut() async {

_138

try {

_138

await supabase.auth.signOut();

_138

} on AuthException catch (error) {

_138

if (mounted) context.showSnackBar(error.message, isError: true);

_138

} catch (error) {

_138

if (mounted) {

_138

context.showSnackBar('Unexpected error occurred', isError: true);

_138

}

_138

} finally {

_138

if (mounted) {

_138

Navigator.of(context).pushReplacement(

_138

MaterialPageRoute(builder: (_) => const LoginPage()),

_138

);

_138

}

_138

}

_138

}

_138

_138

@override

_138

void initState() {

_138

super.initState();

_138

_getProfile();

_138

}

_138

_138

@override

_138

void dispose() {

_138

_usernameController.dispose();

_138

_websiteController.dispose();

_138

super.dispose();

_138

}

_138

_138

@override

_138

Widget build(BuildContext context) {

_138

return Scaffold(

_138

appBar: AppBar(title: const Text('Profile')),

_138

body: ListView(

_138

padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 12),

_138

children: [

_138

TextFormField(

_138

controller: _usernameController,

_138

decoration: const InputDecoration(labelText: 'User Name'),

_138

),

_138

const SizedBox(height: 18),

_138

TextFormField(

_138

controller: _websiteController,

_138

decoration: const InputDecoration(labelText: 'Website'),

_138

),

_138

const SizedBox(height: 18),

_138

ElevatedButton(

_138

onPressed: _loading ? null : _updateProfile,

_138

child: Text(_loading ? 'Saving...' : 'Update'),

_138

),

_138

const SizedBox(height: 18),

_138

TextButton(onPressed: _signOut, child: const Text('Sign Out')),

_138

],

_138

),

_138

);

_138

}

_138

}

  
`

### Launch!#

Now that we have all the components in place, let's update `lib/main.dart`.
The `home` of the `MaterialApp`, meaning the initial page shown to the user,
will be the `LoginPage` if the user is not authenticated, and the
`AccountPage` if the user is authenticated. We also included some theming to
make the app look a bit nicer.

lib/main.dart

`  

_55

import 'package:flutter/material.dart';

_55

import 'package:supabase_flutter/supabase_flutter.dart';

_55

import 'package:supabase_quickstart/pages/account_page.dart';

_55

import 'package:supabase_quickstart/pages/login_page.dart';

_55

_55

Future<void> main() async {

_55

await Supabase.initialize(

_55

url: 'YOUR_SUPABASE_URL',

_55

anonKey: 'YOUR_SUPABASE_ANON_KEY',

_55

);

_55

runApp(const MyApp());

_55

}

_55

_55

final supabase = Supabase.instance.client;

_55

_55

class MyApp extends StatelessWidget {

_55

const MyApp({super.key});

_55

_55

@override

_55

Widget build(BuildContext context) {

_55

return MaterialApp(

_55

title: 'Supabase Flutter',

_55

theme: ThemeData.dark().copyWith(

_55

primaryColor: Colors.green,

_55

textButtonTheme: TextButtonThemeData(

_55

style: TextButton.styleFrom(

_55

foregroundColor: Colors.green,

_55

),

_55

),

_55

elevatedButtonTheme: ElevatedButtonThemeData(

_55

style: ElevatedButton.styleFrom(

_55

foregroundColor: Colors.white,

_55

backgroundColor: Colors.green,

_55

),

_55

),

_55

),

_55

home: supabase.auth.currentSession == null

_55

? const LoginPage()

_55

: const AccountPage(),

_55

);

_55

}

_55

}

_55

_55

extension ContextExtension on BuildContext {

_55

void showSnackBar(String message, {bool isError = false}) {

_55

ScaffoldMessenger.of(this).showSnackBar(

_55

SnackBar(

_55

content: Text(message),

_55

backgroundColor: isError

_55

? Theme.of(this).colorScheme.error

_55

: Theme.of(this).snackBarTheme.backgroundColor,

_55

),

_55

);

_55

}

_55

}

  
`

Once that's done, run this in a terminal window to launch on Android or iOS:

`  

_10

flutter run

  
`

Or for web, run the following command to launch it on `localhost:3000`

`  

_10

flutter run -d web-server --web-hostname localhost --web-port 3000

  
`

And then open the browser to [localhost:3000](http://localhost:3000) and you
should see the completed app.

![Supabase User Management example](/docs/img/supabase-flutter-account-
page.png)

## Bonus: Profile photos#

Every Supabase project is configured with [Storage](/docs/guides/storage) for
managing large files like photos and videos.

### Making sure we have a public bucket#

We will be storing the image as a publicly sharable image. Make sure your
`avatars` bucket is set to public, and if it is not, change the publicity by
clicking the dot menu that appears when you hover over the bucket name. You
should see an orange `Public` badge next to your bucket name if your bucket is
set to public.

### Adding image uploading feature to account page#

We will use [`image_picker`](https://pub.dev/packages/image_picker) plugin to
select an image from the device.

Add the following line in your pubspec.yaml file to install `image_picker`:

`  

_10

image_picker: ^1.0.5

  
`

Using [`image_picker`](https://pub.dev/packages/image_picker) requires some
additional preparation depending on the platform. Follow the instruction on
README.md of [`image_picker`](https://pub.dev/packages/image_picker) on how to
set it up for the platform you are using.

Once you are done with all of the above, it is time to dive into coding.

### Create an upload widget#

Let's create an avatar for the user so that they can upload a profile photo.
We can start by creating a new component:

lib/components/avatar.dart

`  

_89

import 'package:flutter/material.dart';

_89

import 'package:image_picker/image_picker.dart';

_89

import 'package:supabase_flutter/supabase_flutter.dart';

_89

import 'package:supabase_quickstart/main.dart';

_89

_89

class Avatar extends StatefulWidget {

_89

const Avatar({

_89

super.key,

_89

required this.imageUrl,

_89

required this.onUpload,

_89

});

_89

_89

final String? imageUrl;

_89

final void Function(String) onUpload;

_89

_89

@override

_89

State<Avatar> createState() => _AvatarState();

_89

}

_89

_89

class _AvatarState extends State<Avatar> {

_89

bool _isLoading = false;

_89

_89

@override

_89

Widget build(BuildContext context) {

_89

return Column(

_89

children: [

_89

if (widget.imageUrl == null || widget.imageUrl!.isEmpty)

_89

Container(

_89

width: 150,

_89

height: 150,

_89

color: Colors.grey,

_89

child: const Center(

_89

child: Text('No Image'),

_89

),

_89

)

_89

else

_89

Image.network(

_89

widget.imageUrl!,

_89

width: 150,

_89

height: 150,

_89

fit: BoxFit.cover,

_89

),

_89

ElevatedButton(

_89

onPressed: _isLoading ? null : _upload,

_89

child: const Text('Upload'),

_89

),

_89

],

_89

);

_89

}

_89

_89

Future<void> _upload() async {

_89

final picker = ImagePicker();

_89

final imageFile = await picker.pickImage(

_89

source: ImageSource.gallery,

_89

maxWidth: 300,

_89

maxHeight: 300,

_89

);

_89

if (imageFile == null) {

_89

return;

_89

}

_89

setState(() => _isLoading = true);

_89

_89

try {

_89

final bytes = await imageFile.readAsBytes();

_89

final fileExt = imageFile.path.split('.').last;

_89

final fileName = '${DateTime.now().toIso8601String()}.$fileExt';

_89

final filePath = fileName;

_89

await supabase.storage.from('avatars').uploadBinary(

_89

filePath,

_89

bytes,

_89

fileOptions: FileOptions(contentType: imageFile.mimeType),

_89

);

_89

final imageUrlResponse = await supabase.storage

_89

.from('avatars')

_89

.createSignedUrl(filePath, 60 * 60 * 24 * 365 * 10);

_89

widget.onUpload(imageUrlResponse);

_89

} on StorageException catch (error) {

_89

if (mounted) {

_89

context.showSnackBar(error.message, isError: true);

_89

}

_89

} catch (error) {

_89

if (mounted) {

_89

context.showSnackBar('Unexpected error occurred', isError: true);

_89

}

_89

}

_89

_89

setState(() => _isLoading = false);

_89

}

_89

}

  
`

### Add the new widget#

And then we can add the widget to the Account page as well as some logic to
update the `avatar_url` whenever the user uploads a new avatar.

lib/pages/account_page.dart

`  

_173

import 'package:flutter/material.dart';

_173

import 'package:supabase_flutter/supabase_flutter.dart';

_173

import 'package:supabase_quickstart/components/avatar.dart';

_173

import 'package:supabase_quickstart/main.dart';

_173

import 'package:supabase_quickstart/pages/login_page.dart';

_173

_173

class AccountPage extends StatefulWidget {

_173

const AccountPage({super.key});

_173

_173

@override

_173

State<AccountPage> createState() => _AccountPageState();

_173

}

_173

_173

class _AccountPageState extends State<AccountPage> {

_173

final _usernameController = TextEditingController();

_173

final _websiteController = TextEditingController();

_173

_173

String? _avatarUrl;

_173

var _loading = true;

_173

_173

/// Called once a user id is received within `onAuthenticated()`

_173

Future<void> _getProfile() async {

_173

setState(() {

_173

_loading = true;

_173

});

_173

_173

try {

_173

final userId = supabase.auth.currentSession!.user.id;

_173

final data =

_173

await supabase.from('profiles').select().eq('id', userId).single();

_173

_usernameController.text = (data['username'] ?? '') as String;

_173

_websiteController.text = (data['website'] ?? '') as String;

_173

_avatarUrl = (data['avatar_url'] ?? '') as String;

_173

} on PostgrestException catch (error) {

_173

if (mounted) context.showSnackBar(error.message, isError: true);

_173

} catch (error) {

_173

if (mounted) {

_173

context.showSnackBar('Unexpected error occurred', isError: true);

_173

}

_173

} finally {

_173

if (mounted) {

_173

setState(() {

_173

_loading = false;

_173

});

_173

}

_173

}

_173

}

_173

_173

/// Called when user taps `Update` button

_173

Future<void> _updateProfile() async {

_173

setState(() {

_173

_loading = true;

_173

});

_173

final userName = _usernameController.text.trim();

_173

final website = _websiteController.text.trim();

_173

final user = supabase.auth.currentUser;

_173

final updates = {

_173

'id': user!.id,

_173

'username': userName,

_173

'website': website,

_173

'updated_at': DateTime.now().toIso8601String(),

_173

};

_173

try {

_173

await supabase.from('profiles').upsert(updates);

_173

if (mounted) context.showSnackBar('Successfully updated profile!');

_173

} on PostgrestException catch (error) {

_173

if (mounted) context.showSnackBar(error.message, isError: true);

_173

} catch (error) {

_173

if (mounted) {

_173

context.showSnackBar('Unexpected error occurred', isError: true);

_173

}

_173

} finally {

_173

if (mounted) {

_173

setState(() {

_173

_loading = false;

_173

});

_173

}

_173

}

_173

}

_173

_173

Future<void> _signOut() async {

_173

try {

_173

await supabase.auth.signOut();

_173

} on AuthException catch (error) {

_173

if (mounted) context.showSnackBar(error.message, isError: true);

_173

} catch (error) {

_173

if (mounted) {

_173

context.showSnackBar('Unexpected error occurred', isError: true);

_173

}

_173

} finally {

_173

if (mounted) {

_173

Navigator.of(context).pushReplacement(

_173

MaterialPageRoute(builder: (_) => const LoginPage()),

_173

);

_173

}

_173

}

_173

}

_173

_173

/// Called when image has been uploaded to Supabase storage from within Avatar
widget

_173

Future<void> _onUpload(String imageUrl) async {

_173

try {

_173

final userId = supabase.auth.currentUser!.id;

_173

await supabase.from('profiles').upsert({

_173

'id': userId,

_173

'avatar_url': imageUrl,

_173

});

_173

if (mounted) {

_173

const SnackBar(

_173

content: Text('Updated your profile image!'),

_173

);

_173

}

_173

} on PostgrestException catch (error) {

_173

if (mounted) context.showSnackBar(error.message, isError: true);

_173

} catch (error) {

_173

if (mounted) {

_173

context.showSnackBar('Unexpected error occurred', isError: true);

_173

}

_173

}

_173

if (!mounted) {

_173

return;

_173

}

_173

_173

setState(() {

_173

_avatarUrl = imageUrl;

_173

});

_173

}

_173

_173

@override

_173

void initState() {

_173

super.initState();

_173

_getProfile();

_173

}

_173

_173

@override

_173

void dispose() {

_173

_usernameController.dispose();

_173

_websiteController.dispose();

_173

super.dispose();

_173

}

_173

_173

@override

_173

Widget build(BuildContext context) {

_173

return Scaffold(

_173

appBar: AppBar(title: const Text('Profile')),

_173

body: ListView(

_173

padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 12),

_173

children: [

_173

Avatar(

_173

imageUrl: _avatarUrl,

_173

onUpload: _onUpload,

_173

),

_173

const SizedBox(height: 18),

_173

TextFormField(

_173

controller: _usernameController,

_173

decoration: const InputDecoration(labelText: 'User Name'),

_173

),

_173

const SizedBox(height: 18),

_173

TextFormField(

_173

controller: _websiteController,

_173

decoration: const InputDecoration(labelText: 'Website'),

_173

),

_173

const SizedBox(height: 18),

_173

ElevatedButton(

_173

onPressed: _loading ? null : _updateProfile,

_173

child: Text(_loading ? 'Saving...' : 'Update'),

_173

),

_173

const SizedBox(height: 18),

_173

TextButton(onPressed: _signOut, child: const Text('Sign Out')),

_173

],

_173

),

_173

);

_173

}

_173

}

  
`

Congratulations, you've built a fully functional user management app using
Flutter and Supabase!

## See also#

  * [Flutter Tutorial: building a Flutter chat app](https://supabase.com/blog/flutter-tutorial-building-a-chat-app)
  * [Flutter Tutorial - Part 2: Authentication and Authorization with RLS](https://supabase.com/blog/flutter-authentication-and-authorization-with-rls)

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/tutorials/with-flutter.mdx)

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

