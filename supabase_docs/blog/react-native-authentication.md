[Back](/blog)

[Blog](/blog)

# Getting started with React Native authentication

16 Nov 2023

•

13 minute read

[![Thor Schaeff
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fthorwebdev.png&w=96&q=75)Thor
SchaeffDevRel & DX](https://twitter.com/thorwebdev)

![Getting started with React Native
authentication](/_next/image?url=%2Fimages%2Fblog%2F2023-11-16-react-native-
authentication%2Freact-native-authentication-supabase.jpg&w=3840&q=100)

Authentication is the process of verifying the identity of a user who is
attempting to access a system, application, or online service. In this blog
post, you will learn about React Native authentication, including native
mobile specific login mechanisms like "Sign in with Apple" and "Google One Tap
sign-in", as well as SMS & WhatsApp based authentication.

At the end of this blog post, you will have all the components needed to
create the ideal authentication experience for your mobile app users.

## Prerequisites#

This article assumes you are comfortable with writing a basic application in
React Native. No knowledge of Supabase is required.

We will use the following tools

  * [Expo](https://docs.expo.dev/get-started/create-a-new-app/) \- we used Expo SDK version 49.0.0 (React Native version 0.72)
  * Supabase - create your account [here](https://database.new/) if you do not have one
  * IDE of your choosing

Note: We're using Expo as that's the
[recommended](https://reactnative.dev/docs/environment-setup) way of getting
started with React Native. However, the fundamental approach here applies to
bare React Native applications as well.

## Set up supabase-js for React Native#

Using [`supabase-js`](/docs/reference/javascript/introduction) is the most
convenient way of leveraging the full power of the Supabase stack as it
conveniently combines all the different services (database, auth, realtime,
storage, edge functions) together.

### Install supabase-js and dependencies#

After you have created your [Expo project](https://docs.expo.dev/get-
started/create-a-project), you can install `supabase-js` and the required
dependencies using the following command:

`  

_10

npx expo install @supabase/supabase-js @react-native-async-storage/async-
storage react-native-url-polyfill

  
`

### Authentication storage#

By default, supabase-js uses the browser's `localStorage` mechanism to persist
the user's session but can be extended with platform specific storage
implementations. In React Native we can build native mobile and web
applications with the same code base, so we need a storage implementation that
works for all these platforms: [react-native-async-
storage](https://github.com/react-native-async-storage/async-
storage#supported-platforms).

We need to pass an instance of `react-native-async-storage` to supabase-js to
make sure authentication works reliably across all react native platforms:

lib/supabase.ts

`  

_15

import 'react-native-url-polyfill/auto'

_15

import AsyncStorage from '@react-native-async-storage/async-storage'

_15

import { createClient } from '@supabase/supabase-js'

_15

_15

const supabaseUrl = YOUR_REACT_NATIVE_SUPABASE_URL

_15

const supabaseAnonKey = YOUR_REACT_NATIVE_SUPABASE_ANON_KEY

_15

_15

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {

_15

auth: {

_15

storage: AsyncStorage,

_15

autoRefreshToken: true,

_15

persistSession: true,

_15

detectSessionInUrl: false,

_15

},

_15

})

  
`

You can find your URL and anon key in the [API credentials
section](/dashboard/project/_/settings/api) of the Supabase dashboard.

### Encrypting the user session#

If you wish to encrypt the user's session information, you can use `aes-js`
and store the encryption key in [Expo
SecureStore](https://docs.expo.dev/versions/latest/sdk/securestore). The
[`aes-js` library](https://github.com/ricmoo/aes-js) is a reputable
JavaScript-only implementation of the AES encryption algorithm in CTR mode. A
new 256-bit encryption key is generated using the `react-native-get-random-
values` library. This key is stored inside Expo's SecureStore, while the value
is encrypted and placed inside AsyncStorage.

Please make sure that:

  * You keep the `expo-secure-storage`, `aes-js` and `react-native-get-random-values` libraries up-to-date.
  * Choose the correct [`SecureStoreOptions`](https://docs.expo.dev/versions/latest/sdk/securestore/#securestoreoptions) for your app's needs. E.g. [`SecureStore.WHEN_UNLOCKED`](https://docs.expo.dev/versions/latest/sdk/securestore/#securestorewhen_unlocked) regulates when the data can be accessed.
  * Carefully consider optimizations or other modifications to the above example, as those can lead to introducing subtle security vulnerabilities.

Install the necessary dependencies in the root of your Expo project:

`  

_10

npm install @supabase/supabase-js

_10

npm install @rneui/themed @react-native-async-storage/async-storage react-
native-url-polyfill

_10

npm install aes-js react-native-get-random-values

_10

npx expo install expo-secure-store

  
`

Implement a `LargeSecureStore` class to pass in as Auth storage for the
`supabase-js` client:

lib/supabase.ts

`  

_69

import 'react-native-url-polyfill/auto'

_69

import { createClient } from '@supabase/supabase-js'

_69

import AsyncStorage from '@react-native-async-storage/async-storage'

_69

import * as SecureStore from 'expo-secure-store'

_69

import * as aesjs from 'aes-js'

_69

import 'react-native-get-random-values'

_69

_69

// As Expo's SecureStore does not support values larger than 2048

_69

// bytes, an AES-256 key is generated and stored in SecureStore, while

_69

// it is used to encrypt/decrypt values stored in AsyncStorage.

_69

class LargeSecureStore {

_69

private async _encrypt(key: string, value: string) {

_69

const encryptionKey = crypto.getRandomValues(new Uint8Array(256 / 8))

_69

_69

const cipher = new aesjs.ModeOfOperation.ctr(encryptionKey, new
aesjs.Counter(1))

_69

const encryptedBytes = cipher.encrypt(aesjs.utils.utf8.toBytes(value))

_69

_69

await SecureStore.setItemAsync(key, aesjs.utils.hex.fromBytes(encryptionKey))

_69

_69

return aesjs.utils.hex.fromBytes(encryptedBytes)

_69

}

_69

_69

private async _decrypt(key: string, value: string) {

_69

const encryptionKeyHex = await SecureStore.getItemAsync(key)

_69

if (!encryptionKeyHex) {

_69

return encryptionKeyHex

_69

}

_69

_69

const cipher = new aesjs.ModeOfOperation.ctr(

_69

aesjs.utils.hex.toBytes(encryptionKeyHex),

_69

new aesjs.Counter(1)

_69

)

_69

const decryptedBytes = cipher.decrypt(aesjs.utils.hex.toBytes(value))

_69

_69

return aesjs.utils.utf8.fromBytes(decryptedBytes)

_69

}

_69

_69

async getItem(key: string) {

_69

const encrypted = await AsyncStorage.getItem(key)

_69

if (!encrypted) {

_69

return encrypted

_69

}

_69

_69

return await this._decrypt(key, encrypted)

_69

}

_69

_69

async removeItem(key: string) {

_69

await AsyncStorage.removeItem(key)

_69

await SecureStore.deleteItemAsync(key)

_69

}

_69

_69

async setItem(key: string, value: string) {

_69

const encrypted = await this._encrypt(key, value)

_69

_69

await AsyncStorage.setItem(key, encrypted)

_69

}

_69

}

_69

_69

const supabaseUrl = YOUR_REACT_NATIVE_SUPABASE_URL

_69

const supabaseAnonKey = YOUR_REACT_NATIVE_SUPABASE_ANON_KEY

_69

_69

const supabase = createClient(supabaseUrl, supabaseAnonKey, {

_69

auth: {

_69

storage: new LargeSecureStore(),

_69

autoRefreshToken: true,

_69

persistSession: true,

_69

detectSessionInUrl: false,

_69

},

_69

})

  
`

## Email and password authentication in React Native#

Once we've set up the storage mechanism, building an email and password sign
in flow becomes pretty straight forward. Install
[`@rneui/themed`](https://reactnativeelements.com/) to get some nice cross
platform button and input fields:

`  

_10

npm install @rneui/themed

  
`

Set up a simple email form component:

components/EmailForm.tsx

`  

_83

import React, { useState } from 'react'

_83

import { Alert, StyleSheet, View } from 'react-native'

_83

import { supabase } from '../lib/supabase'

_83

import { Button, Input } from '@rneui/themed'

_83

_83

export default function EmailForm() {

_83

const [email, setEmail] = useState('')

_83

const [password, setPassword] = useState('')

_83

const [loading, setLoading] = useState(false)

_83

_83

async function signInWithEmail() {

_83

setLoading(true)

_83

const { error } = await supabase.auth.signInWithPassword({

_83

email: email,

_83

password: password,

_83

})

_83

_83

if (error) Alert.alert(error.message)

_83

setLoading(false)

_83

}

_83

_83

async function signUpWithEmail() {

_83

setLoading(true)

_83

const {

_83

data: { session },

_83

error,

_83

} = await supabase.auth.signUp({

_83

email: email,

_83

password: password,

_83

})

_83

_83

if (error) Alert.alert(error.message)

_83

if (!session) Alert.alert('Please check your inbox for email verification!')

_83

setLoading(false)

_83

}

_83

_83

return (

_83

<View style={styles.container}>

_83

<View style={[styles.verticallySpaced, styles.mt20]}>

_83

<Input

_83

label="Email"

_83

leftIcon={{ type: 'font-awesome', name: 'envelope' }}

_83

onChangeText={(text) => setEmail(text)}

_83

value={email}

_83

placeholder="[[email protected]](/cdn-cgi/l/email-protection)"

_83

autoCapitalize={'none'}

_83

/>

_83

</View>

_83

<View style={styles.verticallySpaced}>

_83

<Input

_83

label="Password"

_83

leftIcon={{ type: 'font-awesome', name: 'lock' }}

_83

onChangeText={(text) => setPassword(text)}

_83

value={password}

_83

secureTextEntry={true}

_83

placeholder="Password"

_83

autoCapitalize={'none'}

_83

/>

_83

</View>

_83

<View style={[styles.verticallySpaced, styles.mt20]}>

_83

<Button title="Sign in" disabled={loading} onPress={() => signInWithEmail()}
/>

_83

</View>

_83

<View style={styles.verticallySpaced}>

_83

<Button title="Sign up" disabled={loading} onPress={() => signUpWithEmail()}
/>

_83

</View>

_83

</View>

_83

)

_83

}

_83

_83

const styles = StyleSheet.create({

_83

container: {

_83

marginTop: 40,

_83

padding: 12,

_83

},

_83

verticallySpaced: {

_83

paddingTop: 4,

_83

paddingBottom: 4,

_83

alignSelf: 'stretch',

_83

},

_83

mt20: {

_83

marginTop: 20,

_83

},

_83

})

  
`

Note, by default Supabase Auth requires email verification before a session is
created for the users. To support email verification you need to implement
deep link handling which is outlined in the next section.

While testing, you can disable email confirmation in your [project's email
auth provider settings](/dashboard/project/_/auth/providers).

## OAuth, magic links and deep-linking#

As you saw above, we specified `detectSessionInUrl: false` when initializing
supabase-js. By default, in a web based environment, supabase-js will
automatically detect OAuth and magic link redirects and create the user
session.

In native mobile apps, however, OAuth callbacks require a bit more
configuration and the setup of [deep linking](/docs/guides/auth/native-mobile-
deep-linking).

To link to your development build or standalone app, you need to specify a
custom URL scheme for your app. You can register a scheme in your app config
(app.json, app.config.js) by adding a string under the `scheme` key:

`  

_10

{

_10

"expo": {

_10

"scheme": "com.supabase"

_10

}

_10

}

  
`

In your project's [auth
settings](https://supabase.com/dashboard/project/_/auth/url-configuration) add
the redirect URL, e.g. `com.supabase://**`.

Finally, implement the OAuth and linking handlers. See the [supabase-js
reference](/docs/reference/javascript/initializing?example=react-native-
options-async-storage) for instructions on initializing the supabase-js client
in React Native.

./components/Auth.tsx

`  

_68

import { Button } from 'react-native'

_68

import { makeRedirectUri } from 'expo-auth-session'

_68

import * as QueryParams from 'expo-auth-session/build/QueryParams'

_68

import * as WebBrowser from 'expo-web-browser'

_68

import * as Linking from 'expo-linking'

_68

import { supabase } from 'app/utils/supabase'

_68

_68

WebBrowser.maybeCompleteAuthSession() // required for web only

_68

const redirectTo = makeRedirectUri()

_68

_68

const createSessionFromUrl = async (url: string) => {

_68

const { params, errorCode } = QueryParams.getQueryParams(url)

_68

_68

if (errorCode) throw new Error(errorCode)

_68

const { access_token, refresh_token } = params

_68

_68

if (!access_token) return

_68

_68

const { data, error } = await supabase.auth.setSession({

_68

access_token,

_68

refresh_token,

_68

})

_68

if (error) throw error

_68

return data.session

_68

}

_68

_68

const performOAuth = async () => {

_68

const { data, error } = await supabase.auth.signInWithOAuth({

_68

provider: 'github',

_68

options: {

_68

redirectTo,

_68

skipBrowserRedirect: true,

_68

},

_68

})

_68

if (error) throw error

_68

_68

const res = await WebBrowser.openAuthSessionAsync(data?.url ?? '', redirectTo)

_68

_68

if (res.type === 'success') {

_68

const { url } = res

_68

await createSessionFromUrl(url)

_68

}

_68

}

_68

_68

const sendMagicLink = async () => {

_68

const { error } = await supabase.auth.signInWithOtp({

_68

email: '[[email protected]](/cdn-cgi/l/email-protection)',

_68

options: {

_68

emailRedirectTo: redirectTo,

_68

},

_68

})

_68

_68

if (error) throw error

_68

// Email sent.

_68

}

_68

_68

export default function Auth() {

_68

// Handle linking into app from email app.

_68

const url = Linking.useURL()

_68

if (url) createSessionFromUrl(url)

_68

_68

return (

_68

<>

_68

<Button onPress={performOAuth} title="Sign in with Github" />

_68

<Button onPress={sendMagicLink} title="Send Magic Link" />

_68

</>

_68

)

_68

}

  
`

For the best user experience, it is recommended to use universal links which
require a more elaborate setup. You can find the detailed setup instructions
in the [Expo docs](https://docs.expo.dev/guides/deep-linking/).

## Native mobile login mechanisms#

Some native mobile operating systems, like iOS and Android, offer a built-in
identity provider for convenient user authentication.

For iOS, apps that use a third-party or social login service to set up or
authenticate the user’s primary account with the app must also offer Sign in
with Apple as an equivalent option.

There are several benefits and reasons why you might want to add social login
to your applications:

  * **Improved user experience** : Users can register and log in to your application using their existing app store accounts, which can be faster and more convenient than creating a new account from scratch. This makes it easier for users to access your application, improving their overall experience.

  * **Better user engagement** : You can access additional data and insights about your users, such as their interests, demographics, and social connections. This can help you tailor your content and marketing efforts to better engage with your users and provide a more personalized experience.

  * **Increased security** : Social login can improve the security of your application by leveraging the security measures and authentication protocols of the social media platforms that your users are logging in with. This can help protect against unauthorized access and account takeovers.

### Sign in with Apple#

Supabase Auth supports using [Sign in with
Apple](https://developer.apple.com/sign-in-with-apple/) on the web and in
native apps for iOS, macOS, watchOS, or tvOS.

For detailed setup and implementation instructions please refer to the
[docs](https://supabase.com/docs/guides/auth/social-login/auth-apple) and the
[video tutorial](https://youtu.be/-tpcZzTdvN0).

### Sign in with Google#

Supabase Auth supports Sign in with Google on the web, native Android
applications, and Chrome extensions.

For detailed set up and implementation instructions please refer to the
[docs](https://supabase.com/docs/guides/auth/social-login/auth-google) and the
[video tutorial](https://youtu.be/vojHmGUGUGc).

## One time passwords#

Supabase supports various forms of passwordless authentication:

  * [Email Magic Link](/docs/guides/auth/passwordless-login/auth-magic-link)
  * [Email one-time password (OTP)](/docs/guides/auth/passwordless-login/auth-email-otp)
  * [SMS & WhatsApp one-time password (OTP)](/docs/guides/auth/phone-login) (watch the [video tutorial](https://youtu.be/Hca4CKE17I0?feature=shared))

Passwordless login mechanisms have similar benefits as the native mobile login
options mentioned above.

## Conclusion#

In this post, we learned various authentication mechanisms we can use in React
Native applications to provide a delightful experience for our users across
native mobile and web.

## More React Native and Supabase resources#

  * [Watch our React Native video tutorials](https://youtube.com/playlist?list=PL5S4mPUpp4OsrbRTx21k34aACOgpqQGlx&si=Ez-0S4QhBxtayYsq)
  * [React Native file upload with Supabase Storage](/blog/react-native-storage)
  * [Offline-first React Native Apps with WatermelonDB](/blog/react-native-offline-first-watermelon-db)
  * [Send push notifications from edge functions](/docs/guides/functions/examples/push-notifications)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Freact-
native-
authentication&text=Getting%20started%20with%20React%20Native%20authentication)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Freact-
native-
authentication&text=Getting%20started%20with%20React%20Native%20authentication)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Freact-
native-
authentication&t=Getting%20started%20with%20React%20Native%20authentication)

[Last postGitHub OAuth in your Python Flask app21 November
2023](/blog/oauth2-login-python-flask-apps)

[Next postSupabase Beta October 20236 November 2023](/blog/beta-update-
october-2023)

[react-native](/blog/tags/react-native)[auth](/blog/tags/auth)

On this page

  * Prerequisites
  * Set up supabase-js for React Native
    * Install supabase-js and dependencies
    * Authentication storage
    * Encrypting the user session
  * Email and password authentication in React Native
  * OAuth, magic links and deep-linking
  * Native mobile login mechanisms
    * Sign in with Apple
    * Sign in with Google
  * One time passwords
  * Conclusion
  * More React Native and Supabase resources

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Freact-
native-
authentication&text=Getting%20started%20with%20React%20Native%20authentication)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Freact-
native-
authentication&text=Getting%20started%20with%20React%20Native%20authentication)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Freact-
native-
authentication&t=Getting%20started%20with%20React%20Native%20authentication)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

