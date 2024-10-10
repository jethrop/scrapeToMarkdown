[Back](/blog)

[Blog](/blog)

# Create a Figma Clone app with Flutter and Supabase Realtime

26 Jan 2024

•

35 minute read

[![Tyler Shukert
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fdshukertjr.png&w=96&q=75)Tyler
ShukertDevRel](https://twitter.com/dshukertjr)

![Create a Figma Clone app with Flutter and Supabase
Realtime](/_next/image?url=%2Fimages%2Fblog%2Fflutter-figma-clone%2Ffigma-
clone-og.jpg&w=3840&q=100)

Supabase has a low latency real-time communication feature called
[Broadcast](https://supabase.com/docs/guides/realtime/broadcast). With it, you
can have your clients communicate with other clients with low latencies. This
is useful for creating apps with connected experiences. Flutter has a
[CustomPainter](https://api.flutter.dev/flutter/rendering/CustomPainter-
class.html) class, which allows developers to interact with the low-level
canvas API allowing us to render virtually anything on the app. Combining
these two tools allows us to create interactive apps.

In this article, I am combining the Supabase Realtime Broadcast with Flutter’s
`CustomPainter` to create a collaborative design board app like Figma.

You can find the full code example
[here](https://github.com/supabase/supabase/tree/master/examples/realtime/flutter-
figma-clone).

## Overview of the Figma clone app#

We are building an interactive design canvas app where multiple users can
collaborate in real time. We will add the following features to the app:

  * Draw shapes such as circles or rectangles
  * Move those shapes around
  * Sync the cursor position and the design objects with other clients in real-time
  * Persist the state of the canvas in a Postgres database

Okay, Figma clone might be an overstatement. However, the point of this
article is to demonstrate how to build a collaborative app with all the
fundamental elements of a collaborative design canvas. You can take the
concepts of this app, add features, refine it, and make it as sophisticated as
Figma.

## Setting up the app#

### Create a blank Flutter application#

Let’s start by creating a blank Flutter app.

`  

_10

flutter create canvas --empty --platforms=web

  
`

`--empty` flag creates a blank Flutter project without the initial counter
template. `--platforms` specify which platform to support with this Flutter
application. Because we are working on an app that involves cursors, we are
going to focus on the web for this example, but you can certainly run the same
code on other platforms as well.

### Install the dependencies#

We will use two dependencies for this app.

  * [supabase_flutter](https://pub.dev/packages/supabase_flutter): Used to interact with the Supabase instance for real-time communication and storing canvas data.
  * [uuid](https://pub.dev/packages/uuid): Used to generate unique identifiers for each user and canvas objects. To keep this example simple, we will not add authentication, and will just assign randomly generated UUIDs to each user.

Run the following command to add the dependencies to your app.

`  

_10

flutter pub add supabase_flutter uuid

  
`

### Setup the Supabase project#

In this example, we will be using a remote Supabase instance, but if you would
like to follow along with a [local Supabase
instance](https://supabase.com/docs/guides/cli/local-development), that is
fine too.

You can head to [database.new](https://database.new) to create a new Supabase
project for free. It will only take a minute or two to set up your project
with a fully-fledged Postgres database.

Once your project is ready, run the following SQL from the SQL editor of your
dashboard to set up the table and [RLS
policies](https://supabase.com/docs/guides/auth/row-level-security) for this
app. To keep this article simple, we will not implement auth, so the policies
you see are fairly simple.

`  

_10

create table canvas_objects (

_10

id uuid primary key default gen_random_uuid() not null,

_10

"object" jsonb not null,

_10

created_at timestamp with time zone default timezone('utc'::text, now()) not
null

_10

);

_10

_10

alter table canvas_objects enable row level security;

_10

create policy select_canvas_objects on canvas_objects as permissive for select
to anon using (true);

_10

create policy insert_canvas_objects on canvas_objects as permissive for insert
to anon with check (true);

_10

create policy update_canvas_objects on canvas_objects as permissive for update
to anon using (true);

  
`

## Building the Figma clone app#

The app that we will build will have the following structure.

`  

_10

lib/

_10

├── canvas/ # A folder containing the main canvas-related files.

_10

│ ├── canvas_object.dart # Data model definitions.

_10

│ ├── canvas_page.dart # The canvas page widget.

_10

│ └── canvas_painter.dart # Custom painter definitions.

_10

├── utils/

_10

│ └── constants.dart # A file to hold Supabase Realtime specific constants

_10

└── main.dart # Entry point of the app

  
`

### Step1: Initialize Supabase#

Open the `lib/main.dart` file and add the following. You should replace the
credentials with your own from the Supabase dashboard under `settings > API`.
You should see an error with the import of the `canvas_page.dart` file, but we
will create it momentarily.

`  

_27

import 'package:canvas/canvas/canvas_page.dart';

_27

import 'package:flutter/material.dart';

_27

import 'package:supabase_flutter/supabase_flutter.dart';

_27

_27

void main() async {

_27

Supabase.initialize(

_27

// TODO: Replace the credentials with your own

_27

url: 'YOUR_SUPABASE_URL',

_27

anonKey: 'YOUR_SUPABASE_ANON_KEY',

_27

);

_27

runApp(const MyApp());

_27

}

_27

_27

final supabase = Supabase.instance.client;

_27

_27

class MyApp extends StatelessWidget {

_27

const MyApp({super.key});

_27

_27

@override

_27

Widget build(BuildContext context) {

_27

return const MaterialApp(

_27

title: 'Figma Clone',

_27

debugShowCheckedModeBanner: false,

_27

home: CanvasPage(),

_27

);

_27

}

_27

}

  
`

### Step 2: Create the constants file#

It is nice to organize the app’s constants in a file. Create
`lib/utils/constants.dart` file and add the following. These values will later
be used when we are setting up Supabase Realtime listeners.

`  

_10

abstract class Constants {

_10

/// Name of the Realtime channel

_10

static const String channelName = 'canvas';

_10

_10

/// Name of the broadcast event

_10

static const String broadcastEventName = 'canvas';

_10

}

  
`

### Step 3: Create the data model#

We will need to create data models for each of the following:

  * The cursor position of the user.
  * The objects we can draw on the canvas. Includes:
    * Circle
    * Rectangle

Create `lib/canvas/canvas_object.dart` file. The file is a bit long, so I will
break it down in each component below. Add all of the code into the
`canvas_object.dart` file as we step through them.

At the top of the file, we have an extension method to generate random colors.
One of the methods generates a random color, which will be used to set the
color of a newly created object, and the other generates a random with a seed
of a UUID, which will be used to determine the user’s cursor color.

`  

_19

import 'dart:convert';

_19

import 'dart:math';

_19

import 'dart:ui';

_19

_19

import 'package:uuid/uuid.dart';

_19

_19

/// Handy extension method to create random colors

_19

extension RandomColor on Color {

_19

static Color getRandom() {

_19

return Color((Random().nextDouble() * 0xFFFFFF).toInt()).withOpacity(1.0);

_19

}

_19

_19

/// Quick and dirty method to create a random color from the userID

_19

static Color getRandomFromId(String id) {

_19

final seed = utf8.encode(id).reduce((value, element) => value + element);

_19

return Color((Random(seed).nextDouble() * 0xFFFFFF).toInt())

_19

.withOpacity(1.0);

_19

}

_19

}

  
`

We then have the `SyncedObject` class. `SyncedObject` class is the base class
for anything that will be synced in real time, this includes both the cursor
and the objects. It has an `id` property, which will be UUID, and it has
`toJson` method, which is required to pass the object information over
Supabase’s broadcast feature.

`  

_22

/// Objects that are being synced in realtime over broadcast

_22

///

_22

/// Includes mouse cursor and design objects

_22

abstract class SyncedObject {

_22

/// UUID unique identifier of the object

_22

final String id;

_22

_22

factory SyncedObject.fromJson(Map<String, dynamic> json) {

_22

final objectType = json['object_type'];

_22

if (objectType == UserCursor.type) {

_22

return UserCursor.fromJson(json);

_22

} else {

_22

return CanvasObject.fromJson(json);

_22

}

_22

}

_22

_22

SyncedObject({

_22

required this.id,

_22

});

_22

_22

Map<String, dynamic> toJson();

_22

}

  
`

Now to sync the user’s cursor with other clients, we have the `UserCursor`
class. It inherits the `SyncedObject` class and has JSON parsing implemented.

`  

_29

/// Data model for the cursors displayed on the canvas.

_29

class UserCursor extends SyncedObject {

_29

static String type = 'cursor';

_29

_29

final Offset position;

_29

final Color color;

_29

_29

UserCursor({

_29

required super.id,

_29

required this.position,

_29

}) : color = RandomColor.getRandomFromId(id);

_29

_29

UserCursor.fromJson(Map<String, dynamic> json)

_29

: position = Offset(json['position']['x'], json['position']['y']),

_29

color = RandomColor.getRandomFromId(json['id']),

_29

super(id: json['id']);

_29

_29

@override

_29

Map<String, dynamic> toJson() {

_29

return {

_29

'object_type': type,

_29

'id': id,

_29

'position': {

_29

'x': position.dx,

_29

'y': position.dy,

_29

}

_29

};

_29

}

_29

}

  
`

There is an additional set of data that we want to sync in real-time, and that
is the individual shapes within the canvas. We create the `CanvasObject`
abstract class, which is the base class for any shapes within the canvas. This
class extends the `SyncedObject` because we want to sync it to other clients.
In addition to the `id` property, we have a `color` property, because every
shape needs a color. We also have a few methods.

  * `intersectsWith()` takes a point within the canvas and returns whether the point intersects with the shape or not. This is used when grabbing the shape on the canvas.
  * `copyWith()` is a standard method to create a copy of the instance.
  * `move()` is a method to create a version of the instance that is moved by `delta`. This will be used when the shape is being dragged on canvas.

`  

_27

/// Base model for any design objects displayed on the canvas.

_27

abstract class CanvasObject extends SyncedObject {

_27

final Color color;

_27

_27

CanvasObject({

_27

required super.id,

_27

required this.color,

_27

});

_27

_27

factory CanvasObject.fromJson(Map<String, dynamic> json) {

_27

if (json['object_type'] == CanvasCircle.type) {

_27

return CanvasCircle.fromJson(json);

_27

} else if (json['object_type'] == CanvasRectangle.type) {

_27

return CanvasRectangle.fromJson(json);

_27

} else {

_27

throw UnimplementedError('Unknown object_type: ${json['object_type']}');

_27

}

_27

}

_27

_27

/// Whether or not the object intersects with the given point.

_27

bool intersectsWith(Offset point);

_27

_27

CanvasObject copyWith();

_27

_27

/// Moves the object to a new position

_27

CanvasObject move(Offset delta);

_27

}

  
`

Now that we have the base class for the canvas objects, let’s define the
actual shapes we will support in this application. Each object will inherit
`CanvasObject` and will have additional properties like `center` and `radius`
for the circle.

In this article, we are only supporting circles and rectangles, but you can
easily expand this and add support for other shapes.

`  

_141

/// Circle displayed on the canvas.

_141

class Circle extends CanvasObject {

_141

static String type = 'circle';

_141

_141

final Offset center;

_141

final double radius;

_141

_141

Circle({

_141

required super.id,

_141

required super.color,

_141

required this.radius,

_141

required this.center,

_141

});

_141

_141

Circle.fromJson(Map<String, dynamic> json)

_141

: radius = json['radius'],

_141

center = Offset(json['center']['x'], json['center']['y']),

_141

super(id: json['id'], color: Color(json['color']));

_141

_141

/// Constructor to be used when first starting to draw the object on the
canvas

_141

Circle.createNew(this.center)

_141

: radius = 0,

_141

super(id: const Uuid().v4(), color: RandomColor.getRandom());

_141

_141

@override

_141

Map<String, dynamic> toJson() {

_141

return {

_141

'object_type': type,

_141

'id': id,

_141

'color': color.value,

_141

'center': {

_141

'x': center.dx,

_141

'y': center.dy,

_141

},

_141

'radius': radius,

_141

};

_141

}

_141

_141

@override

_141

Circle copyWith({

_141

double? radius,

_141

Offset? center,

_141

Color? color,

_141

}) {

_141

return Circle(

_141

radius: radius ?? this.radius,

_141

center: center ?? this.center,

_141

id: id,

_141

color: color ?? this.color,

_141

);

_141

}

_141

_141

@override

_141

bool intersectsWith(Offset point) {

_141

final centerToPointerDistance = (point - center).distance;

_141

return radius > centerToPointerDistance;

_141

}

_141

_141

@override

_141

Circle move(Offset delta) {

_141

return copyWith(center: center + delta);

_141

}

_141

}

_141

_141

/// Rectangle displayed on the canvas.

_141

class Rectangle extends CanvasObject {

_141

static String type = 'rectangle';

_141

_141

final Offset topLeft;

_141

final Offset bottomRight;

_141

_141

Rectangle({

_141

required super.id,

_141

required super.color,

_141

required this.topLeft,

_141

required this.bottomRight,

_141

});

_141

_141

Rectangle.fromJson(Map<String, dynamic> json)

_141

: bottomRight =

_141

Offset(json['bottom_right']['x'], json['bottom_right']['y']),

_141

topLeft = Offset(json['top_left']['x'], json['top_left']['y']),

_141

super(id: json['id'], color: Color(json['color']));

_141

_141

/// Constructor to be used when first starting to draw the object on the
canvas

_141

Rectangle.createNew(Offset startingPoint)

_141

: topLeft = startingPoint,

_141

bottomRight = startingPoint,

_141

super(color: RandomColor.getRandom(), id: const Uuid().v4());

_141

_141

@override

_141

Map<String, dynamic> toJson() {

_141

return {

_141

'object_type': type,

_141

'id': id,

_141

'color': color.value,

_141

'top_left': {

_141

'x': topLeft.dx,

_141

'y': topLeft.dy,

_141

},

_141

'bottom_right': {

_141

'x': bottomRight.dx,

_141

'y': bottomRight.dy,

_141

},

_141

};

_141

}

_141

_141

@override

_141

Rectangle copyWith({

_141

Offset? topLeft,

_141

Offset? bottomRight,

_141

Color? color,

_141

}) {

_141

return Rectangle(

_141

topLeft: topLeft ?? this.topLeft,

_141

id: id,

_141

bottomRight: bottomRight ?? this.bottomRight,

_141

color: color ?? this.color,

_141

);

_141

}

_141

_141

@override

_141

bool intersectsWith(Offset point) {

_141

final minX = min(topLeft.dx, bottomRight.dx);

_141

final maxX = max(topLeft.dx, bottomRight.dx);

_141

final minY = min(topLeft.dy, bottomRight.dy);

_141

final maxY = max(topLeft.dy, bottomRight.dy);

_141

return minX < point.dx &&

_141

point.dx < maxX &&

_141

minY < point.dy &&

_141

point.dy < maxY;

_141

}

_141

_141

@override

_141

Rectangle move(Offset delta) {

_141

return copyWith(

_141

topLeft: topLeft + delta,

_141

bottomRight: bottomRight + delta,

_141

);

_141

}

_141

}

  
`

That is it for the `canvas_object.dart` file.

### Step 4: Create the custom painter#

`CustomPainter` is a low-level API to interact with the canvas within a
Flutter application. We will create our own `CustomPainter` that takes the
cursor positions and the objects within the app and draws them on a canvas.

Create `lib/canvas/canvas_painter.dart` file and add the following.

`  

_48

import 'package:canvas/canvas/canvas_object.dart';

_48

import 'package:flutter/material.dart';

_48

_48

class CanvasPainter extends CustomPainter {

_48

final Map<String, UserCursor> userCursors;

_48

final Map<String, CanvasObject> canvasObjects;

_48

_48

CanvasPainter({

_48

required this.userCursors,

_48

required this.canvasObjects,

_48

});

_48

_48

@override

_48

void paint(Canvas canvas, Size size) {

_48

// Draw each canvas objects

_48

for (final canvasObject in canvasObjects.values) {

_48

if (canvasObject is Circle) {

_48

final position = canvasObject.center;

_48

final radius = canvasObject.radius;

_48

canvas.drawCircle(

_48

position, radius, Paint()..color = canvasObject.color);

_48

} else if (canvasObject is Rectangle) {

_48

final position = canvasObject.topLeft;

_48

final bottomRight = canvasObject.bottomRight;

_48

canvas.drawRect(

_48

Rect.fromLTRB(

_48

position.dx, position.dy, bottomRight.dx, bottomRight.dy),

_48

Paint()..color = canvasObject.color);

_48

}

_48

}

_48

_48

// Draw the cursors

_48

for (final userCursor in userCursors.values) {

_48

final position = userCursor.position;

_48

canvas.drawPath(

_48

Path()

_48

..moveTo(position.dx, position.dy)

_48

..lineTo(position.dx + 14.29, position.dy + 44.84)

_48

..lineTo(position.dx + 20.35, position.dy + 25.93)

_48

..lineTo(position.dx + 39.85, position.dy + 24.51)

_48

..lineTo(position.dx, position.dy),

_48

Paint()..color = userCursor.color);

_48

}

_48

}

_48

_48

@override

_48

bool shouldRepaint(oldPainter) => true;

_48

}

  
`

`userCursors` and `canvasObjects` represent the cursors and the objects within
the canvas respectively. The key of the `Map` is the UUID unique identifiers.

The `paint()` method is where the drawing on the canvas happens. It first
loops through the objects and draws them on the canvas. Each shape has its
drawing method, so we will check the type of the object in each loop and apply
the respective drawing method.

Once we have all the objects drawn, we draw the cursors. The reason why we
draw the cursors after the objects is because within a custom painter,
whatever is drawn later draws over the previously drawn objects. Because we do
not want the cursors to be hidden behind the objects, we draw all the cursors
after all of the objects are done being drawn.

`shouldRepaint()` defines whether we want the canvas to be repainted when the
`CustomPainter` receives a new set of properties. In our case, we want to
redraw the painter whenever we receive a new set of properties, so we always
return true.

### Step 5: Create the canvas page#

Now that we have the data models and our custom painter ready, it is time to
put everything together. We will create a canvas page, the only page of this
app, which allows users to draw shapes and move those shapes around while
keeping the states in sync with other users.

Create `lib/canvas/canvas_page.dart` file. Add all of the code shown within
this step into `canvas_page.dart`. Start by adding all the necessary imports
for this app.

`  

_10

import 'dart:math';

_10

_10

import 'package:canvas/canvas/canvas_object.dart';

_10

import 'package:canvas/canvas/canvas_painter.dart';

_10

import 'package:canvas/main.dart';

_10

import 'package:canvas/utils/constants.dart';

_10

import 'package:flutter/material.dart';

_10

import 'package:supabase_flutter/supabase_flutter.dart';

_10

import 'package:uuid/uuid.dart';

  
`

We can then create an enum to represent the three different actions we can
perform in this app, `pointer` for moving objects around, `circle` for drawing
circles, and `rectangle` for drawing rectangles.

`  

_16

/// Different input modes users can perform

_16

enum _DrawMode {

_16

/// Mode to move around existing objects

_16

pointer(iconData: Icons.pan_tool_alt),

_16

_16

/// Mode to draw circles

_16

circle(iconData: Icons.circle_outlined),

_16

_16

/// Mode to draw rectangles

_16

rectangle(iconData: Icons.rectangle_outlined);

_16

_16

const _DrawMode({required this.iconData});

_16

_16

/// Icon used in the IconButton to toggle the mode

_16

final IconData iconData;

_16

}

  
`

Finally, we can get to the meat of the app, creating the `CanvasPage` widget.
Create an empty `StatefulWidget` with a blank `Scaffold`. We will be adding
properties, methods, and widgets to it.

`  

_19

_19

/// Interactive art board page to draw and collaborate with other users.

_19

class CanvasPage extends StatefulWidget {

_19

const CanvasPage({super.key});

_19

_19

@override

_19

State<CanvasPage> createState() => _CanvasPageState();

_19

}

_19

_19

class _CanvasPageState extends State<CanvasPage> {

_19

// TODO: Add properties

_19

_19

// TODO: Add methods

_19

_19

@override

_19

Widget build(BuildContext context) {

_19

return Scaffold();

_19

}

_19

}

  
`

First, we can define all of the properties we need for this widget.
`_userCursors` and `_canvasObjects` will hold the cursors and canvas objects
the app receives from the real-time listener. `_canvasChanel` is the gateway
for the client to communicate with other clients using [Supabase
Realtime](https://supabase.com/docs/guides/realtime). We will later implement
the logic to send and receive information about the canvas. Then there are a
few states that will be used when we implement the drawing on the canvas.

`  

_32

class _CanvasPageState extends State<CanvasPage> {

_32

/// Holds the cursor information of other users

_32

final Map<String, UserCursor> _userCursors = {};

_32

_32

/// Holds the list of objects drawn on the canvas

_32

final Map<String, CanvasObject> _canvasObjects = {};

_32

_32

/// Supabase Realtime channel to communicate to other clients

_32

late final RealtimeChannel _canvasChanel;

_32

_32

/// Randomly generated UUID for the user

_32

late final String _myId;

_32

_32

/// Whether the user is using the pointer to move things around, or in drawing
mode.

_32

_DrawMode _currentMode = _DrawMode.pointer;

_32

_32

/// A single Canvas object that is being drawn by the user if any.

_32

String? _currentlyDrawingObjectId;

_32

_32

/// The point where the pan started

_32

Offset? _panStartPoint;

_32

_32

/// Cursor position of the user.

_32

Offset _cursorPosition = const Offset(0, 0);

_32

_32

// TODO: Add methods

_32

_32

@override

_32

Widget build(BuildContext context) {

_32

return Scaffold();

_32

}

_32

}

  
`

Now that we have the properties defined, we can run some initialization code
to set up the scene. There are a few things we are doing in this
initialization step.

One, assigning a randomly generated UUID to the user. Two, setting up the
real-time listener for Supabase. We are listening to [Realtime Broadcast
events](https://supabase.com/docs/guides/realtime/broadcast?language=dart),
which are low-latency real-time communication mechanisms that Supabase offers.
Within the callback of the broadcast event, we obtain the cursor and object
information sent from other clients and set the state accordingly. And three,
we load the initial state of the canvas from the database and set it as the
initial state of the widget.

Now that the app has been initialized, we are ready to implement the logic of
the user drawing and interacting with the canvas.

`  

_48

class _CanvasPageState extends State<CanvasPage> {

_48

...

_48

_48

@override

_48

void initState() {

_48

super.initState();

_48

_initialize();

_48

}

_48

_48

Future<void> _initialize() async {

_48

// Generate a random UUID for the user.

_48

// We could replace this with Supabase auth user ID if we want to make it

_48

// more like Figma.

_48

_myId = const Uuid().v4();

_48

_48

// Start listening to broadcast messages to display other users' cursors and
objects.

_48

_canvasChanel = supabase

_48

.channel(Constants.channelName)

_48

.onBroadcast(

_48

event: Constants.broadcastEventName,

_48

callback: (payload) {

_48

final cursor = UserCursor.fromJson(payload['cursor']);

_48

_userCursors[cursor.id] = cursor;

_48

_48

if (payload['object'] != null) {

_48

final object = CanvasObject.fromJson(payload['object']);

_48

_canvasObjects[object.id] = object;

_48

}

_48

setState(() {});

_48

})

_48

.subscribe();

_48

_48

final initialData = await supabase

_48

.from('canvas_objects')

_48

.select()

_48

.order('created_at', ascending: true);

_48

for (final canvasObjectData in initialData) {

_48

final canvasObject = CanvasObject.fromJson(canvasObjectData['object']);

_48

_canvasObjects[canvasObject.id] = canvasObject;

_48

}

_48

setState(() {});

_48

}

_48

_48

@override

_48

Widget build(BuildContext context) {

_48

return Scaffold();

_48

}

_48

}

  
`

We have three methods triggered by user actions, `_onPanDown()`,
`_onPanUpdate()`, and `_onPanEnd()`, and a method to sync the user action with
other clients `_syncCanvasObject()`.

What the three pan methods do could be two things, either to draw the object
or to move the object.

When drawing an object, on pan down it will add the object to the canvas with
size 0, essentially a point. As the user drags the mouse, the pan update
method is called which gives the object some size while syncing the object to
other clients along the way.

When the user is in `pointer` mode, the pan-down method first determines if
there is an object under where the user’s pointer currently is located. If
there is an object, it holds the object’s id as the widget’s state. As the
user drags the screen, the position of the object is moved the same amount the
user’s cursor moves, while syncing the object’s information through broadcast
along the way.

In both cases, when the user is done dragging, the pan end is called which
does some clean-ups of the local state and stores the object information in
the database to store the canvas data permanently.

`  

_122

class _CanvasPageState extends State<CanvasPage> {

_122

...

_122

_122

/// Syncs the user's cursor position and the currently drawing object with

_122

/// other users.

_122

Future<void> _syncCanvasObject(Offset cursorPosition) {

_122

final myCursor = UserCursor(

_122

position: cursorPosition,

_122

id: _myId,

_122

);

_122

return _canvasChanel.sendBroadcastMessage(

_122

event: Constants.broadcastEventName,

_122

payload: {

_122

'cursor': myCursor.toJson(),

_122

if (_currentlyDrawingObjectId != null)

_122

'object': _canvasObjects[_currentlyDrawingObjectId]?.toJson(),

_122

},

_122

);

_122

}

_122

_122

/// Called when pan starts.

_122

///

_122

/// For [_DrawMode.pointer], it will find the first object under the cursor.

_122

///

_122

/// For other draw modes, it will start drawing the respective canvas objects.

_122

void _onPanDown(DragDownDetails details) {

_122

switch (_currentMode) {

_122

case _DrawMode.pointer:

_122

// Loop through the canvas objects to find if there are any

_122

// that intersects with the current mouse position.

_122

for (final canvasObject in _canvasObjects.values.toList().reversed) {

_122

if (canvasObject.intersectsWith(details.globalPosition)) {

_122

_currentlyDrawingObjectId = canvasObject.id;

_122

break;

_122

}

_122

}

_122

break;

_122

case _DrawMode.circle:

_122

final newObject = Circle.createNew(details.globalPosition);

_122

_canvasObjects[newObject.id] = newObject;

_122

_currentlyDrawingObjectId = newObject.id;

_122

break;

_122

case _DrawMode.rectangle:

_122

final newObject = Rectangle.createNew(details.globalPosition);

_122

_canvasObjects[newObject.id] = newObject;

_122

_currentlyDrawingObjectId = newObject.id;

_122

break;

_122

}

_122

_cursorPosition = details.globalPosition;

_122

_panStartPoint = details.globalPosition;

_122

setState(() {});

_122

}

_122

_122

/// Called when the user clicks and drags the canvas.

_122

///

_122

/// Performs different actions depending on the current mode.

_122

void _onPanUpdate(DragUpdateDetails details) {

_122

switch (_currentMode) {

_122

// Moves the object to [details.delta] amount.

_122

case _DrawMode.pointer:

_122

if (_currentlyDrawingObjectId != null) {

_122

_canvasObjects[_currentlyDrawingObjectId!] =

_122

_canvasObjects[_currentlyDrawingObjectId!]!.move(details.delta);

_122

}

_122

break;

_122

_122

// Updates the size of the Circle

_122

case _DrawMode.circle:

_122

final currentlyDrawingCircle =

_122

_canvasObjects[_currentlyDrawingObjectId!]! as Circle;

_122

_canvasObjects[_currentlyDrawingObjectId!] =

_122

currentlyDrawingCircle.copyWith(

_122

center: (details.globalPosition + _panStartPoint!) / 2,

_122

radius: min((details.globalPosition.dx - _panStartPoint!.dx).abs(),

_122

(details.globalPosition.dy - _panStartPoint!.dy).abs()) /

_122

2,

_122

);

_122

break;

_122

_122

// Updates the size of the rectangle

_122

case _DrawMode.rectangle:

_122

_canvasObjects[_currentlyDrawingObjectId!] =

_122

(_canvasObjects[_currentlyDrawingObjectId!] as Rectangle).copyWith(

_122

bottomRight: details.globalPosition,

_122

);

_122

break;

_122

}

_122

_122

if (_currentlyDrawingObjectId != null) {

_122

setState(() {});

_122

}

_122

_cursorPosition = details.globalPosition;

_122

_syncCanvasObject(_cursorPosition);

_122

}

_122

_122

void onPanEnd(DragEndDetails _) async {

_122

if (_currentlyDrawingObjectId != null) {

_122

_syncCanvasObject(_cursorPosition);

_122

}

_122

_122

final drawnObjectId = _currentlyDrawingObjectId;

_122

_122

setState(() {

_122

_panStartPoint = null;

_122

_currentlyDrawingObjectId = null;

_122

});

_122

_122

// Save whatever was drawn to Supabase DB

_122

if (drawnObjectId == null) {

_122

return;

_122

}

_122

await supabase.from('canvas_objects').upsert({

_122

'id': drawnObjectId,

_122

'object': _canvasObjects[drawnObjectId]!.toJson(),

_122

});

_122

}

_122

_122

@override

_122

Widget build(BuildContext context) {

_122

return Scaffold();

_122

}

_122

}

  
`

With all the properties and methods defined, we can proceed to add content to
the build method. The entire region is covered in `MouseRegion`, which is used
to get the cursor position and share it with other clients. Within the mouse
region, we have the `GestureDetector` and the three buttons representing each
action. Because the heavy lifting was done in the methods we have already
defined, the build method is fairly simple.

`  

_51

class _CanvasPageState extends State<CanvasPage> {

_51

...

_51

_51

@override

_51

Widget build(BuildContext context) {

_51

return Scaffold(

_51

body: MouseRegion(

_51

onHover: (event) {

_51

_syncCanvasObject(event.position);

_51

},

_51

child: Stack(

_51

children: [

_51

// The main canvas

_51

GestureDetector(

_51

onPanDown: _onPanDown,

_51

onPanUpdate: _onPanUpdate,

_51

onPanEnd: onPanEnd,

_51

child: CustomPaint(

_51

size: MediaQuery.of(context).size,

_51

painter: CanvasPainter(

_51

userCursors: _userCursors,

_51

canvasObjects: _canvasObjects,

_51

),

_51

),

_51

),

_51

_51

// Buttons to change the current mode.

_51

Positioned(

_51

top: 0,

_51

left: 0,

_51

child: Row(

_51

children: _DrawMode.values

_51

.map((mode) => IconButton(

_51

iconSize: 48,

_51

onPressed: () {

_51

setState(() {

_51

_currentMode = mode;

_51

});

_51

},

_51

icon: Icon(mode.iconData),

_51

color: _currentMode == mode ? Colors.green : null,

_51

))

_51

.toList(),

_51

),

_51

),

_51

],

_51

),

_51

),

_51

);

_51

}

_51

}

  
`

### Step 6: Run the application#

At this point, we have implemented everything we need to create a
collaborative design canvas. Run the app with `flutter run` and run it in your
browser. There is currently a bug in Flutter where `MouseRegion` cannot detect
the position of a cursor in two different Chrome windows at the same time, so
open it in two different browsers like Chrome and Safari, and enjoy
interacting with your design elements in real time.

## Conclusion#

In this article, we learned how we can combine the [Supabase Realtime
Broadcast](https://supabase.com/docs/guides/realtime/broadcast) feature with
Flutter’s `CustomPainter` to create a collaborative design app. We learned how
to implement real-time communication between multiple clients using the
Broadcast feature, and how we can broadcast the shape and cursor data to other
connected clients in real-time.

This article only used circles and rectangles to keep things simple, but you
can easily add support for other types of objects like texts or arrows just by
extending the `CanvasObject` class to make the app more like Figma. Another
fun way to expand this app would be to add authentication using [Supabase
Auth](https://supabase.com/docs/guides/auth) so that we can add proper
authorizations. Adding an image upload feature using [Supabase
Storage](https://supabase.com/docs/guides/storage) would certainly open up
more creative options for the app.

## Resources#

  * [Add live cursor sharing using Flutter and Supabase | Flutter Figma Clone #1](https://youtu.be/QhRNXlFLaeE?si=_hi5WcILUsAv8jJY)
  * [Draw and sync canvas in real-time | Flutter Figma Clone #2](https://youtu.be/zKjrmAMf2Cs?si=i7zILCFKitjDb45K)
  * [Track online users with Supabase Realtime Presence | Flutter Figma Clone #3](https://youtu.be/B2NZvZ2uLNs?si=0rMj7u1gaMH9Bmdm)
  * [How to build a real-time multiplayer game with Flutter Flame](https://supabase.com/blog/flutter-real-time-multiplayer-game)
  * [Getting started with Flutter authentication](https://supabase.com/blog/flutter-authentication)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
figma-
clone&text=Create%20a%20Figma%20Clone%20app%20with%20Flutter%20and%20Supabase%20Realtime)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
figma-
clone&text=Create%20a%20Figma%20Clone%20app%20with%20Flutter%20and%20Supabase%20Realtime)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
figma-
clone&t=Create%20a%20Figma%20Clone%20app%20with%20Flutter%20and%20Supabase%20Realtime)

[Last postGetting started with Ruby on Rails and Postgres on Supabase29
January 2024](/blog/ruby-on-rails-postgres)

[Next postHow pg_graphql works24 January 2024](/blog/how-pg-graphql-works)

[flutter](/blog/tags/flutter)[realtime](/blog/tags/realtime)

On this page

  * Overview of the Figma clone app
  * Setting up the app
    * Create a blank Flutter application
    * Install the dependencies
    * Setup the Supabase project
  * Building the Figma clone app
    * Step1: Initialize Supabase
    * Step 2: Create the constants file
    * Step 3: Create the data model
    * Step 4: Create the custom painter
    * Step 5: Create the canvas page
    * Step 6: Run the application
  * Conclusion
  * Resources

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
figma-
clone&text=Create%20a%20Figma%20Clone%20app%20with%20Flutter%20and%20Supabase%20Realtime)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
figma-
clone&text=Create%20a%20Figma%20Clone%20app%20with%20Flutter%20and%20Supabase%20Realtime)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
figma-
clone&t=Create%20a%20Figma%20Clone%20app%20with%20Flutter%20and%20Supabase%20Realtime)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

