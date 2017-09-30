create table User(
	username varchar(20),
	firstname varchar(20) not null,
	lastname varchar(20) not null,
	password varchar(256) not null,
	email varchar(40) not null,
	primary key (username)
);

create table Album(
	albumid int auto_increment,
	title varchar(50),
	created timestamp default Now(),
	lastupdated timestamp default Now(),
	username varchar(20) not null,
	access ENUM('public', 'private'),
	primary key (albumid),
	foreign key (username) references User(username)
);

create table Photo(
	picid varchar(40),
	format char(3),
	date timestamp default Now(),
	primary key (picid)
);


create table Contain(
	sequencenum int,
	albumid int,
	picid varchar(40) unique,
	caption varchar(255) not null, 
	primary key (sequencenum), 
	foreign key (picid) references Photo(picid),
	foreign key (albumid) references Album(albumid)
);

create table AlbumAccess(
	albumid int not null,
	username varchar(20) not null,
	foreign key (albumid) references Album(albumid),
	foreign key (username) references User(username),
	primary key (username, albumid)
)
