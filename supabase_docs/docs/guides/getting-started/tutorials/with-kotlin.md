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
  4.   5. [Android Kotlin](/docs/guides/getting-started/tutorials/with-kotlin)
  6. 

# Build a Product Management Android App with Jetpack Compose

* * *

This tutorial demonstrates how to build a basic product management app. The
app demonstrates management operations, photo upload, account creation and
authentication using:

  * [Supabase Database](/docs/guides/database) \- a Postgres database for storing your user data and [Row Level Security](/docs/guides/auth#row-level-security) so data is protected and users can only access their own information.
  * [Supabase Auth](/docs/guides/auth) \- users log in through magic links sent to their email (without having to set up a password).
  * [Supabase Storage](/docs/guides/storage) \- users can upload a profile photo.

![manage-product-cover](/docs/img/guides/kotlin/manage-product-cover.png)

If you get stuck while working through this guide, refer to the [full example
on GitHub](https://github.com/hieuwu/product-sample-supabase-kt).

## Project setup#

Before we start building we're going to set up our Database and API. This is
as simple as starting a new Project in Supabase and then creating a "schema"
inside the database.

### Create a project#

  1. [Create a new project](https://app.supabase.com) in the Supabase Dashboard.
  2. Enter your project details.
  3. Wait for the new database to launch.

### Set up the database schema#

Now we are going to set up the database schema. You can just copy/paste the
SQL from below and run it yourself.

SQL

`  

_32

-- Create a table for public profiles

_32

_32

create table

_32

public.products (

_32

id uuid not null default gen_random_uuid (),

_32

name text not null,

_32

price real not null,

_32

image text null,

_32

constraint products_pkey primary key (id)

_32

) tablespace pg_default;

_32

_32

-- Set up Storage!

_32

insert into storage.buckets (id, name)

_32

values ('Product Image', 'Product Image');

_32

_32

-- Set up access controls for storage.

_32

-- See https://supabase.com/docs/guides/storage/security/access-
control#policy-examples for more details.

_32

CREATE POLICY "Enable read access for all users" ON "storage"."objects"

_32

AS PERMISSIVE FOR SELECT

_32

TO public

_32

USING (true)

_32

_32

CREATE POLICY "Enable insert for all users" ON "storage"."objects"

_32

AS PERMISSIVE FOR INSERT

_32

TO authenticated, anon

_32

WITH CHECK (true)

_32

_32

CREATE POLICY "Enable update for all users" ON "storage"."objects"

_32

AS PERMISSIVE FOR UPDATE

_32

TO public

_32

USING (true)

_32

WITH CHECK (true)

  
`

### Get the API Keys#

Now that you've created some database tables, you are ready to insert data
using the auto-generated API. We just need to get the Project URL and `anon`
key from the API settings.

  1. Go to the [API Settings](https://app.supabase.com/project/_/settings/api) page in the Dashboard.
  2. Find your Project `URL`, `anon`, and `service_role` keys on this page.

### Set up Google Authentication#

From the [Google Console](https://console.developers.google.com/apis/library),
create a new project and add OAuth2 credentials.

![Create Google OAuth credentials](/docs/img/guides/kotlin/google-cloud-oauth-
credentials-create.png)

In your [Supabase Auth
settings](https://app.supabase.com/project/_/auth/providers) enable Google as
a provider and set the required credentials as outlined in the [auth
docs](/docs/guides/auth/social-login/auth-google).

## Building the app#

### Create new Android project#

Open Android Studio > New Project > Base Activity (Jetpack Compose).

![Android Studio new project](/docs/img/guides/kotlin/android-studio-new-
project.png)

### Set up API key and secret securely#

#### Create local environment secret#

Create or edit the `local.properties` file at the root (same level as
`build.gradle`) of your project.

> **Note** : Do not commit this file to your source control, for example, by
> adding it to your `.gitignore` file!

`  

_10

SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY

_10

SUPABASE_URL=YOUR_SUPABASE_URL

  
`

#### Read and set value to `BuildConfig`#

In your `build.gradle` (app) file, create a `Properties` object and read the
values from your `local.properties` file by calling the `buildConfigField`
method:

`  

_15

defaultConfig {

_15

applicationId "com.example.manageproducts"

_15

minSdkVersion 22

_15

targetSdkVersion 33

_15

versionCode 5

_15

versionName "1.0"

_15

testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"

_15

_15

// Set value part

_15

Properties properties = new Properties()

_15

properties.load(project.rootProject.file("local.properties").newDataInputStream())

_15

buildConfigField("String", "SUPABASE_ANON_KEY",
"\"${properties.getProperty("SUPABASE_ANON_KEY")}\"")

_15

buildConfigField("String", "SECRET",
"\"${properties.getProperty("SECRET")}\"")

_15

buildConfigField("String", "SUPABASE_URL",
"\"${properties.getProperty("SUPABASE_URL")}\"")

_15

}

  
`

#### Use value from `BuildConfig`#

Read the value from `BuildConfig`:

`  

_10

val url = BuildConfig.SUPABASE_URL

_10

val apiKey = BuildConfig.SUPABASE_ANON_KEY

  
`

### Set up Supabase dependencies#

![Gradle dependencies](/docs/img/guides/kotlin/gradle-dependencies.png)

In the `build.gradle` (app) file, add these dependencies then press "Sync
now." Replace the dependency version placeholders `$supabase_version` and
`$ktor_version` with their respective latest versions.

`  

_10

implementation "io.github.jan-tennert.supabase:postgrest-kt:$supabase_version"

_10

implementation "io.github.jan-tennert.supabase:storage-kt:$supabase_version"

_10

implementation "io.github.jan-tennert.supabase:auth-kt:$supabase_version"

_10

implementation "io.ktor:ktor-client-android:$ktor_version"

_10

implementation "io.ktor:ktor-client-core:$ktor_version"

_10

implementation "io.ktor:ktor-utils:$ktor_version"

  
`

Also in the `build.gradle` (app) file, add the plugin for serialization. The
version of this plugin should be the same as your Kotlin version.

`  

_10

plugins {

_10

...

_10

id 'org.jetbrains.kotlin.plugin.serialization' version '$kotlin_version'

_10

...

_10

}

  
`

### Set up Hilt for dependency injection#

In the `build.gradle` (app) file, add the following:

`  

_10

implementation "com.google.dagger:hilt-android:$hilt_version"

_10

annotationProcessor "com.google.dagger:hilt-compiler:$hilt_version"

_10

implementation("androidx.hilt:hilt-navigation-compose:1.0.0")

  
`

Create a new `ManageProductApplication.kt` class extending Application with
`@HiltAndroidApp` annotation:

`  

_10

// ManageProductApplication.kt

_10

@HiltAndroidApp

_10

class ManageProductApplication: Application()

  
`

Open the `AndroidManifest.xml` file, update name property of Application tag:

`  

_10

<application

_10

...

_10

android:name=".ManageProductApplication"

_10

...

_10

</application>

  
`

Create the `MainActivity`:

`  

_10

@AndroidEntryPoint

_10

class MainActivity : ComponentActivity() {

_10

//This will come later

_10

}

  
`

### Provide Supabase instances with Hilt#

To make the app easier to test, create a `SupabaseModule.kt` file as follows:

`  

_41

@InstallIn(SingletonComponent::class)

_41

@Module

_41

object SupabaseModule {

_41

_41

@Provides

_41

@Singleton

_41

fun provideSupabaseClient(): SupabaseClient {

_41

return createSupabaseClient(

_41

supabaseUrl = BuildConfig.SUPABASE_URL,

_41

supabaseKey = BuildConfig.SUPABASE_ANON_KEY

_41

) {

_41

install(Postgrest)

_41

install(Auth) {

_41

flowType = FlowType.PKCE

_41

scheme = "app"

_41

host = "supabase.com"

_41

}

_41

install(Storage)

_41

}

_41

}

_41

_41

@Provides

_41

@Singleton

_41

fun provideSupabaseDatabase(client: SupabaseClient): Postgrest {

_41

return client.postgrest

_41

}

_41

_41

@Provides

_41

@Singleton

_41

fun provideSupabaseAuth(client: SupabaseClient): Auth {

_41

return client.auth

_41

}

_41

_41

_41

@Provides

_41

@Singleton

_41

fun provideSupabaseStorage(client: SupabaseClient): Storage {

_41

return client.storage

_41

}

_41

_41

}

  
`

### Create a data transfer object#

Create a `ProductDto.kt` class and use annotations to parse data from
Supabase:

`  

_15

@Serializable

_15

data class ProductDto(

_15

_15

@SerialName("name")

_15

val name: String,

_15

_15

@SerialName("price")

_15

val price: Double,

_15

_15

@SerialName("image")

_15

val image: String?,

_15

_15

@SerialName("id")

_15

val id: String,

_15

)

  
`

Create a Domain object in `Product.kt` expose the data in your view:

`  

_10

data class Product(

_10

val id: String,

_10

val name: String,

_10

val price: Double,

_10

val image: String?

_10

)

  
`

### Implement repositories#

Create a `ProductRepository` interface and its implementation named
`ProductRepositoryImpl`. This holds the logic to interact with data sources
from Supabase. Do the same with the `AuthenticationRepository`.

Create the Product Repository:

`  

_10

interface ProductRepository {

_10

suspend fun createProduct(product: Product): Boolean

_10

suspend fun getProducts(): List<ProductDto>?

_10

suspend fun getProduct(id: String): ProductDto

_10

suspend fun deleteProduct(id: String)

_10

suspend fun updateProduct(

_10

id: String, name: String, price: Double, imageName: String, imageFile:
ByteArray

_10

)

_10

}

  
`

`  

_91

class ProductRepositoryImpl @Inject constructor(

_91

private val postgrest: Postgrest,

_91

private val storage: Storage,

_91

) : ProductRepository {

_91

override suspend fun createProduct(product: Product): Boolean {

_91

return try {

_91

withContext(Dispatchers.IO) {

_91

val productDto = ProductDto(

_91

name = product.name,

_91

price = product.price,

_91

)

_91

postgrest.from("products").insert(productDto)

_91

true

_91

}

_91

true

_91

} catch (e: java.lang.Exception) {

_91

throw e

_91

}

_91

}

_91

_91

override suspend fun getProducts(): List<ProductDto>? {

_91

return withContext(Dispatchers.IO) {

_91

val result = postgrest.from("products")

_91

.select().decodeList<ProductDto>()

_91

result

_91

}

_91

}

_91

_91

_91

override suspend fun getProduct(id: String): ProductDto {

_91

return withContext(Dispatchers.IO) {

_91

postgrest.from("products").select {

_91

filter {

_91

eq("id", id)

_91

}

_91

}.decodeSingle<ProductDto>()

_91

}

_91

}

_91

_91

override suspend fun deleteProduct(id: String) {

_91

return withContext(Dispatchers.IO) {

_91

postgrest.from("products").delete {

_91

filter {

_91

eq("id", id)

_91

}

_91

}

_91

}

_91

}

_91

_91

override suspend fun updateProduct(

_91

id: String,

_91

name: String,

_91

price: Double,

_91

imageName: String,

_91

imageFile: ByteArray

_91

) {

_91

withContext(Dispatchers.IO) {

_91

if (imageFile.isNotEmpty()) {

_91

val imageUrl =

_91

storage.from("Product%20Image").upload(

_91

path = "$imageName.png",

_91

data = imageFile,

_91

upsert = true

_91

)

_91

postgrest.from("products").update({

_91

set("name", name)

_91

set("price", price)

_91

set("image", buildImageUrl(imageFileName = imageUrl))

_91

}) {

_91

filter {

_91

eq("id", id)

_91

}

_91

}

_91

} else {

_91

postgrest.from("products").update({

_91

set("name", name)

_91

set("price", price)

_91

}) {

_91

filter {

_91

eq("id", id)

_91

}

_91

}

_91

}

_91

}

_91

}

_91

_91

// Because I named the bucket as "Product Image" so when it turns to an url,
it is "%20"

_91

// For better approach, you should create your bucket name without space
symbol

_91

private fun buildImageUrl(imageFileName: String) =

_91

"${BuildConfig.SUPABASE_URL}/storage/v1/object/public/${imageFileName}".replace("
", "%20")

_91

}

  
`

Create the Authentication Repository:

`  

_10

interface AuthenticationRepository {

_10

suspend fun signIn(email: String, password: String): Boolean

_10

suspend fun signUp(email: String, password: String): Boolean

_10

suspend fun signInWithGoogle(): Boolean

_10

}

  
`

`  

_36

class AuthenticationRepositoryImpl @Inject constructor(

_36

private val auth: Auth

_36

) : AuthenticationRepository {

_36

override suspend fun signIn(email: String, password: String): Boolean {

_36

return try {

_36

auth.signInWith(Email) {

_36

this.email = email

_36

this.password = password

_36

}

_36

true

_36

} catch (e: Exception) {

_36

false

_36

}

_36

}

_36

_36

override suspend fun signUp(email: String, password: String): Boolean {

_36

return try {

_36

auth.signUpWith(Email) {

_36

this.email = email

_36

this.password = password

_36

}

_36

true

_36

} catch (e: Exception) {

_36

false

_36

}

_36

}

_36

_36

override suspend fun signInWithGoogle(): Boolean {

_36

return try {

_36

auth.signInWith(Google)

_36

true

_36

} catch (e: Exception) {

_36

false

_36

}

_36

}

_36

}

  
`

### Implement screens#

To navigate screens, use the AndroidX navigation library. For routes,
implement a `Destination` interface:

`  

_36

_36

interface Destination {

_36

val route: String

_36

val title: String

_36

}

_36

_36

_36

object ProductListDestination : Destination {

_36

override val route = "product_list"

_36

override val title = "Product List"

_36

}

_36

_36

object ProductDetailsDestination : Destination {

_36

override val route = "product_details"

_36

override val title = "Product Details"

_36

const val productId = "product_id"

_36

val arguments = listOf(navArgument(name = productId) {

_36

type = NavType.StringType

_36

})

_36

fun createRouteWithParam(productId: String) = "$route/${productId}"

_36

}

_36

_36

object AddProductDestination : Destination {

_36

override val route = "add_product"

_36

override val title = "Add Product"

_36

}

_36

_36

object AuthenticationDestination: Destination {

_36

override val route = "authentication"

_36

override val title = "Authentication"

_36

}

_36

_36

object SignUpDestination: Destination {

_36

override val route = "signup"

_36

override val title = "Sign Up"

_36

}

  
`

This will help later for navigating between screens.

Create a `ProductListViewModel`:

`  

_45

@HiltViewModel

_45

class ProductListViewModel @Inject constructor(

_45

private val productRepository: ProductRepository,

_45

) : ViewModel() {

_45

_45

private val _productList = MutableStateFlow<List<Product>?>(listOf())

_45

val productList: Flow<List<Product>?> = _productList

_45

_45

_45

private val _isLoading = MutableStateFlow(false)

_45

val isLoading: Flow<Boolean> = _isLoading

_45

_45

init {

_45

getProducts()

_45

}

_45

_45

fun getProducts() {

_45

viewModelScope.launch {

_45

val products = productRepository.getProducts()

_45

_productList.emit(products?.map { it -> it.asDomainModel() })

_45

}

_45

}

_45

_45

fun removeItem(product: Product) {

_45

viewModelScope.launch {

_45

val newList = mutableListOf<Product>().apply { _productList.value?.let {
addAll(it) } }

_45

newList.remove(product)

_45

_productList.emit(newList.toList())

_45

// Call api to remove

_45

productRepository.deleteProduct(id = product.id)

_45

// Then fetch again

_45

getProducts()

_45

}

_45

}

_45

_45

private fun ProductDto.asDomainModel(): Product {

_45

return Product(

_45

id = this.id,

_45

name = this.name,

_45

price = this.price,

_45

image = this.image

_45

)

_45

}

_45

_45

}

  
`

Create the `ProductListScreen.kt`:

`  

_113

@OptIn(ExperimentalMaterial3Api::class, ExperimentalMaterialApi::class)

_113

@Composable

_113

fun ProductListScreen(

_113

modifier: Modifier = Modifier,

_113

navController: NavController,

_113

viewModel: ProductListViewModel = hiltViewModel(),

_113

) {

_113

val isLoading by viewModel.isLoading.collectAsState(initial = false)

_113

val swipeRefreshState = rememberSwipeRefreshState(isRefreshing = isLoading)

_113

SwipeRefresh(state = swipeRefreshState, onRefresh = { viewModel.getProducts()
}) {

_113

Scaffold(

_113

topBar = {

_113

TopAppBar(

_113

backgroundColor = MaterialTheme.colorScheme.primary,

_113

title = {

_113

Text(

_113

text = stringResource(R.string.product_list_text_screen_title),

_113

color = MaterialTheme.colorScheme.onPrimary,

_113

)

_113

},

_113

)

_113

},

_113

floatingActionButton = {

_113

AddProductButton(onClick = {
navController.navigate(AddProductDestination.route) })

_113

}

_113

) { padding ->

_113

val productList = viewModel.productList.collectAsState(initial =
listOf()).value

_113

if (!productList.isNullOrEmpty()) {

_113

LazyColumn(

_113

modifier = modifier.padding(padding),

_113

contentPadding = PaddingValues(5.dp)

_113

) {

_113

itemsIndexed(

_113

items = productList,

_113

key = { _, product -> product.name }) { _, item ->

_113

val state = rememberDismissState(

_113

confirmStateChange = {

_113

if (it == DismissValue.DismissedToStart) {

_113

// Handle item removed

_113

viewModel.removeItem(item)

_113

}

_113

true

_113

}

_113

)

_113

SwipeToDismiss(

_113

state = state,

_113

background = {

_113

val color by animateColorAsState(

_113

targetValue = when (state.dismissDirection) {

_113

DismissDirection.StartToEnd -> MaterialTheme.colorScheme.primary

_113

DismissDirection.EndToStart -> MaterialTheme.colorScheme.primary.copy(

_113

alpha = 0.2f

_113

)

_113

null -> Color.Transparent

_113

}

_113

)

_113

Box(

_113

modifier = modifier

_113

.fillMaxSize()

_113

.background(color = color)

_113

.padding(16.dp),

_113

) {

_113

Icon(

_113

imageVector = Icons.Filled.Delete,

_113

contentDescription = null,

_113

tint = MaterialTheme.colorScheme.primary,

_113

modifier = modifier.align(Alignment.CenterEnd)

_113

)

_113

}

_113

_113

},

_113

dismissContent = {

_113

ProductListItem(

_113

product = item,

_113

modifier = modifier,

_113

onClick = {

_113

navController.navigate(

_113

ProductDetailsDestination.createRouteWithParam(

_113

item.id

_113

)

_113

)

_113

},

_113

)

_113

},

_113

directions = setOf(DismissDirection.EndToStart),

_113

)

_113

}

_113

}

_113

} else {

_113

Text("Product list is empty!")

_113

}

_113

_113

}

_113

}

_113

}

_113

_113

@Composable

_113

private fun AddProductButton(

_113

modifier: Modifier = Modifier,

_113

onClick: () -> Unit,

_113

) {

_113

FloatingActionButton(

_113

modifier = modifier,

_113

onClick = onClick,

_113

containerColor = MaterialTheme.colorScheme.primary,

_113

contentColor = MaterialTheme.colorScheme.onPrimary

_113

) {

_113

Icon(

_113

imageVector = Icons.Filled.Add,

_113

contentDescription = null,

_113

)

_113

}

_113

}

  
`

Create the `ProductDetailsViewModel.kt`:

`  

_68

_68

@HiltViewModel

_68

class ProductDetailsViewModel @Inject constructor(

_68

private val productRepository: ProductRepository,

_68

savedStateHandle: SavedStateHandle,

_68

) : ViewModel() {

_68

_68

private val _product = MutableStateFlow<Product?>(null)

_68

val product: Flow<Product?> = _product

_68

_68

private val _name = MutableStateFlow("")

_68

val name: Flow<String> = _name

_68

_68

private val _price = MutableStateFlow(0.0)

_68

val price: Flow<Double> = _price

_68

_68

private val _imageUrl = MutableStateFlow("")

_68

val imageUrl: Flow<String> = _imageUrl

_68

_68

init {

_68

val productId =
savedStateHandle.get<String>(ProductDetailsDestination.productId)

_68

productId?.let {

_68

getProduct(productId = it)

_68

}

_68

}

_68

_68

private fun getProduct(productId: String) {

_68

viewModelScope.launch {

_68

val result = productRepository.getProduct(productId).asDomainModel()

_68

_product.emit(result)

_68

_name.emit(result.name)

_68

_price.emit(result.price)

_68

}

_68

}

_68

_68

fun onNameChange(name: String) {

_68

_name.value = name

_68

}

_68

_68

fun onPriceChange(price: Double) {

_68

_price.value = price

_68

}

_68

_68

fun onSaveProduct(image: ByteArray) {

_68

viewModelScope.launch {

_68

productRepository.updateProduct(

_68

id = _product.value?.id,

_68

price = _price.value,

_68

name = _name.value,

_68

imageFile = image,

_68

imageName = "image_${_product.value.id}",

_68

)

_68

}

_68

}

_68

_68

fun onImageChange(url: String) {

_68

_imageUrl.value = url

_68

}

_68

_68

private fun ProductDto.asDomainModel(): Product {

_68

return Product(

_68

id = this.id,

_68

name = this.name,

_68

price = this.price,

_68

image = this.image

_68

)

_68

}

_68

}

  
`

Create the `ProductDetailsScreen.kt`:

`  

_167

@OptIn(ExperimentalCoilApi::class)

_167

@SuppressLint("UnusedMaterialScaffoldPaddingParameter")

_167

@Composable

_167

fun ProductDetailsScreen(

_167

modifier: Modifier = Modifier,

_167

viewModel: ProductDetailsViewModel = hiltViewModel(),

_167

navController: NavController,

_167

productId: String?,

_167

) {

_167

val snackBarHostState = remember { SnackbarHostState() }

_167

val coroutineScope = rememberCoroutineScope()

_167

_167

Scaffold(

_167

snackbarHost = { SnackbarHost(snackBarHostState) },

_167

topBar = {

_167

TopAppBar(

_167

navigationIcon = {

_167

IconButton(onClick = {

_167

navController.navigateUp()

_167

}) {

_167

Icon(

_167

imageVector = Icons.Filled.ArrowBack,

_167

contentDescription = null,

_167

tint = MaterialTheme.colorScheme.onPrimary

_167

)

_167

}

_167

},

_167

backgroundColor = MaterialTheme.colorScheme.primary,

_167

title = {

_167

Text(

_167

text = stringResource(R.string.product_details_text_screen_title),

_167

color = MaterialTheme.colorScheme.onPrimary,

_167

)

_167

},

_167

)

_167

}

_167

) {

_167

val name = viewModel.name.collectAsState(initial = "")

_167

val price = viewModel.price.collectAsState(initial = 0.0)

_167

var imageUrl = Uri.parse(viewModel.imageUrl.collectAsState(initial =
null).value)

_167

val contentResolver = LocalContext.current.contentResolver

_167

_167

Column(

_167

modifier = modifier

_167

.padding(16.dp)

_167

.fillMaxSize()

_167

) {

_167

val galleryLauncher =

_167

rememberLauncherForActivityResult(ActivityResultContracts.GetContent())

_167

{ uri ->

_167

uri?.let {

_167

if (it.toString() != imageUrl.toString()) {

_167

viewModel.onImageChange(it.toString())

_167

}

_167

}

_167

}

_167

_167

Image(

_167

painter = rememberImagePainter(imageUrl),

_167

contentScale = ContentScale.Fit,

_167

contentDescription = null,

_167

modifier = Modifier

_167

.padding(16.dp, 8.dp)

_167

.size(100.dp)

_167

.align(Alignment.CenterHorizontally)

_167

)

_167

IconButton(modifier = modifier.align(alignment =
Alignment.CenterHorizontally),

_167

onClick = {

_167

galleryLauncher.launch("image/*")

_167

}) {

_167

Icon(

_167

imageVector = Icons.Filled.Edit,

_167

contentDescription = null,

_167

tint = MaterialTheme.colorScheme.primary

_167

)

_167

}

_167

OutlinedTextField(

_167

label = {

_167

Text(

_167

text = "Product name",

_167

color = MaterialTheme.colorScheme.primary,

_167

style = MaterialTheme.typography.titleMedium

_167

)

_167

},

_167

maxLines = 2,

_167

shape = RoundedCornerShape(32),

_167

modifier = modifier.fillMaxWidth(),

_167

value = name.value,

_167

onValueChange = {

_167

viewModel.onNameChange(it)

_167

},

_167

)

_167

Spacer(modifier = modifier.height(12.dp))

_167

OutlinedTextField(

_167

label = {

_167

Text(

_167

text = "Product price",

_167

color = MaterialTheme.colorScheme.primary,

_167

style = MaterialTheme.typography.titleMedium

_167

)

_167

},

_167

maxLines = 2,

_167

shape = RoundedCornerShape(32),

_167

modifier = modifier.fillMaxWidth(),

_167

value = price.value.toString(),

_167

keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),

_167

onValueChange = {

_167

viewModel.onPriceChange(it.toDouble())

_167

},

_167

)

_167

Spacer(modifier = modifier.weight(1f))

_167

Button(

_167

modifier = modifier.fillMaxWidth(),

_167

onClick = {

_167

if (imageUrl.host?.contains("supabase") == true) {

_167

viewModel.onSaveProduct(image = byteArrayOf())

_167

} else {

_167

val image = uriToByteArray(contentResolver, imageUrl)

_167

viewModel.onSaveProduct(image = image)

_167

}

_167

coroutineScope.launch {

_167

snackBarHostState.showSnackbar(

_167

message = "Product updated successfully !",

_167

duration = SnackbarDuration.Short

_167

)

_167

}

_167

}) {

_167

Text(text = "Save changes")

_167

}

_167

Spacer(modifier = modifier.height(12.dp))

_167

OutlinedButton(

_167

modifier = modifier

_167

.fillMaxWidth(),

_167

onClick = {

_167

navController.navigateUp()

_167

}) {

_167

Text(text = "Cancel")

_167

}

_167

_167

}

_167

_167

}

_167

}

_167

_167

_167

private fun getBytes(inputStream: InputStream): ByteArray {

_167

val byteBuffer = ByteArrayOutputStream()

_167

val bufferSize = 1024

_167

val buffer = ByteArray(bufferSize)

_167

var len = 0

_167

while (inputStream.read(buffer).also { len = it } != -1) {

_167

byteBuffer.write(buffer, 0, len)

_167

}

_167

return byteBuffer.toByteArray()

_167

}

_167

_167

_167

private fun uriToByteArray(contentResolver: ContentResolver, uri: Uri):
ByteArray {

_167

if (uri == Uri.EMPTY) {

_167

return byteArrayOf()

_167

}

_167

val inputStream = contentResolver.openInputStream(uri)

_167

if (inputStream != null) {

_167

return getBytes(inputStream)

_167

}

_167

return byteArrayOf()

_167

}

  
`

Create a AddProductScreen:

`  

_54

@SuppressLint("UnusedMaterial3ScaffoldPaddingParameter")

_54

@OptIn(ExperimentalMaterial3Api::class)

_54

@Composable

_54

fun AddProductScreen(

_54

modifier: Modifier = Modifier,

_54

navController: NavController,

_54

viewModel: AddProductViewModel = hiltViewModel(),

_54

) {

_54

Scaffold(

_54

topBar = {

_54

TopAppBar(

_54

navigationIcon = {

_54

IconButton(onClick = {

_54

navController.navigateUp()

_54

}) {

_54

Icon(

_54

imageVector = Icons.Filled.ArrowBack,

_54

contentDescription = null,

_54

tint = MaterialTheme.colorScheme.onPrimary

_54

)

_54

}

_54

},

_54

backgroundColor = MaterialTheme.colorScheme.primary,

_54

title = {

_54

Text(

_54

text = stringResource(R.string.add_product_text_screen_title),

_54

color = MaterialTheme.colorScheme.onPrimary,

_54

)

_54

},

_54

)

_54

}

_54

) { padding ->

_54

val navigateAddProductSuccess =

_54

viewModel.navigateAddProductSuccess.collectAsState(initial = null).value

_54

val isLoading =

_54

viewModel.isLoading.collectAsState(initial = null).value

_54

if (isLoading == true) {

_54

LoadingScreen(message = "Adding Product",

_54

onCancelSelected = {

_54

navController.navigateUp()

_54

})

_54

} else {

_54

SuccessScreen(

_54

message = "Product added",

_54

onMoreAction = {

_54

viewModel.onAddMoreProductSelected()

_54

},

_54

onNavigateBack = {

_54

navController.navigateUp()

_54

})

_54

}

_54

_54

}

_54

}

  
`

Create the `AddProductViewModel.kt`:

`  

_27

@HiltViewModel

_27

class AddProductViewModel @Inject constructor(

_27

private val productRepository: ProductRepository,

_27

) : ViewModel() {

_27

_27

private val _isLoading = MutableStateFlow(false)

_27

val isLoading: Flow<Boolean> = _isLoading

_27

_27

private val _showSuccessMessage = MutableStateFlow(false)

_27

val showSuccessMessage: Flow<Boolean> = _showSuccessMessage

_27

_27

fun onCreateProduct(name: String, price: Double) {

_27

if (name.isEmpty() || price <= 0) return

_27

viewModelScope.launch {

_27

_isLoading.value = true

_27

val product = Product(

_27

id = UUID.randomUUID().toString(),

_27

name = name,

_27

price = price,

_27

)

_27

productRepository.createProduct(product = product)

_27

_isLoading.value = false

_27

_showSuccessMessage.emit(true)

_27

_27

}

_27

}

_27

}

  
`

Create a `SignUpViewModel`:

`  

_28

@HiltViewModel

_28

class SignUpViewModel @Inject constructor(

_28

private val authenticationRepository: AuthenticationRepository

_28

) : ViewModel() {

_28

_28

private val _email = MutableStateFlow("")

_28

val email: Flow<String> = _email

_28

_28

private val _password = MutableStateFlow("")

_28

val password = _password

_28

_28

fun onEmailChange(email: String) {

_28

_email.value = email

_28

}

_28

_28

fun onPasswordChange(password: String) {

_28

_password.value = password

_28

}

_28

_28

fun onSignUp() {

_28

viewModelScope.launch {

_28

authenticationRepository.signUp(

_28

email = _email.value,

_28

password = _password.value

_28

)

_28

}

_28

}

_28

}

  
`

Create the `SignUpScreen.kt`:

`  

_93

@Composable

_93

fun SignUpScreen(

_93

modifier: Modifier = Modifier,

_93

navController: NavController,

_93

viewModel: SignUpViewModel = hiltViewModel()

_93

) {

_93

val snackBarHostState = remember { SnackbarHostState() }

_93

val coroutineScope = rememberCoroutineScope()

_93

Scaffold(

_93

snackbarHost = { androidx.compose.material.SnackbarHost(snackBarHostState) },

_93

topBar = {

_93

TopAppBar(

_93

navigationIcon = {

_93

IconButton(onClick = {

_93

navController.navigateUp()

_93

}) {

_93

Icon(

_93

imageVector = Icons.Filled.ArrowBack,

_93

contentDescription = null,

_93

tint = MaterialTheme.colorScheme.onPrimary

_93

)

_93

}

_93

},

_93

backgroundColor = MaterialTheme.colorScheme.primary,

_93

title = {

_93

Text(

_93

text = "Sign Up",

_93

color = MaterialTheme.colorScheme.onPrimary,

_93

)

_93

},

_93

)

_93

}

_93

) { paddingValues ->

_93

Column(

_93

modifier = modifier

_93

.padding(paddingValues)

_93

.padding(20.dp)

_93

) {

_93

val email = viewModel.email.collectAsState(initial = "")

_93

val password = viewModel.password.collectAsState()

_93

OutlinedTextField(

_93

label = {

_93

Text(

_93

text = "Email",

_93

color = MaterialTheme.colorScheme.primary,

_93

style = MaterialTheme.typography.titleMedium

_93

)

_93

},

_93

maxLines = 1,

_93

shape = RoundedCornerShape(32),

_93

modifier = modifier.fillMaxWidth(),

_93

value = email.value,

_93

onValueChange = {

_93

viewModel.onEmailChange(it)

_93

},

_93

)

_93

OutlinedTextField(

_93

label = {

_93

Text(

_93

text = "Password",

_93

color = MaterialTheme.colorScheme.primary,

_93

style = MaterialTheme.typography.titleMedium

_93

)

_93

},

_93

maxLines = 1,

_93

shape = RoundedCornerShape(32),

_93

modifier = modifier

_93

.fillMaxWidth()

_93

.padding(top = 12.dp),

_93

value = password.value,

_93

onValueChange = {

_93

viewModel.onPasswordChange(it)

_93

},

_93

)

_93

val localSoftwareKeyboardController = LocalSoftwareKeyboardController.current

_93

Button(modifier = modifier

_93

.fillMaxWidth()

_93

.padding(top = 12.dp),

_93

onClick = {

_93

localSoftwareKeyboardController?.hide()

_93

viewModel.onSignUp()

_93

coroutineScope.launch {

_93

snackBarHostState.showSnackbar(

_93

message = "Create account successfully. Sign in now!",

_93

duration = SnackbarDuration.Long

_93

)

_93

}

_93

}) {

_93

Text("Sign up")

_93

}

_93

}

_93

}

_93

}

  
`

Create a `SignInViewModel`:

`  

_35

@HiltViewModel

_35

class SignInViewModel @Inject constructor(

_35

private val authenticationRepository: AuthenticationRepository

_35

) : ViewModel() {

_35

_35

private val _email = MutableStateFlow("")

_35

val email: Flow<String> = _email

_35

_35

private val _password = MutableStateFlow("")

_35

val password = _password

_35

_35

fun onEmailChange(email: String) {

_35

_email.value = email

_35

}

_35

_35

fun onPasswordChange(password: String) {

_35

_password.value = password

_35

}

_35

_35

fun onSignIn() {

_35

viewModelScope.launch {

_35

authenticationRepository.signIn(

_35

email = _email.value,

_35

password = _password.value

_35

)

_35

}

_35

}

_35

_35

fun onGoogleSignIn() {

_35

viewModelScope.launch {

_35

authenticationRepository.signInWithGoogle()

_35

}

_35

}

_35

_35

}

  
`

Create the `SignInScreen.kt`:

`  

_110

@OptIn(ExperimentalMaterial3Api::class, ExperimentalComposeUiApi::class)

_110

@Composable

_110

fun SignInScreen(

_110

modifier: Modifier = Modifier,

_110

navController: NavController,

_110

viewModel: SignInViewModel = hiltViewModel()

_110

) {

_110

val snackBarHostState = remember { SnackbarHostState() }

_110

val coroutineScope = rememberCoroutineScope()

_110

Scaffold(

_110

snackbarHost = { androidx.compose.material.SnackbarHost(snackBarHostState) },

_110

topBar = {

_110

TopAppBar(

_110

navigationIcon = {

_110

IconButton(onClick = {

_110

navController.navigateUp()

_110

}) {

_110

Icon(

_110

imageVector = Icons.Filled.ArrowBack,

_110

contentDescription = null,

_110

tint = MaterialTheme.colorScheme.onPrimary

_110

)

_110

}

_110

},

_110

backgroundColor = MaterialTheme.colorScheme.primary,

_110

title = {

_110

Text(

_110

text = "Login",

_110

color = MaterialTheme.colorScheme.onPrimary,

_110

)

_110

},

_110

)

_110

}

_110

) { paddingValues ->

_110

Column(

_110

modifier = modifier

_110

.padding(paddingValues)

_110

.padding(20.dp)

_110

) {

_110

val email = viewModel.email.collectAsState(initial = "")

_110

val password = viewModel.password.collectAsState()

_110

androidx.compose.material.OutlinedTextField(

_110

label = {

_110

Text(

_110

text = "Email",

_110

color = MaterialTheme.colorScheme.primary,

_110

style = MaterialTheme.typography.titleMedium

_110

)

_110

},

_110

maxLines = 1,

_110

shape = RoundedCornerShape(32),

_110

modifier = modifier.fillMaxWidth(),

_110

value = email.value,

_110

onValueChange = {

_110

viewModel.onEmailChange(it)

_110

},

_110

)

_110

androidx.compose.material.OutlinedTextField(

_110

label = {

_110

Text(

_110

text = "Password",

_110

color = MaterialTheme.colorScheme.primary,

_110

style = MaterialTheme.typography.titleMedium

_110

)

_110

},

_110

maxLines = 1,

_110

shape = RoundedCornerShape(32),

_110

modifier = modifier

_110

.fillMaxWidth()

_110

.padding(top = 12.dp),

_110

value = password.value,

_110

onValueChange = {

_110

viewModel.onPasswordChange(it)

_110

},

_110

)

_110

val localSoftwareKeyboardController = LocalSoftwareKeyboardController.current

_110

Button(modifier = modifier

_110

.fillMaxWidth()

_110

.padding(top = 12.dp),

_110

onClick = {

_110

localSoftwareKeyboardController?.hide()

_110

viewModel.onGoogleSignIn()

_110

}) {

_110

Text("Sign in with Google")

_110

}

_110

Button(modifier = modifier

_110

.fillMaxWidth()

_110

.padding(top = 12.dp),

_110

onClick = {

_110

localSoftwareKeyboardController?.hide()

_110

viewModel.onSignIn()

_110

coroutineScope.launch {

_110

snackBarHostState.showSnackbar(

_110

message = "Sign in successfully !",

_110

duration = SnackbarDuration.Long

_110

)

_110

}

_110

}) {

_110

Text("Sign in")

_110

}

_110

OutlinedButton(modifier = modifier

_110

.fillMaxWidth()

_110

.padding(top = 12.dp), onClick = {

_110

navController.navigate(SignUpDestination.route)

_110

}) {

_110

Text("Sign up")

_110

}

_110

}

_110

}

_110

}

  
`

### Implement the `MainActivity`#

In the `MainActivity` you created earlier, show your newly created screens:

`  

_61

@AndroidEntryPoint

_61

class MainActivity : ComponentActivity() {

_61

@Inject

_61

lateinit var supabaseClient: SupabaseClient

_61

_61

@OptIn(ExperimentalMaterial3Api::class)

_61

override fun onCreate(savedInstanceState: Bundle?) {

_61

super.onCreate(savedInstanceState)

_61

setContent {

_61

ManageProductsTheme {

_61

// A surface container using the 'background' color from the theme

_61

val navController = rememberNavController()

_61

val currentBackStack by navController.currentBackStackEntryAsState()

_61

val currentDestination = currentBackStack?.destination

_61

Scaffold { innerPadding ->

_61

NavHost(

_61

navController,

_61

startDestination = ProductListDestination.route,

_61

Modifier.padding(innerPadding)

_61

) {

_61

composable(ProductListDestination.route) {

_61

ProductListScreen(

_61

navController = navController

_61

)

_61

}

_61

_61

composable(AuthenticationDestination.route) {

_61

SignInScreen(

_61

navController = navController

_61

)

_61

}

_61

_61

composable(SignUpDestination.route) {

_61

SignUpScreen(

_61

navController = navController

_61

)

_61

}

_61

_61

composable(AddProductDestination.route) {

_61

AddProductScreen(

_61

navController = navController

_61

)

_61

}

_61

_61

composable(

_61

route =
"${ProductDetailsDestination.route}/{${ProductDetailsDestination.productId}}",

_61

arguments = ProductDetailsDestination.arguments

_61

) { navBackStackEntry ->

_61

val productId =

_61

navBackStackEntry.arguments?.getString(ProductDetailsDestination.productId)

_61

ProductDetailsScreen(

_61

productId = productId,

_61

navController = navController,

_61

)

_61

}

_61

}

_61

}

_61

}

_61

}

_61

}

_61

}

  
`

### Create the success screen#

To handle OAuth and OTP signins, create a new activity to handle the deeplink
you set in `AndroidManifest.xml`:

`  

_40

<?xml version="1.0" encoding="utf-8"?>

_40

<manifest xmlns:android="http://schemas.android.com/apk/res/android"

_40

xmlns:tools="http://schemas.android.com/tools">

_40

<uses-permission android:name="android.permission.INTERNET" />

_40

<application

_40

android:name=".ManageProductApplication"

_40

android:allowBackup="true"

_40

android:dataExtractionRules="@xml/data_extraction_rules"

_40

android:enableOnBackInvokedCallback="true"

_40

android:fullBackupContent="@xml/backup_rules"

_40

android:icon="@mipmap/ic_launcher"

_40

android:label="@string/app_name"

_40

android:supportsRtl="true"

_40

android:theme="@style/Theme.ManageProducts"

_40

tools:targetApi="31">

_40

<activity

_40

android:name=".DeepLinkHandlerActivity"

_40

android:exported="true"

_40

android:theme="@style/Theme.ManageProducts" >

_40

<intent-filter android:autoVerify="true">

_40

<action android:name="android.intent.action.VIEW" />

_40

<category android:name="android.intent.category.DEFAULT" />

_40

<category android:name="android.intent.category.BROWSABLE" />

_40

<data

_40

android:host="supabase.com"

_40

android:scheme="app" />

_40

</intent-filter>

_40

</activity>

_40

<activity

_40

android:name=".MainActivity"

_40

android:exported="true"

_40

android:label="@string/app_name"

_40

android:theme="@style/Theme.ManageProducts">

_40

<intent-filter>

_40

<action android:name="android.intent.action.MAIN" />

_40

<category android:name="android.intent.category.LAUNCHER" />

_40

</intent-filter>

_40

</activity>

_40

</application>

_40

</manifest>

  
`

Then create the `DeepLinkHandlerActivity`:

`  

_51

@AndroidEntryPoint

_51

class DeepLinkHandlerActivity : ComponentActivity() {

_51

_51

@Inject

_51

lateinit var supabaseClient: SupabaseClient

_51

_51

private lateinit var callback: (String, String) -> Unit

_51

_51

override fun onCreate(savedInstanceState: Bundle?) {

_51

super.onCreate(savedInstanceState)

_51

supabaseClient.handleDeeplinks(intent = intent,

_51

onSessionSuccess = { userSession ->

_51

Log.d("LOGIN", "Log in successfully with user info: ${userSession.user}")

_51

userSession.user?.apply {

_51

callback(email ?: "", createdAt.toString())

_51

}

_51

})

_51

setContent {

_51

val navController = rememberNavController()

_51

val emailState = remember { mutableStateOf("") }

_51

val createdAtState = remember { mutableStateOf("") }

_51

LaunchedEffect(Unit) {

_51

callback = { email, created ->

_51

emailState.value = email

_51

createdAtState.value = created

_51

}

_51

}

_51

ManageProductsTheme {

_51

Surface(

_51

modifier = Modifier.fillMaxSize(),

_51

color = MaterialTheme.colorScheme.background

_51

) {

_51

SignInSuccessScreen(

_51

modifier = Modifier.padding(20.dp),

_51

navController = navController,

_51

email = emailState.value,

_51

createdAt = createdAtState.value,

_51

onClick = { navigateToMainApp() }

_51

)

_51

}

_51

}

_51

}

_51

}

_51

_51

private fun navigateToMainApp() {

_51

val intent = Intent(this, MainActivity::class.java).apply {

_51

flags = Intent.FLAG_ACTIVITY_CLEAR_TOP

_51

}

_51

startActivity(intent)

_51

}

_51

}

  
`

[Edit this page on GitHub
](https://github.com/supabase/supabase/blob/master/apps/docs/content/guides/getting-
started/tutorials/with-kotlin.mdx)

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

