[Back](/blog)

[Blog](/blog)

# How to build a real-time multiplayer game with Flutter Flame

14 Feb 2023

•

37 minute read

[![Tyler Shukert
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fdshukertjr.png&w=96&q=75)Tyler
ShukertDevRel](https://twitter.com/dshukertjr)

![How to build a real-time multiplayer game with Flutter
Flame](/_next/image?url=%2Fimages%2Fblog%2Fflutter-realtime-game%2Fflutter-
flame-realtime-multiplayer-game.jpg&w=3840&q=100)

Flutter is a UI library to build apps that run on any platform, but it can
also build interactive games thanks to an open-source game engine built on top
of Flutter called [Flame](https://flame-engine.org/). Flame takes care of
things like collision detection or loading image sprites to bring game
development to all the Flutter devs. We can take it a step further to
introduce real-time communication features so that players can play against
each other in real-time.

In this article, we will use Flutter, Flame, and Supabase's real-time features
to build a real-time multiplayer shooting game. You can find the complete code
of this tutorial
[here](https://github.com/supabase/supabase/tree/master/examples/realtime/flutter-
multiplayer-shooting-game).

## Overview of the final game#

The game is a simple shooting game. Each player has a UFO, and you can move it
by dragging your finger across the screen. The UFO will emit bullets
automatically in three directions, and the objective of the game is to hit the
opponents with bullets before your UFO gets destroyed by the opponent’s
bullets. The position and the health points are synced using a low-latency web
socket connection provided by Supabase.

Before entering the main game, there is a lobby where you can wait for other
players to show up. Once another player shows up, you can hit start, which
will kick off the game on both ends.

We will first build the Flutter widgets used to build the basic UI, then build
the Flame game and finally handle the network connection to share the data
between connected clients.

## Build the App#

### Step 1. Create the Flutter App#

We will start out by creating the Flutter app. Open your terminal and create a
new app named with the following command.

`  

_10

flutter create flame_realtime_shooting

  
`

Open the created app with your favorite IDE and let’s get started with coding!

### Step 2. Building the Flutter widgets#

We will have a simple directory structure to build this app. Since we only
have a few widgets, we will just add them inside `main.dart` file.

`  

_10

├── lib/

_10

| ├── game/

_10

│ │ ├── game.dart

_10

│ │ ├── player.dart

_10

│ │ └── bullet.dart

_10

│ └── main.dart

  
`

### Create the Main Game Page#

We will create minimal Flutter widgets for this app as most of the game logic
will be handled in the Flame Game classes later. Our game will have a single
page with two dialogs before the game starts and after the game ends. The page
will simply contain the [GameWidget](https://docs.flame-
engine.org/1.6.0/flame/game_widget.html) while displaying a nice background
image. We will make it a StatefulWidget, because we will add methods to handle
sending and receiving real-time data later on. Add the following to
`main.dart` file.

`  

_81

import 'package:flame/game.dart';

_81

import 'package:flame_realtime_shooting/game/game.dart';

_81

import 'package:flutter/material.dart';

_81

_81

void main() {

_81

runApp(const MyApp());

_81

}

_81

_81

class MyApp extends StatelessWidget {

_81

const MyApp({super.key});

_81

_81

@override

_81

Widget build(BuildContext context) {

_81

return const MaterialApp(

_81

title: 'UFO Shooting Game',

_81

debugShowCheckedModeBanner: false,

_81

home: GamePage(),

_81

);

_81

}

_81

}

_81

_81

class GamePage extends StatefulWidget {

_81

const GamePage({Key? key}) : super(key: key);

_81

_81

@override

_81

State<GamePage> createState() => _GamePageState();

_81

}

_81

_81

class _GamePageState extends State<GamePage> {

_81

late final MyGame _game;

_81

_81

@override

_81

Widget build(BuildContext context) {

_81

return Scaffold(

_81

body: Stack(

_81

fit: StackFit.expand,

_81

children: [

_81

Image.asset('assets/images/background.jpg', fit: BoxFit.cover),

_81

GameWidget(game: _game),

_81

],

_81

),

_81

);

_81

}

_81

_81

@override

_81

void initState() {

_81

super.initState();

_81

_initialize();

_81

}

_81

_81

Future<void> _initialize() async {

_81

_game = MyGame(

_81

onGameStateUpdate: (position, health) async {

_81

// TODO: handle gmae state update here

_81

},

_81

onGameOver: (playerWon) async {

_81

// TODO: handle when the game is over here

_81

},

_81

);

_81

_81

// await for a frame so that the widget mounts

_81

await Future.delayed(Duration.zero);

_81

_81

if (mounted) {

_81

_openLobbyDialog();

_81

}

_81

}

_81

_81

void _openLobbyDialog() {

_81

showDialog(

_81

context: context,

_81

barrierDismissible: false,

_81

builder: (context) {

_81

return _LobbyDialog(

_81

onGameStarted: (gameId) async {

_81

// handle game start here

_81

},

_81

);

_81

});

_81

}

_81

}

  
`

You will see some errors, because we are importing some files that we haven’t
created yet, but don’t worry, because we will get to it soon.

### Create the Lobby Dialog#

Lobby dialog class on the surface is a simple Alert dialog, but will hold its
own states like the list of players that are waiting at the lobby. We will
also add some classes to handle the presence data on the lobby later on, but
for now we will just have a simple AlertDialog. Add the following code at the
end of main.dart file.

`  

_45

class _LobbyDialog extends StatefulWidget {

_45

const _LobbyDialog({

_45

required this.onGameStarted,

_45

});

_45

_45

final void Function(String gameId) onGameStarted;

_45

_45

@override

_45

State<_LobbyDialog> createState() => _LobbyDialogState();

_45

}

_45

_45

class _LobbyDialogState extends State<_LobbyDialog> {

_45

final List<String> _userids = [];

_45

bool _loading = false;

_45

_45

/// TODO: assign unique identifier for the user

_45

final myUserId = '';

_45

_45

@override

_45

Widget build(BuildContext context) {

_45

return AlertDialog(

_45

title: const Text('Lobby'),

_45

content: _loading

_45

? const SizedBox(

_45

height: 100,

_45

child: Center(child: CircularProgressIndicator()),

_45

)

_45

: Text('${_userids.length} users waiting'),

_45

actions: [

_45

TextButton(

_45

onPressed: _userids.length < 2

_45

? null

_45

: () async {

_45

setState(() {

_45

_loading = true;

_45

});

_45

_45

// TODO: notify the other player the start of the game

_45

},

_45

child: const Text('start'),

_45

),

_45

],

_45

);

_45

}

_45

}

  
`

### Step 3. Building the Flame components#

### Creating the FlameGame#

Now the fun part starts! We will start out by creating our game class. We
create a `MyGame` class that extends the [FlameGame](https://docs.flame-
engine.org/1.6.0/flame/game.html) class. `FlameGame` takes care of collision
detection and pan-detection, and it will also be the parent of all the
components that we will add to the game. The game contains 2 components,
`Player` and `Bullet`. `MyGame ` is a class that wraps around all components
of the game and can control the child components.

Let's add flame to our app. Run the following command:

`  

_10

flutter pub add flame

  
`

We can then create `MyGame` class. Add the following code in `lib/game.dart`
file.

`  

_160

import 'dart:async';

_160

_160

import 'package:flame/game.dart';

_160

import 'package:flame/components.dart';

_160

import 'package:flame/events.dart';

_160

import 'package:flame/image_composition.dart' as flame_image;

_160

import 'package:flame_realtime_shooting/game/bullet.dart';

_160

import 'package:flame_realtime_shooting/game/player.dart';

_160

import 'package:flutter/material.dart';

_160

_160

class MyGame extends FlameGame with PanDetector, HasCollisionDetection {

_160

MyGame({

_160

required this.onGameOver,

_160

required this.onGameStateUpdate,

_160

});

_160

_160

static const _initialHealthPoints = 100;

_160

_160

/// Callback to notify the parent when the game ends.

_160

final void Function(bool didWin) onGameOver;

_160

_160

/// Callback for when the game state updates.

_160

final void Function(

_160

Vector2 position,

_160

int health,

_160

) onGameStateUpdate;

_160

_160

/// `Player` instance of the player

_160

late Player _player;

_160

_160

/// `Player` instance of the opponent

_160

late Player _opponent;

_160

_160

bool isGameOver = true;

_160

_160

int _playerHealthPoint = _initialHealthPoints;

_160

_160

late final flame_image.Image _playerBulletImage;

_160

late final flame_image.Image _opponentBulletImage;

_160

_160

@override

_160

Color backgroundColor() {

_160

return Colors.transparent;

_160

}

_160

_160

@override

_160

Future<void>? onLoad() async {

_160

final playerImage = await images.load('player.png');

_160

_player = Player(isMe: true);

_160

final spriteSize = Vector2.all(Player.radius * 2);

_160

_player.add(SpriteComponent(sprite: Sprite(playerImage), size: spriteSize));

_160

add(_player);

_160

_160

final opponentImage = await images.load('opponent.png');

_160

_opponent = Player(isMe: false);

_160

_opponent.add(SpriteComponent.fromImage(opponentImage, size: spriteSize));

_160

add(_opponent);

_160

_160

_playerBulletImage = await images.load('player-bullet.png');

_160

_opponentBulletImage = await images.load('opponent-bullet.png');

_160

_160

await super.onLoad();

_160

}

_160

_160

@override

_160

void onPanUpdate(DragUpdateInfo info) {

_160

_player.move(info.delta.global);

_160

final mirroredPosition = _player.getMirroredPercentPosition();

_160

onGameStateUpdate(mirroredPosition, _playerHealthPoint);

_160

super.onPanUpdate(info);

_160

}

_160

_160

@override

_160

void update(double dt) {

_160

super.update(dt);

_160

if (isGameOver) {

_160

return;

_160

}

_160

for (final child in children) {

_160

if (child is Bullet && child.hasBeenHit && !child.isMine) {

_160

_playerHealthPoint = _playerHealthPoint - child.damage;

_160

final mirroredPosition = _player.getMirroredPercentPosition();

_160

onGameStateUpdate(mirroredPosition, _playerHealthPoint);

_160

_player.updateHealth(_playerHealthPoint / _initialHealthPoints);

_160

}

_160

}

_160

if (_playerHealthPoint <= 0) {

_160

endGame(false);

_160

}

_160

}

_160

_160

void startNewGame() {

_160

isGameOver = false;

_160

_playerHealthPoint = _initialHealthPoints;

_160

_160

for (final child in children) {

_160

if (child is Player) {

_160

child.position = child.initialPosition;

_160

} else if (child is Bullet) {

_160

child.removeFromParent();

_160

}

_160

}

_160

_160

_shootBullets();

_160

}

_160

_160

/// shoots out bullets form both the player and the opponent.

_160

///

_160

/// Calls itself every 500 milliseconds

_160

Future<void> _shootBullets() async {

_160

await Future.delayed(const Duration(milliseconds: 500));

_160

_160

/// Player's bullet

_160

final playerBulletInitialPosition = Vector2.copy(_player.position)

_160

..y -= Player.radius;

_160

final playerBulletVelocities = [

_160

Vector2(0, -100),

_160

Vector2(60, -80),

_160

Vector2(-60, -80),

_160

];

_160

for (final bulletVelocity in playerBulletVelocities) {

_160

add((Bullet(

_160

isMine: true,

_160

velocity: bulletVelocity,

_160

image: _playerBulletImage,

_160

initialPosition: playerBulletInitialPosition,

_160

)));

_160

}

_160

_160

/// Opponent's bullet

_160

final opponentBulletInitialPosition = Vector2.copy(_opponent.position)

_160

..y += Player.radius;

_160

final opponentBulletVelocities = [

_160

Vector2(0, 100),

_160

Vector2(60, 80),

_160

Vector2(-60, 80),

_160

];

_160

for (final bulletVelocity in opponentBulletVelocities) {

_160

add((Bullet(

_160

isMine: false,

_160

velocity: bulletVelocity,

_160

image: _opponentBulletImage,

_160

initialPosition: opponentBulletInitialPosition,

_160

)));

_160

}

_160

_160

_shootBullets();

_160

}

_160

_160

void updateOpponent({required Vector2 position, required int health}) {

_160

_opponent.position = Vector2(size.x * position.x, size.y * position.y);

_160

_opponent.updateHealth(health / _initialHealthPoints);

_160

}

_160

_160

/// Called when either the player or the opponent has run out of health points

_160

void endGame(bool playerWon) {

_160

isGameOver = true;

_160

onGameOver(playerWon);

_160

}

_160

}

  
`

There is a lot going here, so let’s break it down. Within the `onLoad` method,
we are loading all of the sprites used throughout the game. Then we are adding
the player and opponent component.

Within `onPanUpdate`, we handle the user dragging on the screen. Note that we
are calling the `onGameStateUpdate` callback to pass the player’s position so
that we can share it to the opponent’s client later when we handle network
connections. On the other hand, we have the `updateOpponent` method, which is
used to update the opponent’s state with the information coming in from the
network. We will also add logic to call it from the Flutter widgets later.

Upon starting the game, `_shootBullets()` is called, which shoots out bullets
both from the player and the opponent. `_shootBullets()` is a recursive
function that calls itself every 500 milliseconds. If the bullet hits the
player, it is caught inside the `udpate()` method, which is called on every
frame. There we calculate the new player’s health points.

### Creating the Player Component#

`Player` component has the UFO sprite and represents the player and the
opponent. It extends the `PositionComponent` from Flame. Add the following in
`lib/player.dart`

`  

_103

import 'dart:async';

_103

_103

import 'package:flame/collisions.dart';

_103

import 'package:flame/components.dart';

_103

import 'package:flame_realtime_shooting/game/bullet.dart';

_103

import 'package:flutter/material.dart';

_103

_103

class Player extends PositionComponent with HasGameRef, CollisionCallbacks {

_103

Vector2 velocity = Vector2.zero();

_103

_103

late final Vector2 initialPosition;

_103

_103

Player({required bool isMe}) : _isMyPlayer = isMe;

_103

_103

/// Whether it's me or the opponent

_103

final bool _isMyPlayer;

_103

_103

static const radius = 30.0;

_103

_103

@override

_103

Future<void>? onLoad() async {

_103

anchor = Anchor.center;

_103

width = radius * 2;

_103

height = radius * 2;

_103

_103

final initialX = gameRef.size.x / 2;

_103

initialPosition = _isMyPlayer

_103

? Vector2(initialX, gameRef.size.y * 0.8)

_103

: Vector2(initialX, gameRef.size.y * 0.2);

_103

position = initialPosition;

_103

_103

add(CircleHitbox());

_103

add(_Gauge());

_103

await super.onLoad();

_103

}

_103

_103

void move(Vector2 delta) {

_103

position += delta;

_103

}

_103

_103

void updateHealth(double healthLeft) {

_103

for (final child in children) {

_103

if (child is _Gauge) {

_103

child._healthLeft = healthLeft;

_103

}

_103

}

_103

}

_103

_103

@override

_103

void onCollision(Set<Vector2> intersectionPoints, PositionComponent other) {

_103

super.onCollision(intersectionPoints, other);

_103

if (other is Bullet && _isMyPlayer != other.isMine) {

_103

other.hasBeenHit = true;

_103

other.removeFromParent();

_103

}

_103

}

_103

_103

/// returns the mirrored percent position of the player

_103

/// to be broadcasted to other clients

_103

Vector2 getMirroredPercentPosition() {

_103

final mirroredPosition = gameRef.size - position;

_103

return Vector2(mirroredPosition.x / gameRef.size.x,

_103

mirroredPosition.y / gameRef.size.y);

_103

}

_103

}

_103

_103

class _Gauge extends PositionComponent {

_103

double _healthLeft = 1.0;

_103

_103

@override

_103

FutureOr<void> onLoad() {

_103

final playerParent = parent;

_103

if (playerParent is Player) {

_103

width = playerParent.width;

_103

height = 10;

_103

anchor = Anchor.centerLeft;

_103

position = Vector2(0, 0);

_103

}

_103

return super.onLoad();

_103

}

_103

_103

@override

_103

void render(Canvas canvas) {

_103

super.render(canvas);

_103

canvas.drawRect(

_103

Rect.fromPoints(

_103

const Offset(0, 0),

_103

Offset(width, height),

_103

),

_103

Paint()..color = Colors.white);

_103

canvas.drawRect(

_103

Rect.fromPoints(

_103

const Offset(0, 0),

_103

Offset(width * _healthLeft, height),

_103

),

_103

Paint()

_103

..color = _healthLeft > 0.5

_103

? Colors.green

_103

: _healthLeft > 0.25

_103

? Colors.orange

_103

: Colors.red);

_103

}

_103

}

  
`

You can see that it has a `_isMyPlayer` property, which is true for the player
and false for the opponent. If we take a look at the `onLoad` method, we can
use this to position it either at the top if it’s the opponent, or at the
bottom if it’s the player. We can also see that we are adding a
`CircleHitbox`, because we need to detect collisions between it and the
bullets. Lastly, we are adding `_Gauge` as its child, which is the health
point gauge you see on top of each players. Within `onCollision` callback, we
are checking if the collided object is the opponent’s bullet, and if it is, we
flag the bullet as `hasBeenHit` and remove it from the game.

`getMirroredPercentPosition` method is used when sharing the position with the
opponent’s client. It calculates the mirrored position of the player.
`updateHealth` is called when the health changes and updates the bar length of
the `_Gauge` class.

### Adding bullets#

Lastly we will add the `Bullet` class. It represents a single bullet coming
out from the player and the opponent. Within `onLoad` it adds the sprite to
apply the nice image and `CircleHitbox` so that it can collide with other
objects. You can also see that it receives a `velocity` in the constructor,
the position is updated using the velocity and the elapsed time within the
`update` method. This is how you can have it move in a single direction at a
constant speed.

`  

_55

import 'dart:async';

_55

_55

import 'package:flame/collisions.dart';

_55

import 'package:flame/components.dart';

_55

import 'package:flame/image_composition.dart' as flame_image;

_55

_55

class Bullet extends PositionComponent with CollisionCallbacks, HasGameRef {

_55

final Vector2 velocity;

_55

_55

final flame_image.Image image;

_55

_55

static const radius = 5.0;

_55

_55

bool hasBeenHit = false;

_55

_55

final bool isMine;

_55

_55

/// Damage that it deals when it hits the player

_55

final int damage = 5;

_55

_55

Bullet({

_55

required this.isMine,

_55

required this.velocity,

_55

required this.image,

_55

required Vector2 initialPosition,

_55

}) : super(position: initialPosition);

_55

_55

@override

_55

Future<void>? onLoad() async {

_55

anchor = Anchor.center;

_55

_55

width = radius * 2;

_55

height = radius * 2;

_55

_55

add(CircleHitbox()

_55

..collisionType = CollisionType.passive

_55

..anchor = Anchor.center);

_55

_55

final sprite =

_55

SpriteComponent.fromImage(image, size: Vector2.all(radius * 2));

_55

_55

add(sprite);

_55

await super.onLoad();

_55

}

_55

_55

@override

_55

void update(double dt) {

_55

super.update(dt);

_55

position += velocity * dt;

_55

_55

if (position.y < 0 || position.y > gameRef.size.y) {

_55

removeFromParent();

_55

}

_55

}

_55

}

  
`

### Step 4. Add real-time communications between players#

At this point, we have a working shooting game except the opponent does not
move, because we have not added any ways to communicate between clients. We
will use Supabase’s [realtime
features](https://supabase.com/docs/guides/realtime) for this, because it
gives us an out of the box solution to handle low-latency real-time
communication between players. If you do not have a Supabase project created
yet, head over to [database.new](https://database.new/) to create one.

Before we get into any coding, let’s install the Supabase SDK into our app. We
will also use the [uuid package](https://pub.dev/packages/uuid) to generate
random unique ids for the users. Run the following command:

`  

_10

flutter pub add supabase_flutter uuid

  
`

Once `pub get` is complete, let’s initialize Supabase. We will override the
`main` function to initialize Supabase. You can get your Supabase URL and Anon
Key at `Project Setting` > `API`. Copy and paste them into the
`Supabase.initialize` call.

`  

_11

void main() async {

_11

await Supabase.initialize(

_11

url: 'YOUR_SUPABASE_URL',

_11

anonKey: 'YOUR_ANON_KEY',

_11

realtimeClientOptions: const RealtimeClientOptions(eventsPerSecond: 40),

_11

);

_11

runApp(const MyApp());

_11

}

_11

_11

// Extract Supabase client for easy access to Supabase

_11

final supabase = Supabase.instance.client;

  
`

`RealtimeClientOptions` here is a parameter to override how many events per
second each client will send to Supabase. The default is 10, but we want to
override to 40 to provide a more in-synced experience.

With this, we are ready to get into adding the real-time features now.

### Handle the Lobby to wait for Other Players to show up#

We will start by rewriting the `_Lobby` class the first thing we have to do in
the lobby is to wait and detect other online users also at the lobby. We can
implement this using the
[presence](https://supabase.com/docs/guides/realtime/presence) feature in
Supabase.

Add `initState` and inside it initialize a `RealtimeChannel` instance. We can
call it `_lobbyChannel`. If we take a look at the `subscribe()` method, we can
see that upon successful subscription to the lobby channel, we are tracking
our the unique user ID that we create uplon initialization. We are listening
to the `sync` event to get notified whenever anyone is “present”. Within the
callback, we are extracting the userIds of all the users in the lobby and set
it as the state.A game starts when someone taps on the `Start` button. If we
take a look at the `onPressed` callback, we see that we are sending a
[broadcast](https://supabase.com/docs/guides/realtime/broadcast) event to the
lobby channel with two participant ids and a randomly generated game ID.
[Broadcast](https://supabase.com/docs/guides/realtime/broadcast) is a feature
of Supabase to send and receive lightweight low-latency data between clients,
and when the two participants, one of them being the person tapping on the
`start` button, is received on both ends, a game starts. We can observe within
`initState` inside the callback for `game_start` event that upon receiving a
broadcast event, it checks if the player is one of the participants, and if it
is, it will call the `onGameStarted` call back and pop the navigator removing
the dialog. The game has begun!

`  

_94

class _LobbyDialogState extends State<_LobbyDialog> {

_94

List<String> _userids = [];

_94

bool _loading = false;

_94

_94

/// Unique identifier for each players to identify eachother in lobby

_94

final myUserId = const Uuid().v4();

_94

_94

late final RealtimeChannel _lobbyChannel;

_94

_94

@override

_94

void initState() {

_94

super.initState();

_94

_94

_lobbyChannel = supabase.channel(

_94

'lobby',

_94

opts: const RealtimeChannelConfig(self: true),

_94

);

_94

_lobbyChannel

_94

.onPresenceSync((payload, [ref]) {

_94

// Update the lobby count

_94

final presenceStates = _lobbyChannel.presenceState();

_94

_94

setState(() {

_94

_userids = presenceStates

_94

.map((presenceState) => (presenceState.presences.first)

_94

.payload['user_id'] as String)

_94

.toList();

_94

});

_94

})

_94

.onBroadcast(

_94

event: 'game_start',

_94

callback: (payload, [_]) {

_94

// Start the game if someone has started a game with you

_94

final participantIds = List<String>.from(payload['participants']);

_94

if (participantIds.contains(myUserId)) {

_94

final gameId = payload['game_id'] as String;

_94

widget.onGameStarted(gameId);

_94

Navigator.of(context).pop();

_94

}

_94

})

_94

.subscribe(

_94

(status, _) async {

_94

if (status == RealtimeSubscribeStatus.subscribed) {

_94

await _lobbyChannel.track({'user_id': myUserId});

_94

}

_94

},

_94

);

_94

}

_94

_94

@override

_94

void dispose() {

_94

supabase.removeChannel(_lobbyChannel);

_94

super.dispose();

_94

}

_94

_94

@override

_94

Widget build(BuildContext context) {

_94

return AlertDialog(

_94

title: const Text('Lobby'),

_94

content: _loading

_94

? const SizedBox(

_94

height: 100,

_94

child: Center(child: CircularProgressIndicator()),

_94

)

_94

: Text('${_userids.length} users waiting'),

_94

actions: [

_94

TextButton(

_94

onPressed: _userids.length < 2

_94

? null

_94

: () async {

_94

setState(() {

_94

_loading = true;

_94

});

_94

_94

final opponentId =

_94

_userids.firstWhere((userId) => userId != myUserId);

_94

final gameId = const Uuid().v4();

_94

await _lobbyChannel.sendBroadcastMessage(

_94

event: 'game_start',

_94

payload: {

_94

'participants': [

_94

opponentId,

_94

myUserId,

_94

],

_94

'game_id': gameId,

_94

},

_94

);

_94

},

_94

child: const Text('start'),

_94

),

_94

],

_94

);

_94

}

_94

}

  
`

### Sharing Game States with the Opposing Player#

Once a game begins, we need to synchronize the game states between the two
clients. In our case, we will sync only the player’s position and health
points. Whenever a player moves, or the player’s health points change, the
`onGameStateUpdate` callback on our `MyGame` instance that will fire notifying
the update along with its position and health point. We will broadcast those
information to the opponent’s client via Supabase [broadcast
feature](https://supabase.com/docs/guides/realtime/broadcast).

Fill in the `_initialize` method like the following to initialize the game.

`  

_121

class GamePage extends StatefulWidget {

_121

const GamePage({Key? key}) : super(key: key);

_121

_121

@override

_121

State<GamePage> createState() => _GamePageState();

_121

}

_121

_121

class _GamePageState extends State<GamePage> {

_121

late final MyGame _game;

_121

_121

/// Holds the RealtimeChannel to sync game states

_121

RealtimeChannel? _gameChannel;

_121

_121

@override

_121

Widget build(BuildContext context) {

_121

return Scaffold(

_121

body: Stack(

_121

fit: StackFit.expand,

_121

children: [

_121

Image.asset('assets/images/background.jpg', fit: BoxFit.cover),

_121

GameWidget(game: _game),

_121

],

_121

),

_121

);

_121

}

_121

_121

@override

_121

void initState() {

_121

super.initState();

_121

_initialize();

_121

}

_121

_121

Future<void> _initialize() async {

_121

_game = MyGame(

_121

onGameStateUpdate: (position, health) async {

_121

ChannelResponse response;

_121

do {

_121

response = await _gameChannel!.sendBroadcastMessage(

_121

event: 'game_state',

_121

payload: {'x': position.x, 'y': position.y, 'health': health},

_121

);

_121

_121

// wait for a frame to avoid infinite rate limiting loops

_121

await Future.delayed(Duration.zero);

_121

setState(() {});

_121

} while (response == ChannelResponse.rateLimited && health <= 0);

_121

},

_121

onGameOver: (playerWon) async {

_121

await showDialog(

_121

barrierDismissible: false,

_121

context: context,

_121

builder: ((context) {

_121

return AlertDialog(

_121

title: Text(playerWon ? 'You Won!' : 'You lost...'),

_121

actions: [

_121

TextButton(

_121

onPressed: () async {

_121

Navigator.of(context).pop();

_121

await supabase.removeChannel(_gameChannel!);

_121

_openLobbyDialog();

_121

},

_121

child: const Text('Back to Lobby'),

_121

),

_121

],

_121

);

_121

}),

_121

);

_121

},

_121

);

_121

_121

// await for a frame so that the widget mounts

_121

await Future.delayed(Duration.zero);

_121

_121

if (mounted) {

_121

_openLobbyDialog();

_121

}

_121

}

_121

_121

void _openLobbyDialog() {

_121

showDialog(

_121

context: context,

_121

barrierDismissible: false,

_121

builder: (context) {

_121

return _LobbyDialog(

_121

onGameStarted: (gameId) async {

_121

// await a frame to allow subscribing to a new channel in a realtime callback

_121

await Future.delayed(Duration.zero);

_121

_121

setState(() {});

_121

_121

_game.startNewGame();

_121

_121

_gameChannel = supabase.channel(gameId,

_121

opts: const RealtimeChannelConfig(ack: true));

_121

_121

_gameChannel!

_121

.onBroadcast(

_121

event: 'game_state',

_121

callback: (payload, [_]) {

_121

final position = Vector2(

_121

payload['x'] as double, payload['y'] as double);

_121

final opponentHealth = payload['health'] as int;

_121

_game.updateOpponent(

_121

position: position,

_121

health: opponentHealth,

_121

);

_121

_121

if (opponentHealth <= 0) {

_121

if (!_game.isGameOver) {

_121

_game.isGameOver = true;

_121

_game.onGameOver(true);

_121

}

_121

}

_121

},

_121

)

_121

.subscribe();

_121

},

_121

);

_121

});

_121

}

_121

}

  
`

You can see that within `_openLobbyDialog`, there is an `onGameStarted`
callback for when the game has started. Once a game has been started, it
creates a new channel using the game ID as the channel name and starts
listening to game state updates from the opponent.You can see that within the
`onGameOver` callback, we are showing a simple dialog. Upon tapping `Back to
Lobby`, the user will be taken back to the lobby dialog, where they can start
another game if they want to.

With all of that put together, we have a functioning real-time multiplayer
shooting game. Grab a friend, run the app with `flutter run`, and have fun
with it!

## Conclusions#

We learned how to create an interactive shooting game. We took advantage of
Flutter’s dialogs to create a quick and easy lobby and post-game UI. Then we
created the game using Flame. We learned how to detect and handle collisions
and experienced how easy creating a sophisticated game was using Flame.
Finally, we added capabilities to share game states with other clients to
complete a real-time multiplayer experience without managing our own
infrastructure using [Supabase](https://supabase.com/).

## More Flutter Resources#

  * [Complete code of this article](https://github.com/supabase/supabase/tree/master/examples/realtime/flutter-multiplayer-shooting-game)
  * [Flutter Tutorial: building a Flutter chat app](https://supabase.com/blog/flutter-tutorial-building-a-chat-app)
  * [Flutter Authentication and Authorization with RLS](https://supabase.com/blog/flutter-authentication-and-authorization-with-rls)
  * [Generate Flame template using Very Good CLI](https://verygood.ventures/blog/generate-a-game-with-our-new-template)
  * [Supabase Flutter SDK docs](https://supabase.com/docs/reference/dart/start)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
real-time-multiplayer-game&text=How%20to%20build%20a%20real-
time%20multiplayer%20game%20with%20Flutter%20Flame)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
real-time-multiplayer-game&text=How%20to%20build%20a%20real-
time%20multiplayer%20game%20with%20Flutter%20Flame)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
real-time-multiplayer-game&t=How%20to%20build%20a%20real-
time%20multiplayer%20game%20with%20Flutter%20Flame)

[Last postHappyTeams unlocks better performance and reduces cost with
Supabase16 February 2023](/blog/case-study-happyteams)

[Next postSupabase Beta January 20238 February 2023](/blog/supabase-beta-
january-2023)

[flutter](/blog/tags/flutter)[mobile](/blog/tags/mobile)[realtime](/blog/tags/realtime)

On this page

  * Overview of the final game
  * Build the App
    * Step 1. Create the Flutter App
    * Step 2. Building the Flutter widgets
    * Create the Main Game Page
    * Create the Lobby Dialog
    * Step 3. Building the Flame components
    * Creating the FlameGame
    * Creating the Player Component
    * Adding bullets
    * Step 4. Add real-time communications between players
    * Handle the Lobby to wait for Other Players to show up
    * Sharing Game States with the Opposing Player
  * Conclusions
  * More Flutter Resources

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
real-time-multiplayer-game&text=How%20to%20build%20a%20real-
time%20multiplayer%20game%20with%20Flutter%20Flame)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
real-time-multiplayer-game&text=How%20to%20build%20a%20real-
time%20multiplayer%20game%20with%20Flutter%20Flame)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
real-time-multiplayer-game&t=How%20to%20build%20a%20real-
time%20multiplayer%20game%20with%20Flutter%20Flame)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

