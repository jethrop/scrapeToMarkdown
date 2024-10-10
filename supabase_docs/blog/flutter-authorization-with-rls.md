[Back](/blog)

[Blog](/blog)

# Flutter Authorization with RLS

22 Nov 2022

•

67 minute read

[![Tyler Shukert
avatar](/_next/image?url=https%3A%2F%2Fgithub.com%2Fdshukertjr.png&w=96&q=75)Tyler
ShukertDevRel](https://twitter.com/dshukertjr)

![Flutter Authorization with RLS](/_next/image?url=%2Fimages%2Fblog%2Fflutter-
chat-auth%2Fsupabase-flutter-auth.jpg&w=3840&q=100)

This article is the second part of the Flutter tutorial series. During the
series, you will learn how to build cross-platform apps without worrying about
the backend.

In this article, I will show you how you can make a secure chat application by
introducing authorization to the basic chat app that we created
[previously](https://supabase.com/blog/flutter-tutorial-building-a-chat-app).

We will store the chat data on [Supabase](https://supabase.com/). Supabase
utilizes the built in authorization mechanism of PostgreSQL called [Row Level
Security](https://supabase.com/docs/guides/auth/row-level-security) or RLS to
prevent unauthorized access from accessing or writing data to your database.
RLS allows developers to define row-by-row conditions that evaluate to either
`true` or `false` to either allow the access or deny it. We will take a look
at more specific examples of authorization using RLS throughout this article.

## What we created in the previous article#

Before we jump in, let's go over what we built in the [previous
article](blog/flutter-tutorial-building-a-chat-app), because we will be
building on top of it. If you have not gone through it, I recommend you to go
check it out.

In the previous article, we created a basic real-time chat application. Users
will register or sign in using an email address and password. Once they are
signed in, they are taken to a chat page, where they can view and send
messages to everyone in the app. There are no Chat rooms, and everyone's
messages were sent to the same chat room.

You can also find a complete code example [here](https://github.com/supabase-
community/flutter-chat/tree/with_auth) to follow along.

## Overview of the final app#

The app will allow us to have 1 on 1 chat with other users in the app. To
enable this, we will introduce a new rooms page. The rooms page serves two
purposes here, one is to initiate a conversation with other users, and the
other is to display existing chat rooms. At the top of the app, we see a list
of other users' icons. A user can tap the icon to start a 1 on 1 conversation.
Below the icons, there is a list of rooms that the user is a part of.

## Sessing up the scene#

### Install additional dependencies#

We will install flutter_bloc for state management. Introducing a state
management solution will allow us to handle the shared message and profile
data efficiently between the rooms page and the chats page. We can use any
state management solution for this, but we are going with bloc in this
example. Add the following in your pubspec.yaml file to install flutter_bloc
in your app.

`  

_10

flutter_bloc: ^8.0.0

  
`

### Modifying the table schema#

Since the app has evolved, we also need to update our table schema. In order
to store rooms data, we will add a rooms table. We will also modify the
messages table to add a foreign key constraint to the rooms table so that we
can tell which message belongs to which room.

We will also introduce a `create_new_room` function, which is a [database
function](https://supabase.com/docs/guides/database/functions) that handles
chat room creation. It knows to create a new room if a chat room with the two
users does not exist yet, or to just return the room ID if it already exists.

`  

_60

-- *** Table definitions ***

_60

_60

create table if not exists public.rooms (

_60

id uuid not null primary key default gen_random_uuid(),

_60

created_at timestamp with time zone default timezone('utc' :: text, now()) not
null

_60

);

_60

comment on table public.rooms is 'Holds chat rooms';

_60

_60

create table if not exists public.room_participants (

_60

profile_id uuid references public.profiles(id) on delete cascade not null,

_60

room_id uuid references public.rooms(id) on delete cascade not null,

_60

created_at timestamp with time zone default timezone('utc' :: text, now()) not
null,

_60

primary key (profile_id, room_id)

_60

);

_60

comment on table public.room_participants is 'Relational table of users and
rooms.';

_60

_60

alter table public.messages

_60

add column room_id uuid references public.rooms(id) on delete cascade not
null;

_60

_60

-- *** Add tables to the publication to enable realtime ***

_60

_60

alter publication supabase_realtime add table public.room_participants;

_60

_60

-- Creates a new room with the user and another user in it.

_60

-- Will return the room_id of the created room

_60

-- Will return a room_id if there were already a room with those participants

_60

create or replace function create_new_room(other_user_id uuid) returns uuid as
$$

_60

declare

_60

new_room_id uuid;

_60

begin

_60

-- Check if room with both participants already exist

_60

with rooms_with_profiles as (

_60

select room_id, array_agg(profile_id) as participants

_60

from room_participants

_60

group by room_id

_60

)

_60

select room_id

_60

into new_room_id

_60

from rooms_with_profiles

_60

where create_new_room.other_user_id=any(participants)

_60

and auth.uid()=any(participants);

_60

_60

_60

if not found then

_60

-- Create a new room

_60

insert into public.rooms default values

_60

returning id into new_room_id;

_60

_60

-- Insert the caller user into the new room

_60

insert into public.room_participants (profile_id, room_id)

_60

values (auth.uid(), new_room_id);

_60

_60

-- Insert the other_user user into the new room

_60

insert into public.room_participants (profile_id, room_id)

_60

values (other_user_id, new_room_id);

_60

end if;

_60

_60

return new_room_id;

_60

end

_60

$$ language plpgsql security definer;

  
`

### Setup deep links#

Something we skipped in the previous article was sending confirmation emails
to users when they signup. Since today is about security, let's properly send
confirmation emails to people who signup.

When we send confirmation emails, the users need to be brought back to the app
somehow. Since supabase_flutter has a mechanism to detect and handle deep
links, we will register a `io.supabase.chat://login` as our deep link for the
app and bring the users back after confirming their email address.

For iOS we edit the info.plist file to register the deep link.

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

<string>io.supabase.chat</string>

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

For Android we edit the AndroidManifest.xml to register the deep link.

`  

_20

<manifest ...>

_20

<!-- ... other tags -->

_20

<application ...>

_20

<activity ...>

_20

<!-- ... other tags -->

_20

_20

<!-- Add this intent-filter for Deep Links -->

_20

<intent-filter>

_20

<action android:name="android.intent.action.VIEW" />

_20

<category android:name="android.intent.category.DEFAULT" />

_20

<category android:name="android.intent.category.BROWSABLE" />

_20

<!-- Accepts URIs that begin with YOUR_SCHEME://YOUR_HOST -->

_20

<data

_20

android:scheme="io.supabase.chat"

_20

android:host="login" />

_20

</intent-filter>

_20

_20

</activity>

_20

</application>

_20

</manifest>

  
`

We also need to set the deep link in our Supabase dashboard. Go to
`Authentication > URL Configuration` in your dashboard and add
`io.supabase.chat://login` as one of the redirect URLs.

And that is it for deep link configuration.

## Building out the main application#

### Step1: Create rooms page#

The rooms page will load two types of data, recently added users and a list of
rooms that the user belongs to. We will be using bloc to load these two types
of data and display them on the rooms page.

Let's start out by creating states for the rooms page. The rooms page would
have four different states, loading, loaded, empty, and error. We will display
different UI on the rooms page depending on what state it is. Satrt by
defining the `Room` model. Create a `lib/models/room.dart` file and add the
following code.

`  

_50

import 'package:my_chat_app/models/message.dart';

_50

_50

class Room {

_50

Room({

_50

required this.id,

_50

required this.createdAt,

_50

required this.otherUserId,

_50

this.lastMessage,

_50

});

_50

_50

/// ID of the room

_50

final String id;

_50

_50

/// Date and time when the room was created

_50

final DateTime createdAt;

_50

_50

/// ID of the user who the user is talking to

_50

final String otherUserId;

_50

_50

/// Latest message submitted in the room

_50

final Message? lastMessage;

_50

_50

Map<String, dynamic> toMap() {

_50

return {

_50

'id': id,

_50

'createdAt': createdAt.millisecondsSinceEpoch,

_50

};

_50

}

_50

_50

/// Creates a room object from room_participants table

_50

Room.fromRoomParticipants(Map<String, dynamic> map)

_50

: id = map['room_id'],

_50

otherUserId = map['profile_id'],

_50

createdAt = DateTime.parse(map['created_at']),

_50

lastMessage = null;

_50

_50

Room copyWith({

_50

String? id,

_50

DateTime? createdAt,

_50

String? otherUserId,

_50

Message? lastMessage,

_50

}) {

_50

return Room(

_50

id: id ?? this.id,

_50

createdAt: createdAt ?? this.createdAt,

_50

otherUserId: otherUserId ?? this.otherUserId,

_50

lastMessage: lastMessage ?? this.lastMessage,

_50

);

_50

}

_50

}

  
`

We will proceed with defining the states for the rooms page. Create
`lib/cubit/rooms/rooms_state.dart` file and paste the following code. You may
see some errors, but we will take care of them in the next step.

`  

_28

part of 'rooms_cubit.dart';

_28

_28

@immutable

_28

abstract class RoomState {}

_28

_28

class RoomsLoading extends RoomState {}

_28

_28

class RoomsLoaded extends RoomState {

_28

final List<Profile> newUsers;

_28

final List<Room> rooms;

_28

_28

RoomsLoaded({

_28

required this.rooms,

_28

required this.newUsers,

_28

});

_28

}

_28

_28

class RoomsEmpty extends RoomState {

_28

final List<Profile> newUsers;

_28

_28

RoomsEmpty({required this.newUsers});

_28

}

_28

_28

class RoomsError extends RoomState {

_28

final String message;

_28

_28

RoomsError(this.message);

_28

}

  
`

Now that we have the states defined, we will create rooms_cubit. A
[cubit](https://bloclibrary.dev/#/coreconcepts?id=cubit) is a class within the
flutter_bloc library where we will make requests to Supabase to get the data
and transform them into states and emit them to the UI widgets. Let's create a
`lib/cubit/rooms/rooms_cubit.dart` file and complete the cubit.

`  

_140

import 'dart:async';

_140

_140

import 'package:flutter/material.dart';

_140

import 'package:flutter_bloc/flutter_bloc.dart';

_140

import 'package:my_chat_app/cubits/profiles/profiles_cubit.dart';

_140

import 'package:my_chat_app/models/profile.dart';

_140

import 'package:my_chat_app/models/message.dart';

_140

import 'package:my_chat_app/models/room.dart';

_140

import 'package:my_chat_app/utils/constants.dart';

_140

_140

part 'rooms_state.dart';

_140

_140

class RoomCubit extends Cubit<RoomState> {

_140

RoomCubit() : super(RoomsLoading());

_140

_140

final Map<String, StreamSubscription<Message?>>

_140

_messageSubscriptions = {};

_140

_140

late final String _myUserId;

_140

_140

/// List of new users of the app for the user to start talking to

_140

late final List<Profile> _newUsers;

_140

_140

/// List of rooms

_140

List<Room> _rooms = [];

_140

StreamSubscription<List<Map<String, dynamic>>>?

_140

_rawRoomsSubscription;

_140

bool _haveCalledGetRooms = false;

_140

_140

Future<void> initializeRooms(BuildContext context) async {

_140

if (_haveCalledGetRooms) {

_140

return;

_140

}

_140

_haveCalledGetRooms = true;

_140

_140

_myUserId = supabase.auth.currentUser!.id;

_140

_140

late final List data;

_140

_140

try {

_140

data = await supabase

_140

.from('profiles')

_140

.select()

_140

.not('id', 'eq', _myUserId)

_140

.order('created_at')

_140

.limit(12);

_140

} catch (_) {

_140

emit(RoomsError('Error loading new users'));

_140

}

_140

_140

final rows = List<Map<String, dynamic>>.from(data);

_140

_newUsers = rows.map(Profile.fromMap).toList();

_140

_140

/// Get realtime updates on rooms that the user is in

_140

_rawRoomsSubscription =

_140

supabase.from('room_participants').stream(

_140

primaryKey: ['room_id', 'profile_id'],

_140

).listen((participantMaps) async {

_140

if (participantMaps.isEmpty) {

_140

emit(RoomsEmpty(newUsers: _newUsers));

_140

return;

_140

}

_140

_140

_rooms = participantMaps

_140

.map(Room.fromRoomParticipants)

_140

.where((room) => room.otherUserId != _myUserId)

_140

.toList();

_140

for (final room in _rooms) {

_140

_getNewestMessage(

_140

context: context, roomId: room.id);

_140

BlocProvider.of<ProfilesCubit>(context)

_140

.getProfile(room.otherUserId);

_140

}

_140

emit(RoomsLoaded(

_140

newUsers: _newUsers,

_140

rooms: _rooms,

_140

));

_140

}, onError: (error) {

_140

emit(RoomsError('Error loading rooms'));

_140

});

_140

}

_140

_140

// Setup listeners to listen to the most recent message in each room

_140

void _getNewestMessage({

_140

required BuildContext context,

_140

required String roomId,

_140

}) {

_140

_messageSubscriptions[roomId] = supabase

_140

.from('messages')

_140

.stream(primaryKey: ['id'])

_140

.eq('room_id', roomId)

_140

.order('created_at')

_140

.limit(1)

_140

.map<Message?>(

_140

(data) => data.isEmpty

_140

? null

_140

: Message.fromMap(

_140

map: data.first,

_140

myUserId: _myUserId,

_140

),

_140

)

_140

.listen((message) {

_140

final index = _rooms

_140

.indexWhere((room) => room.id == roomId);

_140

_rooms[index] =

_140

_rooms[index].copyWith(lastMessage: message);

_140

_rooms.sort((a, b) {

_140

/// Sort according to the last message

_140

/// Use the room createdAt when last message is not available

_140

final aTimeStamp = a.lastMessage != null

_140

? a.lastMessage!.createdAt

_140

: a.createdAt;

_140

final bTimeStamp = b.lastMessage != null

_140

? b.lastMessage!.createdAt

_140

: b.createdAt;

_140

return bTimeStamp.compareTo(aTimeStamp);

_140

});

_140

if (!isClosed) {

_140

emit(RoomsLoaded(

_140

newUsers: _newUsers,

_140

rooms: _rooms,

_140

));

_140

}

_140

});

_140

}

_140

_140

/// Creates or returns an existing roomID of both participants

_140

Future<String> createRoom(String otherUserId) async {

_140

final data = await supabase.rpc('create_new_room',

_140

params: {'other_user_id': otherUserId});

_140

emit(RoomsLoaded(rooms: _rooms, newUsers: _newUsers));

_140

return data as String;

_140

}

_140

_140

@override

_140

Future<void> close() {

_140

_rawRoomsSubscription?.cancel();

_140

return super.close();

_140

}

_140

}

  
`

Now that we have the states and cubit to power our rooms page, it's time to
create the `RoomsPage`.

We have two list views, one horizontal list view to display other users, and
one vertical list views with list tiles representing each room that the user
is a part of. We will create a `lib/pages/rooms_page.dart` file with the
following content.

`  

_187

import 'package:flutter/material.dart';

_187

import 'package:flutter_bloc/flutter_bloc.dart';

_187

import 'package:my_chat_app/cubits/profiles/profiles_cubit.dart';

_187

_187

import 'package:my_chat_app/cubits/rooms/rooms_cubit.dart';

_187

import 'package:my_chat_app/models/profile.dart';

_187

import 'package:my_chat_app/pages/chat_page.dart';

_187

import 'package:my_chat_app/pages/register_page.dart';

_187

import 'package:my_chat_app/utils/constants.dart';

_187

import 'package:timeago/timeago.dart';

_187

_187

/// Displays the list of chat threads

_187

class RoomsPage extends StatelessWidget {

_187

const RoomsPage({Key? key}) : super(key: key);

_187

_187

static Route<void> route() {

_187

return MaterialPageRoute(

_187

builder: (context) => BlocProvider<RoomCubit>(

_187

create: (context) =>

_187

RoomCubit()..initializeRooms(context),

_187

child: const RoomsPage(),

_187

),

_187

);

_187

}

_187

_187

@override

_187

Widget build(BuildContext context) {

_187

return Scaffold(

_187

appBar: AppBar(

_187

title: const Text('Rooms'),

_187

actions: [

_187

TextButton(

_187

onPressed: () async {

_187

await supabase.auth.signOut();

_187

Navigator.of(context).pushAndRemoveUntil(

_187

RegisterPage.route(),

_187

(route) => false,

_187

);

_187

},

_187

child: const Text('Logout'),

_187

),

_187

],

_187

),

_187

body: BlocBuilder<RoomCubit, RoomState>(

_187

builder: (context, state) {

_187

if (state is RoomsLoading) {

_187

return preloader;

_187

} else if (state is RoomsLoaded) {

_187

final newUsers = state.newUsers;

_187

final rooms = state.rooms;

_187

return BlocBuilder<ProfilesCubit,

_187

ProfilesState>(

_187

builder: (context, state) {

_187

if (state is ProfilesLoaded) {

_187

final profiles = state.profiles;

_187

return Column(

_187

children: [

_187

_NewUsers(newUsers: newUsers),

_187

Expanded(

_187

child: ListView.builder(

_187

itemCount: rooms.length,

_187

itemBuilder: (context, index) {

_187

final room = rooms[index];

_187

final otherUser =

_187

profiles[room.otherUserId];

_187

_187

return ListTile(

_187

onTap: () =>

_187

Navigator.of(context)

_187

.push(ChatPage.route(

_187

room.id)),

_187

leading: CircleAvatar(

_187

child: otherUser == null

_187

? preloader

_187

: Text(otherUser

_187

.username

_187

.substring(0, 2)),

_187

),

_187

title: Text(otherUser == null

_187

? 'Loading...'

_187

: otherUser.username),

_187

subtitle: room.lastMessage !=

_187

null

_187

? Text(

_187

room.lastMessage!

_187

.content,

_187

maxLines: 1,

_187

overflow: TextOverflow

_187

.ellipsis,

_187

)

_187

: const Text(

_187

'Room created'),

_187

trailing: Text(format(

_187

room.lastMessage

_187

?.createdAt ??

_187

room.createdAt,

_187

locale: 'en_short')),

_187

);

_187

},

_187

),

_187

),

_187

],

_187

);

_187

} else {

_187

return preloader;

_187

}

_187

},

_187

);

_187

} else if (state is RoomsEmpty) {

_187

final newUsers = state.newUsers;

_187

return Column(

_187

children: [

_187

_NewUsers(newUsers: newUsers),

_187

const Expanded(

_187

child: Center(

_187

child: Text(

_187

'Start a chat by tapping on available users'),

_187

),

_187

),

_187

],

_187

);

_187

} else if (state is RoomsError) {

_187

return Center(child: Text(state.message));

_187

}

_187

throw UnimplementedError();

_187

},

_187

),

_187

);

_187

}

_187

}

_187

_187

class _NewUsers extends StatelessWidget {

_187

const _NewUsers({

_187

Key? key,

_187

required this.newUsers,

_187

}) : super(key: key);

_187

_187

final List<Profile> newUsers;

_187

_187

@override

_187

Widget build(BuildContext context) {

_187

return SingleChildScrollView(

_187

padding: const EdgeInsets.symmetric(vertical: 8),

_187

scrollDirection: Axis.horizontal,

_187

child: Row(

_187

children: newUsers

_187

.map<Widget>((user) => InkWell(

_187

onTap: () async {

_187

try {

_187

final roomId =

_187

await BlocProvider.of<RoomCubit>(

_187

context)

_187

.createRoom(user.id);

_187

Navigator.of(context)

_187

.push(ChatPage.route(roomId));

_187

} catch (_) {

_187

context.showErrorSnackBar(

_187

message:

_187

'Failed creating a new room');

_187

}

_187

},

_187

child: Padding(

_187

padding: const EdgeInsets.all(8.0),

_187

child: SizedBox(

_187

width: 60,

_187

child: Column(

_187

children: [

_187

CircleAvatar(

_187

child: Text(user.username

_187

.substring(0, 2)),

_187

),

_187

const SizedBox(height: 8),

_187

Text(

_187

user.username,

_187

maxLines: 1,

_187

overflow: TextOverflow.ellipsis,

_187

),

_187

],

_187

),

_187

),

_187

),

_187

))

_187

.toList(),

_187

),

_187

);

_187

}

_187

}

  
`

You may see some errors, but they will go away once we edit the chat page!

### Step 2: Modify the chat page to load messages in the room#

Our `ChatPage` will have a similar layout as the previous one, but will only
display messages sent to a single room. We will start by creating
`MessagesState`. The messages page will also have four different states,
loading, loaded, empty, and error. Create a `lib/cubits/chat/chat_state.dart`
file with the following code.

`  

_18

part of 'chat_cubit.dart';

_18

_18

@immutable

_18

abstract class ChatState {}

_18

_18

class ChatInitial extends ChatState {}

_18

_18

class ChatLoaded extends ChatState {

_18

ChatLoaded(this.messages);

_18

final List<Message> messages;

_18

}

_18

_18

class ChatEmpty extends ChatState {}

_18

_18

class ChatError extends ChatState {

_18

ChatError(this.message);

_18

final String message;

_18

}

  
`

Now let's create chat cubit to retrieve the data from our database and emit it
as states. Create a `lib/cubits/chat/chat_cubit.dart` file and paste the
following.

`  

_72

import 'dart:async';

_72

_72

import 'package:bloc/bloc.dart';

_72

import 'package:meta/meta.dart';

_72

import 'package:my_chat_app/models/message.dart';

_72

import 'package:my_chat_app/utils/constants.dart';

_72

_72

part 'chat_state.dart';

_72

_72

class ChatCubit extends Cubit<ChatState> {

_72

ChatCubit() : super(ChatInitial());

_72

_72

StreamSubscription<List<Message>>? _messagesSubscription;

_72

List<Message> _messages = [];

_72

_72

late final String _roomId;

_72

late final String _myUserId;

_72

_72

void setMessagesListener(String roomId) {

_72

_roomId = roomId;

_72

_72

_myUserId = supabase.auth.currentUser!.id;

_72

_72

_messagesSubscription = supabase

_72

.from('messages')

_72

.stream(primaryKey: ['id'])

_72

.eq('room_id', roomId)

_72

.order('created_at')

_72

.map<List<Message>>(

_72

(data) => data

_72

.map<Message>(

_72

(row) => Message.fromMap(map: row, myUserId: _myUserId))

_72

.toList(),

_72

)

_72

.listen((messages) {

_72

_messages = messages;

_72

if (_messages.isEmpty) {

_72

emit(ChatEmpty());

_72

} else {

_72

emit(ChatLoaded(_messages));

_72

}

_72

});

_72

}

_72

_72

Future<void> sendMessage(String text) async {

_72

/// Add message to present to the user right away

_72

final message = Message(

_72

id: 'new',

_72

roomId: _roomId,

_72

profileId: _myUserId,

_72

content: text,

_72

createdAt: DateTime.now(),

_72

isMine: true,

_72

);

_72

_messages.insert(0, message);

_72

emit(ChatLoaded(_messages));

_72

_72

try {

_72

await supabase.from('messages').insert(message.toMap());

_72

} catch (_) {

_72

emit(ChatError('Error submitting message.'));

_72

_messages.removeWhere((message) => message.id == 'new');

_72

emit(ChatLoaded(_messages));

_72

}

_72

}

_72

_72

@override

_72

Future<void> close() {

_72

_messagesSubscription?.cancel();

_72

return super.close();

_72

}

_72

}

  
`

Chat cubit is pretty simple. It sets a real-time listener to the database
using the stream method and emits an empty state if there are no messages in
the room, or emits a loaded state if there are messages.

Because we are using cubit, we need to modify the MessagesPage widget as well.
Open `lib/pages/chat_page.dart` and let's update it.

`  

_193

import 'package:flutter/material.dart';

_193

import 'package:flutter_bloc/flutter_bloc.dart';

_193

import 'package:my_chat_app/components/user_avatar.dart';

_193

import 'package:my_chat_app/cubits/chat/chat_cubit.dart';

_193

_193

import 'package:my_chat_app/models/message.dart';

_193

import 'package:my_chat_app/utils/constants.dart';

_193

import 'package:timeago/timeago.dart';

_193

_193

/// Page to chat with someone.

_193

///

_193

/// Displays chat bubbles as a ListView and TextField to enter new chat.

_193

class ChatPage extends StatelessWidget {

_193

const ChatPage({Key? key}) : super(key: key);

_193

_193

static Route<void> route(String roomId) {

_193

return MaterialPageRoute(

_193

builder: (context) => BlocProvider<ChatCubit>(

_193

create: (context) => ChatCubit()..setMessagesListener(roomId),

_193

child: const ChatPage(),

_193

),

_193

);

_193

}

_193

_193

@override

_193

Widget build(BuildContext context) {

_193

return Scaffold(

_193

appBar: AppBar(title: const Text('Chat')),

_193

body: BlocConsumer<ChatCubit, ChatState>(

_193

listener: (context, state) {

_193

if (state is ChatError) {

_193

context.showErrorSnackBar(message: state.message);

_193

}

_193

},

_193

builder: (context, state) {

_193

if (state is ChatInitial) {

_193

return preloader;

_193

} else if (state is ChatLoaded) {

_193

final messages = state.messages;

_193

return Column(

_193

children: [

_193

Expanded(

_193

child: ListView.builder(

_193

padding: const EdgeInsets.symmetric(vertical: 8),

_193

reverse: true,

_193

itemCount: messages.length,

_193

itemBuilder: (context, index) {

_193

final message = messages[index];

_193

return _ChatBubble(message: message);

_193

},

_193

),

_193

),

_193

const _MessageBar(),

_193

],

_193

);

_193

} else if (state is ChatEmpty) {

_193

return Column(

_193

children: const [

_193

Expanded(

_193

child: Center(

_193

child: Text('Start your conversation now :)'),

_193

),

_193

),

_193

_MessageBar(),

_193

],

_193

);

_193

} else if (state is ChatError) {

_193

return Center(child: Text(state.message));

_193

}

_193

throw UnimplementedError();

_193

},

_193

),

_193

);

_193

}

_193

}

_193

_193

/// Set of widget that contains TextField and Button to submit message

_193

class _MessageBar extends StatefulWidget {

_193

const _MessageBar({

_193

Key? key,

_193

}) : super(key: key);

_193

_193

@override

_193

State<_MessageBar> createState() => _MessageBarState();

_193

}

_193

_193

class _MessageBarState extends State<_MessageBar> {

_193

late final TextEditingController _textController;

_193

_193

@override

_193

Widget build(BuildContext context) {

_193

return Material(

_193

color: Theme.of(context).cardColor,

_193

child: Padding(

_193

padding: EdgeInsets.only(

_193

top: 8,

_193

left: 8,

_193

right: 8,

_193

bottom: MediaQuery.of(context).padding.bottom,

_193

),

_193

child: Row(

_193

children: [

_193

Expanded(

_193

child: TextFormField(

_193

keyboardType: TextInputType.text,

_193

maxLines: null,

_193

autofocus: true,

_193

controller: _textController,

_193

decoration: const InputDecoration(

_193

hintText: 'Type a message',

_193

border: InputBorder.none,

_193

focusedBorder: InputBorder.none,

_193

contentPadding: EdgeInsets.all(8),

_193

),

_193

),

_193

),

_193

TextButton(

_193

onPressed: () => _submitMessage(),

_193

child: const Text('Send'),

_193

),

_193

],

_193

),

_193

),

_193

);

_193

}

_193

_193

@override

_193

void initState() {

_193

_textController = TextEditingController();

_193

super.initState();

_193

}

_193

_193

@override

_193

void dispose() {

_193

_textController.dispose();

_193

super.dispose();

_193

}

_193

_193

void _submitMessage() async {

_193

final text = _textController.text;

_193

if (text.isEmpty) {

_193

return;

_193

}

_193

BlocProvider.of<ChatCubit>(context).sendMessage(text);

_193

_textController.clear();

_193

}

_193

}

_193

_193

class _ChatBubble extends StatelessWidget {

_193

const _ChatBubble({

_193

Key? key,

_193

required this.message,

_193

}) : super(key: key);

_193

_193

final Message message;

_193

_193

@override

_193

Widget build(BuildContext context) {

_193

List<Widget> chatContents = [

_193

if (!message.isMine) UserAvatar(userId: message.profileId),

_193

const SizedBox(width: 12),

_193

Flexible(

_193

child: Container(

_193

padding: const EdgeInsets.symmetric(

_193

vertical: 8,

_193

horizontal: 12,

_193

),

_193

decoration: BoxDecoration(

_193

color: message.isMine

_193

? Colors.grey[300]

_193

: Theme.of(context).primaryColor,

_193

borderRadius: BorderRadius.circular(8),

_193

),

_193

child: Text(message.content),

_193

),

_193

),

_193

const SizedBox(width: 12),

_193

Text(format(message.createdAt, locale: 'en_short')),

_193

const SizedBox(width: 60),

_193

];

_193

if (message.isMine) {

_193

chatContents = chatContents.reversed.toList();

_193

}

_193

return Padding(

_193

padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 18),

_193

child: Row(

_193

mainAxisAlignment:

_193

message.isMine ? MainAxisAlignment.end : MainAxisAlignment.start,

_193

children: chatContents,

_193

),

_193

);

_193

}

_193

}

  
`

### Step 3: Handle user sign-up/ sign-in#

Because we have modified the setting of our Supabase to send a confirmation
email, we need to make some modifications to the register page and login page
as well.

The main change is how we handle navigation. Previously, we were able to
navigate the user to `ChatPage` right after sign-in was complete. This would
no longer work, as we now have to wait for the user to confirm their email
address. In this case, we would want to listen to auth state of the user and
navigate when the user is signed in with a session. This allows us to react
when the user confirmed their email addresses.

`  

_169

import 'dart:async';

_169

_169

import 'package:flutter/material.dart';

_169

import 'package:my_chat_app/pages/login_page.dart';

_169

import 'package:my_chat_app/pages/rooms_page.dart';

_169

import 'package:my_chat_app/utils/constants.dart';

_169

import 'package:supabase_flutter/supabase_flutter.dart';

_169

_169

class RegisterPage extends StatefulWidget {

_169

const RegisterPage(

_169

{Key? key, required this.isRegistering})

_169

: super(key: key);

_169

_169

static Route<void> route({bool isRegistering = false}) {

_169

return MaterialPageRoute(

_169

builder: (context) =>

_169

RegisterPage(isRegistering: isRegistering),

_169

);

_169

}

_169

_169

final bool isRegistering;

_169

_169

@override

_169

State<RegisterPage> createState() => _RegisterPageState();

_169

}

_169

_169

class _RegisterPageState extends State<RegisterPage> {

_169

final bool _isLoading = false;

_169

_169

final _formKey = GlobalKey<FormState>();

_169

_169

final _emailController = TextEditingController();

_169

final _passwordController = TextEditingController();

_169

final _usernameController = TextEditingController();

_169

_169

late final StreamSubscription<AuthState>

_169

_authSubscription;

_169

_169

@override

_169

void initState() {

_169

super.initState();

_169

_169

bool haveNavigated = false;

_169

// Listen to auth state to redirect user when the user clicks on confirmation
link

_169

_authSubscription =

_169

supabase.auth.onAuthStateChange.listen((data) {

_169

final session = data.session;

_169

if (session != null && !haveNavigated) {

_169

haveNavigated = true;

_169

Navigator.of(context)

_169

.pushReplacement(RoomsPage.route());

_169

}

_169

});

_169

}

_169

_169

@override

_169

void dispose() {

_169

super.dispose();

_169

_169

// Dispose subscription when no longer needed

_169

_authSubscription.cancel();

_169

}

_169

_169

Future<void> _signUp() async {

_169

final isValid = _formKey.currentState!.validate();

_169

if (!isValid) {

_169

return;

_169

}

_169

final email = _emailController.text;

_169

final password = _passwordController.text;

_169

final username = _usernameController.text;

_169

try {

_169

await supabase.auth.signUp(

_169

email: email,

_169

password: password,

_169

data: {'username': username},

_169

emailRedirectTo: 'io.supabase.chat://login',

_169

);

_169

context.showSnackBar(

_169

message:

_169

'Please check your inbox for confirmation email.');

_169

} on AuthException catch (error) {

_169

context.showErrorSnackBar(message: error.message);

_169

} catch (error) {

_169

debugPrint(error.toString());

_169

context.showErrorSnackBar(

_169

message: unexpectedErrorMessage);

_169

}

_169

}

_169

_169

@override

_169

Widget build(BuildContext context) {

_169

return Scaffold(

_169

appBar: AppBar(

_169

title: const Text('Register'),

_169

),

_169

body: Form(

_169

key: _formKey,

_169

child: ListView(

_169

padding: formPadding,

_169

children: [

_169

TextFormField(

_169

controller: _emailController,

_169

decoration: const InputDecoration(

_169

label: Text('Email'),

_169

),

_169

validator: (val) {

_169

if (val == null || val.isEmpty) {

_169

return 'Required';

_169

}

_169

return null;

_169

},

_169

keyboardType: TextInputType.emailAddress,

_169

),

_169

spacer,

_169

TextFormField(

_169

controller: _passwordController,

_169

obscureText: true,

_169

decoration: const InputDecoration(

_169

label: Text('Password'),

_169

),

_169

validator: (val) {

_169

if (val == null || val.isEmpty) {

_169

return 'Required';

_169

}

_169

if (val.length < 6) {

_169

return '6 characters minimum';

_169

}

_169

return null;

_169

},

_169

),

_169

spacer,

_169

TextFormField(

_169

controller: _usernameController,

_169

decoration: const InputDecoration(

_169

label: Text('Username'),

_169

),

_169

validator: (val) {

_169

if (val == null || val.isEmpty) {

_169

return 'Required';

_169

}

_169

final isValid =

_169

RegExp(r'^[A-Za-z0-9_]{3,24}$')

_169

.hasMatch(val);

_169

if (!isValid) {

_169

return '3-24 long with alphanumeric or underscore';

_169

}

_169

return null;

_169

},

_169

),

_169

spacer,

_169

ElevatedButton(

_169

onPressed: _isLoading ? null : _signUp,

_169

child: const Text('Register'),

_169

),

_169

spacer,

_169

TextButton(

_169

onPressed: () {

_169

Navigator.of(context)

_169

.push(LoginPage.route());

_169

},

_169

child:

_169

const Text('I already have an account'))

_169

],

_169

),

_169

),

_169

);

_169

}

_169

}

  
`

Login page becomes simpler. All it is doing is taking a user's email and
password and logging them in. It is not doing any navigation whatsoever. This
is because `LoginPage` is navigated on top of `RegisterPage`, the auth state
listener on `RegisterPage` is still active, and therefore can take care of the
navigation.

`  

_80

import 'package:flutter/material.dart';

_80

import 'package:my_chat_app/utils/constants.dart';

_80

import 'package:supabase_flutter/supabase_flutter.dart';

_80

_80

class LoginPage extends StatefulWidget {

_80

const LoginPage({Key? key}) : super(key: key);

_80

_80

static Route<void> route() {

_80

return MaterialPageRoute(

_80

builder: (context) => const LoginPage());

_80

}

_80

_80

@override

_80

_LoginPageState createState() => _LoginPageState();

_80

}

_80

_80

class _LoginPageState extends State<LoginPage> {

_80

bool _isLoading = false;

_80

final _emailController = TextEditingController();

_80

final _passwordController = TextEditingController();

_80

_80

Future<void> _signIn() async {

_80

setState(() {

_80

_isLoading = true;

_80

});

_80

try {

_80

await supabase.auth.signInWithPassword(

_80

email: _emailController.text,

_80

password: _passwordController.text,

_80

);

_80

} on AuthException catch (error) {

_80

context.showErrorSnackBar(message: error.message);

_80

} catch (_) {

_80

context.showErrorSnackBar(

_80

message: unexpectedErrorMessage);

_80

}

_80

if (mounted) {

_80

setState(() {

_80

_isLoading = true;

_80

});

_80

}

_80

}

_80

_80

@override

_80

void dispose() {

_80

_emailController.dispose();

_80

_passwordController.dispose();

_80

super.dispose();

_80

}

_80

_80

@override

_80

Widget build(BuildContext context) {

_80

return Scaffold(

_80

appBar: AppBar(title: const Text('Sign In')),

_80

body: ListView(

_80

padding: formPadding,

_80

children: [

_80

TextFormField(

_80

controller: _emailController,

_80

decoration:

_80

const InputDecoration(labelText: 'Email'),

_80

keyboardType: TextInputType.emailAddress,

_80

),

_80

spacer,

_80

TextFormField(

_80

controller: _passwordController,

_80

decoration: const InputDecoration(

_80

labelText: 'Password'),

_80

obscureText: true,

_80

),

_80

spacer,

_80

ElevatedButton(

_80

onPressed: _isLoading ? null : _signIn,

_80

child: const Text('Login'),

_80

),

_80

],

_80

),

_80

);

_80

}

_80

}

  
`

Notice that I have not used bloc anywhere on the register or login page. I try
to only use state management libraries for pages that have some complexity.
Since both register and login pages are relatively simple, I am going with the
good old `setState`.

We should also modify the splash page to redirect signed-in users to the
RoomsPage by default.

`  

_51

import 'package:flutter/material.dart';

_51

import 'package:my_chat_app/pages/register_page.dart';

_51

import 'package:my_chat_app/pages/rooms_page.dart';

_51

import 'package:my_chat_app/utils/constants.dart';

_51

import 'package:supabase_flutter/supabase_flutter.dart';

_51

_51

/// Page to redirect users to the appropriate page depending on the initial
auth state

_51

class SplashPage extends StatefulWidget {

_51

const SplashPage({Key? key}) : super(key: key);

_51

_51

@override

_51

SplashPageState createState() => SplashPageState();

_51

}

_51

_51

class SplashPageState extends State<SplashPage> {

_51

@override

_51

void initState() {

_51

getInitialSession();

_51

super.initState();

_51

}

_51

_51

Future<void> getInitialSession() async {

_51

// quick and dirty way to wait for the widget to mount

_51

await Future.delayed(Duration.zero);

_51

_51

try {

_51

final session =

_51

await SupabaseAuth.instance.initialSession;

_51

if (session == null) {

_51

Navigator.of(context).pushAndRemoveUntil(

_51

RegisterPage.route(), (_) => false);

_51

} else {

_51

Navigator.of(context).pushAndRemoveUntil(

_51

RoomsPage.route(), (_) => false);

_51

}

_51

} catch (_) {

_51

context.showErrorSnackBar(

_51

message: 'Error occurred during session refresh',

_51

);

_51

Navigator.of(context).pushAndRemoveUntil(

_51

RegisterPage.route(), (_) => false);

_51

}

_51

}

_51

_51

@override

_51

Widget build(BuildContext context) {

_51

return const Scaffold(

_51

body: Center(child: CircularProgressIndicator()),

_51

);

_51

}

_51

}

  
`

Finally we implement those `ProfilesCubit` that you saw here and there
throughout the code. This cubit will act as in memory cache of all the
profiles data so that the app does not have to go fetch the same profiles
every single time it needs it. Create `profiles_state.dart` and
`profiles_cubit.dart` under `lib/cubits/` and add the following code.

`  

_14

part of 'profiles_cubit.dart';

_14

_14

@immutable

_14

abstract class ProfilesState {}

_14

_14

class ProfilesInitial extends ProfilesState {}

_14

_14

class ProfilesLoaded extends ProfilesState {

_14

ProfilesLoaded({

_14

required this.profiles,

_14

});

_14

_14

final Map<String, Profile?> profiles;

_14

}

  
`

`  

_33

import 'dart:async';

_33

_33

import 'package:bloc/bloc.dart';

_33

import 'package:meta/meta.dart';

_33

import 'package:my_chat_app/models/profile.dart';

_33

import 'package:my_chat_app/utils/constants.dart';

_33

_33

part 'profiles_state.dart';

_33

_33

class ProfilesCubit extends Cubit<ProfilesState> {

_33

ProfilesCubit() : super(ProfilesInitial());

_33

_33

/// Map of app users cache in memory with profile_id as the key

_33

final Map<String, Profile?> _profiles = {};

_33

_33

Future<void> getProfile(String userId) async {

_33

if (_profiles[userId] != null) {

_33

return;

_33

}

_33

_33

final data = await supabase

_33

.from('profiles')

_33

.select()

_33

.match({'id': userId}).single();

_33

_33

if (data == null) {

_33

return;

_33

}

_33

_profiles[userId] = Profile.fromMap(data);

_33

_33

emit(ProfilesLoaded(profiles: _profiles));

_33

}

_33

}

  
`

We will make the `ProfilesCubit` accessible from anywhere in the app with the
following code in `main.dart` file.

`  

_36

import 'package:flutter/material.dart';

_36

import 'package:flutter_bloc/flutter_bloc.dart';

_36

import 'package:my_chat_app/cubits/profiles/profiles_cubit.dart';

_36

import 'package:my_chat_app/utils/constants.dart';

_36

import 'package:supabase_flutter/supabase_flutter.dart';

_36

import 'package:my_chat_app/pages/splash_page.dart';

_36

_36

Future<void> main() async {

_36

WidgetsFlutterBinding.ensureInitialized();

_36

_36

await Supabase.initialize(

_36

// TODO: Replace credentials with your own

_36

url: 'supabase_url',

_36

anonKey: 'supabase_anon_key',

_36

authCallbackUrlHostname: 'login',

_36

);

_36

_36

runApp(const MyApp());

_36

}

_36

_36

class MyApp extends StatelessWidget {

_36

const MyApp({Key? key}) : super(key: key);

_36

_36

@override

_36

Widget build(BuildContext context) {

_36

return BlocProvider<ProfilesCubit>(

_36

create: (context) => ProfilesCubit(),

_36

child: MaterialApp(

_36

title: 'SupaChat',

_36

debugShowCheckedModeBanner: false,

_36

theme: appTheme,

_36

home: const SplashPage(),

_36

),

_36

);

_36

}

_36

}

  
`

### Step 4: Authorization with Row Level Security (RLS)#

At this point, we seemingly have a complete app. But if we open the app right
now, we will see every users' room along with all the messages that have ever
been sent. This is because we have not set up Row Level Security to prevent
users from accessing rooms that don't belong to them. There are two ways we
can define Row Level Security policies in Supabase: with the GUI or through
SQL. Today we will use SQL. Let's run the following SQL to set the security
policy.

`  

_34

-- Returns true if the signed in user is a participant of the room

_34

create or replace function is_room_participant(room_id uuid)

_34

returns boolean as $$

_34

select exists(

_34

select 1

_34

from room_participants

_34

where room_id = is_room_participant.room_id and profile_id = auth.uid()

_34

);

_34

$$ language sql security definer;

_34

_34

_34

-- *** Row level security polities ***

_34

_34

_34

alter table public.profiles enable row level security;

_34

create policy "Public profiles are viewable by everyone."

_34

on public.profiles for select using (true);

_34

_34

_34

alter table public.rooms enable row level security;

_34

create policy "Users can view rooms that they have joined"

_34

on public.rooms for select using (is_room_participant(id));

_34

_34

_34

alter table public.room_participants enable row level security;

_34

create policy "Participants of the room can view other participants."

_34

on public.room_participants for select using (is_room_participant(room_id));

_34

_34

_34

alter table public.messages enable row level security;

_34

create policy "Users can view messages on rooms they are in."

_34

on public.messages for select using (is_room_participant(room_id));

_34

create policy "Users can insert messages on rooms they are in."

_34

on public.messages for insert with check (is_room_participant(room_id) and
profile_id = auth.uid());

  
`

Notice that we have created a handy `is_room_participant` function that will
return whether a particular user is a participant or not in a specific room.

With the Row Level Security policies set up, our application is complete. We
now have a real-time chat application with proper authentication and
authorization in place.

## Conclusions/ Future Improvements#

Continuing from our [previous article](https://supabase.com/blog/flutter-
tutorial-building-a-chat-app), we added proper authorization to our chat
application using Row Level Security, which enabled us to add 1 on 1 chat
feature. We used bloc for our state management solution. One thing we could
have done differently if we were to write test codes was to pass the supabase
instance as a parameter of the cubit so that we could [write tests using the
bloc_test package](https://bloclibrary.dev/#/testing).

We could also explore some cool feature improvement. At the top of the rooms
page, we are loading the newest created users to start a conversation. This is
fine, but it only allows users to start a conversation with new users. We can
for example update this to a list of users that are online at the same time.
We can implement this using the [presence
feature](https://supabase.com/docs/guides/realtime/presence) of Supabase.

## More Flutter Resources#

  * [Complete set of code of this chat app](https://github.com/supabase-community/flutter-chat/tree/with_auth)
  * [supabase-flutter docs](https://supabase.com/docs/reference/dart)
  * [How to build a real-time multiplayer game with Flutter Flame](https://supabase.com/blog/flutter-real-time-multiplayer-game)
  * [Flutter Supabase Quick Starter Guide](https://supabase.com/docs/guides/with-flutter)
  * [supabase-flutter v1.0 released](https://supabase.com/blog/supabase-flutter-sdk-v1-released)
  * [Build a Flutter app with Very Good CLI and Supabase](https://verygood.ventures/blog/flutter-app-very-good-cli-supabase)

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
authorization-with-
rls&text=Flutter%20Authorization%20with%20RLS)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
authorization-with-
rls&text=Flutter%20Authorization%20with%20RLS)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
authorization-with-rls&t=Flutter%20Authorization%20with%20RLS)

[Last postSQL or NoSQL? Why not use both (with PostgreSQL)?24 November
2022](/blog/sql-or-nosql-both-with-postgresql)

[Next postFetching and caching Supabase data in Next.js 13 Server Components17
November 2022](/blog/fetching-and-caching-supabase-data-in-next-js-server-
components)

[flutter](/blog/tags/flutter)[auth](/blog/tags/auth)

On this page

  * What we created in the previous article
  * Overview of the final app
  * Sessing up the scene
    * Install additional dependencies
    * Modifying the table schema
    * Setup deep links
  * Building out the main application
    * Step1: Create rooms page
    * Step 2: Modify the chat page to load messages in the room
    * Step 3: Handle user sign-up/ sign-in
    * Step 4: Authorization with Row Level Security (RLS)
  * Conclusions/ Future Improvements
  * More Flutter Resources

Share this article

[](https://twitter.com/intent/tweet?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
authorization-with-
rls&text=Flutter%20Authorization%20with%20RLS)[](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
authorization-with-
rls&text=Flutter%20Authorization%20with%20RLS)[](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fsupabase.com%2Fblog%2Fflutter-
authorization-with-rls&t=Flutter%20Authorization%20with%20RLS)

## Build in a weekend, scale to millions

[Start your project](https://supabase.com/dashboard)[Request a
demo](/contact/sales)

