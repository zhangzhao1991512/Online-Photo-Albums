INSERT INTO User (username, firstname, lastname, password, email) VALUES
('sportslover', 'Paul', 'Walker', 'sha512$7c65daeaa526432ba5e1054018542b28$fd35210c5aa3176eea7e6e9aea65e0f9fa59200ae4100964dd94dfcecec6c302691d52562fb0f2cd580aa8f8be9ed38563420411e306b1453b371c6c27e0b98a', 'sportslover@hotmail.com'),
('traveler', 'Rebecca', 'Travolta', 'sha512$6a28f4809415487c8fe27400fe8f354f$30d7be93cf5a7b6cebf172c63344a176404d539ce8f216051bea78f8ea572f81b6250380b994305377923f747ee066e95f809970cbf11da5478d88b5855c88ae', 'rebt@explorer.org'), 
('spacejunkie', 'Bob', 'Spacey', 'sha512$0b720b37c7cb4bada3bbc67b183eee24$963ea57847a04ea47204f1066187e6141a6ef3174a61ad7522d2d83ce9fe29a7541be6e1b0384f9a6be5a6b6692861b4db2366d5f7875ccf3741576866f0b5b3', 'bspace@spacejunkies.net');

INSERT INTO Album (title, created, lastupdated, username, access) VALUES
('I love sports', NOW(), NOW(), 'sportslover', 'public'),
('I love football', NOW(), NOW(), 'sportslover', 'private'),
('Around The World', NOW(), NOW(), 'traveler', 'public'),
('Cool Space Shots', NOW(), NOW(), 'spacejunkie', 'private'); 

 INSERT INTO Photo(picid, format) values("001025dd643b0eb0661e359de86e3ea9", "jpg"); 
 INSERT INTO Photo(picid, format) values("9a0a7d25af4f7a73f67dde74e8e54cff", "jpg"); 
 INSERT INTO Photo(picid, format) values("c8e60100f13ffe374d59e39dc4b6a318", "jpg"); 
 INSERT INTO Photo(picid, format) values("5e8b6207f007338243d3e29d6b82acab", "jpg"); 
 INSERT INTO Photo(picid, format) values("4ddba6e2f905e9778c6b6a48b6fc8e03", "jpg"); 
 INSERT INTO Photo(picid, format) values("09d8a979fa638125b02ae1578eb943fa", "jpg"); 
 INSERT INTO Photo(picid, format) values("143ba34cb5c7e8f12420be1b576bda1a", "jpg"); 
 INSERT INTO Photo(picid, format) values("e615a10fc4222ede59ca3316c3fb751c", "jpg"); 
 INSERT INTO Photo(picid, format) values("65fb1e2aa4977d9414d1b3a7e4a3badd", "jpg"); 
 INSERT INTO Photo(picid, format) values("b94f256c23dec8a2c0da546849058d9e", "jpg"); 
 INSERT INTO Photo(picid, format) values("01e37cbdd55913df563f527860b364e8", "jpg"); 
 INSERT INTO Photo(picid, format) values("8d554cd1d8bb7b49ca798381d1fc171b", "jpg"); 
 INSERT INTO Photo(picid, format) values("2e9e69e19342b98141789925e5f87f60", "jpg"); 
 INSERT INTO Photo(picid, format) values("298e8943ef1942159ef88be21c4619c9", "jpg"); 
 INSERT INTO Photo(picid, format) values("cefe45eaeaeb599256dda325c2e972da", "jpg"); 
 INSERT INTO Photo(picid, format) values("bf755d13bb78e1deb59ef66b6d5c6a70", "jpg"); 
 INSERT INTO Photo(picid, format) values("5f8d7957874f1303d8300e50f17e46d6", "jpg"); 
 INSERT INTO Photo(picid, format) values("bac4fca50bed35b9a5646f632bf4c2e8", "jpg"); 
 INSERT INTO Photo(picid, format) values("f5b57bd7a2c962c54d55b5ddece37158", "jpg"); 
 INSERT INTO Photo(picid, format) values("b7d833dd3aae203ca618759fc6f4fc01", "jpg"); 
 INSERT INTO Photo(picid, format) values("faa20c04097d40cb10793a19246f2754", "jpg"); 
 INSERT INTO Photo(picid, format) values("aaaadd578c78d21defaa73e7d1f08235", "jpg"); 
 INSERT INTO Photo(picid, format) values("adb5c3af19664129141268feda90a275", "jpg"); 
 INSERT INTO Photo(picid, format) values("abf97ffd1f964f42790fb358e5258e8d", "jpg"); 
 INSERT INTO Photo(picid, format) values("ea2db8b970671856e43dd011d7df5fad", "jpg"); 
 INSERT INTO Photo(picid, format) values("76d79b81b9073a2323f0790965b00a68", "jpg"); 
 INSERT INTO Photo(picid, format) values("6510a4add59ef655ae3f0b6cdb24e140", "jpg"); 
 INSERT INTO Photo(picid, format) values("28d38afca913a728b2a6bcf01aa011cd", "jpg"); 
 INSERT INTO Photo(picid, format) values("5fb04eb11cbf99429a05c12ce2f50615", "jpg"); 
 INSERT INTO Photo(picid, format) values("39ee267d13ccd32b50c1de7c2ece54d6", "jpg");


 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (0,  2, "001025dd643b0eb0661e359de86e3ea9", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (1,  2, "9a0a7d25af4f7a73f67dde74e8e54cff", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (2,  2, "c8e60100f13ffe374d59e39dc4b6a318", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (3,  2, "5e8b6207f007338243d3e29d6b82acab", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (4,  4, "4ddba6e2f905e9778c6b6a48b6fc8e03", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (5,  4, "09d8a979fa638125b02ae1578eb943fa", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (6,  4, "143ba34cb5c7e8f12420be1b576bda1a", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (7,  4, "e615a10fc4222ede59ca3316c3fb751c", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (8,  4, "65fb1e2aa4977d9414d1b3a7e4a3badd", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (9,  1, "b94f256c23dec8a2c0da546849058d9e", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (10, 1, "01e37cbdd55913df563f527860b364e8", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (11, 1, "8d554cd1d8bb7b49ca798381d1fc171b", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (12, 1, "2e9e69e19342b98141789925e5f87f60", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (13, 1, "298e8943ef1942159ef88be21c4619c9", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (14, 1, "cefe45eaeaeb599256dda325c2e972da", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (15, 1, "bf755d13bb78e1deb59ef66b6d5c6a70", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (16, 1, "5f8d7957874f1303d8300e50f17e46d6", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (17, 3, "bac4fca50bed35b9a5646f632bf4c2e8", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (18, 3, "f5b57bd7a2c962c54d55b5ddece37158", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (19, 3, "b7d833dd3aae203ca618759fc6f4fc01", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (20, 3, "faa20c04097d40cb10793a19246f2754", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (21, 3, "aaaadd578c78d21defaa73e7d1f08235", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (22, 3, "adb5c3af19664129141268feda90a275", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (23, 3, "abf97ffd1f964f42790fb358e5258e8d", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (24, 3, "ea2db8b970671856e43dd011d7df5fad", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (25, 3, "76d79b81b9073a2323f0790965b00a68", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (26, 3, "6510a4add59ef655ae3f0b6cdb24e140", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (27, 3, "28d38afca913a728b2a6bcf01aa011cd", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (28, 3, "5fb04eb11cbf99429a05c12ce2f50615", ""); 
 INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (29, 3, "39ee267d13ccd32b50c1de7c2ece54d6", ""); 


