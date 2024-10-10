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
  4.   5. [Swift](/docs/guides/getting-started/tutorials/with-swift)
  6. 

# Build a User Management App with Swift and SwiftUI

* * *

This tutorial demonstrates how to build a basic user management app. The app
authenticates and identifies the user, stores their profile information in the
database, and allows the user to log in, update their profile details, and
upload a profile photo. The app uses:

  * [Supabase Database](/docs/guides/database) \- a Postgres database for storing your user data and [Row Level Security](/docs/guides/auth#row-level-security) so data is protected and users can only access their own information.
  * [Supabase Auth](/docs/guides/auth) \- allow users to sign up and log in.
  * [Supabase Storage](/docs/guides/storage) \- users can upload a profile photo.

![Supabase User Management example](/docs/img/supabase-swift-demo.png)

If you get stuck while working through this guide, refer to the [full example
on GitHub](https://github.com/supabase/supabase/tree/master/examples/user-
management/swift-user-management).

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

Let's start building the SwiftUI app from scratch.

### Create a SwiftUI app in Xcode#

Open Xcode and create a new SwiftUI project.

Add the [supabase-swift](https://github.com/supabase/supabase-swift)
dependency.

Add the `https://github.com/supabase/supabase-swift` package to your app. For
instructions, see the [Apple tutorial on adding package
dependencies](https://developer.apple.com/documentation/xcode/adding-package-
dependencies-to-your-app).

Create a helper file to initialize the Supabase client. You need the API URL
and the `anon` key that you copied earlier. These variables will be exposed on
the application, and that's completely fine since you have [Row Level
Security](/docs/guides/auth#row-level-security) enabled on your database.

Supabase.swift

`  

_10

import Supabase

_10

_10

let supabase = SupabaseClient(

_10

supabaseURL: URL(string: "YOUR_SUPABASE_URL")!,

_10

supabaseKey: "YOUR_SUPABASE_ANON_KEY"

_10

)

  
`

### Set up a login view#

Set up a SwiftUI view to manage logins and sign ups. Users should be able to
sign in using a magic link.

AuthView.swift

`  

_66

import SwiftUI

_66

import Supabase

_66

_66

struct AuthView: View {

_66

@State var email = ""

_66

@State var isLoading = false

_66

@State var result: Result<Void, Error>?

_66

_66

var body: some View {

_66

Form {

_66

Section {

_66

TextField("Email", text: $email)

_66

.textContentType(.emailAddress)

_66

.textInputAutocapitalization(.never)

_66

.autocorrectionDisabled()

_66

}

_66

_66

Section {

_66

Button("Sign in") {

_66

signInButtonTapped()

_66

}

_66

_66

if isLoading {

_66

ProgressView()

_66

}

_66

}

_66

_66

if let result {

_66

Section {

_66

switch result {

_66

case .success:

_66

Text("Check your inbox.")

_66

case .failure(let error):

_66

Text(error.localizedDescription).foregroundStyle(.red)

_66

}

_66

}

_66

}

_66

}

_66

.onOpenURL(perform: { url in

_66

Task {

_66

do {

_66

try await supabase.auth.session(from: url)

_66

} catch {

_66

self.result = .failure(error)

_66

}

_66

}

_66

})

_66

}

_66

_66

func signInButtonTapped() {

_66

Task {

_66

isLoading = true

_66

defer { isLoading = false }

_66

_66

do {

_66

try await supabase.auth.signInWithOTP(

_66

email: email,

_66

redirectTo: URL(string: "io.supabase.user-management://login-callback")

_66

)

_66

result = .success(())

_66

} catch {

_66

result = .failure(error)

_66

}

_66

}

_66

}

_66

}

  
`

The example uses a custom `redirectTo` URL. For this to work, add a custom
redirect URL to Supabase and a custom URL scheme to your SwiftUI application.
Follow the guide on [implementing deep link
handling](/docs/guides/auth/native-mobile-deep-linking?platform=swift).

### Account view#

After a user is signed in, you can allow them to edit their profile details
and manage their account.

Create a new view for that called `ProfileView.swift`.

ProfileView.swift

`  

_95

import SwiftUI

_95

_95

struct ProfileView: View {

_95

@State var username = ""

_95

@State var fullName = ""

_95

@State var website = ""

_95

_95

@State var isLoading = false

_95

_95

var body: some View {

_95

NavigationStack {

_95

Form {

_95

Section {

_95

TextField("Username", text: $username)

_95

.textContentType(.username)

_95

.textInputAutocapitalization(.never)

_95

TextField("Full name", text: $fullName)

_95

.textContentType(.name)

_95

TextField("Website", text: $website)

_95

.textContentType(.URL)

_95

.textInputAutocapitalization(.never)

_95

}

_95

_95

Section {

_95

Button("Update profile") {

_95

updateProfileButtonTapped()

_95

}

_95

.bold()

_95

_95

if isLoading {

_95

ProgressView()

_95

}

_95

}

_95

}

_95

.navigationTitle("Profile")

_95

.toolbar(content: {

_95

ToolbarItem(placement: .topBarLeading){

_95

Button("Sign out", role: .destructive) {

_95

Task {

_95

try? await supabase.auth.signOut()

_95

}

_95

}

_95

}

_95

})

_95

}

_95

.task {

_95

await getInitialProfile()

_95

}

_95

}

_95

_95

func getInitialProfile() async {

_95

do {

_95

let currentUser = try await supabase.auth.session.user

_95

_95

let profile: Profile = try await supabase

_95

.from("profiles")

_95

.select()

_95

.eq("id", value: currentUser.id)

_95

.single()

_95

.execute()

_95

.value

_95

_95

self.username = profile.username ?? ""

_95

self.fullName = profile.fullName ?? ""

_95

self.website = profile.website ?? ""

_95

_95

} catch {

_95

debugPrint(error)

_95

}

_95

}

_95

_95

func updateProfileButtonTapped() {

_95

Task {

_95

isLoading = true

_95

defer { isLoading = false }

_95

do {

_95

let currentUser = try await supabase.auth.session.user

_95

_95

try await supabase

_95

.from("profiles")

_95

.update(

_95

UpdateProfileParams(

_95

username: username,

_95

fullName: fullName,

_95

website: website

_95

)

_95

)

_95

.eq("id", value: currentUser.id)

_95

.execute()

_95

} catch {

_95

debugPrint(error)

_95

}

_95

}

_95

}

_95

}

  
`

### Models#

In `ProfileView.swift`, you used 2 model types for deserializing the response
and serializing the request to Supabase. Add those in a new `Models.swift`
file.

Models.swift

`  

_23

struct Profile: Decodable {

_23

let username: String?

_23

let fullName: String?

_23

let website: String?

_23

_23

enum CodingKeys: String, CodingKey {

_23

case username

_23

case fullName = "full_name"

_23

case website

_23

}

_23

}

_23

_23

struct UpdateProfileParams: Encodable {

_23

let username: String

_23

let fullName: String

_23

let website: String

_23

_23

enum CodingKeys: String, CodingKey {

_23

case username

_23

case fullName = "full_name"

_23

case website

_23

}

_23

}

  
`

### Launch!#

Now that you've created all the views, add an entry point for the application.
This will verify if the user has a valid session and route them to the
authenticated or non-authenticated state.

Add a new `AppView.swift` file.

AppView.swift

`  

_22

import SwiftUI

_22

_22

struct AppView: View {

_22

@State var isAuthenticated = false

_22

_22

var body: some View {

_22

Group {

_22

if isAuthenticated {

_22

ProfileView()

_22

} else {

_22

AuthView()

_22

}

_22

}

_22

.task {

_22

for await state in supabase.auth.authStateChanges {

_22

if [.initialSession, .signedIn, .signedOut].contains(state.event) {

_22

isAuthenticated = state.session != nil

_22

}

_22

}

_22

}

_22

}

_22

}

  
`

Update the entry point to the newly created `AppView`. Run in Xcode to launch
your application in the simulator.

## Bonus: Profile photos#

Every Supabase project is configured with [Storage](/docs/guides/storage) for
managing large files like photos and videos.

### Add PhotosPicker#

Let's add support for the user to pick an image from the library and upload
it. Start by creating a new type to hold the picked avatar image:

AvatarImage.swift

`  

_31

import SwiftUI

_31

_31

struct AvatarImage: Transferable, Equatable {

_31

let image: Image

_31

let data: Data

_31

_31

static var transferRepresentation: some TransferRepresentation {

_31

DataRepresentation(importedContentType: .image) { data in

_31

guard let image = AvatarImage(data: data) else {

_31

throw TransferError.importFailed

_31

}

_31

_31

return image

_31

}

_31

}

_31

}

_31

_31

extension AvatarImage {

_31

init?(data: Data) {

_31

guard let uiImage = UIImage(data: data) else {

_31

return nil

_31

}

_31

_31

let image = Image(uiImage: uiImage)

_31

self.init(image: image, data: data)

_31

}

_31

}

_31

_31

enum TransferError: Error {

_31

case importFailed

_31

}

  
`

#### Add PhotosPicker to profile page#

ProfileView.swift

`  

_161

struct ProfileView: View {

_161

@State var username = ""

_161

@State var fullName = ""

_161

@State var website = ""

_161

_161

@State var isLoading = false

_161

_161

+ @State var imageSelection: PhotosPickerItem?

_161

+ @State var avatarImage: AvatarImage?

_161

_161

var body: some View {

_161

NavigationStack {

_161

Form {

_161

+ Section {

_161

+ HStack {

_161

+ Group {

_161

+ if let avatarImage {

_161

+ avatarImage.image.resizable()

_161

+ } else {

_161

+ Color.clear

_161

+ }

_161

+ }

_161

+ .scaledToFit()

_161

+ .frame(width: 80, height: 80)

_161

+

_161

+ Spacer()

_161

+

_161

+ PhotosPicker(selection: $imageSelection, matching: .images) {

_161

+ Image(systemName: "pencil.circle.fill")

_161

+ .symbolRenderingMode(.multicolor)

_161

+ .font(.system(size: 30))

_161

+ .foregroundColor(.accentColor)

_161

+ }

_161

+ }

_161

+ }

_161

_161

Section {

_161

TextField("Username", text: $username)

_161

.textContentType(.username)

_161

.textInputAutocapitalization(.never)

_161

TextField("Full name", text: $fullName)

_161

.textContentType(.name)

_161

TextField("Website", text: $website)

_161

.textContentType(.URL)

_161

.textInputAutocapitalization(.never)

_161

}

_161

_161

Section {

_161

Button("Update profile") {

_161

updateProfileButtonTapped()

_161

}

_161

.bold()

_161

_161

if isLoading {

_161

ProgressView()

_161

}

_161

}

_161

}

_161

.navigationTitle("Profile")

_161

.toolbar(content: {

_161

ToolbarItem {

_161

Button("Sign out", role: .destructive) {

_161

Task {

_161

try? await supabase.auth.signOut()

_161

}

_161

}

_161

}

_161

})

_161

+ .onChange(of: imageSelection) { _, newValue in

_161

+ guard let newValue else { return }

_161

+ loadTransferable(from: newValue)

_161

+ }

_161

}

_161

.task {

_161

await getInitialProfile()

_161

}

_161

}

_161

_161

func getInitialProfile() async {

_161

do {

_161

let currentUser = try await supabase.auth.session.user

_161

_161

let profile: Profile = try await supabase.database

_161

.from("profiles")

_161

.select()

_161

.eq("id", value: currentUser.id)

_161

.single()

_161

.execute()

_161

.value

_161

_161

username = profile.username ?? ""

_161

fullName = profile.fullName ?? ""

_161

website = profile.website ?? ""

_161

_161

+ if let avatarURL = profile.avatarURL, !avatarURL.isEmpty {

_161

+ try await downloadImage(path: avatarURL)

_161

+ }

_161

_161

} catch {

_161

debugPrint(error)

_161

}

_161

}

_161

_161

func updateProfileButtonTapped() {

_161

Task {

_161

isLoading = true

_161

defer { isLoading = false }

_161

do {

_161

+ let imageURL = try await uploadImage()

_161

_161

let currentUser = try await supabase.auth.session.user

_161

_161

let updatedProfile = Profile(

_161

username: username,

_161

fullName: fullName,

_161

website: website,

_161

+ avatarURL: imageURL

_161

)

_161

_161

try await supabase.database

_161

.from("profiles")

_161

.update(updatedProfile)

_161

.eq("id", value: currentUser.id)

_161

.execute()

_161

} catch {

_161

debugPrint(error)

_161

}

_161

}

_161

}

_161

_161

+ private func loadTransferable(from imageSelection: PhotosPickerItem) {

_161

+ Task {

_161

+ do {

_161

+ avatarImage = try await imageSelection.loadTransferable(type: AvatarImage.self)

_161

+ } catch {

_161

+ debugPrint(error)

_161

+ }

_161

+ }

_161

+ }

_161

+

_161

+ private func downloadImage(path: String) async throws {

_161

+ let data = try await supabase.storage.from("avatars").download(path: path)

_161

+ avatarImage = AvatarImage(data: data)

_161

+ }

_161

+

_161

+ private func uploadImage() async throws -> String? {

_161

+ guard let data = avatarImage?.data else { return nil }

_161

+

_161

+ let filePath = "\(UUID().uuidString).jpeg"

_161

+

_161

+ try await supabase.storage

_161

+ .from("avatars")

_161

+ .upload(

_161

+ path: filePath,

_161

+ file: data,

_161

+ options: FileOptions(contentType: "image/jpeg")

_161

+ )

_161

+

_161

+ return filePath

_161

+ }

_161

}

  
`

Finally, update your Models.

Models.swift

`  

_13

struct Profile: Codable {

_13

let username: String?

_13

let fullName: String?

_13

let website: String?

_13

let avatarURL: String?

_13

_13

enum CodingKeys: String, CodingKey {

_13

case username

_13

case fullName = "full_name"

_13

case website

_13

case avatarURL = "avatar_url"

_13

}

_13

}

  
`

You no longer need the `UpdateProfileParams` struct, as you can now reuse the
`Profile` struct for both request and response calls.

At this stage you have a fully functional application!

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/tutorials/with-swift.mdx)

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

